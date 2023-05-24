##!/usr/bin/env python
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------
# Archivo: record.py
# Capitulo: Estilo Publica-Suscribe
# Autor(es): Perla Velasco & Yonathan Mtz. & Jorge Solís
# Version: 3.0.0 Marzo 2022
# Descripción:
#
#   Esta clase define el suscriptor que recibirá mensajes desde el distribuidor de mensajes
#   y los almacena en un archivo de texto que simula el expediente de los pacientes
#
#   Este archivo también define el punto de ejecución del Suscriptor
#
#   A continuación se describen los métodos que se implementaron en la clase Record:
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
#           |                        |    mensajes              |                       |             |                       |
#           +------------------------+--------------------------+-----------------------+
#
#-------------------------------------------------------------------------
import json, time, sys, os, stomp
import MsgListener
from stomp import utils

# Se hereda de una clase padre llamada MsgListener 
class RecordMsgListener(MsgListener.MsgListener) :

    # Se sobrescribe el metodo que se ocupa y se reutiliza codigo ya escrito
    def on_message(self, message):        
        data = utils.convert_frame(message)

        data.pop()
        data = data.pop()        

        print("datos recibidos, actualizando expediente del paciente...")
        data = json.loads(data.decode("utf-8"))
        record_file = open (f"./records/{data['ssn']}.txt",'a')
        record_file.write(f"\n[{data['wearable']['date']}]: {data['name']} {data['last_name']}... ssn: {data['ssn']}, edad: {data['age']}, temperatura: {round(data['wearable']['temperature'], 1)}, ritmo cardiaco: {data['wearable']['heart_rate']}, presión arterial: {data['wearable']['blood_pressure']}, dispositivo: {data['wearable']['id']}")
        record_file.close()
        time.sleep(1)

class Record:

    def __init__(self):
        self.topic = "monitor"

    def suscribe(self):
        print("Inicio de monitoreo de signos vitales...")
        print()
        self.consume(queue=self.topic)

    def consume(self, queue):
        try:
            conn = stomp.Connection([("localhost", 61613)]) 
            conn.set_listener("monitorlistener", RecordMsgListener())
            conn.connect("admin", "admin", wait=True)
            while True:
                conn.subscribe(queue, header={}, id="suscriber", ack="client")
                time.sleep(5)

        except (KeyboardInterrupt, SystemExit):
            conn.unsubscribe("suscriber")
            sys.exit("Conexión finalizada...")

if __name__ == '__main__':
    record = Record()
    record.suscribe()
