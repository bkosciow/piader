#!/usr/bin/python
# -*- coding: utf-8 -*-

"""Simple key read"""
__author__ = 'Bartosz Kościów'

import socket
import termios, fcntl, sys, os

TCP_IP = '127.0.0.1'
TCP_PORT = 5005
BUFFER_SIZE = 1024


class Keyboard(object):
    """Read keyboard"""
    def __init__(self):
        self.actions = {
            'a': 'move.left',
            'd': 'move.right',
            'w': 'move.up',
            's': 'move.down',
            ' ': 'action',
            'q': 'back'
        }
        self.conn_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.conn_socket.connect((TCP_IP, TCP_PORT))
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
        self.conn_socket.send(event)

    def shutdown(self):
        """restore console"""
        termios.tcsetattr(
            self.file_descriptior,
            termios.TCSAFLUSH,
            self.oldterm
        )
        fcntl.fcntl(self.file_descriptior, fcntl.F_SETFL, self.oldflags)
