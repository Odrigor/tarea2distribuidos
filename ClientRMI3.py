import os
import json
import requests
import re
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Configuración
logs_folder = r"C:\Users\rodci\OneDrive\Escritorio\game2\Game\logs"
endpoint = "http://127.0.0.1:5000/registrar_datos"

# Patrón de regex para los logs (ignora la primera línea de encabezado)
log_pattern = re.compile(r'(?P<timestamp>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\s+(?P<status>\w+)\s+(?P<gameid>\d+)\s+(?P<team>\d+)\s+(?P<nick>\w+)')

class LogHandler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory and event.src_path.endswith(".log"):
            self.process_log(event.src_path)

    def process_log(self, log_path):
        try:
            with open(log_path, 'r') as file:
                next(file)  # Ignora la primera línea (encabezado)
                for log_line in file:
                    match = log_pattern.match(log_line.strip())
                    if match:
                        log_data = {k.lower(): v for k, v in match.groupdict().items()}  # Convierte las claves a minúsculas
                        self.send_log(log_data)
                    else:
                        print(f"Log line does not match pattern: {log_line}")
        except Exception as e:
            print(f"Error processing log file {log_path}: {e}")

    def send_log(self, log_data):
        try:
            json_data = json.dumps(log_data)
            response = requests.post(endpoint, data=json_data, headers={'Content-Type': 'application/json'})
            if response.status_code == 200:
                print(f"Log sent successfully: {json_data}")
            else:
                print(f"Failed to send log. Status code: {response.status_code}, Response: {response.text}")
        except Exception as e:
            print(f"Error sending log data: {e}")

if __name__ == "__main__":
    print(f"Client RMI started, observing folder: {logs_folder}")

    event_handler = LogHandler()
    observer = Observer()
    observer.schedule(event_handler, path=logs_folder, recursive=False)
    observer.start()

    try:
        while True:
            pass  # Mantén el script corriendo
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
