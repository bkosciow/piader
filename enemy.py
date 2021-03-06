#!/usr/bin/python
# -*- coding: utf-8 -*-
#pylint: disable=I0011,W0231

"""Enemy class"""

import random
import item
import bomb
import missile


class Enemy(item.Item):
    """DMO - defined moving object"""

    sprite = "<*>"

    def __init__(self, x, y, max_x, objects, cfg):
        """init enemy"""
        item.Item.__init__(self, x, y)
        self.cfg = cfg
        self.bombs = {
            "current": 0,
            "max": 1,
            "chance": 100
        }
        if cfg.difficulty == 'easy':
            self.bombs['chance'] = 30
        self.max_x = max_x
        self.objects = objects

    def tick(self):
        """action in tick"""
        if self.bombs['max'] > self.bombs['current'] and \
                        random.randint(1, 100) < self.bombs['chance']:
            self.bombs['current'] += 1
            self.objects.append(bomb.Bomb(self.pos_x + 1, self.pos_y, self))

        direction = []
        if self.pos_x > 2:
            direction.append(-1)
        if self.pos_x < self.max_x - len(self.sprite) - 1:
            direction.append(1)
        self.pos_x += random.choice(direction)

    def event_discard(self):
        """discard enemy - we are discarding enemy elsewhere"""
        pass

    def can_hit(self):
        """enemy can't hit anything"""
        return False

    def is_hit(self, target):
        """enemy can be hit"""
        if isinstance(target, missile.Missile):
            target_position = target.get_position()
            if target_position[1] == self.pos_y and \
                self.pos_x <= target_position[0] <= self.pos_x + 2:
                return True

        return False
