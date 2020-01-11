import pygame
from Player import *


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



def play(board):


    block_size = 50
    pygame.init()

    pygame.display.set_caption("Connect4")
    font = pygame.font.SysFont("microsoftsansserif",20)
    clock = pygame.time.Clock()

    buttons = ["Reset"]





    screen = pygame.display.set_mode((400, 800))
    done = False

    init_offset_x = 30
    init_offset_y = 30

    board_map = {}
    while not done:
        action = None
        player = board.get_player_turn()

        if not board.game_over:
            if isinstance(player, Human):
                human_turn = True
            else:
                human_turn = False
                action = player.get_choice(board)


        x_offset = init_offset_x
        y_offset = init_offset_y

        player_colour_map = {0: (255, 255, 255)}

        players = board.get_players()
        for player in players:
            player_colour_map[player] = player.get_rgb()

        for r in range(board.rows):
            for c in range(board.cols):
                #            for r in range(state.rows - 1, -1, -1):
                #                for c in range(0, state.cols):
                cell = board.get(r, c)

                try:
                    colour = player_colour_map[cell]
                except:
                    colour = player_colour_map[0]

                pygame.draw.rect(screen, colour, pygame.Rect(x_offset, y_offset, block_size, block_size))

                board_map[x_offset - (x_offset % block_size), y_offset - (y_offset % block_size)] = c
                x_offset += block_size + 1
            x_offset = init_offset_x
            y_offset += block_size + 1

        clock_box = pygame.Rect(init_offset_x, init_offset_y - 25, 60, 20)
        reset_button = pygame.Rect(x_offset, y_offset + 15, 80, 30)
        reset_text = font.render("Reset", True, Player.colours["WHITE"])
        pygame.display.update()


        player_turn_text = font.render(str(player) + "'s turn!", True, Player.colours[str(player)])
        print(str(player))

        pygame.draw.rect(screen, Player.colours["AQUA"], clock_box)
        pygame.draw.rect(screen, Player.colours["AQUA"], reset_button)
        screen.blit(reset_text, (reset_button.centerx - reset_button.width / 2 + 10, reset_button.centery - reset_button.height / 2 + 5))
        screen.blit(player_turn_text, (init_offset_x + clock_box.width + 10, init_offset_y - 25))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                if reset_button.collidepoint(event.pos):
                    board.reset()
                if human_turn:
                    x, y = pygame.mouse.get_pos()
                    try:
                        x = (x - init_offset_x)
                        y = (y - init_offset_y)
                        x = x - (x % block_size)
                        y = y - (y % block_size)

                        action = board_map[x, y]
                    except:
                        continue




        if action is not None:
            board.place(action)
            player = board.get_player_turn()
        pygame.display.flip()