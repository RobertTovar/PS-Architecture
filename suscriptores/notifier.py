##!/usr/bin/env python
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------
# Archivo: notifier.py
# Capitulo: Estilo Publica-Suscribe
# Autor(es): Perla Velasco & Yonathan Mtz. & Jorge Solís
# Version: 3.0.0 Marzo 2022
# Descripción:
#
#   Esta clase define el suscriptor que recibirá mensajes desde el distribuidor de mensajes
#   y lo notificará a un(a) enfermero(a) én particular para la atención del adulto mayor en
#   cuestión
#
#   Este archivo también define el punto de ejecución del Suscriptor
#
#   A continuación se describen los métodos que se implementaron en la clase Notifier:
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
import telepot
import MsgListener
from stomp import utils

# Se hereda de una clase padre llamada MsgListener 
class NotifierMsgListener(MsgListener.MsgListener) :

    # Se sobrescribe el metodo que se ocupa y se reutiliza codigo ya escrito
    def __init__ (self, token, chat_id) :
        self .msg_received = 0
        self.token = token
        self.chat_id = chat_id

    # Se sobrescribe el metodo que se ocupa y se reutiliza codigo ya escrito
    def on_message(self, message):
        data = utils.convert_frame(message)

        data.pop()
        data = data.pop()

        print("enviando notificación de signos vitales...")
        if self.token and self.chat_id:
            data = json.loads(data.decode("utf-8"))
            message = f"ADVERTENCIA!!!\n[{data['wearable']['date']}]: asistir al paciente {data['name']} {data['last_name']}...\nssn: {data['ssn']}, edad: {data['age']}, temperatura: {round(data['wearable']['temperature'], 1)}, ritmo cardiaco: {data['wearable']['heart_rate']}, presión arterial: {data['wearable']['blood_pressure']}, dispositivo: {data['wearable']['id']}"
            bot = telepot.Bot(self.token)
            bot.sendMessage(self.chat_id, message)
        time.sleep(1)


class Notifier:

    def __init__(self):
        self.topic = "notifier"
        self.token = ""
        self.chat_id = ""

    def suscribe(self):
        print("Inicio de monitoreo de signos vitales...")
        print()
        self.consume(queue=self.topic)

    def consume(self, queue):
        try:
            conn = stomp.Connection([("localhost", 61613)]) 
            conn.set_listener("monitorlistener", NotifierMsgListener(self.token, self.chat_id))
            conn.connect("admin", "admin", wait=True)
            while True:
                conn.subscribe(queue, header={}, id="suscriber", ack="client")
                time.sleep(5)

        except (KeyboardInterrupt, SystemExit):
            conn.unsubscribe("suscriber")
            sys.exit("Conexión finalizada...")

if __name__ == '__main__':
    notifier = Notifier()
    notifier.suscribe()
