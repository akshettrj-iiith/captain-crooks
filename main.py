# For the variables and function declarations see config file

import config  # Importing the config file

config.pg.init()

while config.running_game:  # The game loop
    # Time for which previous frame ran
    time_prev_frame = config.clock.tick(144) / 1000
    #   Timer for player 1
    if config.p1_play:
        config.time_p1 += time_prev_frame  # In game time for player 1
        config.idle_time_p1 += time_prev_frame  # Idle time
    #   Timer for player 2
    elif config.p2_play:
        config.time_p2 += time_prev_frame  # In game time for player 2
        config.idle_time_p2 += time_prev_frame  # Idle time

    #   Filling game screen with blue color
    config.screen.fill((0, 119, 190))
    #   Getting all the keys that are pressed at present in list named keys
    keys = config.pg.key.get_pressed()

    #   Displaying the bonus coins
    for coin in config.coin:
        if coin[3]:
            config.screen.blit(coin[0], (coin[1], coin[2]))

    #   Adding moving obstacles for Player1
    if config.p1_play:
        for ship in config.moving_obstacles1:
            config.screen.blit(ship[4], (ship[0], ship[1]))
    #   Adding moving obstacles for Player 2
    if config.p2_play:
        for ship in config.moving_obstacles2:
            config.screen.blit(ship[4], (ship[0], ship[1]))

    #   Getting all the events in game window / screen
    for event in config.pg.event.get():
        #   For the Window Close button
        if event.type == config.pg.QUIT:
            config.running_game = False

        #   Pressing Alt + F4 will exit the game
        if keys[config.pg.K_LALT] or keys[config.pg.K_RALT]:
            if keys[config.pg.K_F4]:
                config.running_game = False

        #   Pressing Esc will pause the game
        if event.type == config.pg.KEYUP:
            if event.key == config.pg.K_ESCAPE:
                config.pause_game()

        #   Controls for Player 1 : Arrow Keys
        if config.p1_play:
            #   If the arrow keys are pressed down,
            #   then the change in position will take place
            if event.type == config.pg.KEYDOWN:
                # If Left Shift is pressed, then the player's speed will
                # increase
                if keys[config.pg.K_LSHIFT]:
                    if event.key == config.pg.K_RIGHT:
                        config.pl1_changeX = +2
                        config.idle_time_p1 = 0
                    if event.key == config.pg.K_LEFT:
                        config.pl1_changeX = -2
                        config.idle_time_p1 = 0
                    if event.key == config.pg.K_UP:
                        config.pl1_changeY = -2
                        config.idle_time_p1 = 0
                    if event.key == config.pg.K_DOWN:
                        config.pl1_changeY = +2
                        config.idle_time_p1 = 0
                #   If Left Shift key is not pressed
                else:
                    if event.key == config.pg.K_RIGHT:
                        config.pl1_changeX = +1.5
                        config.idle_time_p1 = 0
                    if event.key == config.pg.K_LEFT:
                        config.pl1_changeX = -1.5
                        config.idle_time_p1 = 0
                    if event.key == config.pg.K_UP:
                        config.pl1_changeY = -1.5
                        config.idle_time_p1 = 0
                    if event.key == config.pg.K_DOWN:
                        config.pl1_changeY = +1.5
                        config.idle_time_p1 = 0
            #   When the arrow keys are released, the player will stop moving
            if event.type == config.pg.KEYUP:
                if event.key == config.pg.K_RIGHT:
                    config.pl1_changeX = 0
                    config.idle_time_p1 = 0
                if event.key == config.pg.K_LEFT:
                    config.pl1_changeX = 0
                    config.idle_time_p1 = 0
                if event.key == config.pg.K_UP:
                    config.pl1_changeY = 0
                    config.idle_time_p1 = 0
                if event.key == config.pg.K_DOWN:
                    config.pl1_changeY = 0
                    config.idle_time_p1 = 0

            # Controls for Player2's turn : W : up, A : left, S : down, D :
            # right
        if config.p2_play:
            #   If keys are pressed down, the player will move
            if event.type == config.pg.KEYDOWN:
                # If Left Shift is pressed, then the player's speed will
                # increase
                if keys[config.pg.K_LSHIFT]:
                    if event.key == config.pg.K_d:
                        config.pl2_changeX = +2
                        config.idle_time_p2 = 0
                    if event.key == config.pg.K_a:
                        config.pl2_changeX = -2
                        config.idle_time_p2 = 0
                    if event.key == config.pg.K_w:
                        config.pl2_changeY = -2
                        config.idle_time_p2 = 0
                    if event.key == config.pg.K_s:
                        config.pl2_changeY = +2
                        config.idle_time_p2 = 0
                #    If Left Shift key is not pressed
                else:
                    if event.key == config.pg.K_d:
                        config.pl2_changeX = +1.5
                        config.idle_time_p2 = 0
                    if event.key == config.pg.K_a:
                        config.pl2_changeX = -1.5
                        config.idle_time_p2 = 0
                    if event.key == config.pg.K_w:
                        config.pl2_changeY = -1.5
                        config.idle_time_p2 = 0
                    if event.key == config.pg.K_s:
                        config.pl2_changeY = +1.5
                        config.idle_time_p2 = 0
            # If the control keys are released, then the player will stop
            # moving
            if event.type == config.pg.KEYUP:
                if event.key == config.pg.K_d:
                    config.pl2_changeX = 0
                    config.idle_time_p2 = 0
                if event.key == config.pg.K_a:
                    config.pl2_changeX = 0
                    config.idle_time_p2 = 0
                if event.key == config.pg.K_w:
                    config.pl2_changeY = 0
                    config.idle_time_p2 = 0
                if event.key == config.pg.K_s:
                    config.pl2_changeY = 0
                    config.idle_time_p2 = 0

    #   Adding the partitions i.e. the slabs in between
    for i in range(6):
        config.pg.draw.line(config.screen, config.brown_color, (0,
                            config.slab_height[i]),
                            (config.screen_width, config.slab_height[i]), 20)

    #   Adding the starting and ending
    #   point texts for the players according to whose turn is there
    config.start_point(config.p1_play, config.p2_play)
    config.end_point(config.p1_play, config.p2_play)

    #   Adding the player's icon according to whose turn is there
    config.player1(config.pl1_X, config.pl1_Y, config.p1_play)
    config.player2(config.pl2_X, config.pl2_Y, config.p2_play)

    # Variable whether the player 1 is on slab or not (will be updated in the
    # if block below)
    pl1_on_slab = False
    #   Executes in Player 1's turn
    if config.p1_play:

        #   Checking for idle time
        if config.idle_time_p1 > 5 and config.score_p1 > 5:
            config.score_p1 -= 5
            config.idle_time_p1 = 0

        #   Checking if player is on any slab
        for slab in config.slab_height:
            if abs(config.pl1_Y + 32 - slab) < 15:
                pl1_on_slab = True
                break

        #   Checking for collision with fixed obstacles and score is passed
        for i in config.fixed_obstacles:
            config.screen.blit(i[0], (i[1], i[2]))
            if config.is_collision(config.pl1_X, config.pl1_Y, i[1], i[2]):
                #   If collided, then starting the game for player 2
                config.trans_died()
            # If not collided and passed it once then increase it's score
            elif (i[2] - config.pl1_Y > 64) and (not i[3]):
                #   Variable so that it doesn't increase again
                i[3] = True
                config.score_p1 += 5
        #   Changing the position of player 1 according to the key pressed
        config.pl1_X += config.pl1_changeX
        config.pl1_Y += config.pl1_changeY

        # Condition so that player doesn't leave the screen
        if config.pl1_X < 5:
            config.pl1_X = 5
        elif config.pl1_X > 1440:
            config.pl1_X = 1440

        if config.pl1_Y < -30:
            config.pl1_Y = -30
        elif config.pl1_Y > config.screen_height - 30:
            config.pl1_Y = config.screen_height - 30

        #   Handling the moving obstacles
        for i in config.moving_obstacles1:
            #   Changing there position of the moving obstacles
            i[0] += i[2]
            #   If reached the end of the screen, then move in other direction
            if i[0] >= config.screen_width - 60 or i[0] <= 5:
                if i[4] == config.moving_obstacles_img[0]:
                    i[2] *= -1
                elif i[4] == config.moving_obstacles_img[1]:
                    i[0] = 5

            # If the player is not on slabs, then checking for collision and
            # score like fixed obstacles
            if not pl1_on_slab:
                if config.is_collision(config.pl1_X, config.pl1_Y, i[0], i[1]):
                    config.trans_died()
                #   If not collided and crossed, then increase score
                elif i[1] - config.pl1_Y > 64 and (not i[3]):
                    config.score_p1 += 10
                    i[3] = True

        #   Checking if player has reached the end
        x = config.pl1_X + 32
        y = config.pl1_Y
        if config.screen_width // 3 + \
                79 <= x <= config.screen_width // 3 + 79 + 38 and y <= 23:
            config.trans_win()

        #   Checking if player collected ant coin
        for coin in config.coin:
            if coin[3] and config.distance(
                    config.pl1_X + 32, config.pl1_Y + 32, coin[1] + 16,
                    coin[2] + 16) < 60:
                coin[3] = False
                print(coin[0])
                if coin[0] == config.coin_img:
                    config.score_p1 += 10
                else:
                    config.score_p1 += 20
    #   The same things for player 2 as they were for player 1
    pl2_on_slab = False
    if config.p2_play:

        #   Checking for idle time
        if config.idle_time_p2 > 5 and config.score_p2 > 5:
            config.score_p2 -= 5
            config.idle_time_p2 = 0

        for slab in config.slab_height:
            if abs(config.pl2_Y + 32 - slab) < 15:
                pl2_on_slab = True
                break

        for i in config.fixed_obstacles:
            config.screen.blit(i[0], (i[1], i[2]))
            if config.is_collision(config.pl2_X, config.pl2_Y, i[1], i[2]):
                config.new_round()
            elif config.pl2_Y - i[2] > 64 and (not i[3]):
                config.score_p2 += 5
                i[3] = True

        config.pl2_X += config.pl2_changeX
        config.pl2_Y += config.pl2_changeY

        if config.pl2_X < 5:
            config.pl2_X = 5
        elif config.pl2_X > 1440:
            config.pl2_X = 1440

        if config.pl2_Y < -30:
            config.pl2_Y = -30
        elif config.pl2_Y > config.screen_height - 30:
            config.pl2_Y = config.screen_height - 30

        for i in config.moving_obstacles2:
            i[0] += i[2]
            if i[0] >= config.screen_width - 60 or i[0] <= 5:
                i[2] *= -1
            if not pl2_on_slab:
                if config.is_collision(config.pl2_X, config.pl2_Y, i[0], i[1]):
                    config.new_round()
            elif config.pl2_Y - i[1] > 64 and (not i[3]):
                i[3] = True
                config.score_p2 += 10
        x = config.pl2_X + 32
        y = config.pl2_Y + 64
        if y >= config.screen_height - 30 \
                and config.screen_width / 3 + 80 <= x\
                <= config.screen_width / 3 + 80 + 34:
            config.new_round_win()

        for coin in config.coin:
            if coin[3] and \
                config.distance(
                    config.pl2_X + 32, config.pl2_Y + 32,
                    coin[1] + 16, coin[2] + 16) < 60:
                coin[3] = False
                if coin[0] == config.coin_img:
                    config.score_p2 += 10
                else:
                    config.score_p2 += 20
    #   Displaying the score and time for both the players
    config.disp_score(
        config.score_p1,
        config.p1_play,
        config.score_p2,
        config.p2_play)
    config.disp_time(
        config.time_p1,
        config.p1_play,
        config.time_p2,
        config.p2_play)

    #   Updating the game screen
    config.pg.display.update()
