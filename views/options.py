# -*- coding: utf-8 -*-

""" options view
"""

import abstract.view as view
import lcdmanager.widget.pane as pane #pylint: disable=I0011,F0401
import lcdmanager.widget.button as button #pylint: disable=I0011,F0401
import lcdmanager.widget.label as label #pylint: disable=I0011,F0401


class Options(view.View):
    """Options view"""
    def __init__(self, lcdmanager, game):
        """create all widgets"""
        self.manager = lcdmanager
        self.pane = pane.Pane(0, 0, 'options')
        self.pane.width = lcdmanager.width
        self.pane.height = lcdmanager.height
        self.active_button = 0
        self.game = game
        title = label.Label(self.pane.width / 2 - 4, 0, 'title')
        title.label = "Options"
        self.pane.add_widget(title)

        pos = self.pane.width / 2 - 11
        if pos < 0:
            pos = 0
        button_lives = button.Button(pos + 5, 1, 'btn_lives')
        button_lives.label = " Lives"
        button_lives.pointer_after = ""
        button_lives.callback = self._button_lives
        self.pane.add_widget(button_lives)

        self.label_lives = label.Label(pos + 12, 1)
        self.label_lives.label = str(self.game.cfg.lives)
        self.pane.add_widget(self.label_lives)

        button_difficulty = button.Button(pos, 2, 'btn_difficulty')
        button_difficulty.label = " Difficulty"
        button_difficulty.pointer_after = ""
        button_difficulty.callback = self._button_difficulty
        self.pane.add_widget(button_difficulty)

        self.label_difficulty = label.Label(pos + 12, 2)
        self.label_difficulty.label = str(self.game.cfg.difficulty)
        self.pane.add_widget(self.label_difficulty)

        button_back = button.Button(self.pane.width / 2 - 3, 3, 'btn_back')
        button_back.label = " Back "
        button_back.callback = self._button_back
        self.pane.add_widget(button_back)

        self.buttons = [
            button_lives, button_difficulty, button_back
        ]
        self.manager.add_widget(self.pane)

    def hide(self):
        """hide home tab"""
        self.buttons[self.active_button].event_blur()
        self.pane.visibility = False

    def show(self):
        """show home tab"""
        self.active_button = 0
        self.pane.visibility = True
        self.pane.get_widget('btn_lives').event_focus()

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

    def _button_back(self, widget):
        """back to home tab"""
        self.game.set_tab('home')

    def _button_difficulty(self, widget):
        """set difficulty level"""
        idx = self.game.cfg.difficulty_dict.index(self.game.cfg.difficulty) + 1
        if idx > len(self.game.cfg.difficulty_dict) - 1:
            idx = 0
        self.game.cfg.difficulty = self.game.cfg.difficulty_dict[idx]
        self.label_difficulty.label = str(self.game.cfg.difficulty)

    def _button_lives(self, widget):
        """set lives number"""
        idx = self.game.cfg.lives_dict.index(self.game.cfg.lives) + 1
        if idx > len(self.game.cfg.lives_dict) - 1:
            idx = 0
        self.game.cfg.lives = self.game.cfg.lives_dict[idx]
        self.label_lives.label = str(self.game.cfg.lives)
