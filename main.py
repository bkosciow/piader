#!/usr/bin/python
# -*- coding: utf-8 -*-

"""Piader v2"""

import RPi.GPIO as GPIO #pylint: disable=I0011,F0401
from charlcd import buffered #pylint: disable=I0011,F0401
from charlcd.drivers.gpio import Gpio #pylint: disable=I0011,F0401
from charlcd.drivers.i2c import I2C #pylint: disable=I0011,F0401
from charlcd import virtual_buffered #pylint: disable=I0011,F0401
from lcdmanager import manager #pylint: disable=I0011,F0401
import game

GPIO.setmode(GPIO.BCM)


def main():
    """set lcds and start game"""
    # lcd_two = buffered.CharLCD(16, 2, I2C(0x20, 1), 0, 0)
    #lcd_one = buffered.CharLCD(20, 4, Gpio(), 0, 0)
    #lcd_one.init()

    # drv = I2C(0x3a, 1)
    # drv.pins['E2'] = 6
    # lcd_three = buffered.CharLCD(40, 4, drv, 0, 0)
    # lcd_three.init()

    # vlcd_main = virtual_buffered.CharLCD(16, 4)
    # vlcd_main.add_display(0, 0, lcd_one, 4, 0)
    # vlcd_main.init()
    #
    # vlcd_support = virtual_buffered.CharLCD(4, 4)
    # vlcd_support.add_display(0, 0, lcd_one)
    # vlcd_support.init()

    i2c_20x4 = I2C(0x3b, 1)

    i2c_20x4.pins = {
        'RS': 6,
        'E': 4,
        'E2': None,
        'DB4': 0,
        'DB5': 1,
        'DB6': 2,
        'DB7': 3
    }
    lcd_game = buffered.CharLCD(20, 4, i2c_20x4, 0, 0)
    lcd_game.init()
    game_manager = manager.Manager(lcd_game)

    score_manager = None
    #score_manager = manager.Manager(vlcd_support)

    # game_manager = manager.Manager(lcd_one)
    # score_manager = manager.Manager(lcd_three)

    my_game = game.Piader(game_manager, score_manager)
    my_game.main_loop()


main()
