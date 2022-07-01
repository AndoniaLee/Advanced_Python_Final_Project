import pygame
from ball import *

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

def check_collide(ball, p_x, p_y, p_w):
    lose = ball.lose
    if lose:
        return
    [b_x, b_y] = ball.get_pos()
    b_d = ball.get_size()

    if b_y + b_d >= p_y: 
        if b_x + (b_d / 2) > p_x + p_w \
            or b_x + (b_d / 2) < p_x:
            ball.set_lose()
        else: # collide
            ball.add_score()
            ball.reverse_y_speed()


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
    ball_x = 150
    ball_y = 150
    ball_d = 20
    ball_x_speed = 2
    ball_y_speed = 2
    ball_list = []
    ball_list.append(Ball(ball_img, ball_x, ball_y, ball_d, ball_x_speed, ball_y_speed))
    timer = 0
    
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
                elif key == pygame.K_r and status == END:
                    status = BEGINNING
            elif event.type == pygame.KEYUP:
                paddle_speed = 0

        if status == PLAYING:

            screen.blit(bg, (0, 0))
            timer += 1
            if timer == 1000:
                ball_x = random.randint(100,SCREEN_WIDTH)
                ball_y = random.randint(40,SCREEN_HEIGHT/3)
                ball_list.append(Ball(ball_img, ball_x, ball_y, ball_d, ball_x_speed, ball_y_speed))
                timer = 0
                
            # ball position change
            for ball in ball_list:
                [lose, score] = ball.move(SCREEN_WIDTH, SCREEN_HEIGHT)
                if lose:
                    print(ball_x,ball_y)
                    status = END
                    break
                
                check_collide(ball, paddle_x, paddle_y, paddle_width)
                ball.draw(screen)

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
        
        elif status == BEGINNING:

            screen.blit(bg, (0, 0))
            # show text
            welcomestring = "Welcome to the pong game"
            text = font.render(welcomestring,True,WHITE)
            screen.blit(text,(300,200))

            welcomestring = "Please press S to start"
            text = font.render(welcomestring,True,WHITE)
            screen.blit(text,(310,220))

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
