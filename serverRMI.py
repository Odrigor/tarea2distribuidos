from flask import Flask, request
import time
import datetime
import os

# Definir la ruta del archivo log
ruta_archivo_log = "registro.log"

# Crear la aplicación Flask
app = Flask(__name__)

# Definir la ruta del endpoint para recibir datos
@app.route("/registrar_datos", methods=["POST"])
def registrar_datos():
  # Obtener los datos de la petición POST
  datos_recibidos = request.get_json()

  # Validar la existencia de datos obligatorios
  if not datos_recibidos or "status" not in datos_recibidos or "gameid" not in datos_recibidos or "team" not in datos_recibidos or "nick" not in datos_recibidos:
    return "Datos incompletos", 400

  # Obtener el timestamp actual
  timestamp_segundos = time.time()
  fecha_hora = datetime.datetime.fromtimestamp(timestamp_segundos)
  timestamp_formateado = fecha_hora.strftime("%Y-%m-%d %H:%M:%S")

  # Formatear los datos para el registro
  datos_formateados = f"{timestamp_formateado}\t{datos_recibidos['status']}\t{datos_recibidos['gameid']}\t{datos_recibidos['team']}\t{datos_recibidos['nick']}\n"

  # Verificar si el archivo log existe
  if not os.path.exists(ruta_archivo_log):
    # Crear el archivo log si no existe
    with open(ruta_archivo_log, "w") as archivo:
      archivo.write("Timestamp\tStatus\tGameID\tTeam\tNick\n")

  # Abrir el archivo log en modo append
  with open(ruta_archivo_log, "a") as archivo:
    archivo.write(datos_formateados)

  # Devolver una respuesta exitosa
  return "Datos registrados correctamente", 200

# Iniciar el servidor Flask
if __name__ == "__main__":
  app.run(debug=True)