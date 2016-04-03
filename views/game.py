# -*- coding: utf-8 -*-

""" game view
"""
__author__ = 'Bartosz Kościów'

import abstract.view as view
import lcdmanager.widget.canvas as canvas #pylint: disable=I0011,F0401
import player
import enemy
import random


class Game(view.View):
    """Game view"""
    player = None

    def __init__(self, lcdmanager, game):
        self._options = {
            'objects': [],
            'lives': 0,
            'score': 0
        }
        self.manager = lcdmanager
        self.game = game
        self.canvas = canvas.Canvas(0, 0, lcdmanager.width, lcdmanager.height)
        self.manager.add_widget(self.canvas)

    def hide(self):
        """hide game tab"""
        self.canvas.visibility = False

    def show(self):
        """show game tab"""
        self._options['objects'] = []
        self.player = player.Player(
            (self.canvas.width / 2) - 2,
            self.canvas.height - 1,
            self.canvas.width,
            self._options['objects']
        )
        self._options['objects'].append(
            enemy.Enemy(2, 0, self.canvas.width, self._options['objects'])
        )
        self._options['objects'].append(self.player)
        self._options['lives'] = self.game.cfg.lives
        self.canvas.visibility = True

    def loop(self, action):
        """game tick"""
        if action == 'move.left':
            self.player.move_left()
        if action == 'move.right':
            self.player.move_right()
        if action == 'action':
            self.player.fire()

        self.canvas.clear()
        for item in self._options['objects']:
            item.tick()
            self.draw(item)

        self.collision_check()

    def draw(self, item):
        """draw sprite on screen"""
        (position_x, position_y) = item.get_position()

        if position_y >= self.canvas.height or position_y < 0:
            self._options['objects'].remove(item)
            item.event_discard()
            return

        self.canvas.write(item.get_sprite(), position_x, position_y)

    def collision_check(self):
        """checks for collisions"""
        for source in self._options['objects']:
            if source.can_hit():
                for target in self._options['objects']:
                    if target.is_hit(source):
                        if isinstance(target, player.Player):
                            self.player_hit()
                        if isinstance(target, enemy.Enemy):
                            self.enemy_hit(source, target)


    def enemy_hit(self, source, target):
        """event enemy hit"""
        self._options['score'] += 1
        target.event_discard()
        source.event_discard()
        self._options['objects'].remove(source)
        self._options['objects'].remove(target)
        self._options['objects'].append(
            enemy.Enemy(
                random.randint(1, self.canvas.width - 3),
                random.randint(0, self.canvas.height - 3),
                self.canvas.width,
                self._options['objects']
            )
        )

    def player_hit(self):
        """player is hit"""
        self._options['lives'] -= 1
        if self._options['lives'] <= 0:
            self.game.set_tab('gameover')
