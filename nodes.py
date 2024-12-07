import numpy as np

class Node:
    def __init__(self, x, y, i):
        self._x = x
        self._y = y
        self._connected_to = []
        self._index = i
        self._nb_connections = 0
        self._food = 0
        self._is_nest = False
        self._distances = []

    def set_neighbors(self, nodes, nb_closest, nb_neighbors):
        closest = []

        nodes_copy = nodes.copy()
        nodes_copy.remove(self)

        for i in range(nb_closest):
            closest_distance = float('inf')
            closest_node = None
            for node in nodes_copy:
                distance = np.power((self._x - node._x), 2) + np.power((self._y - node._y), 2)
                if distance < closest_distance:
                    closest_distance = distance
                    closest_node = node

            closest.append(closest_node)
            nodes_copy.remove(closest_node)

        self._connected_to = np.random.choice(closest, nb_neighbors, replace=False)
        self._nb_connections = len(self._connected_to)

    def set_both_ways(self):
        for n in self._connected_to:
            found = False
            for nn in n._connected_to:
                if nn._index == self._index:
                    found = True
                    break
            if not found:
                n._connected_to = np.append(n._connected_to, self)

    def set_connection_distances(self):
        for n in self._connected_to:
            dx = n._x - self._x
            dy = n._y - self._y
            self._distances.append(np.sqrt(dx * dx + dy * dy))
        self._nb_connections = len(self._connected_to)