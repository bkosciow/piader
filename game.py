#!/usr/bin/python
# -*- coding: utf-8 -*-

""" Piader v2
"""
__author__ = 'Bartosz Kościów'

import Queue
import event_server
import local_key
import player
import enemy
import time


class Piader(object):
    """Piader main class"""
    game_tick = 0.5 #1.0
    objects = []
    score = 0
    game_on = True
    gui_current_tab = 'home'
    player = None

    def __init__(self, game_manager, score_manager=None):
        """init class"""
        self.game_manager = game_manager
        self.score_manager = score_manager
        self.width = self.game_manager.width
        self.height = self.game_manager.height
        if self.width < 6:
            raise ValueError("Width must be larger than 5")
        if self.height < 3:
            raise ValueError("Height must be larger than 2")
        self.queue = Queue.Queue()
        self.event_server = event_server.EventServerThread(self.queue)
        self.local_keyboard = local_key.Keyboard()

        self.init_game()

    def init_game(self):
        """start game"""
        self.player = player.Player(
            (self.width / 2) - 2,
            self.height - 1,
            self.width,
            self.objects
        )
        self.objects = []
        self.objects.append(enemy.Enemy(2, 0, self.width, self.objects))
        self.objects.append(self.player)

    def home_tab(self, action):
        """home tab"""
        pass

    def options_tab(self, action):
        """options tab"""
        pass

    def game_tab(self, action):
        """game tab"""
        pass

    def main_loop(self):
        """main loop"""
        self.event_server.start()
        try:
            while self.game_on:
                start = time.time()
                self.local_keyboard.read()
                action = self._get_action()
                if self.gui_current_tab == 'home':
                    self.home_tab(action)
                elif self.gui_current_tab == 'options':
                    self.options_tab(action)
                elif self.gui_current_tab == 'game':
                    self.game_tab(action)

                end = time.time()
                if end - start < self.game_tick:
                    t_delta = end - start
                    time.sleep(max(0, self.game_tick - t_delta))
        finally:
            self.local_keyboard.shutdown()
            self.event_server.join()

    def _get_action(self):
        """get event and return it"""
        try:
            event = self.queue.get(True, 0.05)
        except Queue.Empty:
            event = None

        return event
