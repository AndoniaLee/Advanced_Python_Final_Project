# Advanced_Python_Final_Project Documentation

## Final Project: Mini-game Pong!

by Team A:
- Xiaonan Li
- Xujia Li
- Xinyu Wang
- Peiyu Xiao

### **Conceptual specifications**

Pong! is a simple, easy to play mini-game. The player only needs to control paddle to catch the ball, and once the ball is not caught, the game is over. The number of balls increases over time and the game becomes more difficult.

The player's score is displayed in the top left corner of the game and the final score is displayed in the centre of the screen at the end of the game.

### **Technical Specifications**

Development language: **Python 3**

Third-party library: **Pygame, Random**.

The game is designed for 2 class: **Ball** and **Size_change_ball** stored in **ball.py** and file **pong_oop.py**.

**Class functionality/Requirements**:
1. The base class `Ball`: 
- Responsible for the storage of ball types. In `class Ball`, main constructor will initialize the ball types: coordinates, position, velocity and size of the ball; sounds including hitting sound and losing sound. 
- Define the way the ball moves: once the ball touches the x-axis, it moves in the -1 direction on the y-axis and vice versa.

2. The derived class `Size_change_ball`:
Inherited from the base class, to generate balls that can vary in size in the game.


3. Pygame File `pong_oop.py`: 
- The game file is responsible for the main part of the game operation, which has 3 status of the game, beginning, playing, and end. 
- The game is run by calling the classes & functions in the class file, the user monitor function is also running to check the user's keyboard input.

#### **Class File `ball.py`**
- General Ball Class: A class that saves the functions and pramaters regarding the balls.
```py
NORMAL = 0
SIZE_CHANGING = 1
SPEED_CHANGING = 2

class Ball:
    def __init__(self, img, x, y, d, x_speed, y_speed):
        self.img = img
        self.x = x
        self.y = y
        self.d = d
        self.x_speed = x_speed
        self.y_speed = y_speed
        self.lose = False
        self.score = 0

        # sounds
        self.hit_sound = pygame.mixer.Sound("sounds/hitWall.wav")
        self.loss_sound = pygame.mixer.Sound("sounds/lifeLoss.wav")
```
- Move: Define how the ball will move and display the picture of the ball in real time on the coordinates
```py
 def move(self, screen_width, screen_height):
        if self.y <= 0:
            self.y_speed *= -1
        if self.x >= screen_width - self.d or self.x <= 0:
            self.x_speed *= -1

        self.x += self.x_speed
        self.y += self.y_speed

        return self.lose, self.score

    def draw(self, screen):
        if not self.lose:
            screen.blit(self.img, (self.x, self.y))
```
- Return ball-related parameters
```py
    def get_pos(self):
        return [self.x, self.y]

    def get_size(self):
        return self.d

    def set_lose(self):
        self.lose = True
```
- Ball-related events that occur under specified conditions
```py
    def add_score(self):
        self.score += 1
        
    def reverse_y_speed(self):
        self.y_speed *= -1

    def play_lose_sound(self):
        self.loss_sound.play()

    def play_hit_sound(self):
        self.hit_sound.play()
```

#### **Pygame File `pong_oop.py`**
- Set up Pygame: import `ball.py`, set up window size, background, constants, fonts
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

- Collision detector: chech the status of the ball
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
- Load the ball and paddle to the game
```py
def main():
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

- User Input Monitor: Keyup, KeyDown, Quit
```py
    # main loop
    while 1:
        
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
- Playing Status: create a ball, and let it move, check if it touches the ground
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
            
            # ball position change
            score = 0
            if timer_update == 20:
                if_update = True
                timer_update = 0
                
            for ball in ball_list:
                [lose, ball_score] = ball.move(SCREEN_WIDTH, SCREEN_HEIGHT)
                score += ball_score
                if lose:
                    status = END
                    break
                
                check_collide(ball, paddle_x, paddle_y, paddle_width)

                if if_update:
                    ball.update()
                ball.draw(screen)
            if if_update:
                if_update = False
```
- Move the paddle and limit it in the window
```py
            # paddle position change
            paddle_x += paddle_speed
            if paddle_x + paddle_width >= SCREEN_WIDTH:
                paddle_x = SCREEN_WIDTH - paddle_width
            if paddle_x <= 0:
                paddle_x = 0

            # draw

            screen.blit(paddle, (paddle_x, paddle_y))

            # show score
            gamestring = " Score: "+str(score)
            text = font.render(gamestring,True,WHITE)
            screen.blit(text,(50,50))
```

- Beginning Interface
```py

       elif status == BEGINNING:

            screen.blit(bg, (0, 0))
            
            ball_list = []
            ball_list.append(Ball(ball_img, ball_x, ball_y, ball_d, ball_x_speed, ball_y_speed))

            # show text
            welcomestring = "Welcome to the pong game"
            text = font.render(welcomestring,True,WHITE)
            screen.blit(text,(300,200))

            welcomestring = "Please press S to start"
            text = font.render(welcomestring,True,WHITE)
            screen.blit(text,(310,220))

```

- Ending Interface
```py
        elif status == END:
            
            resultstring = " You get "+str(score)+" points."
            text = font.render(resultstring,True,WHITE)
            screen.blit(text,(300,200))

            resultstring = "Please press R to return"
            text = font.render(resultstring,True,WHITE)
            screen.blit(text,(310,220))
        
        pygame.display.update()

main()
pygame.quit()
```

### Execution Model

When the code is run, the user is taken to the Pygame main form, where user can press 'S' to start the game.

In the game, the player controls the paddle via the left and right keyboard keys. The game consists of two states: Beginning and End：

In Beginning, the player can play the game and each time the paddle catches a ball, the player adds one point to the score, which is displayed in the top left corner of the window. Method 'check_collide' will monitor if the ball has been successfully taken by the paddle and achieve a ball bounce if the player does not lose. In addition to the player controlling the paddle, the game is made more difficult by generating an extra ball every 1000 frames. When the player does not receive the ball, the game fails and the game goes to the state End.

In state End, the game displays the player's final score. The player can replay the game by pressing the R button.

### Github link & Last Commit
- ball.py:
https://github.com/AndoniaLee/Advanced_Python_Final_Project/blob/main/ball.py

| Name      | Date          | Full Commit SHA                           | Content                           |
|-----------|---------------|------------------------------|----------------------------------|
| Xiaonan Li | June 27 2022  | 00e57320dfdb77b91b8c749d6ddf656a9f0735d7  | Added ball class python file                              |
| Xinyu Wang | July 3 2022   | cbc85802e0c8d74464a62f58b75dcfe0b3adfb02  | Added a child class: ball type that changes sizes along time      |

- pong_oop.py:
https://github.com/AndoniaLee/Advanced_Python_Final_Project/blob/main/pong_oop.py

| Name      | Date          | Full Commit SHA                           | Content                           |
|-----------|---------------|------------------------------|----------------------------------|
| Xiaonan Li | June 30 2022  | 6da54cd73512dfce5591b2bd35c8288375c31ede  | Add images and main running code                              |
| Peiyu Xiao | July 1 2022   | 6132fdce66afdc1c4fdc404db9f3779f8215860a  | Added beginning interface and ending interface                    |
| Peiyu Xiao | July 1 2022   | d13cae5fa42ff64d6f0443a3e38eccdb657c119d  | Added multiple balls and levels to the game                       |
| Xinyu Wang | July 2 2022   | 227b0f2cec3a68a69640b4430d89509c85da4c0b  | Fixing the problem that the game cannot restart after losing          |
| Xujia Li | July 3 2022   | 待贴  | 待贴          |
| Xujia Li | July 3 2022   | 待贴  | 待贴          |
