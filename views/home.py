# -*- coding: utf-8 -*-

""" home view
"""
__author__ = 'Bartosz Kościów'

import abstract.view as view
import lcdmanager.widget.pane as pane
import lcdmanager.widget.button as button
import lcdmanager.widget.label as label


class Home(view.View):
    """Home view"""
    def __init__(self, lcdmanager, game):
        """create all widgets"""
        self.manager = lcdmanager
        self.pane = pane.Pane(0, 0, 'home')
        self.pane.width = lcdmanager.width
        self.pane.height = lcdmanager.height
        self.active_button = 0
        self.game = game
        title = label.Label(self.pane.width / 2 - 5, 0, 'title')
        title.label = "Piader v2.0"
        self.pane.add_widget(title)

        button_start = button.Button(self.pane.width / 2 - 4, 1, 'btn_start')
        button_start.label = " Start "
        button_start.callback = self._button_start
        self.pane.add_widget(button_start)

        button_options = button.Button(self.pane.width / 2 - 5, 2, 'btn_options')
        button_options.label = " Options "
        button_options.callback = self._button_options
        self.pane.add_widget(button_options)

        button_quit = button.Button(self.pane.width / 2 - 3, 3, 'btn_quit')
        button_quit.label = " Quit "
        button_quit.callback = self._button_quit
        self.pane.add_widget(button_quit)

        self.buttons = [
            button_start, button_options, button_quit
        ]
        self.manager.add_widget(self.pane)

    def hide(self):
        """hide home tab"""
        self.pane.visibility = False

    def show(self):
        """show home tab"""
        self.pane.visibility = True
        self.pane.get_widget('btn_start').event_focus()

    def loop(self, action):
        """tick"""
        if action == 'move.up':
            self.buttons[self.active_button].event_blur()
            self._prev_button()
            self.buttons[self.active_button].event_focus()

        if action == 'move.down':
            self.buttons[self.active_button].event_blur()
            self._next_button()
            self.buttons[self.active_button].event_focus()

        if action == 'action':
            self.buttons[self.active_button].event_action()

    def _prev_button(self):
        """select previous button"""
        self.active_button -= 1
        if self.active_button < 0:
            self.active_button = len(self.buttons) - 1

    def _next_button(self):
        """select next button"""
        self.active_button += 1
        if self.active_button > len(self.buttons) - 1:
            self.active_button = 0

    def _button_quit(self, widget):
        """quit option"""
        self.game.quit_game()

    def _button_options(self, widget):
        """options"""
        print "options"

    def _button_start(self, widget):
        """start game"""
        print "start game"
