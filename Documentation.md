# Advanced_Python_Final_Project Documentation

## Final Project: Mini-game Pong!

by Team A:
- Xiaonan Li
- Xujia Li
- Xinyu Wang
- Peiyu Xiao

## Overview

### Conceptual specifications

Pong! is a simple, easy to play mini-game. The player only needs to control Pedal. The aim is to catch the ball and once the ball is not caught, the game is over. The number of balls increases over time and the game becomes more difficult.

The player's score is displayed in the top left corner of the game and the final score is displayed in the centre of the screen at the end of the game.

### Technical Specifications

Development language: **Python 3**

Third-party library: **Pygame, Random**.

The game is designed for 2 classes: **Ball** and **Main**.

Class functionality/Requirements:
- The base class `Ball` is responsible for the storage of ball types. In `class Ball`, main constructor will initialize the ball types: coordinates, position, velocity and size of the ball; sounds including hitting sound and losing sound. Define the way the ball moves: once the ball touches the x-axis, it moves in the -1 direction on the y-axis and vice versa.

- The three types has been specified in class `Type1`, `Type2` and `Type3`. The three types inherit from class `Warehouse`.

- All the classes and their functions are stored in a seprated file `ball.py`

Pygame File `pong_oop.py`: 
- the code for the game operation 
- User montior function to check user's keyboard input
- Has 3 status of the game, beginning, playing, and end
- It can call the classes & functions in the class file



## Code Intro & Demo
### Pygame File `pong_oop.py`
Set up Pygame: import `ball.py`, set up window size, background, constants, fonts
```py
import pygame
from ball import *
import random

# initialize the game
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

pygame.init()
screen = pygame.display.set_mode([SCREEN_WIDTH,SCREEN_HEIGHT])
pygame.display.set_caption("Pong!")

# load images
# background
bg = pygame.image.load("images/bg.jpg")

# some constants
BEGINNING = 0
PLAYING = 1
END = 2
WHITE = (255, 255, 255)

# fonts
font = pygame.font.SysFont("Stencil",24)
```

Collision detector: chech the status of the ball
```py
def check_collide(ball, p_x, p_y, p_w):
    lose = ball.lose
    if lose:
        return
    [b_x, b_y] = ball.get_pos()
    b_d = ball.get_size()

    if b_y + b_d >= p_y: 
        if b_x + (b_d / 2) * 0.7 > p_x + p_w \
            or b_x + (b_d / 2) * 1.3 < p_x:
            ball.set_lose()
        else: # collide
            ball.add_score()
            ball.reverse_y_speed()
```


## Github link & Last Commit

## Execution Run Demo


pygame:
Userinput monitor: key, exit, 

### Different Status of the Game 
At Beginning: set the beginning score to 0 
The begainning location of the paddel is in the center area, 5 units above the bottom line of the screen
The begainning location, speed and diameter of the ball
```py
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

timer = 0
timer_update = 0
if_update = False
```

When the game is playing:
Press different directional key changes the movement direction of the paddle 
```py
for event in pygame.event.get():
    if event.type == pygame.QUIT:
        return
    elif event.type == pygame.KEYDOWN:
        key = event.key
        if key == pygame.K_RIGHT:
            paddle_speed = 10
        elif key == pygame.K_LEFT:
            paddle_speed = -10
        elif key == pygame.K_s and status == BEGINNING:
            status = PLAYING
            timer = 0
            timer_update = 0
        elif key == pygame.K_r and status == END:
            status = BEGINNING
    elif event.type == pygame.KEYUP:
        paddle_speed = 0
``` 

After each 1000 frames, a new ball would appear in a random location in the upper area
```py 
if status == PLAYING:
    screen.blit(bg, (0, 0))
    timer += 1
    timer_update += 1
    if timer == 1000:
        ball_x = random.randint(100,SCREEN_WIDTH)
        ball_y = random.randint(40,SCREEN_HEIGHT/3)
        ball_list.append(Size_Change_Ball(ball_img, ball_x, ball_y, ball_d, ball_x_speed, ball_y_speed))
        timer = 0
``` 




playing 每隔多久出现一个球 在list里，move，是否在界外check collide, paddle position， score update
end：score restart


class: size change， grow mode can change size, update every frame
