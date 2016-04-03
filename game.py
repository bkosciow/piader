#!/usr/bin/python
# -*- coding: utf-8 -*-

""" Piader v2
"""
__author__ = 'Bartosz Kościów'

import Queue
import event_server
import local_key
import time
import views.home as home_view
import views.options as options_view
import views.game as game_view
import configuration as cfg


class Piader(object):
    """Piader main class"""
    option = {
        'game_tick': 0.5,
        'game_on': True,
        'score': 0,
        'objects': [],
        'gui_current_tab': 'home'
    }
    views = {}

    def __init__(self, game_manager, score_manager=None):
        """init class"""
        self.game_manager = game_manager
        self.score_manager = score_manager
        if self.game_manager.width < 6:
            raise ValueError("Width must be larger than 5")
        if self.game_manager.height < 4:
            raise ValueError("Height must be larger than 3")
        self.cfg = cfg.Configuration()
        self.queue = Queue.Queue()
        self.event_server = event_server.EventServerThread(self.queue)
        self.local_keyboard = local_key.Keyboard()
        self.views['home'] = home_view.Home(self.game_manager, self)
        self.views['options'] = options_view.Options(self.game_manager, self)
        self.views['game'] = game_view.Game(self.game_manager, self)

    def home_tab(self, action):
        """home tab"""
        self.views['home'].loop(action)

    def options_tab(self, action):
        """options tab"""
        self.views['options'].loop(action)

    def game_tab(self, action):
        """game tab"""
        self.views['game'].loop(action)

    def tick(self):
        """render view"""
        self.game_manager.render()
        self.game_manager.flush()

    def main_loop(self):
        """main loop"""
        self.event_server.start()
        self.set_tab('home')
        try:
            while self.option['game_on']:
                start = time.time()
                self.local_keyboard.read()
                action = self._get_action()
                if self.option['gui_current_tab'] == 'home':
                    self.home_tab(action)
                elif self.option['gui_current_tab'] == 'options':
                    self.options_tab(action)
                elif self.option['gui_current_tab'] == 'game':
                    self.game_tab(action)

                self.tick()

                end = time.time()
                if end - start < self.option['game_tick']:
                    t_delta = end - start
                    time.sleep(max(0, self.option['game_tick'] - t_delta))
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

    def quit_game(self):
        """quit game"""
        self.option['game_on'] = False

    def set_tab(self, tab):
        """change views"""
        self.views['home'].hide()
        self.views['options'].hide()
        self.views['game'].hide()
        self.views[tab].show()
        self.option['gui_current_tab'] = tab
