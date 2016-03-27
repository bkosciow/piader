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
    def __init__(self, lcdmanager):
        """create all widgets"""
        self.manager = lcdmanager
        self.pane = pane.Pane(0, 0, 'home')
        self.pane.width = lcdmanager.width
        self.pane.height = lcdmanager.height

        title = label.Label(self.pane.width / 2 - 5, 0, 'title')
        title.label = "Piader v2.0"
        self.pane.add_widget(title)

        button_start = button.Button(self.pane.width / 2 - 4, 1, 'btn_start')
        button_start.label = " Start "
        self.pane.add_widget(button_start)

        button_options = button.Button(self.pane.width / 2 - 5, 2, 'btn_options')
        button_options.label = " Options "
        self.pane.add_widget(button_options)

        button_quit = button.Button(self.pane.width / 2 - 3, 3, 'btn_quit')
        button_quit.label = " Quit "
        self.pane.add_widget(button_quit)

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
        pass

