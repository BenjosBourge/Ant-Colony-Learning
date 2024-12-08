import numpy as np
import pygame
from matplotlib import pyplot as plt
from sklearn.datasets import *
from sklearn.metrics import accuracy_score

from ant import Ant
from nodes import *


def old_main():
    np.random.seed(42)
    nb_node = 100
    nb_closest = 5
    nb_neighbors = 2
    nb_ants = 100
    start_nest = True
    nodes = setup_nodes(nb_node, nb_closest, nb_neighbors)
    ants = setup_ants(nodes, nb_ants, start_nest)

    score = 0

    pygame.init()

    width, height = 1280, 640
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 24)
    screen = setup_screen(height, width)

    # random ants
    np.random.seed()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        deltaTime = clock.get_time() / 1000

        screen.fill((30, 30, 30))

        for node in nodes:
            for n in node._connected_to:
                color = (255, 255, 255)
                p = n._pheromones
                if p > 100:
                    p = 100
                if p < 0:
                    p = 0
                ratio = float(p) / float(100)
                cr = color[0] * (1. - ratio) + 253. * (ratio)
                cg = color[1] * (1. - ratio) + 121. * (ratio)
                cb = color[2] * (1. - ratio) + 168. * (ratio)
                pygame.draw.line(screen, (cr, cg, cb), (node._x + 140, node._y + 70),
                                 (n._link._x + 140, n._link._y + 70), width=1)

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
            score += ant.turn(100 * deltaTime)
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

        for node in nodes:
            node.decay(10 * deltaTime)

        fps = int(clock.get_fps())
        fps_text = font.render(f"FPS: {fps}", True, (255, 255, 255))
        screen.blit(fps_text, (10, 10))

        fps_text = font.render(f"Score: {score}", True, (255, 255, 255))
        screen.blit(fps_text, (100, 10))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == '__main__':
    main()
