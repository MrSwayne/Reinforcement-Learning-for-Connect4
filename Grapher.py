import pygame
import pickle

def get_state():
    f = open("tree5.pickle", "rb")
    tree = pickle.load(f)
    return tree

def draw(tree, width=1280, height=720):
    pygame.init()
    screen = pygame.display.set_mode((width, height))
    done = False
    screen.fill((0, 0, 0))

    colour_map = {"white": (255, 255, 255),
                  "black": (0,0,0),
                  "red": (255,0,0),
                  "green": (0,255,0),
                  "blue": (0,0,255)
                  }
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                done = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                break

        pygame.draw.circle(screen, colour_map["red"], (pygame.mouse.get_pos()), 25)
        pygame.display.flip()
tree = get_state()
draw(tree)