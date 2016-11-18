#!/usr/bin/python
# -*- coding: utf-8 -*-

"""Simple key read"""
from builtins import object
import socket
import termios, fcntl, sys, os
import json

ADDRESS = ('<broadcast>', 5053)

class Keyboard(object):
    """Read keyboard"""
    def __init__(self):
        self.actions = {
            'a': 'event.left',
            'd': 'event.right',
            'w': 'event.up',
            's': 'event.down',
            ' ': 'event.action1',
            'q': 'event.action2'
        }
        self.conn_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.conn_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.file_descriptior = sys.stdin.fileno()

        self.oldterm = termios.tcgetattr(self.file_descriptior)
        self.newattr = termios.tcgetattr(self.file_descriptior)
        self.newattr[3] = self.newattr[3] & ~termios.ICANON & ~termios.ECHO
        termios.tcsetattr(self.file_descriptior, termios.TCSANOW, self.newattr)

        self.oldflags = fcntl.fcntl(self.file_descriptior, fcntl.F_GETFL)
        fcntl.fcntl(
            self.file_descriptior,
            fcntl.F_SETFL,
            self.oldflags | os.O_NONBLOCK
        )

    def read(self):
        """read one key from buffer if avaible"""
        try:
            key = sys.stdin.read(1)
            if key in self.actions:
                self.send(self.actions[key])
        except IOError:
            pass

    def send(self, event):
        """send event to game"""
        packet = {
            "node": "local-keyboard",
            "event": event
        }
        self.conn_socket.sendto(json.dumps(packet).encode('UTF-8'), ADDRESS)

    def shutdown(self):
        """restore console"""
        termios.tcsetattr(
            self.file_descriptior,
            termios.TCSAFLUSH,
            self.oldterm
        )
        fcntl.fcntl(self.file_descriptior, fcntl.F_SETFL, self.oldflags)
