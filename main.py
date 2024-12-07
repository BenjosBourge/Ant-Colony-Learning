import numpy as np
import pygame
from matplotlib import pyplot as plt
from sklearn.datasets import *
from sklearn.metrics import accuracy_score

from ant import Ant
from nodes import *


def setup_screen(height, width):
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("NN experimentation")
    return screen

def setup_nodes(nb_nodes, nb_closest, nb_neighbors):
    nodes = []
    for i in range(nb_nodes):
        nodes.append(Node(np.random.randint(0, 1000), np.random.randint(0, 500), i))

    for node in nodes:
        node.set_neighbors(nodes, nb_closest, nb_neighbors)

    for node in nodes:
        node.set_both_ways()

    for node in nodes:
        node.set_connection_distances()

    nodes[np.random.randint(0, nb_nodes)]._is_nest = True

    # error management
    for node in nodes:
        for c in node._connected_to:  # every connection
            found = False
            for cc in c._connected_to:
                if cc._index == node._index:
                    found = True
            if not found:
                print(node._index, " DOESN'T HAVE ITSELF IN CONNECTED ", c._index)

    l = 0
    for node in nodes:
        l += node._nb_connections
    print("number of connections: ", l)
    l /= len(nodes)
    print("mean number of connections per nodes: ", l)

    return nodes


def setup_ants(nodes, nb_ants):
    ants = []
    for i in range(nb_ants):
        r = np.random.randint(0, len(nodes))
        ants.append(Ant(nodes[r]))
    return ants


def main():
    np.random.seed(42)
    nb_node = 100
    nb_closest = 5
    nb_neighbors = 2
    nb_ants = 200
    nodes = setup_nodes(nb_node, nb_closest, nb_neighbors)
    ants = setup_ants(nodes, nb_ants)

    pygame.init()

    width, height = 1280, 640
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 24)
    screen = setup_screen(height, width)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        deltaTime = clock.get_time() / 1000

        screen.fill((30, 30, 30))

        for node in nodes:
            for n in node._connected_to:
                pygame.draw.line(screen, (255, 255, 255), (node._x + 140, node._y + 70), (n._x + 140, n._y + 70), width=1)

        for node in nodes:
            color = (255, 255, 255)
            size = 0 + 2 * node._nb_connections
            if node._is_nest:
                color = (9, 132, 227)
                size += 6
            if node._food > 0:
                color = (0, 184, 148)
                size += node._food / 200
            pygame.draw.circle(screen, color, (node._x + 140, node._y + 70), size)

        for ant in ants:
            ant.turn(100 * deltaTime)
            x = ant._current_node._x + 140
            y = ant._current_node._y + 70
            if ant._in_path:
                dest_x = ant._current_path._x + 140
                dest_y = ant._current_path._y + 70
                x = x + (dest_x - x) * (1 - (ant._distanceLeft / ant._maxDistance))
                y = y + (dest_y - y) * (1 - (ant._distanceLeft / ant._maxDistance))
            color = (108, 92, 231)
            size = 3
            pygame.draw.circle(screen, color, (x, y), size)

        fps = int(clock.get_fps())
        fps_text = font.render(f"FPS: {fps}", True, (255, 255, 255))
        screen.blit(fps_text, (10, 10))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == '__main__':
    main()
