import sys
import time
import pygame
from RushHour4.core import Map
from RushHour4.interact import Game

blockSize = 50
ROWS, COLS = 8, 8
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

    mymap = Map(ROWS, COLS)
    # obstruct_ids = [42, 43, 44, 45, 46, 64, 65, 66, 67, 68, 69, 281,
    #                 85, 105, 125, 145, 170, 171, 172, 173, 191, 192,
    #                 193, 282, 283, 237, 257, 277]
    # for position in obstruct_ids:
    #     mymap.obstruct(position, index=True)

    game = Game(mymap, blockSize)
    game.initialize()
    game.setup_agents({'1': game.random_state()})
    game.setup_agents({'2': game.random_state()})
    game.setup_agents({'x': game.random_state()})
    drawGrid(game.grid, objects)
    pygame.display.update()
    cop_1_update, cop_2_update = {}, {}
    cop_1_updated, cop_2_updated = False, False
    cop_1_action, cop_2_action = None, None

    while True:
        key = pygame.key.get_pressed()

        # if key[pygame.K_0]: agent = 'x'
        if key[pygame.K_UP]: cop_1_action = 'up'
        if key[pygame.K_DOWN]: cop_1_action = 'down'
        if key[pygame.K_LEFT]: cop_1_action = 'left'
        if key[pygame.K_RIGHT]: cop_1_action = 'right'

        if key[pygame.K_w]: cop_2_action = 'up'
        if key[pygame.K_s]: cop_2_action = 'down'
        if key[pygame.K_a]: cop_2_action = 'left'
        if key[pygame.K_d]: cop_2_action = 'right'
        
        if cop_1_action != None:
            cop_1_update = {'1': cop_1_action}
        
        if cop_2_action != None:
            cop_2_update = {'2': cop_2_action}

        if '1' in cop_1_update.keys() and not cop_1_updated:
            game.update(cop_1_update)
            drawGrid(game.grid, objects)
            pygame.display.update()
            cop_1_action, cop_1_update = None, {}
            cop_1_updated = True
        
        if '2' in cop_2_update.keys() and cop_1_updated and not cop_2_updated:
            game.update(cop_2_update)
            drawGrid(game.grid, objects)
            pygame.display.update()
            cop_2_action, cop_2_update = None, {}
            cop_2_updated = True
        
        if cop_1_updated and cop_2_updated:
            time.sleep(1)
            thief_pos = game.locate_agent('x')
            thief_run_direction = game.thief_run()
            if thief_run_direction in game.valid_actions(thief_pos, index=True):
                game.update({'x': thief_run_direction})
            
            drawGrid(game.grid, objects)
            pygame.display.update()
            cop_1_update, cop_2_update = {}, {}
            cop_1_updated, cop_2_updated = False, False
            cop_1_action, cop_2_action = None, None
        
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
            if grid[X][Y] == 'x':
                thief_rect.topleft = (col, row)
                screen.blit(thief, thief_rect)
            if grid[X][Y] == 'o':
                path_rect.topleft = (col, row)
                screen.blit(path, path_rect)
            Y += 1
        X += 1

if __name__ == '__main__':
    main()