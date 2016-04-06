# -*- coding: utf-8 -*-

""" scoreboard view
"""
__author__ = 'Bartosz Kościów'

import abstract.view as view
import lcdmanager.widget.pane as pane #pylint: disable=I0011,F0401
import lcdmanager.widget.label as label #pylint: disable=I0011,F0401

class Scoreboard(view.View):
    """Scoreboard view"""
    def __init__(self, lcdmanager, game):
        """create all widgets"""
        self.manager = lcdmanager
        self.pane = pane.Pane(0, 0, 'scoreboard')
        self.pane.width = lcdmanager.width
        self.pane.height = lcdmanager.height
        self.game = game
        score_label = label.Label(0, 0)
        score_label.label = "S"
        self.pane.add_widget(score_label)

        live_label = label.Label(0, 1)
        live_label.label = "L"
        self.pane.add_widget(live_label)

        self.score = label.Label(2, 0)
        self.score.label = "0"
        self.pane.add_widget(self.score)

        self.lives = label.Label(2, 1)
        self.lives.label = "0"
        self.pane.add_widget(self.lives)

        self.manager.add_widget(self.pane)

    def hide(self):
        """hide tab"""
        self.pane.visibility = False

    def show(self):
        """show tab"""
        self.pane.visibility = True

    def loop(self, action):
        """tick"""
        self.score.label = str(self.game.cfg.scoreboard['score'])
        self.lives.label = str(self.game.cfg.scoreboard['lives'])
