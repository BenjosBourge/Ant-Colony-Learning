import numpy as np

from nodes import *

class Ant:
    def __init__(self, node):
        self._current_node = node
        self._current_path = None
        self._past_node = None
        self._in_path = False
        self._distanceLeft = 0
        self._maxDistance = 0
        self._carrying_food = False
        self._oneIt = True

    def get_pheromones_value(self, pheromones):
        if not self._carrying_food:
            pheromones *= -1
        return max(pheromones, 1)

    def turn(self, distance):
        score = 0
        if self._in_path:
            # walking toward the new node
            self._distanceLeft -= distance
            if self._distanceLeft < 0:
                self._in_path = False
                self._past_node = self._current_node
                self._current_node = self._current_path
        else:
            # action in the node
            if self._current_node._food > 0 and not self._carrying_food:
                self._current_node._food -= 5
                if self._current_node._food < 0:
                    self._current_node._food = 0
                self._carrying_food = True

                # Going back
                if self._past_node is not None:
                    self._current_path = self._past_node
                    self._distanceLeft = self._maxDistance
                    self._in_path = True

                    link = None
                    for l in self._current_node._connected_to:
                        if l._link == self._current_path:
                            link = l
                            break

                    link._new_pheromones += 1
                    for l in link._link._connected_to:
                        if l._link == self._current_node:
                            l._new_pheromones -= 1
                    return 0

            if self._current_node._is_nest and self._carrying_food:
                self._carrying_food = False
                score = 1

            max = 0
            for l in self._current_node._connected_to:
                if l._link == self._past_node:
                    continue
                max += self.get_pheromones_value(l._pheromones)
            rr = np.random.randint(0, max)
            r = 0
            for l in self._current_node._connected_to:
                if l._link == self._past_node:
                    r += 1
                    continue
                p = self.get_pheromones_value(l._pheromones)
                if rr < p:
                    break
                rr -= p
                r += 1

            link = self._current_node._connected_to[r]
            self._current_path = link._link
            self._distanceLeft = link._distance
            self._maxDistance = link._distance
            if self._carrying_food:
                link._new_pheromones += 1
                for l in link._link._connected_to:
                    if l._link == self._current_node:
                        l._new_pheromones -= 1

            self._in_path = True
        return score