#!/usr/bin/python
# -*- coding: utf-8 -*-

""" Piader v2
"""
from future import standard_library
standard_library.install_aliases()
from builtins import object
import queue
import event_server
import local_key
import time
import views.home as home_view
import views.options as options_view
import views.game as game_view
import views.gameover as gameover_view
import views.scoreboard as scoreboard_view
import configuration as cfg
from lcdmanager import display


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
        self.queue = queue.Queue()
        self.event_server = event_server.EventServerThread(self.queue)
        self.display = display.Display(0.5, True)
        self.display.add(self.game_manager, 'one')
        if self.score_manager:
            self.display.add(self.score_manager, 'two')
        self.local_keyboard = local_key.Keyboard()
        self.views['home'] = home_view.Home(self.game_manager, self)
        self.views['options'] = options_view.Options(self.game_manager, self)
        self.views['game'] = game_view.Game(self.game_manager, self)
        self.views['gameover'] = gameover_view.Gameover(self.game_manager, self)
        if self.score_manager:
            self.scoreboard_view = scoreboard_view.Scoreboard(self.score_manager, self)

    def main_loop(self):
        """main loop"""
        self.event_server.start()
        self.display.start()
        self.set_tab('home')
        try:
            while self.option['game_on']:
                start = time.time()
                self.local_keyboard.read()
                action = self._get_action()
                self.views[self.option['gui_current_tab']].loop(action)
                if self.score_manager:
                    self.scoreboard_view.loop(action)

                end = time.time()
                if end - start < self.option['game_tick']:
                    t_delta = end - start
                    time.sleep(max(0, self.option['game_tick'] - t_delta))
        finally:
            self.local_keyboard.shutdown()
            self.event_server.join()
            self.display.join()

    def _get_action(self):
        """get event and return it"""
        try:
            event = self.queue.get(True, 0.05)
        except queue.Empty:
            event = None

        return event

    def quit_game(self):
        """quit game"""
        self.option['game_on'] = False

    def set_tab(self, tab):
        """change views"""
        for view in self.views:
            self.views[view].hide()
        self.views[tab].show()
        self.option['gui_current_tab'] = tab
