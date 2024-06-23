Requiete instalar 

python-socketio
flask-scoketio
flask


version de python con la que se probo:3.9.13

considerar ejecutar primero el servidor con

python .\GameServer.py

configurar las normas, esperar que se levante el servidor

Ejecutar los Players necesarios con

python .\Player.py


Observaciones del codigo: El juego funciona con p2p, pero solo se puede jugar de 2 equipos, aun asi hay que poner que se desea jugar con 2 equipos, los dos equipos pueden tener la cantidad de players que se configure, y una vez inicia el juego, el servidor va diciendo a quien le toca lanzar, pero todos pueden lanzar, hasta que un equipo llegue a la meta y gane. el servidor avisa por brodcast cuando un equipo gana.