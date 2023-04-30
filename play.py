import sys
import time
import pygame
from RushHour4.core import Map
from RushHour4.interact import Game

COLORS = {'Black':(0, 0, 0),
          'White':(175, 175, 175),
          'Blue': (0, 0, 175),
          'Red': (175, 0, 0),
          'Green': (0, 175, 175)}

blockSize = 50
ROWS, COLS = 6, 9
WINDOW_HEIGHT = blockSize * ROWS
WINDOW_WIDTH = blockSize * COLS

def main():
    global screen, CLOCK
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    clock = pygame.time.Clock()
    screen.fill(COLORS['Black'])

    map = Map(ROWS, COLS)
    obstruct_ids = [12, 13, 21, 30, 20, 29, 33, 34, 42, 43, 7, 8, 23]
    for position in obstruct_ids:
        map.obstruct(position, index=True)
    
    game = Game(map)
    agents = {'a': 0, 'b': 45, '*': 35}
    game.initialize(agents)

    while True:
        key = pygame.key.get_pressed()
        agents = keyboardInput(key, agents)
        game.update(agents)
        drawGrid(game.grid)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()

def keyboardInput(key, agents):
    if key[pygame.K_w]: agents['cop1'] = 'up'
    if key[pygame.K_s]: agents['cop1'] = 'down'
    if key[pygame.K_a]: agents['cop1'] = 'left'
    if key[pygame.K_d]: agents['cop1'] = 'right'

    if key[pygame.K_t]: agents['cop2'] = 'up'
    if key[pygame.K_g]: agents['cop2'] = 'down'
    if key[pygame.K_f]: agents['cop2'] = 'left'
    if key[pygame.K_h]: agents['cop2'] = 'right'

    if key[pygame.K_i]: agents['thief'] = 'up'
    if key[pygame.K_k]: agents['thief'] = 'down'
    if key[pygame.K_j]: agents['thief'] = 'left'
    if key[pygame.K_l]: agents['thief'] = 'right'

    return agents
    

def drawGrid(grid):
    cop1 = pygame.image.load('Images/cop1.png').convert_alpha()
    cop2 = pygame.image.load('Images/cop2.png').convert_alpha()
    thief = pygame.image.load('Images/thief.png').convert_alpha()

    X, Y = 0, 0
    for row in range(0, WINDOW_HEIGHT, blockSize):
        Y = 0
        for col in range(0, WINDOW_WIDTH, blockSize):
            rect = pygame.Rect(col, row, blockSize, blockSize)
            if grid[X][Y] == 'x':
                pygame.draw.rect(screen, COLORS['Black'], rect, 1)
            if grid[X][Y] == 'a':
                screen.blit(cop1, (col, row))
            if grid[X][Y] == 'b':
                screen.blit(cop2, (col, row))
            if grid[X][Y] == '*':
                screen.blit(thief, (col, row))
            if grid[X][Y] == 'o':
                pygame.draw.rect(screen, COLORS['White'], rect, 1)
            Y += 1
        X += 1

if __name__ == '__main__':
    main()