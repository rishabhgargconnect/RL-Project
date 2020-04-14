__author__ = 'Akansha Agarwal & Rishabh Garg'

import pygame
import random
import math
from pygame import mixer
import cv2

pygame.init()

class SpaceShooterGame:
    def __init__(self):

        # game initializations
        self.height = 400
        self.width = 600
        self.slack_right = self.width/10
        self.slack_left = self.width/100
        self.screen = pygame.display.set_mode((self.width,self.height))
        mixer.music.load('audio/background.wav')
        mixer.music.play(-1)
        self.c_sound = mixer.Sound('audio/explosion.wav')
        self.bullet_sound = mixer.Sound('audio/laser.wav')
        pygame.display.set_caption('   Space Fighter')
        self.icon = pygame.image.load('images/icon/icon_ufo.png')
        pygame.display.set_icon(self.icon)
        self.font = pygame.font.Font('freesansbold.ttf',16)

        # load images
        self.background_img = pygame.image.load('images/background/background_7.jpg')
        self.player_img = pygame.image.load('images/battleship/battleship_8.png')
        self.enemy_img = [pygame.image.load('images/alien/alien_1.png'),
                            pygame.image.load('images/alien/alien_1.png'),
                            pygame.image.load('images/alien/alien_1.png'),
                            pygame.image.load('images/alien/alien_1.png'),
                            pygame.image.load('images/alien/alien_1.png'),
                            pygame.image.load('images/alien/alien_1.png')]
        self.bullet_img = pygame.image.load('images/bullet/bullet_1.png')

        # game variables
        self.game_over = False
        self.high_score = 0
        self.score = 0
        self.num_enemy = 6

        # component variables
        #player
        self.player_x = (self.width-50)/2
        self.player_y = (self.height-self.height/5)
        self.player_x_speed_change = 5
        self.player_y_speed_change = 0
        #enemy
        self.enemy_x = []
        self.enemy_y = []
        self.enemy_x_speed_change = []
        self.enemy_y_speed_change = []
        self.enemy_direction = []
        for e in range(0,self.num_enemy):
            self.enemy_x.append(random.randint(int(self.width/100),int(self.width-self.width/10)))
            self.enemy_y.append(random.randint(int(self.height/90),int(self.height/70)))
            self.enemy_direction.append(random.choice([-1,1]))
            self.enemy_x_speed_change.append(3)
            self.enemy_y_speed_change.append(50)
        # bullet
        self.bullet_x = self.player_x + 35
        self.bullet_y = self.player_y
        self.bullet_y_speed_change = 5
        self.bullet_x_pos_change = self.bullet_x
        self.bullet_y_pos_change = self.bullet_y
    
    # SETTERS AND GETTERS
    # for game initializations
    def set_height(self,height):
        self.height = height
    def get_height(self):
        return self.height
    def set_width(self,width):
        self.width = width
    def get_width(self):
        return self.width
    # for game variables
    def set_score(self,score):
        self.score = score
    def get_score(self):
        return self.score
    def set_high_score(self,score):
        self.high_score = high_score
    def get_high_score(self):
        return self.high_score
    def set_enemy_count(self,count):
        self.num_enemy = count
    def get_enemy_count(self):
        return self.num_enemy
    def set_game_over(self,flag):
        self.game_over=flag
    def get_game_over(self):
        return self.game_over
    # for component variables
    def set_player_x(self,x):
        self.player_x = x
    def get_player_x(self):
        return self.player_x
    def set_player_y(self,y):
        self.player_y = y
    def get_player_y(self):
        return self.player_y
    def set_enemy_x(self,enemy_number,x):
        self.enemy_x[enemy_number]=x
    def get_enemy_x(self,enemy_number):
        return self.enemy_x[enemy_number]
    def set_enemy_y(self,enemy_number,y):
        self.enemy_y[enemy_number]=y
    def get_enemy_y(self,enemy_number):
        return self.enemy_y[enemy_number]
    def set_bullet_x(self,x):
        self.bullet_x = x
    def get_bullet_x(self):
        return self.bullet_x
    def set_bullet_y(self,y):
        self.bullet_y = y
    def get_bullet_y(self):
        return self.bullet_y
    def set_bullet_speed(self,speed):
        self.bullet_y_speed_change = speed
    def get_bullet_speed(self):
        return self.bullet_y_speed_change
    def set_player_speed(self,speed):
        self.player_x_speed_change = speed
    def get_player_speed(self):
        return self.player_x_speed_change

    # component blit functions
    def player(self):
        self.screen.blit(self.player_img,(self.player_x,self.player_y))
    def enemy(self,enemy_number):
        self.screen.blit(self.enemy_img[enemy_number],(self.enemy_x[enemy_number],self.enemy_y[enemy_number]))
    def bullet(self):
        self.screen.blit(self.bullet_img,(self.bullet_x_pos_change,self.bullet_y_pos_change))

    # player movements (game controls)
    def move_left(self):
        self.player_x+= -1 * self.player_x_speed_change
        if self.player_x<self.slack_left:
            self.player_x=self.slack_left
    def move_right(self):
        self.player_x+= 1 * self.player_x_speed_change
        if self.player_x>self.slack_right:
            self.player_x=self.slack_right
    def no_action(self):
        self.player_x = self.player_x
    
    # bullet and enemy movements (automatic)
    def fire_bullet(self):
        self.bullet_y_pos_change-=self.bullet_y_speed_change
        if self.bullet_y_pos_change<0:
            self.bullet_sound.play()
            self.bullet_y_pos_change = self.bullet_y 
            self.bullet_x_pos_change = self.player_x + 35
    def move_all_enemies(self,e):
        self.enemy_x[e] += self.enemy_x_speed_change[e]*self.enemy_direction[e]
        if self.enemy_x[e]>self.width-self.slack_right:
            self.enemy_direction[e] = -1
            self.enemy_y[e] += self.enemy_y_speed_change[e]
        if self.enemy_x[e]<self.slack_left:
            self.enemy_direction[e] = 1
            self.enemy_y[e] += self.enemy_y_speed_change[e]

    # COLLISIONS & GAME OVER
    def check_collision_enemy_bullet(self,e_x,e_y,b_x,b_y):
        # print(math.sqrt((e_x-b_x)**2 + (e_y-b_y)**2))
        return math.sqrt((e_x-b_x)**2 + (e_y-b_y)**2)<40
    def update_collision_effects(self,e):
        if self.check_collision_enemy_bullet(self.enemy_x[e],self.enemy_y[e],self.bullet_x_pos_change,self.bullet_y_pos_change):
            self.c_sound.play()
            self.bullet_y_pos_change = self.bullet_y 
            self.bullet_x_pos_change = self.player_x + 35
            self.score += 1
            self.enemy_x[e] = random.randint(int(self.width/100),int(self.width-self.width/10))
            self.enemy_y[e] = random.randint(int(self.height/90),int(self.height/70))
            self.enemy_direction[e] = random.choice([-1,1])
            print(self.score)
    def check_collision_enemy_player(self,e):
        distance_from_player = math.sqrt((self.enemy_x[e]-self.player_x)**2 + (self.enemy_y[e]-self.player_y)**2)
        if distance_from_player<50:
            self.game_over = True
            for e1 in range(0,self.num_enemy):
                self.enemy_y[e1] = self.height + 1000
            self.bullet_y_speed_change = 0
            self.bullet_y_pos_change = self.height + 1000 
            self.game_over_display(self.height/2,self.width/2)
    def check_enemy_game_over_boundary(self,e):
        if self.enemy_y[e]>self.height-self.height/10:
            self.game_over = True
            for e1 in range(0,self.num_enemy):
                self.enemy_y[e1] = self.height + 1000
            self.bullet_y_speed_change = 0
            self.bullet_y_pos_change = self.height + 1000 
            self.bullet_x_pos_change = self.player_x + 35
            self.game_over_display(self.height/2,self.width/2)
        
    # GAME DISPLAYS
    def score_display(self,x,y):
        score_display = self.font.render("Score : "+str(self.score),True,(255,255,255))
        self.screen.blit(score_display,(x,y))
    def game_over_display(self,x,y):
        self.game_over = True
        over_text = self.font.render('GAME OVER',True,(255,255,255))
        self.screen.blit(over_text,(x,y))

    # RESTART
    def restart_game(self):
        # RE-INITIALIZE
        # game variables
        self.game_over = False
        self.score = 0

        # component variables
        #player
        self.player_x = (self.width-50)/2
        self.player_y = (self.height-self.height/5)
        self.player_x_speed_change = 5
        self.player_y_speed_change = 0
        #enemy
        self.enemy_x = []
        self.enemy_y = []
        self.enemy_x_speed_change = []
        self.enemy_y_speed_change = []
        self.enemy_direction = []
        for e in range(0,self.num_enemy):
            self.enemy_x.append(random.randint(int(self.width/100),int(self.width-self.width/10)))
            self.enemy_y.append(random.randint(int(self.height/90),int(self.height/70)))
            self.enemy_direction.append(random.choice([-1,1]))
            self.enemy_x_speed_change.append(3)
            self.enemy_y_speed_change.append(50)
        # bullet
        self.bullet_x = self.player_x + 35
        self.bullet_y = self.player_y
        self.bullet_y_speed_change = 5
        self.bullet_x_pos_change = self.bullet_x
        self.bullet_y_pos_change = self.bullet_y

    def quit_game(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game_over = True

    def perform_one_step(self,action):
        self.screen.blit(self.background_img,(0,0))
        # player 
        if(action[0]==1):
            self.move_right()
        if(action[1]==1):
            self.move_left()
        if(action[2]==1):
            self.no_action()
        self.player()
        # bullet
        self.bullet()
        self.fire_bullet()
        # enemy
        for e in range(self.num_enemy):
            self.enemy(e)
            self.check_enemy_game_over_boundary(e)
            self.check_collision_enemy_player(e)
            self.move_all_enemies(e)
            self.update_collision_effects(e)

        self.score_display(10,10)
        pygame.display.update()

    def get_screenshot(self):
        rect = pygame.Rect(0, 0, self.width, self.height)
        pixels_matrix = pygame.surfarray.array3d(self.screen.subsurface(rect)).swapaxes(0,1)
        self.preprocess_screenshot(pixels_matrix)
        return pixels_matrix

    def preprocess_screenshot(self, pixels_matrix):
        grey_scale_screenshot = cv2.cvtColor(pixels_matrix, cv2.COLOR_RGB2GRAY)
        #To save image
        # cv2.imwrite('greyscale.jpg', grey_scale_screenshot)
        grey_scale_screenshot_resized = cv2.resize(grey_scale_screenshot, (84,84)) 
        grey_scale_screenshot_resized = np.reshape(grey_scale_screenshot_resized, (84,84,1))
        grey_scale_screenshot_resized_transpose = np.transpose(grey_scale_screenshot_resized, (2,0,1))
        grey_scale_screenshot_resized_transpose = grey_scale_screenshot_resized_transpose.astype(np.float32)
        #to tensor object
        grey_scale_screenshot_tensor = torch.from_numpy(grey_scale_screenshot_resized_transpose)
        # print('grey_scale_screenshot_tensor = ', grey_scale_screenshot_tensor)
        return grey_scale_screenshot_tensor