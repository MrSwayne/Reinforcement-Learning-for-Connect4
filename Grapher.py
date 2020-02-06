import pygame

class Node:

    def __init__(self,v, parent=None):
        self.children = []
        self.parent = parent
        self.value = v

    def add_child(self, *nodes):
        for n in nodes:
            self.children.append(n)



def draw(node, width, height, depth=0, max_depth=4):
    if depth == max_depth + 1:
      #  print()
        return


   # print(depth, "\t", node.value, "..", width)
    W = width[1] - width[0]

    current_width = int(W/2 + width[0])

    for i in range(len(node.children)):
        child = node.children[i]

        w1 = (i  / len(node.children) * W) + width[0]
        w2 = ((i+1)      / len(node.children) * W) + width[0]

        new_height = height + 100
        new_width = (w1,w2)
        draw(child, new_width, new_height, depth + 1)

        pygame.draw.line(screen, (255,255,255), (current_width, height), ((w2 - w1) / 2 + w1, new_height), 4)
    pygame.draw.circle(screen, (126, 126, 126), (current_width, height), 15)
n = Node(5)
n.add_child(Node(1), Node(2), Node(3), Node(4), Node(5), Node(6), Node(7))
for child in n.children:
    for i in range(7):
        child.add_child(Node(i))
pygame.init()
screen = pygame.display.set_mode((1280, 720))
done = False
while not done:
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            print(pygame.mouse.get_pos())
        if event.type == pygame.QUIT:
            pygame.quit()
            done = True
    draw(n, (0,1280), 15)
    pygame.display.flip()