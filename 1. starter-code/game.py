# Imports
import pygame
import random
import json


# Window settings
GRID_SIZE = 64
WIDTH = 12 * GRID_SIZE
HEIGHT = 16 * GRID_SIZE
TITLE = "Gumbloid"
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
GRAY = (175, 175, 175)

# Stages
START = 0
PLAYING = 1
LOSE = 2
LEVEL_COMPLETE = 3
WIN = 4


# Load fonts
font_xl = pygame.font.Font(None, 96)
font_lg = pygame.font.Font(None, 64)
font_md = pygame.font.Font('assets/fonts/Dinomouse-Regular.otf', 32)
font_sm = pygame.font.Font('assets/fonts/Dinomouse-Regular.otf', 24)
font_xs = pygame.font.Font(None, 14)


#Load background
bground1_img = pygame.image.load('assets/images/tiles/background.png').convert_alpha()

# Load images

hero_idle_imgs_rt = [pygame.image.load('assets/images/characters/player_idle.png').convert_alpha()]
hero_walk_imgs_rt = [pygame.image.load('assets/images/characters/player_walk1.png').convert_alpha(),
                     pygame.image.load('assets/images/characters/player_walk2.png').convert_alpha()]

hero_jump_imgs_rt = [pygame.image.load('assets/images/characters/player_jump.png').convert_alpha()]

hero_idle_imgs_lt = [pygame.transform.flip(img, True, False) for img in hero_idle_imgs_rt]
hero_walk_imgs_lt = [pygame.transform.flip(img, True, False) for img in hero_walk_imgs_rt]
hero_jump_imgs_lt = [pygame.transform.flip(img, True, False) for img in hero_jump_imgs_rt]

grass_dirt_img = pygame.image.load('assets/images/tiles/grass_dirt.png').convert_alpha()
platform_img = pygame.image.load('assets/images/tiles/block.png').convert_alpha()
gem_img = pygame.image.load('assets/images/items/gem.png').convert_alpha()

enemy1_imgs = [pygame.image.load('assets/images/characters/enemy2a.png').convert_alpha(),
               pygame.image.load('assets/images/characters/enemy2a.png').convert_alpha()]

gpink_imgs = [pygame.image.load('assets/images/characters/pink_goon.png').convert_alpha()]

gyellow_imgs = [pygame.image.load('assets/images/characters/yellow_goon_walk1.gif').convert_alpha(),
                pygame.image.load('assets/images/characters/yellow_goon_walk2.gif').convert_alpha()]

gyellow_imgs_rt = [pygame.image.load('assets/images/characters/yellow_goon_walk1.gif').convert_alpha(),
                  pygame.image.load('assets/images/characters/yellow_goon_walk2.gif').convert_alpha()]
gyellow_imgs_lt = [pygame.transform.flip(img,True, False) for img in gyellow_imgs_rt]



heart_img = pygame.image.load('assets/images/items/heart.png').convert_alpha()
door_img = pygame.image.load('assets/images/tiles/door.png').convert_alpha()




# Levels
levels = ['assets/levels/world-1.json',
          'assets/levels/world-2.json',
          'assets/levels/world-3.json']

# Load sounds


# Game classes

class Entity(pygame.sprite.Sprite):

    def __init__ (self,x, y, image):
        super(). __init__()

        self.image = image
        self.rect = self.image.get_rect()
        self.rect.centerx = x * GRID_SIZE + GRID_SIZE // 2
        self.rect.centery = y * GRID_SIZE + GRID_SIZE // 2

        self.vx = 0
        self.vy = 0

    def apply_gravity(self):
        self.vy += gravity

        if self.vy > terminal_velocity:
            self.vy = terminal_velocity

class AnimatedEntity(Entity):
    def __init__(self, x, y, images):
        super().__init__(x, y, images[0])

        self.images = images
        self.image_index = 0
        self.ticks = 0
        self.animation_speed = 10
        
    def set_image_list(self):
        self.images = self.images
        
    def animate(self):
        self.set_image_list()
        self.ticks += 1

        if self.ticks % self.animation_speed == 0:
            self.image_index += 1

            if self.image_index >= len(self.images):
                self.image_index = 0
                
            self.image = self.images[self.image_index]
    
        
class Hero(AnimatedEntity):
    
    def __init__(self, x, y, images):
        super().__init__(x, y, images)
        
        self.speed = 5
        self.jump_power = 7
        self.vx = 0
        self.vy = 0
        self.facing_right = True
        self.jumping = False
        self.hurt_timer = 2
        self.gems = 0
        self.hearts = 3
        self.score = 0

    def move_to(self,x, y):
        self.rect.centerx = x * GRID_SIZE + GRID_SIZE // 2
        self.rect.centery = y * GRID_SIZE + GRID_SIZE // 2
        
       
    def move_right(self):
    	self.vx = self.speed
    	self.facing_right = True
    	
    def move_left(self):
    	self.vx = -1 * self.speed
    	self.facing_right = False

    def stop(self):
        self.vx = 0
    
    def jump(self):
        self.rect.y += 2
        hits = pygame.sprite.spritecollide(self, platforms, False)
        self.rect.y -= 2

        if len(hits) > 0:
            self.vy = -1 * self.jump_power
            self.jumpimg = True


    def move_and_check_platforms(self):
        self.rect.x += self.vx

        hits = pygame.sprite.spritecollide(self, platforms, False)

        for hit in hits:
            if self.vx > 0:
                self.rect.right = hit.rect.left
            elif self.vx < 0:
                self.rect.left = hit.rect.right

        self.rect.y += self.vy

        hits = pygame.sprite.spritecollide(self, platforms, False)

        for hit in hits:
            if self.vy > 0:
                self.rect.bottom = hit.rect.top
                self.jumping = False
            elif self.vy < 0:
                self.rect.top = hit.rect.top

            self.vy = 0
        

    def check_world_edges(self):
        
        if self.rect.left < 0:
            self.rect.left =  0
        elif self.rect.right > world_width:
            self.rect.right = world_width
    def check_items(self):
        hits = pygame.sprite.spritecollide(self, items, True)

        for item in hits:
            item.apply(self)

    def check_enemies(self):
        hits = pygame.sprite.spritecollide(self, enemies, False)

        for enemy in hits:
            
            if self.hurt_timer == 0:
                self.hearts -= 1
                print(self.hearts)
                print("OOF")
                self.hurt_timer = 1.0 * FPS
            

            if self.rect.x < enemy.rect.x:
                self.vx = -100
            elif self.rect.x > enemy.rect.x:
                self.vx = 15

            if self.rect.y < enemy.rect.y:
                self.vy = -5
                enemy.kill()
            elif self.rect.y > enemy.rect.y:
                self.vy = 5
        else:
                self.hurt_timer -= 1

                if self.hurt_timer < 0:
                    self.hurt_timer = 0
            

    def reached_goal(self):
        return pygame.sprite.spritecollideany(self, goal)
    
    def set_image_list(self):
        if self.facing_right:
            if self.jump:
                self.images = hero_jump_imgs_rt
            elif self.vx == 0:
                self.images = hero_idle_imgs_rt
            else:
                self.imges = hero_walk_imgs_rt
        else:
            if self.vx == 0:
                self.images = hero_idle_imgs_lt
                
            elif self.vx == 0:
                self.images = hero_idle_imgs_lt
            
            else:
                self.images = hero_walk_imgs_lt
        
        
    def update(self):
        self.apply_gravity()
        self.move_and_check_platforms()
        self.check_world_edges()
        self.check_enemies()
        self.move_and_check_platforms()
        self.check_items()
        self.animate()

    	 
class Platform(Entity):
    
    def __init__(self, x, y, image):
        super().__init__(x, y, image)


class Door(Entity):
    
    def __init__(self, x, y, image):
        super().__init__(x, y, image)



        
class Items(Entity):
    def __init__(self, x, y, image):
        super().__init__(x, y, image)

        #self.rect.x = x * GRID_SIZE
        #self.rect.y = y * GRID_SIZE


    def apply(self, character):
        character.gems += 1
        character.score += 10
        print(character.gems)

class Enemy(AnimatedEntity):
    
    def __init__(self, x, y, image):
        super().__init__(x, y, image)
        

        self.speed = 2
        self.vx = -1 * self.speed
        self.vy = 0


    def reverse(self):
        self.vx *= -1

    def move_and_check_platforms(self):
        self.rect.x += self.vx

        hits = pygame.sprite.spritecollide(self, platforms, False)

        for hit in hits:
            if self.vx > 0:
                self.rect.right = hit.rect.left
                self.reverse()
            elif self.vx < 0:
                self.rect.left = hit.rect.right
                self.reverse()

        self.rect.y += self.vy

        hits = pygame.sprite.spritecollide(self, platforms, False)

        for hit in hits:
            if self.vy > 0:
                self.rect.bottom = hit.rect.top

            elif self.vy < 0:
                self.rect.top = hit.rect.top

            self.vy = 0

    def check_world_edges(self):
        
        if self.rect.left < 0:
            self.rect.left =  0
            self.reverse()
        elif self.rect.right > world_width:
            self.rect.right = world_width
            self.reverse()


    def check_platform_edges(self):
        self.rect.y += 2
        hits = pygame.sprite.spritecollide(self, platforms, False)
        self.rect.y -= 2
        
        must_reverse = True
        
        for platform in hits:
            if self.vx < 0 and platform.rect.left <= self.rect.left:
                must_reverse = False
            elif self.vx > 0 and platform.rect.right >= self.rect.right:
                must_reverse = False

        if must_reverse:
            self.reverse()


class Flyguy (Enemy):

    def __int__ (self, x, y, images):
        super().__init__ (x, y, images)

    def update (self):
        self.move_and_check_platforms()
        self.check_world_edges()
        self.animate()


class Groundtoid (Enemy):

    def __int__ (self, x, y, images):
        super().__init__ (x, y, images)

    def update (self):
        self.move_and_check_platforms()
        self.check_world_edges()
        self.apply_gravity()
        self.animate()


class Plattoid (Enemy):
    def __int__ (self, x, y, images):
        super().__init__ (x, y, images)
        self.animation_speed = 8
        
    def set_image_list(self):
        if self.vx > 0:
            self.images = gyellow_imgs_rt
        else:
            self.images = gyellow_imgs_lt
            
    def update (self):
        self.move_and_check_platforms()
        self.check_world_edges()
        self.apply_gravity()
        self.check_platform_edges()
        self.animate()
    

# Helper functions
def show_start_screen():
    text = font_xl.render(TITLE, True, WHITE)
    rect = text.get_rect()
    rect.midbottom = WIDTH // 2, HEIGHT // 2 - 8
    screen.blit(text, rect)

    text = font_sm.render('Press any key to start', True, WHITE)
    rect = text.get_rect()
    rect.midtop = WIDTH // 2, HEIGHT // 2 + 8
    screen.blit(text, rect)


def show_lose_screen():
    text = font_lg.render('GAME OVER', True, WHITE)
    rect = text.get_rect()
    rect.midbottom = WIDTH // 2, HEIGHT // 2 - 8
    screen.blit(text, rect)

    text = font_sm.render("Press r to try again", True, WHITE)
    rect = text.get_rect()
    rect.midtop = WIDTH // 2, HEIGHT // 2 + 8
    screen.blit(text, rect)

def show_win_screen():
    text = font_lg.render('You Win!', True, WHITE)
    rect = text.get_rect()
    rect.midbottom = WIDTH // 2, HEIGHT // 2 - 8
    screen.blit(text, rect)

    text = font_sm.render("Press r to play again", True, WHITE)
    rect = text.get_rect()
    rect.midtop = WIDTH // 2, HEIGHT // 2 + 8
    screen.blit(text, rect)


def show_level_complete_screen():
    text = font_lg.render('Level Complete', True, WHITE)
    rect = text.get_rect()
    rect.midbottom = WIDTH // 2, HEIGHT // 2 - 8
    screen.blit(text, rect)

    text = font_sm.render("Press r to try again", True, WHITE)
    rect = text.get_rect()
    rect.midtop = WIDTH // 2, HEIGHT // 2 + 8
    screen.blit(text, rect)


def show_hud():
    text = font_md.render(str(hero.score), False, WHITE)
    rect = text.get_rect()
    rect.midtop = WIDTH // 2, 16
    screen.blit(text, rect)

    screen.blit(gem_img, [WIDTH - 100, 24])
    text = font_sm.render('x' + str(hero.gems), True, WHITE)
    rect = text.get_rect()
    rect.topleft = ([WIDTH - 60, 24])
    screen.blit(text, rect)

    for i in range(hero.hearts):
        x = i * 36 + 16
        y = 16
        screen.blit(heart_img, [x, y])
    


def draw_grid(offset_x=0, offset_y=0):
    for x in range(0, WIDTH + GRID_SIZE, GRID_SIZE):
        adj_x = x - offset_x % GRID_SIZE
        pygame.draw.line(screen, GRAY, [adj_x, 0], [adj_x, HEIGHT], 1)

    for y in range(0, HEIGHT + GRID_SIZE, GRID_SIZE):
        adj_y = y - offset_y % GRID_SIZE
        pygame.draw.line(screen, GRAY, [0, adj_y], [WIDTH, adj_y], 1)

    for x in range(0, WIDTH + GRID_SIZE, GRID_SIZE):
        for y in range(0, HEIGHT + GRID_SIZE, GRID_SIZE):
            adj_x = x - offset_x % GRID_SIZE + 4
            adj_y = y - offset_y % GRID_SIZE + 4
            disp_x = x // GRID_SIZE + offset_x // GRID_SIZE
            disp_y = y // GRID_SIZE + offset_y // GRID_SIZE
            
            point = '(' + str(disp_x) + ',' + str(disp_y) + ')'
            text = font_xs.render(point, True, GRAY)
            screen.blit(text, [adj_x, adj_y])

        


#Setup
def start_game():
    global stage, hero, current_level

    hero = Hero(0, 0, hero_idle_imgs_rt)
    stage = START
    current_level = 0


def start_level():
    global player, platforms, items, enemies, stage, hero, goal
    global gravity, terminal_velocity
    global world_width, world_height

    player = pygame.sprite.GroupSingle()
    platforms = pygame.sprite.Group()
    items = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    platforms = pygame.sprite.Group()
    goal = pygame.sprite.Group()


    with open(levels[current_level]) as f:
        data = json.load(f)
    hero.move_to(data['start'][0], data['start'][1])
    player.add(hero)

    world_height = data['height'] * GRID_SIZE
    world_width = data['width'] * GRID_SIZE

    for i, loc in enumerate(data["door_locs"]):
        if i == 0:
            goal.add( Door(loc[0], loc[1], door_img) )

    for loc in data['grassblock_locs']:
        platforms.add( Platform(loc[0], loc[1], grass_dirt_img) )

    for loc in data['platform_locs']:
        platforms.add( Platform(loc[0], loc[1], platform_img) )

    for loc in data['item_locs']:
        items.add( Items(loc[0], loc[1], gem_img) )

    for loc in data ['flyguy_locs']:
        enemies.add(Flyguy(loc[0], loc [1], gpink_imgs))

    for loc in data['groundtoid_locs']:
        enemies.add(Groundtoid(loc[0], loc [1], enemy1_imgs))

    for loc in data['plattoid_locs']:
        enemies.add(Plattoid(loc[0], loc [1], gyellow_imgs_lt))


# Physics  settings
gravity = 0.5
terminal_velocity = 50


# Game loop
running = True
grid_on = False

start_game()
start_level()

grid_on = False

while running:
    # Input handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if stage == START:
                stage = PLAYING

            elif stage == PLAYING:
                if event.key == pygame.K_SPACE:
                    hero.jump()

            elif stage == LOSE or stage == WIN:
                if event.key == pygame.K_r:
                    start_game()
                    start_level()
                    
            if event.key == pygame.K_g:
                grid_on = not grid_on

    pressed = pygame.key.get_pressed()

    if pressed[pygame.K_LEFT]:
        hero.move_left()
    elif pressed[pygame.K_RIGHT]:
        hero.move_right()
    else:
        hero.stop()
    
    # Game logic
    if stage == PLAYING:
        player.update()
        enemies.update()

        if hero.hearts == 0:
            stage = LOSE
        elif hero.reached_goal():
            stage = LEVEL_COMPLETE
            countdown = 2 * FPS
    elif stage == LEVEL_COMPLETE:
        countdown -= 1
        if countdown <= 0:
            current_level += 1
            
            if current_level < len(levels):
                start_level()
                stage = PLAYING
            else:
                stage = WIN
            
    
    if hero.rect.centery < HEIGHT //2:
        offset_y = 0
    elif hero.rect.centery > world_height - HEIGHT // 2:
        offset_y = world_height - HEIGHT
    else:
        offset_y = hero.rect.centery - HEIGHT // 2
    
        
    # Drawing code
    screen.blit(bground1_img, [0,0])
    
    for sprite in platforms:
        screen.blit(sprite.image, [sprite.rect.x, sprite.rect.y - offset_y])

    for sprite in player:
        screen.blit(sprite.image, [sprite.rect.x, sprite.rect.y - offset_y])

    for sprite in items:
        screen.blit(sprite.image, [sprite.rect.x, sprite.rect.y - offset_y])
        
    for sprite in enemies:
        screen.blit(sprite.image, [sprite.rect.x, sprite.rect.y - offset_y])

    for sprite in goal:
        screen.blit(sprite.image, [sprite.rect.x, sprite.rect.y - offset_y])
    show_hud()

    if grid_on:
        draw_grid(0, offset_y)

    if stage == START:
        show_start_screen()
    elif stage == LOSE:
        show_lose_screen()

    elif stage == LEVEL_COMPLETE:
        show_level_complete_screen()
    elif stage == WIN:
        show_win_screen()

        
    # Update screen
    pygame.display.update()


    # Limit refresh rate of game loop 
    clock.tick(FPS)


# Close window and quit
pygame.quit()

