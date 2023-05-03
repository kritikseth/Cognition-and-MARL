import sys
import time
import pygame
import pickle
from RushHour4.core import Map
from RushHour4.interact import FourAgentGame
from RushHour4.utils import *

blockSize = 100
ROWS, COLS = 8, 8
WINDOW_HEIGHT = blockSize * ROWS
WINDOW_WIDTH = blockSize * COLS
BLACK, RED = (0, 0, 0), (255, 0, 0)

def main(model_type='common'):
    global screen, CLOCK
    agent, action = None, None
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    clock = pygame.time.Clock()
    screen.fill((0, 0, 0))

    path = pygame.image.load('Images/1_path.png').convert_alpha()
    path_rect = path.get_rect()
    wall = pygame.image.load('Images/wall.png').convert_alpha()
    cop_1 = pygame.image.load('Images/1_cop_1.png').convert_alpha()
    cop_1_rect = cop_1.get_rect()
    cop_2 = pygame.image.load('Images/1_cop_2.png').convert_alpha()
    cop_2_rect = cop_2.get_rect()
    cop_3 = pygame.image.load('Images/1_cop_3.png').convert_alpha()
    cop_3_rect = cop_2.get_rect()
    thief = pygame.image.load('Images/1_thief.png').convert_alpha()
    thief_rect = thief.get_rect()
    objects_original = [wall, path, path_rect, thief, thief_rect, cop_1, cop_1_rect, cop_2, cop_2_rect, cop_3, cop_3_rect]

    mymap = Map(ROWS, COLS)
    game = FourAgentGame(mymap, blockSize)
    game.initialize()
    game.setup_agents({'1': game.random_state()})
    game.setup_agents({'2': game.random_state()})
    game.setup_agents({'3': game.random_state()})
    game.setup_agents({'x': game.random_state()})
    drawGrid(game.grid, objects_original, '1')
    pygame.display.update()

    action_done = False
    action_direction = ['up', 'down', 'left', 'right']

    count_1_match, count_2_match, count_3_match = 0, 0, 0
    total_steps = 1
    
    if model_type == 'common':
        start_q_table1 = 'Models/qtable_common.pickle' # None or Filename
        with open(start_q_table1, 'rb') as f:
            q_table1 = pickle.load(f)
            q_table2 = q_table1
            q_table3 = q_table1
    elif model_type == 'separate':
        start_q_table1 = 'Models/qtable_1.pickle' # None or Filename
        start_q_table2 = 'Models/qtable_2.pickle' # None or Filename
        start_q_table3 = 'Models/qtable_3.pickle' # None or Filename
        with open(start_q_table1, 'rb') as f:
            q_table1 = pickle.load(f)
        with open(start_q_table2, 'rb') as f:
            q_table2 = pickle.load(f)
        with open(start_q_table3, 'rb') as f:
            q_table3 = pickle.load(f)

    while True:
        next = True
        drawGrid(game.grid, objects_original, '1')
        pygame.display.update()
        for agent in ['1', '2', '3']:

            next, action_done = True, False

            cop1_pos = game.locate_agent('1')
            cop2_pos = game.locate_agent('2')
            cop3_pos = game.locate_agent('3')
            thief_pos = game.locate_agent('x')
            cop1_state, cop2_state, cop3_state = get_cop_states(cop1_pos, cop2_pos, cop3_pos, thief_pos)

            while next:
                if not action_done:
                    
                    key = pygame.key.get_pressed()
                    if key[pygame.K_UP]: action = 'up'
                    elif key[pygame.K_DOWN]: action = 'down'
                    elif key[pygame.K_LEFT]: action = 'left'
                    elif key[pygame.K_RIGHT]: action = 'right'

                    if action in ['up', 'down', 'left', 'right']:
                        game.update({agent: action})

                        if agent == '1':
                            model1_prediction = perform_action(cop1_state, q_table1, 0.0)
                            if action == action_direction[model1_prediction]:
                                count_1_match += 1

                        elif agent == '2':
                            model2_prediction = perform_action(cop2_state, q_table2, 0.0)
                            if model2_prediction not in (0,1,2,3) or  action == action_direction[model2_prediction]:
                                count_2_match += 1

                        elif agent == '3':
                            model3_prediction = perform_action(cop3_state, q_table3, 0.0)
                            if model3_prediction not in (0,1,2,3) or action == action_direction[model3_prediction]:
                                count_3_match += 1
                        
                        drawGrid(game.grid, objects_original)
                        pygame.display.update()
                        
                        action_done, action = True, None

                if action_done and action == None:
                    key = pygame.key.get_pressed()
                    if key[pygame.K_SPACE]:
                        if agent == '1':
                            drawGrid(game.grid, objects_original, '2')
                            pygame.display.update()

                        elif agent == '2':
                            drawGrid(game.grid, objects_original, '3')
                            pygame.display.update()

                        elif agent == '3':
                            drawGrid(game.grid, objects_original, '1')
                            pygame.display.update()
                        next = False

                pygame.event.pump()
                
        time.sleep(1)
        thief_pos = game.locate_agent('x')
        if game._agent_location['x'] == 'end':
            total_matches = count_1_match + count_2_match + count_3_match
            print('Percentage Actions Matched : Cop 1 :', count_1_match * 100 / total_steps)
            print('Percentage Actions Matched : Cop 2 :', count_2_match * 100 / total_steps)
            print('Percentage Actions Matched : Cop 2 :', count_3_match * 100 / total_steps)
            print('Percentage Actions Matched         :', total_matches * 100 / (total_steps*3))
            print('Total Number Of Steps To Catch     :', total_steps)
            pygame.quit()
            sys.exit()
        else:
            thief_run_direction = game.thief_run()
            total_steps += 1

        if thief_run_direction in game.valid_actions(thief_pos, index=True):
            game.update({'x': thief_run_direction})

            drawGrid(game.grid, objects_original)
            pygame.display.update()

        pygame.event.pump()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                total_matches = count_1_match + count_2_match + count_3_match
                print('Percentage Actions Matched : Cop 1 :', count_1_match / total_steps)
                print('Percentage Actions Matched : Cop 2 :', count_2_match / total_steps)
                print('Percentage Actions Matched : Cop 2 :', count_3_match / total_steps)
                print('Percentage Actions Matched         :', total_matches / (total_steps*3))
                print('Total Number Of Steps To Catch     :', total_steps)
                pygame.quit()
                sys.exit()

def drawGrid(grid, objects, agent=None):
    wall, path, path_rect, thief, thief_rect, cop_1, cop_1_rect, cop_2, cop_2_rect, cop_3, cop_3_rect = objects
    X, Y = 0, 0
    for row in range(0, WINDOW_HEIGHT, blockSize):
        Y = 0
        for col in range(0, WINDOW_WIDTH, blockSize):
            rect = pygame.Rect(col, row, blockSize, blockSize)

            if agent == None:
                if grid[X][Y] == '1':
                    pygame.draw.rect(screen, BLACK, pygame.Rect(col, row, blockSize, blockSize))
                    cop_1_rect.topleft = (col, row)
                    screen.blit(cop_1, cop_1_rect)
                if grid[X][Y] == '2':
                    pygame.draw.rect(screen, BLACK, pygame.Rect(col, row, blockSize, blockSize))
                    cop_2_rect.topleft = (col, row)
                    screen.blit(cop_2, cop_2_rect)
                if grid[X][Y] == '3':
                    pygame.draw.rect(screen, BLACK, pygame.Rect(col, row, blockSize, blockSize))
                    cop_3_rect.topleft = (col, row)
                    screen.blit(cop_3, cop_3_rect)

            if agent == '1':
                if grid[X][Y] == '1':
                    pygame.draw.rect(screen, RED, pygame.Rect(col, row, blockSize, blockSize))
                    cop_1_rect.topleft = (col, row)
                    screen.blit(cop_1, cop_1_rect)
                if grid[X][Y] == '2':
                    pygame.draw.rect(screen, BLACK, pygame.Rect(col, row, blockSize, blockSize))
                    cop_2_rect.topleft = (col, row)
                    screen.blit(cop_2, cop_2_rect)
                if grid[X][Y] == '3':
                    pygame.draw.rect(screen, BLACK, pygame.Rect(col, row, blockSize, blockSize))
                    cop_3_rect.topleft = (col, row)
                    screen.blit(cop_3, cop_3_rect)
            
            elif agent == '2':
                if grid[X][Y] == '1':
                    pygame.draw.rect(screen, BLACK, pygame.Rect(col, row, blockSize, blockSize))
                    cop_1_rect.topleft = (col, row)
                    screen.blit(cop_1, cop_1_rect)
                if grid[X][Y] == '2':
                    pygame.draw.rect(screen, RED, pygame.Rect(col, row, blockSize, blockSize))
                    cop_2_rect.topleft = (col, row)
                    screen.blit(cop_2, cop_2_rect)
                if grid[X][Y] == '3':
                    pygame.draw.rect(screen, BLACK, pygame.Rect(col, row, blockSize, blockSize))
                    cop_3_rect.topleft = (col, row)
                    screen.blit(cop_3, cop_3_rect)
            
            elif agent == '3':
                if grid[X][Y] == '1':
                    pygame.draw.rect(screen, BLACK, pygame.Rect(col, row, blockSize, blockSize))
                    cop_1_rect.topleft = (col, row)
                    screen.blit(cop_1, cop_1_rect)
                if grid[X][Y] == '2':
                    pygame.draw.rect(screen, BLACK, pygame.Rect(col, row, blockSize, blockSize))
                    cop_2_rect.topleft = (col, row)
                    screen.blit(cop_2, cop_2_rect)
                if grid[X][Y] == '3':
                    pygame.draw.rect(screen, RED, pygame.Rect(col, row, blockSize, blockSize))
                    cop_3_rect.topleft = (col, row)
                    screen.blit(cop_3, cop_3_rect)
               
            if grid[X][Y] == '[]':
                pygame.draw.rect(screen, BLACK, pygame.Rect(col, row, blockSize, blockSize), 3)
                screen.blit(wall, (col, row))
            if grid[X][Y] == 'x':
                pygame.draw.rect(screen, BLACK, pygame.Rect(col, row, blockSize, blockSize), 3)
                thief_rect.topleft = (col, row)
                screen.blit(thief, thief_rect)
            if grid[X][Y] == 'o':
                pygame.draw.rect(screen, BLACK, pygame.Rect(col, row, blockSize, blockSize), 3)
                path_rect.topleft = (col, row)
                screen.blit(path, path_rect)
            Y += 1
        X += 1

if __name__ == '__main__':
    model_type = 'common'
    if len(sys.argv) == 2:
        model_type = sys.argv[1]
    main(model_type)