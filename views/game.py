# -*- coding: utf-8 -*-

""" game view
"""
__author__ = 'Bartosz Kościów'

import abstract.view as view
import lcdmanager.widget.canvas as canvas #pylint: disable=I0011,F0401


class Game(view.View):
    """Game view"""
    def __init__(self, lcdmanager, game):
        self.manager = lcdmanager
        self.game = game
        self.canvas = canvas.Canvas(0, 0, lcdmanager.width, lcdmanager.height)
        self.manager.add_widget(self.canvas)

    def hide(self):
        """hide game tab"""
        self.canvas.visibility = False

    def show(self):
        """show home tab"""
        self.canvas.visibility = True

    def loop(self, action):
        pass
