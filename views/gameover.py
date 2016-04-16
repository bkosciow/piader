# -*- coding: utf-8 -*-

""" game over view
"""
__author__ = 'Bartosz Kościów'

import abstract.view as view
import lcdmanager.widget.pane as pane #pylint: disable=I0011,F0401
import lcdmanager.widget.label as label #pylint: disable=I0011,F0401


class Gameover(view.View):
    """Game Over view"""
    def __init__(self, lcdmanager, game):
        """create all widgets"""
        self.manager = lcdmanager
        self.pane = pane.Pane(0, 0, 'gameover')
        self.pane.width = lcdmanager.width
        self.pane.height = lcdmanager.height
        self.game = game
        title = label.Label(
            self.pane.width / 2 - 5,
            self.pane.height / 2,
            'title'
        )
        title.label = "Game Over"
        self.pane.add_widget(title)

        self.manager.add_widget(self.pane)

    def hide(self):
        """hide tab"""
        self.pane.visibility = False

    def show(self):
        """show tab"""
        self.pane.visibility = True

    def loop(self, action):
        """tick"""
        if action != None:
            self.game.set_tab('home')
