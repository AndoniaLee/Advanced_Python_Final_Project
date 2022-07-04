'''
Created By  : Xiaonan Li / Peiyu Xiao / Xinyu Wang / Xujia Li
Created Date: 04 / 07 / 2022
Created For : Advanced Programming of Python Final Project
'''

import pygame
from ball import *
import random


'''
Game Initialization:
    1) Set up the macros, constants and flags
    2) Load the images, sound effects and fonts
'''

print("---------------------------------------------------------------------------")
print("Game Initializing...")

# macros
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BEGINNING = 0
PLAYING = 1
END = 2
WHITE = (255, 255, 255)

# initialize pygame
pygame.init()
screen = pygame.display.set_mode([SCREEN_WIDTH,SCREEN_HEIGHT])
pygame.display.set_caption("Pong!")

# load images and fonts
bg = pygame.image.load("images/bg.jpg")
title_font = pygame.font.SysFont("Arial Black",60)
font = pygame.font.SysFont("Ayuthaya",24)




'''
Functions:
    Set up functions that is used for the game.
'''

def check_collide(ball, p_x, p_y, p_w):
    '''
        Parameters: ball instance, paddle's x and y coordinates and paddle's width
        Return: None. But change the ball's status based on calculations
    '''
    lose = ball.lose
    if lose:
        return
    [b_x, b_y] = ball.get_pos()
    b_d = ball.get_size()

    if b_y + b_d >= p_y: 
        if b_x + (b_d / 2) * 0.7 > p_x + p_w \
            or b_x + (b_d / 2) * 1.3 < p_x:
            ball.set_lose()
            ball.play_lose_sound()
        else: # collide
            ball.play_hit_sound()
            ball.add_score()
            ball.reverse_y_speed()
'''
Main:
    Main function that contains the game loop.
'''

def main():

    #### Variable Initialization ####

    # initialize score and status
    score = 0
    status = BEGINNING
   
    # initialize paddle
    paddle = pygame.image.load("images/paddle.png")
    paddle_width = 100
    paddle_height = 25
    paddle_x = 400
    paddle_y = SCREEN_HEIGHT - paddle_height - 5
    paddle_speed = 0

    # instantiate ball
    ball_img = pygame.image.load("images/ball.png")
    ball_x_speed = 1
    ball_y_speed = 1
    ball_x = 150
    ball_y = 150
    ball_d = 20
    ball_list = []
    ball_list.append(Ball(ball_img, ball_x, ball_y, ball_d, ball_x_speed, ball_y_speed))

    # initialize timer
    timer = 0
    timer_update = 0
    if_update = False
    
    #### Main While Loop ####

    print("---------------------------------------------------------------------------")
    print("Game at beginning stage")
    
    while True:

        # Event monitoring
        
        for event in pygame.event.get():

            # Monitor quit button
            if event.type == pygame.QUIT:
                print("---------------------------------------------------------------------------")
                print("Quiting game...")
                return

            # Monitor keyboard inputs
            elif event.type == pygame.KEYDOWN:
                key = event.key
                if key == pygame.K_RIGHT:
                    paddle_speed = 15
                elif key == pygame.K_LEFT:
                    paddle_speed = -15
                elif key == pygame.K_s and status == BEGINNING:
                    status = PLAYING
                    timer = 0
                    timer_update = 0
                    print("---------------------------------------------------------------------------")
                    print("Game at playing stage")  
                elif key == pygame.K_r and status == END:
                    status = BEGINNING
                    print("---------------------------------------------------------------------------")
                    print("Game restarting...")
            elif event.type == pygame.KEYUP:
                paddle_speed = 0

        # Status checking
        if status == PLAYING:
            
            screen.blit(bg, (0, 0))
            timer += 1
            timer_update += 1

            # Generate a random ball at random place every 1000 frames
            if timer == 1000:
                ball_x = random.randint(100,SCREEN_WIDTH)
                ball_y = random.randint(40,SCREEN_HEIGHT/3)
                which_ball = random.choice([Ball,Speed_Change_Ball,Size_Change_Ball])
                new_ball = which_ball(ball_img, ball_x, ball_y, ball_d, ball_x_speed, ball_y_speed)
                print("A",new_ball.get_type(),"ball is generated...")
                ball_list.append(new_ball)
                timer = 0
            
            # Change ball position, update ball's speed or size based on its class
            score = 0
            if timer_update == 20:
                if_update = True
                timer_update = 0
                
            for ball in ball_list:
                [lose, ball_score] = ball.move(SCREEN_WIDTH, SCREEN_HEIGHT)
                score += ball_score
                if lose:
                    print("---------------------------------------------------------------------------")
                    print("Game at ending stage")
                    status = END
                    break
                
                check_collide(ball, paddle_x, paddle_y, paddle_width)

                if if_update:
                    ball.update()
                ball.draw(screen)

            if if_update:
                if_update = False
            
            # Change paddle position 
            paddle_x += paddle_speed
            if paddle_x + paddle_width >= SCREEN_WIDTH:
                paddle_x = SCREEN_WIDTH - paddle_width
            if paddle_x <= 0:
                paddle_x = 0
            screen.blit(paddle, (paddle_x, paddle_y))

            # Show score
            gamestring = " Score: "+str(score)
            text = font.render(gamestring,True,WHITE)
            screen.blit(text,(50,50))

        elif status == BEGINNING:
            
            screen.blit(bg, (0, 0))

            # Add the first ball
            ball_list = []
            ball_list.append(Ball(ball_img, ball_x, ball_y, ball_d, ball_x_speed, ball_y_speed))

            # Show text
            welcomestring = "MINI PONG"
            text = title_font.render(welcomestring,True,WHITE)
            screen.blit(text,(220,200))
            
            welcomestring = "Welcome to the pong game"
            text = font.render(welcomestring,True,WHITE)
            screen.blit(text,(240,350))

            welcomestring = "Please press S to start"
            text = font.render(welcomestring,True,WHITE)
            screen.blit(text,(250,400))

        elif status == END:


            screen.blit(bg, (0, 0))

            # Show text
            welcomestring = "GAME OVER"
            text = title_font.render(welcomestring,True,WHITE)
            screen.blit(text,(220,200))
            
            resultstring = " You get "+str(score)+" points."
            text = font.render(resultstring,True,WHITE)
            screen.blit(text,(240,350))

            resultstring = "Please press R to return"
            text = font.render(resultstring,True,WHITE)
            screen.blit(text,(250,400))
        
        pygame.display.update()

main()
pygame.quit()
print("---------------------------------------------------------------------------")
print("Game quitted...")
print("---------------------------------------------------------------------------")
