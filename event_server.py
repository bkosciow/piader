#!/usr/bin/python
# -*- coding: utf-8 -*-
#pylint: disable=I0011,W0231

"""Game event catcher"""
from __future__ import print_function
from future import standard_library
standard_library.install_aliases()
import socket
from threading import Thread
import json

BUFFER_SIZE = 1024
ADDRESS = ('', 5053)

class EventServerThread(Thread):
    """server thread"""
    def __init__(self, queue):
        Thread.__init__(self)
        self.work = True
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.socket.bind(ADDRESS)
        self.queue = queue

    def run(self):
        """start server thread"""
        try:
            print ("Server is listening for connections...")
            while self.work:
                try:
                    message, address = self.socket.recvfrom(BUFFER_SIZE)
                    message = self.__decode(message)
                    if message:
                        self.queue.put(message)
                except socket.timeout:
                    pass
        finally:
            self.socket.close()
        print("Server down")

    def join(self, timeout=None):
        """stop server and all listeners"""
        self.work = False
        Thread.join(self, timeout)

    def __decode(self, message):
        """decode network packet to json and extract event name"""
        message = message.decode("UTF-8")
        try:
            data = json.loads(message)
        except ValueError:
            data = None

        if type(data) is dict and 'event' in data:
            return data['event']

        return None