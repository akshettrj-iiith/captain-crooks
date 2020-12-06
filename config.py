import pygame as pg
import random  # For generating random values
from math import *  # Importing math functions
import os  # Importing os for centering the game window

#   A clock for timers and running loops at constant fps
clock = pg.time.Clock()

#   Variable that game is running
running_game = True

#   Centering the game window
os.environ['SDL_VIDEO_CENTERED'] = '1'

#   Setting dimensions of the game window
screen_height = 800
screen_width = 1200

# print(screen_width / 3 + 80)

#   Parameters for Player1
pl1_X = screen_width / 3 + 100  # Initial horizontal position
pl1_Y = screen_height - 50  # Initial vertical position
p1_play = True  # Whether it is player 1's turn or not
score_p1 = 0  # Storing the score
pl1_changeX = 0  # Change in horizontal position in each frame
pl1_changeY = 0  # Change in vertical position in each frame
ship_change1 = 1  # The speed of moving obstacles for player 1
time_p1 = 0  # The time taken by player to complete the round
died_p1 = False  # Storing whether the player died or completed the round
idle_time_p1 = 0  # Idle time for player 1

#   Parameters for Player2
pl2_X = screen_width / 3 + 100  # Initial horizontal position
pl2_Y = -20  # Initial vertical position
p2_play = False  # Whether it is player 2's turn or not
score_p2 = 0  # Storing the score
pl2_changeX = 0  # Change in horizontal position in each frame
pl2_changeY = 0  # Change in vertical position in each frame
ship_change2 = 1  # The speed of moving obstacles for player 2
time_p2 = 0  # The time taken by player to complete the round
died_p2 = False  # Storing whether the player died or completed the round
idle_time_p2 = 0  # Idle time for player 2

#   RGB value for colors of slab
brown_color = (156, 91, 91)

#   Loading the icons for all the players, obstacles, coins
pl1_img = pg.image.load("icons/pl1.png")  # Player 1
pl2_img = pg.image.load("icons/pl2.png")  # Player 2
icon = pg.image.load("icons/icon.png")  # Icon for game window
rock_img = pg.image.load("icons/rock.png")  # Fixed Obstacle 1
stone_img = pg.image.load("icons/stone.png")  # Fixed Obstacle 2
ship_img = pg.image.load("icons/ship.png")  # Moving Obstacle 1
shark_img = pg.image.load('icons/shark.png')  # Moving Obstacle 2
coin_img = pg.image.load('icons/coin.png')  # Bonus Coin
loot_img = pg.image.load('icons/coinloot.png')  # Bonus Coins

#   Making list of Fixed and Moving Obstacles' Images respectively
fixed_obstacle_img = [rock_img, stone_img]
moving_obstacles_img = [ship_img, shark_img]

#   Initializing the game window
screen = pg.display.set_mode((screen_width, screen_height))  # Width and Height
pg.display.set_caption("Captain Crooks")  # Window Caption
pg.display.set_icon(icon)  # Window Icon

#   List to store the position of all the slabs
slab_height = []
#   Adding the slab positions
for i in range(5):
    slab_height.append(screen_height // 5 * i + 10)
slab_height.append(screen_height - 10)

#   List for span of each partition made by slabs
partitions = []

for i in range(5):
    partitions.append([slab_height[i], slab_height[i + 1]])

pg.init()

#   Font for Score and Time
font = pg.font.SysFont(None, 28)

#   Generating the parameters for Fixed Obstacles
fixed_obstacles = []

for i in range(1, len(slab_height) - 1):
    count = 0
    third = screen_width / 3
    for j in range(random.randint(1, 3)):
        fixed_obstacles.append([
            fixed_obstacle_img[random.randint(0, 1)],
            random.randint(third * count + 10, third * (count + 1) - 60),
            slab_height[i] - 50,
            False
        ])
        count += 1
fixed_obstacles.append([
    fixed_obstacle_img[random.randint(0, 1)],
    random.randint((screen_width / 3) * 2 + 10, (screen_width / 3) * 3 - 60),
    slab_height[0] - 50,
    False
])
fixed_obstacles.append([
    fixed_obstacle_img[random.randint(0, 1)],
    random.randint(10, (screen_width / 3) - 60),
    slab_height[5] - 50,
    False
])
fixed_obstacles.append([
    fixed_obstacle_img[random.randint(0, 1)],
    random.randint((screen_width / 3) * 2 + 10, (screen_width / 3) * 3 - 60),
    slab_height[5] - 50,
    False
])

#   Generating parameters for Moving Obstacles for Both the players
#   These differ only in the speed of the obstacles
moving_obstacles1 = []
moving_obstacles2 = []

for part in partitions:
    count = 0
    third = screen_width / 2
    for i in range(random.randint(1, 2)):
        moving_obstacles1.append([
            random.randint(third * count + 10, third * (count + 1) - 60),
            random.randint(part[0] + 10, part[1] - 70),
            ship_change1 + random.randint(-1, 1) / 2,
            False,
            moving_obstacles_img[random.randint(0, 1)]
        ])
        count += 1
for i in moving_obstacles1:
    moving_obstacles2.append(
        [i[0], i[1], ship_change2 + random.randint(-1, 1) / 2, i[3], i[4]])

#   Storing the bonus object images
coins = [coin_img, loot_img]
#   Generating the parameters for bonus objects
coin = []

for part in partitions:
    for i in range(random.randint(0, 1)):
        coin.append([
            coins[random.randint(0, 1)],
            random.randint(50, screen_width - 50),
            random.randint(part[0] + 10, part[1] - 70),
            True
        ])


#   Function to calculate distance between two points
def distance(x1, y1, x2, y2):
    return sqrt(pow(x1 - x2, 2) + pow(y1 - y2, 2))


#   Function to check collision
def is_collision(x1, y1, x2, y2):
    if distance(x1, y1, x2, y2) < 64:
        return True
    return False


#   Function to add Player1 according to turn
def player1(x, y, z):
    if z:
        screen.blit(pl1_img, (x, y))


#   Function to add Player2 according to turn
def player2(x, y, z):
    if z:
        screen.blit(pl2_img, (x, y))


#   Function to display the score of the current player
def disp_score(a, b, c, d):
    if b:
        score1 = font.render('Score: ' + str(a), True, (255, 255, 255))
    elif d:
        score1 = font.render('Score: ' + str(c), True, (255, 255, 255))
    screen.blit(score1, (0, 0))


#   Function to display the time of the current player
def disp_time(a, b, c, d):
    if b:
        time1 = font.render('Time: ' + str(round(a, 3)), True, (255, 255, 255))
    elif d:
        time1 = font.render('Time: ' + str(round(c, 3)), True, (255, 255, 255))
    screen.blit(time1, (screen_width - 150, 0))


#   Function to display the starting point of the current player
def start_point(x, y):
    start_mssg = font.render('START', True, (255, 255, 255))
    if x:
        screen.blit(start_mssg, (screen_width / 3 + 80, screen_height - 30))
    elif y:
        screen.blit(start_mssg, (screen_width / 3 + 80, 7))


#   Function to display the end point of the current player
def end_point(x, y):
    end_mssg = font.render('END', True, (255, 255, 255))
    if x:
        screen.blit(end_mssg, (screen_width / 3 + 80, 7))
    elif y:
        screen.blit(end_mssg, (screen_width / 3 + 80, screen_height - 30))


#   Generate text surface
def text_objects(font_x, text, clr):
    text_surface = font_x.render(text, True, clr)
    return text_surface, text_surface.get_rect()


#   Displaying Screen - centered text messages
def draw_text(surf, text, size, y, clr):
    font1 = pg.font.SysFont(None, size)
    text_surf, text_rect = text_objects(font1, text, clr)
    text_rect.center = (screen_width // 2), y
    surf.blit(text_surf, text_rect)


#   Function to reset the game
def reset_game():
    global pl1_X
    global pl1_Y
    global p1_play
    global score_p1
    global pl1_changeX
    global pl1_changeY
    global ship_change1
    global time_p1
    global died_p1
    pl1_X = screen_width / 3 + 100
    pl1_Y = screen_height - 50
    p1_play = True
    score_p1 = 0
    pl1_changeX = 0
    pl1_changeY = 0
    ship_change1 = 1
    time_p1 = 0
    died_p1 = False

    global pl2_X
    global pl2_Y
    global p2_play
    global score_p2
    global pl2_changeX
    global pl2_changeY
    global ship_change2
    global time_p2
    global died_p2
    pl2_X = screen_width / 3 + 100
    pl2_Y = -20
    p2_play = False
    score_p2 = 0
    pl2_changeX = 0
    pl2_changeY = 0
    ship_change2 = 1
    time_p2 = 0
    died_p2 = False

    globals()['idle_time_p1'] = 0
    globals()['idle_time_p2'] = 0

    global moving_obstacles1
    global moving_obstacles2
    global fixed_obstacles
    global coin
    moving_obstacles2 = []
    moving_obstacles1 = []
    fixed_obstacles = []
    coin = []

    for i in range(1, len(slab_height) - 1):
        count = 0
        third = screen_width / 3
        for j in range(random.randint(1, 3)):
            fixed_obstacles.append([
                fixed_obstacle_img[random.randint(0, 1)],
                random.randint(third * count + 10, third * (count + 1) - 60),
                slab_height[i] - 50,
                False
            ])
            count += 1
    fixed_obstacles.append([
        fixed_obstacle_img[random.randint(0, 1)],
        random.randint(
            (screen_width / 3) * 2 + 10,
            (screen_width / 3) * 3 - 60),
        slab_height[0] - 50,
        False
    ])
    fixed_obstacles.append([
        fixed_obstacle_img[random.randint(0, 1)],
        random.randint(10, (screen_width / 3) - 60),
        slab_height[5] - 50,
        False
    ])
    fixed_obstacles.append([
        fixed_obstacle_img[random.randint(0, 1)],
        random.randint(
            (screen_width / 3) * 2 + 10,
            (screen_width / 3) * 3 - 60),
        slab_height[5] - 50,
        False
    ])

    for part in partitions:
        count = 0
        third = screen_width / 2
        for i in range(random.randint(1, 2)):
            moving_obstacles1.append([
                random.randint(third * count + 10, third * (count + 1) - 60),
                random.randint(part[0] + 10, part[1] - 70),
                ship_change1 + random.randint(-1, 1) / 2,
                False,
                moving_obstacles_img[random.randint(0, 1)]
            ])
            count += 1
    for i in moving_obstacles1:
        moving_obstacles2.append(
            [i[0], i[1], ship_change2 + random.randint(-1, 1) / 2, i[3], i[4]])

    for part in partitions:
        for i in range(random.randint(0, 1)):
            coin.append([
                coins[random.randint(0, 1)],
                random.randint(50, screen_width - 50),
                random.randint(part[0] + 10, part[1] - 70),
                True
            ])


#   Function to confirm reset in pause menu
def confirm():
    text_color = (37, 225, 181)
    screen.fill((255, 255, 255))
    menu_confirm = True
    while menu_confirm:
        clock.tick(144)
        draw_text(
            screen,
            'Press Enter to continue',
            80,
            screen_height // 4,
            text_color)
        draw_text(
            screen,
            'Press Escape to cancel',
            80,
            3 * screen_height // 4,
            text_color)
        keys = pg.key.get_pressed()
        for event in pg.event.get():
            if keys[pg.K_LALT] or keys[pg.K_RALT]:
                if keys[pg.K_F4]:
                    menu_confirm = False
                    globals()['running_game'] = False
            if event.type == pg.QUIT:
                menu_confirm = False
                globals()['running_game'] = False
            if event.type == pg.KEYUP:
                if event.key == pg.K_RETURN:
                    reset_game()
                    menu_confirm = False
            if event.type == pg.KEYUP:
                if event.key == pg.K_ESCAPE:
                    menu_confirm = False

        pg.display.update()

    return False


#   Function for the case if player 1 collides with an obstacle
def trans_died():
    for obst in fixed_obstacles:
        obst[3] = False
    screen.fill((30, 30, 30))
    global coin
    globals()['p1_play'] = False
    globals()['p2_play'] = True
    globals()['died_p1'] = True
    globals()['idle_time_p1'] = 0
    globals()['idle_time_p2'] = 0
    for i in coin:
        i[3] = True
    wait = True
    while wait:
        clock.tick(144)
        draw_text(screen, 'Player1 Died', 80, screen_height // 4, (200, 0, 0))
        draw_text(screen,
                  'Score: ' + str(globals()['score_p1']), 50,
                  2 * screen_height // 4 - 30, (200, 0, 0)
                  )

        draw_text(screen,
                  'Time: ' + str(round(globals()['time_p1'], 3)), 50,
                  2 * screen_height // 4 + 30, (200, 0, 0)
                  )
        draw_text(screen, 'Press Enter to continue', 30,
                  3 * screen_height // 4, (200, 0, 0))
        pg.display.flip()
        keys = pg.key.get_pressed()
        for event in pg.event.get():
            if keys[pg.K_LALT] or keys[pg.K_RALT]:
                if keys[pg.K_F4]:
                    wait = False
                    globals()['running_game'] = False
            if event.type == pg.QUIT:
                wait = False
                globals()['running_game'] = False
            if event.type == pg.KEYUP:
                if event.key == pg.K_RETURN:
                    wait = False
        pg.display.update()
    globals()['score_p1'] = 0
    globals()['time_p1'] = 0


#   Function for the case if Player 1  reaches the end
def trans_win():
    for obst in fixed_obstacles:
        obst[3] = False
    screen.fill((30, 30, 30))
    globals()['p1_play'] = False
    globals()['p2_play'] = True
    globals()['died_p1'] = False
    globals()['idle_time_p1'] = 0
    globals()['idle_time_p2'] = 0
    global coin
    for i in coin:
        i[3] = True
    wait = True
    while wait:
        clock.tick(144)
        draw_text(screen, 'Hurray!!! Player1 reached the end',
                  80, screen_height // 4, (200, 0, 0))
        draw_text(screen,
                  'Score: ' + str(globals()['score_p1']), 50,
                  2 * screen_height // 4 - 30, (200, 0, 0)
                  )

        draw_text(screen,
                  'Time: ' + str(round(globals()['time_p1'], 3)), 50,
                  2 * screen_height // 4 + 30, (200, 0, 0)
                  )
        draw_text(screen, 'Press Enter to continue', 30,
                  3 * screen_height // 4, (200, 0, 0))
        pg.display.flip()
        keys = pg.key.get_pressed()
        for event in pg.event.get():
            if keys[pg.K_LALT] or keys[pg.K_RALT]:
                if keys[pg.K_F4]:
                    wait = False
                    globals()['running_game'] = False
            if event.type == pg.QUIT:
                wait = False
                globals()['running_game'] = False
            if event.type == pg.KEYUP:
                if event.key == pg.K_RETURN:
                    wait = False
        pg.display.update()
    globals()['score_p1'] = 0
    globals()['time_p1'] = 0


#   Function for the case if Player 2 dies in the game
def new_round():
    screen.fill((30, 30, 30))
    globals()['p2_play'] = False
    globals()['p1_play'] = True
    globals()['idle_time_p1'] = 0
    globals()['idle_time_p2'] = 0
    for obst in fixed_obstacles:
        obst[3] = False
    global moving_obstacles2
    global moving_obstacles1
    global coin
    moving_obstacles2 = []
    moving_obstacles1 = []
    coin = []
    globals()['died_p2'] = True

    winner = 0
    if globals()['died_p2'] == globals()['died_p1']:
        if globals()['score_p1'] > globals()['score_p2']:
            winner = 1
            globals()['ship_change1'] += 0.5
        elif globals()['score_p1'] < globals()['score_p2']:
            winner = 2
            globals()['ship_change2'] += 0.5
        elif globals()['score_p1'] == globals()['score_p2']:
            if globals()['time_p1'] > globals()['time_p2']:
                winner = 2
                globals()['ship_change2'] += 0.5
            elif globals()['time_p1'] < globals()['time_p2']:
                winner = 1
                globals()['ship_change1'] += 0.5
            else:
                winner = 0
                globals()['ship_change1'] += 0.5
                globals()['ship_change2'] += 0.5
    elif globals()['died_p1']:
        winner = 1

    elif globals()['died_p2']:
        winner = 2

    wait = True
    while wait:
        clock.tick(144)

        draw_text(screen, 'Player2 Died', 80, screen_height // 5, (200, 0, 0))
        draw_text(screen,
                  'Score: ' + str(globals()['score_p2']), 50,
                  2 * screen_height // 5 - 30, (200, 0, 0)
                  )

        draw_text(screen,
                  'Time: ' + str(round(globals()['time_p2'], 3)), 50,
                  2 * screen_height // 5 + 30, (200, 0, 0)
                  )
        if winner != 0:
            draw_text(screen, 'Player' +
                      str(winner) +
                      ' won this round!!', 40, 3 *
                      screen_height //
                      5, (200, 0, 0))
        else:
            draw_text(
                screen,
                'The round was tied, increasing speeds for both',
                40,
                3 *
                screen_height //
                5,
                (200,
                 0,
                 0))
        draw_text(screen,
                  "Press Enter for the next round", 30,
                  4 * screen_height // 5 + 30, (200, 0, 0)
                  )
        pg.display.flip()
        keys = pg.key.get_pressed()
        for events in pg.event.get():
            if keys[pg.K_LALT] or keys[pg.K_RALT]:
                if keys[pg.K_F4]:
                    wait = False
                    globals()['running_game'] = False
            if events.type == pg.QUIT:
                wait = False
                globals()['running_game'] = False
            if events.type == pg.KEYUP:
                if events.key == pg.K_RETURN:
                    wait = False
        pg.display.update()

    for part in partitions:
        for i in range(random.randint(0, 1)):
            coin.append([
                coins[random.randint(0, 1)],
                random.randint(50, screen_width - 50),
                random.randint(part[0] + 10, part[1] - 70),
                True
            ])

    for part in partitions:
        count = 0
        third = screen_width / 2
        for i in range(random.randint(1, 2)):
            moving_obstacles1.append([
                random.randint(third * count + 10, third * (count + 1) - 60),
                random.randint(part[0] + 10, part[1] - 70),
                ship_change1 + random.randint(-1, 1) / 2,
                False,
                moving_obstacles_img[random.randint(0, 1)]
            ])
            count += 1
    for i in moving_obstacles1:
        moving_obstacles2.append(
            [i[0], i[1], ship_change2 + random.randint(-1, 1) / 2, i[3], i[4]])

    globals()['score_p1'] = 0
    globals()['time_p1'] = 0
    globals()['score_p2'] = 0
    globals()['time_p2'] = 0
    globals()['pl1_X'] = screen_width / 3 + 100
    globals()['pl1_Y'] = screen_height - 50
    globals()['pl2_X'] = screen_width / 3 + 100
    globals()['pl2_Y'] = -20
    globals()['pl2_changeX'] = 0
    globals()['pl2_changeY'] = 0
    globals()['pl1_changeX'] = 0
    globals()['pl1_changeY'] = 0


#   Function for the case if Player 2 reaches the end
def new_round_win():
    screen.fill((30, 30, 30))
    globals()['p2_play'] = False
    globals()['p1_play'] = True
    globals()['idle_time_p1'] = 0
    globals()['idle_time_p2'] = 0
    for obst in fixed_obstacles:
        obst[3] = False
    global moving_obstacles2
    global moving_obstacles1
    moving_obstacles2 = []
    moving_obstacles1 = []
    global coin
    coin = []

    globals()['died_p2'] = False
    winner = 0
    if globals()['died_p2'] == globals()['died_p1']:
        if globals()['score_p1'] > globals()['score_p2']:
            winner = 1
            globals()['ship_change1'] += 0.5
        elif globals()['score_p1'] < globals()['score_p2']:
            winner = 2
            globals()['ship_change2'] += 0.5
        elif globals()['score_p1'] == globals()['score_p2']:
            if globals()['time_p1'] > globals()['time_p2']:
                winner = 2
                globals()['ship_change2'] += 0.5
            elif globals()['time_p1'] < globals()['time_p2']:
                winner = 1
                globals()['ship_change1'] += 0.5
            else:
                winner = 0
                globals()['ship_change1'] += 0.5
                globals()['ship_change2'] += 0.5

    elif globals()['died_p1']:
        winner = 1

    elif globals()['died_p2']:
        winner = 2

    wait = True
    while wait:
        clock.tick(144)

        draw_text(screen, 'Hurray!!! Player2 reached the end',
                  80, screen_height // 5, (200, 0, 0))
        draw_text(screen,
                  'Score: ' + str(globals()['score_p2']), 50,
                  2 * screen_height // 5 - 30, (200, 0, 0)
                  )

        draw_text(screen,
                  'Time: ' + str(round(globals()['time_p2'], 3)), 50,
                  2 * screen_height // 5 + 30, (200, 0, 0)
                  )
        if winner != 0:
            draw_text(screen, 'Player' +
                      str(winner) +
                      ' won this round!!', 40, 3 *
                      screen_height //
                      5, (200, 0, 0))
        else:
            draw_text(
                screen,
                'The round was tied, increasing speeds for both',
                40,
                3 *
                screen_height //
                5,
                (200,
                 0,
                 0))
        draw_text(screen,
                  "Press Enter for the next round", 30,
                  4 * screen_height // 5 + 30, (200, 0, 0)
                  )
        pg.display.flip()
        keys = pg.key.get_pressed()
        for events in pg.event.get():
            if keys[pg.K_LALT] or keys[pg.K_RALT]:
                if keys[pg.K_F4]:
                    wait = False
                    globals()['running_game'] = False
            if events.type == pg.QUIT:
                wait = False
                globals()['running_game'] = False
            if events.type == pg.KEYUP:
                if events.key == pg.K_RETURN:
                    wait = False
        pg.display.update()

    for part in partitions:
        for i in range(random.randint(0, 1)):
            coin.append([
                coins[random.randint(0, 1)],
                random.randint(50, screen_width - 50),
                random.randint(part[0] + 10, part[1] - 70),
                True
            ])

    for part in partitions:
        count = 0
        third = screen_width / 2
        for i in range(random.randint(1, 2)):
            moving_obstacles1.append([
                random.randint(third * count + 10, third * (count + 1) - 60),
                random.randint(part[0] + 10, part[1] - 70),
                ship_change1 + random.randint(-1, 1) / 2,
                False,
                moving_obstacles_img[random.randint(0, 1)]
            ])
            count += 1
    for i in moving_obstacles1:
        moving_obstacles2.append(
            [i[0], i[1], ship_change2 + random.randint(-1, 1) / 2, i[3], i[4]])

    globals()['score_p1'] = 0
    globals()['time_p1'] = 0
    globals()['score_p2'] = 0
    globals()['time_p2'] = 0
    globals()['pl1_X'] = screen_width / 3 + 100
    globals()['pl1_Y'] = screen_height - 50
    globals()['pl2_X'] = screen_width / 3 + 100
    globals()['pl2_Y'] = -20
    globals()['pl2_changeX'] = 0
    globals()['pl2_changeY'] = 0
    globals()['pl1_changeX'] = 0
    globals()['pl1_changeY'] = 0


#   Function for pause menu
def pause_game():
    text_color = (37, 225, 181)
    game_paused = True
    screen.fill((255, 255, 255))
    while game_paused:
        clock.tick(144)
        draw_text(screen, 'Game Paused', 80, screen_height // 4, text_color)
        draw_text(
            screen,
            'Press Enter to Continue',
            50,
            2 * screen_height // 4,
            text_color)
        draw_text(screen, 'Press Backspace to Reset Whole Game',
                  50, 3 * screen_height // 4, text_color)
        keys = pg.key.get_pressed()
        for event in pg.event.get():
            if keys[pg.K_LALT] or keys[pg.K_RALT]:
                if keys[pg.K_F4]:
                    game_paused = False
                    globals()['running_game'] = False
            if event.type == pg.QUIT:
                game_paused = False
                globals()['running_game'] = False
            if event.type == pg.KEYUP:
                if event.key in [pg.K_ESCAPE, pg.K_RETURN]:
                    game_paused = False
                if event.key == pg.K_BACKSPACE:
                    game_paused = confirm()

        pg.display.update()
