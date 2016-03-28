#!/usr/bin/python
# -*- coding: utf-8 -*-

""" Piader v2 - configuration
"""
__author__ = 'Bartosz Kościów'


class Configuration(object):
    """Configuraton class"""
    def __init__(self):
        self.lives = 1
        self.difficulty = 'easy'
        self.lives_dict = [1, 3, 5, 7, 10]
        self.difficulty_dict = ['easy', 'hard']
