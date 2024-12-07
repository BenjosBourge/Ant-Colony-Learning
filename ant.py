import numpy as np

from nodes import *

class Ant:
    def __init__(self, node):
        self._current_node = node
        self._current_path = None
        self._in_path = False
        self._distanceLeft = 0
        self._maxDistance = 0

    def turn(self, distance):
        if self._in_path:
            # walking toward the new node
            self._distanceLeft -= distance
            if self._distanceLeft < 0:
                self._in_path = False
                self._current_node = self._current_path
        else:
            # action in the node
            r = np.random.randint(0, len(self._current_node._connected_to))
            self._current_path = self._current_node._connected_to[r]
            self._distanceLeft = self._current_node._distances[r]
            self._maxDistance = self._current_node._distances[r]
            self._in_path = True