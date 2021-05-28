# Imports
import pygame
import random


# Window settings
GRID_SIZE = 64
WIDTH = 16 * GRID_SIZE
HEIGHT = 9 * GRID_SIZE
TITLE = "Game Title"
FPS = 60


# Create window
pygame.init()
screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption(TITLE)
clock = pygame.time.Clock()


# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
SKY_BLUE = (0, 150, 255)


# Load fonts


# Load images
hero_img = pygame.image.load('assets/images/characters/player_idle.png').convert_alpha()
grass_dirt_img = pygame.image.load('assets/images/tiles/grass_dirt.png').convert_alpha()
platform_img = pygame.image.load('assets/images/tiles/block.png').convert_alpha()


# Load sounds


# Game classes
class Hero(pygame.sprite.Sprite):
    
    def __init__(self, x, y, image):
        super().__init__()
        
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x * GRID_SIZE
        self.rect.y = y * GRID_SIZE

        self.speed = 5
        self.vx = 0
        self.vy = 0
       
    def move_right(self):
    	self.vx = self.speed
    	
    def move_left(self):
    	self.vx =- self.speed

    def stop(self):
        self.vx = 0
    
    def jump(self):
    	pass

    def update(self):
        self.rect.x += self.vx

        hits = pygame.sprite.spritecollide(self, platforms, False)

        for hit in hits:
            if self.vx > 0:
                self.rect.right = hit.rect.left
            
        
    	 
class Platform(pygame.sprite.Sprite):
    
    def __init__(self, x, y, image):
        super().__init__()
        
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x * GRID_SIZE
        self.rect.y = y * GRID_SIZE
        

#Setup
platforms = pygame.sprite.Group()

platform_locs = [[0, 8], [1, 8], [2, 8], [3, 8], [4, 8], [5, 8], [6, 8], [7, 8], [8, 8], [9, 8], [10, 8], [11, 8], [13, 8], [14, 8], [15, 8], ]

for loc in platform_locs:
    x = loc[0]
    y = loc[1]
    p = Platform(x, y, grass_dirt_img)
    platforms.add(p)

platform_locs = [[11, 5], [12, 5], [13, 5], [4, 3], [5,3], [6,3]]

for loc in platform_locs:
    x = loc[0]
    y = loc[1]
    p = Platform(x, y, platform_img)
    platforms.add(p)

player = pygame.sprite.GroupSingle()

start_x = 3
start_y = 7

hero = Hero(start_x, start_y, hero_img)
player.add(hero)



# Game loop
running = True

while running:
    # Input handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pressed = pygame.key.get_pressed()

    if pressed[pygame.K_LEFT]:
        hero.move_left()
    elif pressed[pygame.K_RIGHT]:
        hero.move_right()
    else:
        hero.stop()
    
    # Game logic
    player.update()

        
    # Drawing code
    screen.fill(SKY_BLUE)
    player.draw(screen)
    platforms.draw(screen)
        
    # Update screen
    pygame.display.update()


    # Limit refresh rate of game loop 
    clock.tick(FPS)


# Close window and quit
pygame.quit()

