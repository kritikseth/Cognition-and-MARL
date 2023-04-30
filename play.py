import sys
import time
import pygame
from RushHour4.core import Map
from RushHour4.interact import Game

blockSize = 50
ROWS, COLS = 6, 9
WINDOW_HEIGHT = blockSize * ROWS
WINDOW_WIDTH = blockSize * COLS

def main():
    global screen, CLOCK
    agent, action = None, None
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    clock = pygame.time.Clock()
    screen.fill((0, 0, 0))

    path = pygame.image.load('Images/path.png').convert_alpha()
    path_rect = path.get_rect()
    wall = pygame.image.load('Images/wall.png').convert_alpha()
    cop_1 = pygame.image.load('Images/cop_1.png').convert_alpha()
    cop_1_rect = cop_1.get_rect()
    cop_2 = pygame.image.load('Images/cop_2.png').convert_alpha()
    cop_2_rect = cop_2.get_rect()
    thief = pygame.image.load('Images/thief.png').convert_alpha()
    thief_rect = thief.get_rect()
    objects = (wall, path, path_rect, cop_1, cop_1_rect, cop_2, cop_2_rect, thief, thief_rect)

    map = Map(ROWS, COLS)
    obstruct_ids = [12, 13, 21, 30, 20, 29, 33, 34, 42, 43, 7, 8]
    for position in obstruct_ids:
        map.obstruct(position, index=True)

    game = Game(map, blockSize)
    agents = {'1': 0, '2': 45, '0': 35}
    game.initialize(agents)
    drawGrid(game.grid, objects)
    pygame.display.update()

    while True:
        key = pygame.key.get_pressed()

        if key[pygame.K_0]: agent = '0'
        if key[pygame.K_1]: agent = '1'
        if key[pygame.K_2]: agent = '2'

        if key[pygame.K_UP]: action = 'up'
        if key[pygame.K_DOWN]: action = 'down'
        if key[pygame.K_LEFT]: action = 'left'
        if key[pygame.K_RIGHT]: action = 'right'
        
        if agent in ['0', '1', '2'] and action != None:
            
            game.update({agent: action})
            agent, action = None, None

            drawGrid(game.grid, objects)
            pygame.display.update()

        if agent == None:   
            action = None
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
 

def drawGrid(grid, objects):
    wall, path, path_rect, cop_1, cop_1_rect, cop_2, cop_2_rect, thief, thief_rect = objects
    X, Y = 0, 0
    for row in range(0, WINDOW_HEIGHT, blockSize):
        Y = 0
        for col in range(0, WINDOW_WIDTH, blockSize):
            rect = pygame.Rect(col, row, blockSize, blockSize)
            if grid[X][Y] == '[]':
                screen.blit(wall, (col, row))
            if grid[X][Y] == '1':
                cop_1_rect.topleft = (col, row)
                screen.blit(cop_1, cop_1_rect)
            if grid[X][Y] == '2':
                cop_2_rect.topleft = (col, row)
                screen.blit(cop_2, cop_2_rect)
            if grid[X][Y] == '0':
                thief_rect.topleft = (col, row)
                screen.blit(thief, thief_rect)
            if grid[X][Y] == 'o':
                path_rect.topleft = (col, row)
                screen.blit(path, path_rect)
            Y += 1
        X += 1

if __name__ == '__main__':
    main()