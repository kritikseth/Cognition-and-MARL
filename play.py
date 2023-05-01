import sys
import pygame
from RushHour4.core import Map
from RushHour4.interact import Game

blockSize = 50
ROWS, COLS = 15, 30
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
    game.setup_agents(agents)
    drawGrid(game.grid, objects)
    pygame.display.update()

    while True:
        key = pygame.key.get_pressed()

        if key[pygame.K_0]: agent = 'x'
        if key[pygame.K_1]: agent = '1'
        if key[pygame.K_2]: agent = '2'

        if key[pygame.K_UP]: action = 'up'
        if key[pygame.K_DOWN]: action = 'down'
        if key[pygame.K_LEFT]: action = 'left'
        if key[pygame.K_RIGHT]: action = 'right'
        
        if agent in ['x', '1', '2'] and action != None:
            
            X, Y = game.locate_agent(agent, index=False)
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