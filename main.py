import sys
import pygame

from pygame.locals import *


turn = 1
available = True
grid = [[0, 0, 0],
        [0, 0, 0],
        [0, 0, 0]]
values = {
    0: ' ',
    1: 'X',
    -1: 'O'
}
colors = {
    0: (114, 120, 173),
    1: (198, 29, 209),
    -1: (37, 207, 197)
}

dark_blue = 0, 27, 253
light_purple = 114, 120, 173
dark_purple = 35, 0, 135
light_green = 16, 194, 81

x_win = 0
o_win = 0
pygame.init()
pygame.font.init()
pygame.display.set_caption('Tic Tac Toe')
size = w, h = 600, 400
screen = pygame.display.set_mode(size)
font = pygame.font.SysFont('Sans', 64)
font2 = pygame.font.SysFont('Sans', 16)


def draw_grid_lines(s):
    screen.fill(light_purple)
    for i in range(1, 3):
        pygame.draw.line(s, dark_blue, (int(400 * (i / 3)), 0), (int(400 * (i / 3)), 400), 2)
        pygame.draw.line(s, dark_blue, (0, int(400 * (i / 3))), (400, int(400 * (i / 3))), 2)
    pygame.draw.line(s, dark_purple, (400, 0), (400, 400), 4)
    pygame.draw.line(s, dark_purple, (500, 25), (500, 225), 4)
    pygame.draw.line(s, dark_purple, (450, 50), (550, 50), 4)
    text = font2.render('X', True, dark_purple, light_purple)
    text_rect = text.get_rect()
    text_rect.center = (475, 35)
    s.blit(text, text_rect)
    text = font2.render('O', True, dark_purple, light_purple)
    text_rect = text.get_rect()
    text_rect.center = (525, 35)
    s.blit(text, text_rect)


def display_win(winner, s):
    global x_win
    global o_win
    if winner == 'X':
        x_win += 1
    elif winner == 'O':
        o_win += 1
    if x_win > 40:
        x_win = 0
    if o_win > 40:
        o_win = 0
    text = font2.render(winner + ' has won the game', True, dark_purple, light_purple)
    text_rect = text.get_rect()
    text_rect.center = (500, 350)
    s.blit(text, text_rect)
    text = font2.render('Press R to Restart or Q to Quit', True, dark_purple, light_purple)
    text_rect = text.get_rect()
    text_rect.center = (500, 375)
    s.blit(text, text_rect)


def display_tallies(s):
    x_x_start = 455
    o_x_start = 510
    x_y_start = 55
    o_y_start = 55
    for i in range(x_win):
        if (i + 1) % 5 == 0:
            pygame.draw.line(s, dark_purple, (490, x_y_start), (455, x_y_start + 15), 1)
            x_y_start += 20
            x_x_start = 445
        else:
            pygame.draw.line(s, dark_purple, (x_x_start, x_y_start), (x_x_start, x_y_start + 15), 1)
        x_x_start += 10
    for i in range(o_win):
        if (i + 1) % 5 == 0:
            pygame.draw.line(s, dark_purple, (545, o_y_start), (510, o_y_start + 15), 1)
            o_y_start += 20
            o_x_start = 500
        else:
            pygame.draw.line(s, dark_purple, (o_x_start, o_y_start), (o_x_start, o_y_start + 15), 1)
        o_x_start += 10


def get_location(val):
    a = -1
    b = -1
    for i in range(3, 0, -1):
        if val[0] < int(400 * (i / 3)):
            a = i
        if val[1] < int(400 * (i / 3)):
            b = i
    return a, b


def draw_grid(l, s):
    global grid
    global turn
    global available
    loc = get_location(l)
    if grid[loc[0] - 1][loc[1] - 1] == 0:
        grid[loc[0] - 1][loc[1] - 1] = turn
    else:
        turn *= -1
    draw_grid_lines(s)
    for x in range(3):
        for y in range(3):
            x_pos = int((400 * (x / 3) + 400 * ((x + 1) / 3)) / 2)
            y_pos = int((400 * (y / 3) + 400 * ((y + 1) / 3)) / 2)
            text = font.render(values[grid[x][y]], True, colors[grid[x][y]], light_purple)
            text_rect = text.get_rect()
            text_rect.center = (x_pos, y_pos)
            s.blit(text, text_rect)
    blank = False
    if check_win(grid):
        available = False
        draw_win_line(grid, s)
        display_win(values[turn], s)
        blank = True
    for x in grid:
        for y in x:
            if y == 0:
                blank = True
    if not blank:
        available = False
        display_win('Nobody', s)
    turn *= -1


def check_win(g):
    val = 0
    for x in range(3):
        val = max(abs(g[x][0] + g[x][1] + g[x][2]), val)
    for x in range(3):
        val = max(abs(g[0][x] + g[1][x] + g[2][x]), val)
    val = max(abs(g[0][0] + g[1][1] + g[2][2]), val)
    val = max(abs(g[0][2] + g[1][1] + g[2][0]), val)
    if val == 3:
        return True
    else:
        return False


def draw_win_line(g, s):
    for x in range(3):
        if g[x][0] == g[x][1] == g[x][2]:
            x_pos = int((400 * (x / 3) + 400 * ((x + 1) / 3)) / 2)
            pygame.draw.line(s, light_green, (x_pos, 25), (x_pos, 375), 2)
            return 1
    for y in range(3):
        if g[0][y] == g[1][y] == g[2][y]:
            y_pos = int((400 * (y / 3) + 400 * ((y + 1) / 3)) / 2)
            pygame.draw.line(s, light_green, (25, y_pos), (375, y_pos), 2)
            return 2
    if g[0][0] == g[1][1] == g[2][2]:
        pygame.draw.line(s, light_green, (25, 25), (375, 375), 2)
        return 3
    elif g[0][2] == g[1][1] == g[2][0]:
        pygame.draw.line(s, light_green, (25, 375), (375, 25), 2)
        return 4


draw_grid_lines(screen)
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and available:
                if pygame.mouse.get_pos()[0] < 400:
                    draw_grid(pygame.mouse.get_pos(), screen)
        elif event.type == KEYDOWN:
            if event.key == K_q:
                pygame.quit()
                sys.exit()
            if event.key == K_r:
                available = True
                grid = [[0, 0, 0],
                        [0, 0, 0],
                        [0, 0, 0]]
                draw_grid_lines(screen)
    display_tallies(screen)
    pygame.display.flip()
