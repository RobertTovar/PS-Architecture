##!/usr/bin/env python
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------
# Archivo: monitor.py
# Capitulo: Estilo Publica-Suscribe
# Autor(es): Perla Velasco & Yonathan Mtz. & Jorge Solís
# Version: 3.0.0 Marzo 2022
# Descripción:
#
#   Esta clase define el suscriptor que recibirá mensajes desde el distribuidor de mensajes
#   y los mostrará al área interesada para su monitoreo continuo
#
#   Este archivo también define el punto de ejecución del Suscriptor
#
#   A continuación se describen los métodos que se implementaron en la clase Monitor:
#
#                                             Métodos:
#           +------------------------+--------------------------+-----------------------+
#           |         Nombre         |        Parámetros        |        Función        |
#           +------------------------+--------------------------+-----------------------+
#           |       __init__()       |  - self: definición de   |  - constructor de la  |
#           |                        |    la instancia de la    |    clase              |
#           |                        |    clase                 |                       |
#           +------------------------+--------------------------+-----------------------+
#           |       suscribe()       |  - self: definición de   |  - inicializa el      |
#           |                        |    la instancia de la    |    proceso de         |
#           |                        |    clase                 |    monitoreo de       |
#           |                        |                          |    signos vitales     |
#           +------------------------+--------------------------+-----------------------+
#           |        consume()       |  - self: definición de   |  - realiza la         |
#           |                        |    la instancia de la    |    suscripción en el  |
#           |                        |    clase                 |    distribuidor de    |
#           |                        |  - queue: ruta a la que  |    mensajes para      |
#           |                        |    el suscriptor está    |    comenzar a recibir |
#           |                        |    interesado en recibir |    mensajes           |
#           |                        |    mensajes              |                       |
#           +------------------------+--------------------------+-----------------------+
#
#-------------------------------------------------------------------------
import json, time, sys, stomp
import MsgListener
from stomp import utils

# conn = stomp.Connection([("localhost", 61613)]) 
# conn.connect("admin", "admin", wait=True)
# conn.send(queue, data)
# conn.disconnect()

# Se hereda de una clase padre llamada MsgListener 
class MonitorMsgListener(MsgListener.MsgListener) :

    # Se sobrescribe el metodo que se ocupa y se reutiliza codigo ya escrito
    def on_message(self, message):
        print("ADVERTENCIA!!!")
        
        data = utils.convert_frame(message)

        data.pop()
        data = data.pop()

        data = json.loads(data.decode("utf-8"))

        print(f"[{data['wearable']['date']}]: asistir al paciente {data['name']} {data['last_name']}... con wearable {data['wearable']['id']}")
        print(f"ssn: {data['ssn']}, edad: {data['age']}, temperatura: {round(data['wearable']['temperature'], 1)}, ritmo cardiaco: {data['wearable']['heart_rate']}, presión arterial: {data['wearable']['blood_pressure']}, dispositivo: {data['wearable']['id']}")
        print()
        time.sleep(1)

class Monitor:

    def __init__(self):
        self.topic = "monitor"

    def suscribe(self):
        print("Inicio de monitoreo de signos vitales...")
        print()
        self.consume(queue=self.topic)

    def consume(self, queue):
        try:
            conn = stomp.Connection([("localhost", 61613)]) 
            conn.set_listener("monitorlistener", MonitorMsgListener())
            conn.connect("admin", "admin", wait=True)
            while True:
                conn.subscribe(queue, header={}, id="suscriber", ack="client")
                time.sleep(5)

        except (KeyboardInterrupt, SystemExit):
            conn.unsubscribe("suscriber")
            sys.exit("Conexión finalizada...")

if __name__ == '__main__':
    monitor = Monitor()
    monitor.suscribe()


