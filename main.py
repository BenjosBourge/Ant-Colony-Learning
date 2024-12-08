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

    r = np.random.randint(0, nb_nodes)
    nodes[r]._is_nest = True
    nodes[r]._food = 0

    # error management
    for node in nodes:
        for c in node._connected_to:  # every connection
            found = False
            for cc in c._link._connected_to:
                if cc._link._index == node._index:
                    found = True
            if not found:
                print(node._index, " DOESN'T HAVE ITSELF IN CONNECTED ", c._link._index)

    l = 0
    for node in nodes:
        l += node._nb_connections
    print("number of connections: ", l)
    l /= len(nodes)
    print("mean number of connections per nodes: ", l)

    return nodes


def setup_ants(nodes, nb_ants, start_nest):
    ants = []
    r = 0
    if start_nest:
        for i in range(len(nodes)):
            if nodes[i]._is_nest:
                r = i
    for i in range(nb_ants):
        if not start_nest:
            r = np.random.randint(0, len(nodes))
        ants.append(Ant(nodes[r]))
    return ants


def main():
    np.random.seed(42)
    nb_node = 100
    nb_closest = 5
    nb_neighbors = 2
    nb_ants = 100
    start_nest = True
    nodes = setup_nodes(nb_node, nb_closest, nb_neighbors)
    ants = setup_ants(nodes, nb_ants, start_nest)

    score = 0
    mean_score = 0
    all_time_score = 0
    last_score = 0

    pygame.init()

    width, height = 1280, 640
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 24)
    screen = setup_screen(height, width)

    # random ants
    np.random.seed()
    it = 0
    time_spent = 0.0

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        deltaTime = clock.get_time() / 1000

        time_spent += deltaTime

        screen.fill((30, 30, 30))

        for node in nodes:
            for n in node._connected_to:
                color = (255, 255, 255)
                p = n._pheromones
                p = abs(p)
                if p > 100:
                    p = 100
                ratio = float(p) / float(100)
                cr = color[0] * (1. - ratio) + 253. * (ratio)
                cg = color[1] * (1. - ratio) + 121. * (ratio)
                cb = color[2] * (1. - ratio) + 168. * (ratio)
                pygame.draw.line(screen, (cr, cg, cb), (node._x + 140, node._y + 70), (n._link._x + 140, n._link._y + 70), width=1)

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

        new_ants = []
        for ant in ants:
            res = ant.turn(1000 * deltaTime)
            if res == 0:
                new_ants.append(ant)
            score += res
            x = ant._current_node._x + 140
            y = ant._current_node._y + 70
            if ant._in_path:
                dest_x = ant._current_path._x + 140
                dest_y = ant._current_path._y + 70
                x = x + (dest_x - x) * (1 - (ant._distanceLeft / ant._maxDistance))
                y = y + (dest_y - y) * (1 - (ant._distanceLeft / ant._maxDistance))
            color = (108, 92, 231)
            if ant._carrying_food:
                color = (232, 67, 147)
            size = 3
            pygame.draw.circle(screen, color, (x, y), size)
        ants = new_ants

        if time_spent > 5. or len(ants) == 0:
            for node in nodes:
                node.update_end_iteration()
            time_spent = 0.0
            ants = setup_ants(nodes, nb_ants, start_nest)
            it += 1
            all_time_score += score
            mean_score = all_time_score / it
            last_score = score
            score = 0

        fps = int(clock.get_fps())
        fps_text = font.render(f"FPS: {fps}", True, (255, 255, 255))
        screen.blit(fps_text, (10, 10))

        fps_text = font.render(f"Score: {all_time_score}", True, (255, 255, 255))
        screen.blit(fps_text, (100, 10))

        fps_text = font.render(f"Last Score: {last_score}", True, (255, 255, 255))
        screen.blit(fps_text, (250, 10))

        fps_text = font.render(f"This Score: {score}", True, (255, 255, 255))
        screen.blit(fps_text, (400, 10))

        fps_text = font.render(f"Mean Score: {mean_score}", True, (255, 255, 255))
        screen.blit(fps_text, (550, 10))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == '__main__':
    main()
