##!/usr/bin/env python
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------
# Archivo: MsgListener.py
# Capitulo: Estilo Publica-Suscribe
# Autor(es): Roberto Tovar, Jonathan Carrera, Cesar Villegas & Jan Dehuma
# Version: 1.0.0 Mayo 2023
# Descripción:
#
#   Esta clase se encarga de servir como interfaz con el broker, en este caso activeMQ
#
#
#   A continuación se describen los métodos que se implementaron en esta clase:
#
#                                             Métodos:
#   +------------------------+--------------------------+-----------------------+
#   |         Nombre         |        Parámetros        |        Función        |
#   +------------------------+--------------------------+-----------------------+
#   |       __init__()       |  - self: definición de   |  - constructor de la  |
#   |                        |    la instancia de la    |    clase              |
#   |                        |    clase                 |                       |
#   +------------------------+--------------------------+-----------------------+
#   | on_error(self, message)|  - self: definición de   |  - maneja los errores |
#   |                        |    la instancia de la    |    durante el         |
#   |                        |    clase                 |    proceso            |
#   |                        |                          |                       |
#   |                        |  - message: el mensaje   |                       |
#   |                        |    de error recibido     |                       |
#   +------------------------+--------------------------+-----------------------+
#   | on_message(self,       |  - self: definición de   |  - maneja los mensajes|
#   | message)               |    la instancia de la    |    recibidos          |
#   |                        |    clase                 |                       |
#   |                        |                          |                       |
#   |                        |  - message: el mensaje   |                       |
#   |                        |    recibido              |                       |
#   +------------------------+--------------------------+-----------------------+
#
#-------------------------------------------------------------------------

import stomp
# Clase de la cual se aplicara polimorfismo para no reescribir codigo
class MsgListener(stomp.ConnectionListener) :

    def init (self, token, chat_id) :
        self .msg_received = 0
        self.token = token
        self.chat_id = chat_id

    def on_error(self, message) :
        print("received an error")
        print (message)

    def on_message(self, message):
        pass