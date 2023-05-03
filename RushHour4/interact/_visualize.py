import sys
import pygame
from RushHour4.core import Map
from RushHour4.interact import Game
    
    
def load_image_objects():
    path = pygame.image.load('Images/path_border.png').convert_alpha()
    path_rect = path.get_rect()
    wall = pygame.image.load('Images/wall.png').convert_alpha()
    cop_1 = pygame.image.load('Images/cop_1_border.png').convert_alpha()
    cop_1_rect = cop_1.get_rect()
    cop_2 = pygame.image.load('Images/cop_2_border.png').convert_alpha()
    cop_2_rect = cop_2.get_rect()
    cop_3 = pygame.image.load('Images/cop_3_border.png').convert_alpha()
    cop_3_rect = cop_2.get_rect()
    thief = pygame.image.load('Images/thief_border.png').convert_alpha()
    thief_rect = thief.get_rect()

    return (wall,
            path, path_rect,
            thief, thief_rect,
            cop_1, cop_1_rect,
            cop_2, cop_2_rect,
            cop_3, cop_3_rect)

def visualize(screen, grid, image_objects, rows, cols, blockSize):
    wall, path, path_rect, thief, thief_rect, \
        cop_1, cop_1_rect, cop_2, cop_2_rect, cop_3, cop_3_rect = image_objects

    X, Y = 0, 0
    for row in range(0, blockSize * rows, blockSize):
        Y = 0
        for col in range(0, blockSize * cols, blockSize):
            rect = pygame.Rect(col, row, blockSize, blockSize)
            if grid[X][Y] == '[]':
                screen.blit(wall, (col, row))
            if grid[X][Y] == '1':
                cop_1_rect.topleft = (col, row)
                screen.blit(cop_1, cop_1_rect)
            if grid[X][Y] == '2':
                cop_2_rect.topleft = (col, row)
                screen.blit(cop_2, cop_2_rect)
            if grid[X][Y] == '3':
                cop_3_rect.topleft = (col, row)
                screen.blit(cop_3, cop_3_rect)
            if grid[X][Y] == 'x':
                thief_rect.topleft = (col, row)
                screen.blit(thief, thief_rect)
            if grid[X][Y] == 'o':
                path_rect.topleft = (col, row)
                screen.blit(path, path_rect)
            Y += 1
        X += 1