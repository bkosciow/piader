#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__ = 'Bartosz Kościów'

import RPi.GPIO as GPIO #pylint: disable=I0011,F0401
from charlcd import buffered
from charlcd.drivers.gpio import Gpio
from charlcd.drivers.i2c import I2C
from charlcd import virtual_buffered
from lcdmanager import manager
import game

GPIO.setmode(GPIO.BCM)

def main():
    """set lcds and start game"""
    # lcd_two = buffered.CharLCD(16, 2, I2C(0x20, 1), 0, 0)
    lcd_one = buffered.CharLCD(20, 4, Gpio(), 0, 0)

    drv = I2C(0x3a, 1)
    drv.pins['E2'] = 6
    lcd_three = buffered.CharLCD(40, 4, drv, 0, 0)
    lcd_three.init()

    # vlcd_main = virtual_buffered.CharLCD(16, 6)
    # vlcd_main.add_display(0, 0, lcd_one, 4, 0)
    # vlcd_main.add_display(0, 4, lcd_two)
    # vlcd_main.init()

    vlcd_support = virtual_buffered.CharLCD(4, 4)
    vlcd_support.add_display(0, 0, lcd_one)
    vlcd_support.init()

    game_manager = manager.Manager(lcd_three)
    score_manager = manager.Manager(vlcd_support)
    my_game = game.Piader(game_manager, score_manager)
    my_game.main_loop()


main()
