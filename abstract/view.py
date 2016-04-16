#!/usr/bin/python
# -*- coding: utf-8 -*-
#pylint: disable=I0011,R0913,R0902,R0921

"""View interface"""
from builtins import object


class View(object):
    """Class for views"""
    def hide(self):
        """on hide event"""
        raise NotImplementedError("hide not implemented")

    def show(self):
        """on show event - used when switching to this view.
        Should reinitialize view
        """
        raise NotImplementedError("show not implemented")

    def loop(self, action):
        """main loop, called from view manager"""
        raise NotImplementedError("loop not implemented")
