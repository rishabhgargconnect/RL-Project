__author__ = 'Akansha Agarwal & Rishabh Garg'

import pygame
import random
import math
from pygame import mixer

class SpaceShooterGame:
    #Global Variables
    game_over = False

    # initialize the pygame (important step)
    pygame.init()
    # display by creating a screen which takes height and width as input
    height = 600
    width = 800
    slack_right = 100
    slack_left = 10
    screen = pygame.display.set_mode((width,height))
    score = 0
    num_enemy = 6
    # the display will persist only for few milliseconds if not in a loop
    # we can control this using keys or checking for quit events
    # in pygame easy to look for events, loop over all events and 
    # check if the event being selected(key pressed) corresponds to quit
    # if it is quit then change flag value

    # background
    background_img = pygame.image.load('images/background/background_7.jpg')

    # background sound
    mixer.music.load('audio/background.wav')
    mixer.music.play(-1)

    # title and icon
    # title reference : self-innovation
    # icon reference : Icons made by flaticon.com
    pygame.display.set_caption('   Space Fighter')
    icon = pygame.image.load('images/icon/icon_ufo.png')
    pygame.display.set_icon(icon)

    # display score on screen
    font = pygame.font.Font('freesansbold.ttf',16)
    text_x = 10
    text_y = 10
    def display_score(x,y):
        score_display = font.render("Score : "+str(score),True,(255,255,255))
        screen.blit(score_display,(x,y))

    # GAME OVER
    def game_over(x,y):
        is_game_over = True
        over_text = font.render('GAME OVER',True,(255,255,255))
        screen.blit(over_text,(x,y))

    # PLAYER [BATTLESHIP]
    # image for player
    player_img = pygame.image.load('images/battleship/battleship_8.png')
    # coordinates are given such that player appears in the middle of screen
    player_x = 370
    player_y = 480
    direction_for_player = 1
    player_x_speed_change = 5
    player_y_speed_change = 1
    player_x_pos_change = 0
    player_y_pos_change = 0
    # function for player
    def player(x,y):
        # to draw something on screen, blit is used
        screen.blit(player_img,(x,y))


    # ENEMY [ALIEN]
    # image for enemy
    enemy_img = [pygame.image.load('images/alien/alien_1.png'),
                    pygame.image.load('images/alien/alien_1.png'),
                    pygame.image.load('images/alien/alien_1.png'),
                    pygame.image.load('images/alien/alien_1.png'),
                    pygame.image.load('images/alien/alien_1.png'),
                    pygame.image.load('images/alien/alien_1.png')]
    # coordinates are given such that player appears in the middle of screen

    enemy_x = []
    enemy_y = []
    enemy_x_pos_change = []
    enemy_y_pos_change = []
    enemy_x_speed_change = []
    enemy_y_speed_change = []
    direction_for_enemy = []
    for e in range(0,num_enemy):
        enemy_x.append(random.randint(10,700))
        enemy_y.append(random.randint(10,200))
        direction_for_enemy.append(random.choice([-1,1]))
        # we want enemy to move left and right
        enemy_x_speed_change.append(3)
        # we want enemy to go down when it hits boundary
        enemy_y_speed_change.append(50)
        enemy_x_pos_change.append(0)
        enemy_y_pos_change.append(0)
    # function for enemy
    def enemy(i,x,y):
        # to draw something on screen, blit is used
        screen.blit(enemy_img[i],(x,y))

    # BULLET
    # bullet will have 2 states, when it is ready for fire
    # and when it is fired
    bullet_img = pygame.image.load('images/bullet/bullet_1.png')
    # coordinates are given such that player appears in the middle of screen
    bullet_x = player_x + 35
    bullet_y = player_y
    bullet_y_speed_change = 10
    bullet_x_pos_change = bullet_x
    bullet_y_pos_change = bullet_y
    # ready state means we cannot see bullet on screen
    # fire means the bullet is moving
    # function for bullet
    def bullet(x,y):
        # to draw something on screen, blit is used
        screen.blit(bullet_img,(x,y))

    # COLLISION
    def collision(e_x,e_y,b_x,b_y):
        distance = math.sqrt((e_x-b_x)**2 + (e_y-b_y)**2)
        if distance<40:
            return True
        return False

    running = True
    # GAME LOOP : makes sure that game is running infinitely
    while running:
        # if we want something to appear continuously, it should be in this loop
        # screen.fill((48,34,75))
        screen.blit(background_img,(0,0))
        # exit condition
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
            # check for left and right arrow keys
            # keydown means that if any key is pressed
            if event.type == pygame.KEYDOWN:
                # check if key pressed is left or right
                if event.key == pygame.K_LEFT:
                    player_x_pos_change = -1*player_x_speed_change
                if event.key == pygame.K_RIGHT:
                    player_x_pos_change = player_x_speed_change
            # need to check the release of keys too
            # keyup used for that
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    player_x_pos_change=0

        # player movement
        # once the key events are handled,
        # we define boundaries as well as change the coordinates accordingly
        player_x+=player_x_pos_change
        if player_x<slack_left:
            player_x=slack_left
        if player_x>width-slack_right:
            player_x=width-slack_right
        player(player_x,player_y)
        
        # enemy movement
        # for enemy we define random position, horizontal as well as
        # vertical movement, also a check for boundaries is placed
        # for e in range(0,num_enemy):
        #     enemy(enemy_img,enemy_x[e],enemy_y[e])
        for e in range(0,num_enemy):
            # game over
            if enemy_y[e]>500:
                for e1 in range(0,num_enemy):
                    enemy_y[e1] = 1000
                bullet_y_speed_change = 0
                bullet_y_pos_change = 1000 
                bullet_x_pos_change = player_x + 35
                game_over(250,250)
                break
            distance_from_player = math.sqrt((enemy_x[e]-player_x)**2 + (enemy_y[e]-player_y)**2)
            if distance_from_player<50:
                for e1 in range(0,num_enemy):
                    enemy_y[e1] = 1000
                bullet_y_speed_change = 0
                bullet_y_pos_change = 1000 
                bullet_x_pos_change = player_x + 35
                game_over(250,250)
                break

            enemy(e,enemy_x[e],enemy_y[e])
            enemy_x[e] += enemy_x_speed_change[e]*direction_for_enemy[e]
            if enemy_x[e]>width-slack_right:
                direction_for_enemy[e] = -1
                enemy_y[e] += enemy_y_speed_change[e]
            if enemy_x[e]<slack_left:
                direction_for_enemy[e] = 1
                enemy_y[e] += enemy_y_speed_change[e]

            # collision detection
            collided = collision(enemy_x[e],enemy_y[e],bullet_x_pos_change,bullet_y_pos_change)
            if collided:
                c_sound = mixer.Sound('audio/explosion.wav')
                c_sound.play()
                bullet_y_pos_change = bullet_y 
                bullet_x_pos_change = player_x + 35
                score += 1
                if(score%10 == 0):
                    enemy_x_speed_change[e]+=2
                    enemy_y_speed_change[e]+=10
                enemy_x[e] = random.randint(10,700)
                enemy_y[e] = random.randint(10,200)
                print(score)



        # fire bullet as soon as previous one goes from screen
        bullet(bullet_x_pos_change,bullet_y_pos_change)
        bullet_y_pos_change-=bullet_y_speed_change
        if bullet_y_pos_change<0:
            bullet_sound = mixer.Sound('audio/laser.wav')
            bullet_sound.play()
            bullet_y_pos_change = bullet_y 
            bullet_x_pos_change = player_x + 35
        
    
        display_score(text_x,text_y)
        # need to update everyone that is added (important)
        pygame.display.update()



    #Getters and Setters and more functions
    def is_game_over():
        return game_over
        

    def restart_game():
        # re-initialise variables define new function
        game_over = False
        player_x = 370
        player_y = 480
        direction_for_player = 1
        player_x_speed_change = 5
        player_y_speed_change = 1
        player_x_pos_change = 0
        player_y_pos_change = 0
        enemy_x = []
        enemy_y = []
        enemy_x_pos_change = []
        enemy_y_pos_change = []
        enemy_x_speed_change = []
        enemy_y_speed_change = []
        direction_for_enemy = []   
        bullet_x = player_x + 35
        bullet_y = player_y
        bullet_y_speed_change = 10
        bullet_x_pos_change = bullet_x
        bullet_y_pos_change = bullet_y 
        running = True

        # Now call function for starting while loop
        return True