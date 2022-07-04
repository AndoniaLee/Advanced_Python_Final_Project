import pygame

class Ball:
    '''
        Create generic ball class
    '''
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

    def move(self, screen_width, screen_height):
        '''
            Make the ball move along time
        '''
        if self.y <= 0:
            self.y_speed *= -1
        if self.x >= screen_width - self.d or self.x <= 0:
            self.x_speed *= -1

        self.x += self.x_speed
        self.y += self.y_speed

        return self.lose, self.score

    def draw(self, screen):
        '''
            Draw ball image on the screen
        '''
        if not self.lose:
            screen.blit(self.img, (self.x, self.y))

    def update(self):
        '''
            The update class is for other ball type. To avoid errors, we put
            a dummy update class here.
        '''
        pass

    def get_pos(self):
        '''
            Return current ball x,y position
        '''
        return [self.x, self.y]

    def get_size(self):
        '''
            Return ball size
        '''
        return self.d

    def get_type(self):
        '''
            Return ball type
        '''
        return "normal"

    def set_lose(self):
        '''
            Set ball's status to lose, which will lead to game's ending
        '''
        self.lose = True

    def add_score(self):
        '''
            Add ball's score by 1
        '''
        self.score += 1
        
    def reverse_y_speed(self):
        '''
            Change the y speed of ball to the opposite
        '''
        self.y_speed *= -1

    def play_lose_sound(self):
        '''
            Play loss sound
        '''
        self.loss_sound.play()

    def play_hit_sound(self):
        '''
            Play hit sound
        '''
        self.hit_sound.play()

class Size_Change_Ball(Ball):
    
    def __init__(self,img, x, y, d, x_speed, y_speed):
        super().__init__(img, x, y, d, x_speed, y_speed)
        self.grow = 0
        self.mode = 1
        self.orig_img = img
    
    def get_type(self):
        '''
            Return ball type
        '''
        return "size changing"

    def update(self):
        '''
            Update ball's size up to 40, and then shrink it back to normal size
        '''
        if self.grow > 40:
            self.mode = -1
        if self.grow < 1:
            self.mode = 1
        self.grow += self.mode 

        self.d = self.orig_img.get_size()[0] + round(self.grow)
        self.img = pygame.transform.scale(self.orig_img, (self.d, self.d))


class Speed_Change_Ball(Ball):
    
    def __init__(self,img, x, y, d, x_speed, y_speed):
        super().__init__(img, x, y, d, x_speed, y_speed)
        self.grow = 0
        self.mode = 1
    
    def get_type(self):
        '''
            Return ball type
        '''
        return "speed changing"

    def update(self):
        '''
            Update ball's speed up to 1, and then shrink it back to normal speed
        '''
        if self.grow > 1:
            self.mode = -1
        if self.grow < 1:
            self.mode = 1
        self.grow += self.mode 

        self.x_speed += self.grow
        self.y_speed += self.grow

