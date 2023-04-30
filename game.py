import pygame
from RushHour4.interact import Game

BLACK = (0, 0, 0)
WHITE = (200, 200, 200)

blockSize = 50
ROWS, COLS = 10, 10
WINDOW_HEIGHT = blockSize * ROWS
WINDOW_WIDTH = blockSize * COLS

def main():
    global SCREEN, CLOCK
    pygame.init()
    SCREEN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    CLOCK = pygame.time.Clock()
    SCREEN.fill(BLACK)

    while True:
        drawGrid()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()

def drawGrid():
    for x in range(0, WINDOW_WIDTH, blockSize):
        for y in range(0, WINDOW_HEIGHT, blockSize):
            rect = pygame.Rect(x, y, blockSize, blockSize)
            pygame.draw.rect(SCREEN, WHITE, rect, 1)

if __name__ == '__main__':
    main()