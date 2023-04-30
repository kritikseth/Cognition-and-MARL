import sys
import pygame
from RushHour4.setup import Map
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
    CLOCK = pygame.time.Clock()
    screen.fill(COLORS['Black'])

    map = Map(ROWS, COLS)
    obstruct_ids = [12, 13, 21, 30, 20, 29, 33, 34, 42, 43, 7, 8, 23]
    for position in obstruct_ids:
        map.obstruct(position, index=True)
    
    game = Game(map)
    agents = {'a': 0, 'b': 45, '*': 35}
    game.initialize(agents)

    while True:
        drawGrid(game.grid)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()

def drawGrid(grid):
    X, Y = 0, 0
    for row in range(0, WINDOW_HEIGHT, blockSize):
        Y = 0
        for col in range(0, WINDOW_WIDTH, blockSize):
            print(X, Y)
            rect = pygame.Rect(col, row, blockSize, blockSize)
            if grid[X][Y] == 'x':
                pygame.draw.rect(screen, COLORS['Black'], rect, 1)
            if grid[X][Y] == 'a':
                pygame.draw.rect(screen, COLORS['Blue'], rect, 1)
            if grid[X][Y] == 'b':
                pygame.draw.rect(screen, COLORS['Green'], rect, 1)
            if grid[X][Y] == '*':
                pygame.draw.rect(screen, COLORS['Red'], rect, 1)
            if grid[X][Y] == 'o':
                pygame.draw.rect(screen, COLORS['White'], rect, 1)
            Y += 1
        X += 1

if __name__ == '__main__':
    main()