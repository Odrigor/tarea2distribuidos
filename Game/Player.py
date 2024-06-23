import socketio
import json

socket = socketio.Client()

connected_players = []
GameStart = []

def get_nickname():
    while True:
        nickname = input("Ingrese su apodo: ")
        if nickname:
            return nickname
        else:
            print("El apodo no puede estar vacío.")

def get_team():
    while True:
        team = input("Ingrese team1 o team2")
        if team=='team1' or team=='team2':
            return team
        else:
            print("ingreso no valido, team1 o team2")

nickname = get_nickname()
team=get_team();

data = {"nick": nickname, "team":team}
message_json = json.dumps(data)
socket.connect('http://localhost:5000')
socket.emit('message', message_json)

@socket.on('message')
def handle_message(message):
    print(f"Mensaje recibido: {message}")

def send_message():
    message = input(f"{nickname}: ")

    data = {"msj": message}
    message_json = json.dumps(data)
    socket.emit('message', message_json)

while True:
    send_message()

