import pygame
from Player import *
from Algorithms.MCTS import *
from threading import *
from queue import Queue
import time

def drawGraph(screen, font, node, width, height, depth=0, max_depth=4):
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

        new_height = height + 50
        new_width = (w1,w2)
        drawGraph(screen, font, child, new_width, new_height, depth + 1)

        x1 = current_width
        x2 = (w2 - w1) / 2 + w1
        y1 = height
        y2 = new_height
        pygame.draw.line(screen, (126,126,126), (x1,y1), (x2, y2), 4)
        actionText = font.render("A: " + str(child.prev_action), True, (255,255,255))
        screen.blit(actionText, ((x1 + x2) / 2, (y1 + y2) / 2))

     #  pygame.draw.circle(screen, (126, 126, 126), (current_width, height), 15)

    valueText = font.render("V: " + str(round(node.V, 3)), True, (255,255,255))
    visitText = font.render("N: " + str(round(node.visit_count, 3)), True, (255,255,255))

    circle = pygame.Rect(current_width - 7.5, height - 7.5, 15, 15)
    pygame.draw.circle(screen, node.player.get_rgb(), circle.center, 7)
    screen.blit(valueText, (circle.centerx - circle.width / 2 + 10, circle.centery - circle.height / 2 + 30))
    screen.blit(visitText, (circle.centerx - circle.width / 2 + 10, circle.centery - circle.height / 2 + 40))


def draw(states, width=1280, height=720):
    pygame.init()
    screen = pygame.display.set_mode((width, height))

    done = False

    player_colour_map = {0: (255, 255, 255)}

    players = states[0].get_players()
    for player in players:
        player_colour_map[player] = player.get_rgb()


    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                pygame.image.save(screen, "output.png")
                done = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                break
               # print(pygame.mouse.get_pos())

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    pass
        state_offset_x = 0
        state_offset_y = 0

        count = 1
        for state in states:

            x_offset = 15 + state_offset_x
            y_offset = 15 + state_offset_y

            for r in range(state.rows):
                for c in range(state.cols):
                    #            for r in range(state.rows - 1, -1, -1):
                    #                for c in range(0, state.cols):
                    cell = state.get(r, c)

                    try:
                        colour = player_colour_map[cell]
                    except:
                        colour = player_colour_map[0]


                    pygame.draw.rect(screen, colour, pygame.Rect(x_offset, y_offset, 30, 30))
                    x_offset += 31
                x_offset = 15 + state_offset_x
                y_offset += 31
            state_offset_y = y_offset + 2

            if count % 3 == 0:
                state_offset_x += 260
                state_offset_y = 0

            count += 1


        pygame.display.flip()



def play(board, simulation=False, W = 1280, H=720):
    paused = False
    play_text = "Pause"
    threads = {}
    for p in board.players:
        threads[p] = None
    action_queue = Queue()


    block_size = 50
    pygame.init()

    pygame.display.set_caption("Connect4")
    font = pygame.font.SysFont("microsoftsansserif",20)
    clock = pygame.time.Clock()

    screen = pygame.display.set_mode((W, H))
    done = False

    init_offset_x = 30
    init_offset_y = 30

    board_map = {}

    t0 = time.clock()
    paused_time = 0
    while not done:
        screen.fill((0,0,0))

        if simulation and board.game_over:
            return board

        player_turn = board.get_player_turn()

        x_offset = init_offset_x
        y_offset = init_offset_y

        player_colour_map = {0: (255, 255, 255)}

        players = board.get_players()
        for player in players:
            player_colour_map[player] = player.get_rgb()
        action = None

        graph_font = pygame.font.SysFont("microsoftsansserif", 12)

        best_action = None
        worst_action = None
        for p in players:
            if isinstance(p.algorithm, MCTS):
                if p.algorithm.root is not None:
                    w = (x_offset + block_size * board.rows + 70, W - 100)
                    h = 10
                    depth = 4
                    drawGraph(screen=screen, font=graph_font, node=p.algorithm.root, width=w, height=h)

                    if p.algorithm.root.parent is not None:
                        drawGraph(screen=screen, font=graph_font, node=p.algorithm.root.parent, width=w,
                                  height=h + (60 * (depth + 1)), max_depth=depth)

                    if p.algorithm.root.best_child is not None:
                        best_action = p.algorithm.root.best_child.prev_action
                    if p.algorithm.root.worst_child is not None:
                        worst_action = p.algorithm.root.worst_child.prev_action

        for r in range(board.rows):
            for c in range(board.cols):
                #            for r in range(state.rows - 1, -1, -1):
                #                for c in range(0, state.cols):
                cell = board.get(r, c)

                try:
                    colour = player_colour_map[cell]
                except:
                    colour = player_colour_map[0]


                sz = 2.5

                ##Basically wallhack for connect4
                '''
                if c == best_action:
                    pygame.draw.rect(screen, (0,255,0), pygame.Rect(x_offset - sz, y_offset, block_size + sz/2, block_size + sz/2))
                if c == worst_action:
                    pygame.draw.rect(screen, (255,0,0), pygame.Rect(x_offset - sz, y_offset, block_size + sz/2, block_size + sz/2))
                
                
                '''
                pygame.draw.rect(screen, colour, pygame.Rect(x_offset, y_offset, block_size, block_size))

                board_map[x_offset - (x_offset % block_size), y_offset - (y_offset % block_size)] = c
                x_offset += block_size + 1
            x_offset = init_offset_x
            y_offset += block_size + 1

        for p in board.players:
            if isinstance(p, Bot):
               # if isinstance(p.algorithm, MCTS):
                    y_offset += 15

                    vals = deepcopy(p.algorithm.get_values())
                    for a, value in vals.items():
                        x = x_offset + block_size * (a) + block_size/4
                        y = y_offset
                        f = pygame.font.SysFont("microsoftsansserif", 10)
                        txt = f.render(str(round(value, 3)), True, p.get_rgb())

                        screen.blit(txt, (x, y))

        if board.game_over:
            winner = board.winner

            if winner == 0:
                txt = "DRAW"
            else:
                txt = str(winner) + " won!"

            winner_text = font.render(txt, True, Player.colours["WHITE"])

            game_over_button = pygame.Rect(y_offset / 2, y_offset / 2, 120, 60)
            pygame.draw.rect(screen, Player.colours["BLACK"], game_over_button)

            screen.blit(winner_text, (
                game_over_button.centerx - game_over_button.width / 2 + 10,
                game_over_button.centery - game_over_button.height / 2 + 5))

        else:

            player_turn_text = font.render(str(player_turn) + "'s turn!", True, Player.colours[str(player_turn)])
            screen.blit(player_turn_text, (init_offset_x + 50 + 10, init_offset_y - 25))

            if not paused:


                if isinstance(player_turn, Human):
                    human_turn = True
                else:
                    if threads[player_turn] is None:
                        t = Thread(target = lambda queue, board: queue.put(player_turn.get_choice(board)), args=(action_queue, board))
                        t.start()
                        threads[player_turn] = t
                        human_turn = False

                    else:
                        if action_queue.not_empty:
                            action = action_queue.get()
                            threads[player_turn] = None


        clock_box = pygame.Rect(init_offset_x, init_offset_y - 25, 60, 20)
        pygame.draw.rect(screen, Player.colours["AQUA"], clock_box)


       # t = time.clock() - t0
       # clock_text = font.render(str(t), True, Player.colours["WHITE"])
       # screen.blit(clock_text, (clock_box.centerx - clock_box.width / 2 + 10, clock_box.centery - clock_box.height / 2 + 5))

        reset_button = pygame.Rect(x_offset, y_offset + 15, 80, 30)
        reset_text = font.render("Reset", True, Player.colours["WHITE"])
        pygame.draw.rect(screen, Player.colours["AQUA"], reset_button)
        screen.blit(reset_text, (
        reset_button.centerx - reset_button.width / 2 + 10, reset_button.centery - reset_button.height / 2 + 5))

        play_button = pygame.Rect(reset_button.right + 20, reset_button.top, 80, 30)
        play_text_f = font.render(play_text, True, Player.colours["WHITE"])
        pygame.draw.rect(screen,Player.colours["AQUA"], play_button)
        screen.blit(play_text_f, (play_button.centerx - play_button.width / 2 + 10, play_button.centery - play_button.height / 2 + 5))

        undo_button = pygame.Rect(play_button.right + 20, reset_button.top, 80, 30)
        undo_text = font.render("Undo", True, Player.colours["WHITE"])
        pygame.draw.rect(screen,Player.colours["AQUA"], undo_button)
        screen.blit(undo_text, (
        undo_button.centerx - undo_button.width / 2 + 10, undo_button.centery - undo_button.height / 2 + 5))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                if reset_button.collidepoint(event.pos):
                    board.reset()
                    t0 = time.clock()
                    print("-----------------------------------------------------")

                if play_button.collidepoint(event.pos):
                    paused = not paused

                    if paused:
                        play_text = "Play"
                        paused_time = time.clock()
                    else:
                        play_text = "Pause"
                        t0 += paused_time
                        paused_time = 0

                if undo_button.collidepoint(event.pos):
                    board.undo()
                    print("undo")
                    pygame.display.flip()
                if human_turn:
                    x, y = pygame.mouse.get_pos()
                    try:
                        x = (x - init_offset_x)
                        y = (y - init_offset_y)
                        x = x - (x % block_size)
                        y = y - (y % block_size)

                        action = board_map[x, y]
                        if action is not None:
                            if paused:
                                paused = False
                                play_text = "Pause"
                    except:
                        continue

        if action is not None and not paused:
            board.place(action)
        pygame.display.flip()