# -*- coding: utf-8 -*-

class WORKER:

    def __init__(self, name):
        self.name = name

    def enqueue(self, *args):
        put(self.name, *args)

    def dequeue(self, count):
        return get(self.name, count)

from .mp_manager import put, get
