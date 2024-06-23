from flask import Flask, request
from flask_socketio import SocketIO, emit
import json
import random

connected_players = []
sids = []

app = Flask(__name__)
socketio = SocketIO(app)




global team1
global team2
global totalteam1
global totalteam2
global turnos
global id_nickname_map
global pt1
global pt2
pt1=[]
pt2=[]

team1=[]
team2=[]
totalteam1=0
totalteam2=0
turnos=[]
id_nickname_map={}


def lanzar_dado(min,max):
    global dado_lanzado
    dado_lanzado = random.randint(min, max)
    return int(dado_lanzado)


def get_variables():
    """
    Solicita al usuario las variables del juego y las valida.

    Devuelve:
        tupla: Una tupla con los valores de las variables del juego.
    """
    while True:
        try:
            max_teams = int(input("Ingrese la cantidad máxima de equipos (número entero positivo, minimo 2, or 0 for dev fast config): "))
            if max_teams > 1 :
                break
            elif max_teams==0:
                return  2, 1, 20, 3, 15
            else:
                print("La cantidad máxima de equipos debe ser un número positivo.")
        except ValueError:
            print("Entrada no válida. Ingrese un número entero.")

    while True:
        try:
            max_players_per_team = int(input("Ingrese la cantidad máxima de jugadores por equipo (número entero positivo): "))
            if max_players_per_team > 0:
                break
            else:
                print("La cantidad máxima de jugadores por equipo debe ser un número positivo.")
        except ValueError:
            print("Entrada no válida. Ingrese un número entero.")

    while True:
        try:
            max_positions = int(input("Ingrese la cantidad máxima de posiciones del tablero (número entero positivo): "))
            if max_positions > 0:
                break
            else:
                print("La cantidad máxima de posiciones debe ser un número positivo.")
        except ValueError:
            print("Entrada no válida. Ingrese un número entero.")

    while True:
        try:
            min_dice_value = int(input("Ingrese el valor mínimo del dado (número entero positivo): "))
            if min_dice_value > 0:
                break
            else:
                print("El valor mínimo del dado debe ser un número positivo.")
        except ValueError:
            print("Entrada no válida. Ingrese un número entero.")

    while True:
        try:
            max_dice_value = int(input("Ingrese el valor máximo del dado (número entero positivo): "))
            if max_dice_value >= min_dice_value:
                break
            else:
                print("El valor máximo del dado debe ser mayor o igual que el valor mínimo.")
        except ValueError:
            print("Entrada no válida. Ingrese un número entero.")

    return max_teams, max_players_per_team, max_positions, min_dice_value, max_dice_value

max_teams, max_players_per_team, max_positions, min_dice_value, max_dice_value = get_variables()

print(f"**Servidor iniciado con las siguientes variables:**")
print(f"- Cantidad máxima de equipos: {max_teams}")
print(f"- Cantidad máxima de jugadores por equipo: {max_players_per_team}")
print(f"- Cantidad máxima de posiciones del tablero: {max_positions}")
print(f"- Valor mínimo del dado: {min_dice_value}")
print(f"- Valor máximo del dado: {max_dice_value}")
print(f"- team 1: {team1}")
print(f"- team 2: {team2}")
print(f"- puntos team 1: {totalteam1}")
print(f"- puntos team 2: {totalteam2}")



""" def handle_message(message):
    
    Maneja los mensajes recibidos de los clientes.

    Args:
        message (str): El mensaje recibido.
    
    print(f"**Mensaje recibido:** {message}")
    emit('message', message, broadcast=True)"""
@socketio.on('message')
def handle_message(message_json):
    
    try:
        message_data = json.loads(message_json)
        nickname = message_data.get('nick')
        team_aux = message_data.get('team')
        msj= message_data.get('msj')
        print("Mensaje dice: ")
        print(msj)

        if nickname :
            if nickname not in connected_players:
                connected_players.append(nickname)
                
                sids.append(request.sid)
                print(f"Jugador {nickname} conectado.")
                # Enviar mensaje de bienvenida al nuevo jugador
                #print(str(sids[-1]))

                #Creamos el diccionario que vincular nicks e ids
                id_nickname_map[request.sid] = nickname
                

                if (team_aux =="team1" or team_aux=="team2"):
                    if(team_aux =="team1"):
                        team1.append(request.sid)
                    else:
                        team2.append(request.sid)


                # Notificar a todos los jugadores sobre la nueva conexión
                emit('message', f"¡Bienvenido al juego, {nickname}!", broadcast=True)

                
            else:
                print(f"El apodo {nickname} ya está en uso.")
        
        #print("team 1: ")
        #print(team1)
        #print("team 2: ")
        #print(team2)
        if ((len(team1)+ len(team2))>= max_players_per_team *2 and not msj):
            turnos=team1+team2
            random.shuffle(turnos)
            print("turnos: ")
            print(turnos)
            emit('message', f"¡equipos llenos, el juego comenzara eligiendo un equipo y miembros al azar para comenzar a lanzar, preparen sus dados!", broadcast=True)
            emit('message', f"¡Es tu turno, envia 'lanzar' : !", to=turnos[0])

        message = message_data.get('message')

        if 'totalteam1' in locals():  # Check if 'totalteam1' exists in the local scope
        # totalteam1 already exists, handle it as needed (optional)
            pass
        else:
            totalteam1 = 0
        if 'totalteam1' in locals():  # Check if 'totalteam1' exists in the local scope
        # totalteam1 already exists, handle it as needed (optional)
            pass
        else:
            totalteam2 = 0

            
        if (msj=="lanzar"):
            print("se lanzaron los dados")
            dice_aux=lanzar_dado(min_dice_value, max_dice_value)
            if (request.sid in team1):
                pt1.append(dice_aux)
                print(f"EL dado saco {dice_aux}")
            else:
                pt2.append(dice_aux)
                print(f"EL dado saco {dice_aux}")
            totalteam1=sum(pt1)
            totalteam2=sum(pt2)
            if totalteam1 >= max_positions:
                emit('message', f"¡El equipo 1 ha resultado ganador con {totalteam1} puntos!, juego finalizado, si desea volver a jugar reinice el servidor y los usuarios", broadcast=True)

            if totalteam2 >= max_positions:
                emit('message', f"¡El equipo 2 ha resultado ganador con {totalteam2} puntos!, juego finalizado, si desea volver a jugar reinice el servidor y los usuarios", broadcast=True)
        
        if message:
            print(f"Mensaje recibido de {nickname}: {message}")
            emit('message', f"{nickname}: {message}", broadcast=True)
    except json.JSONDecodeError:
        print("Error al decodificar JSON: ", message_json)


if __name__ == '__main__':
    print("**Iniciando servidor GameServer...**")
    socketio.run(app, host='0.0.0.0', port=5000)
