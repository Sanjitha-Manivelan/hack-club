import pygame
from sys import exit
from random import randint, choice

def image_color(image, color):
    changing_color = image.copy()
    changing_color.fill(color, special_flags = pygame.BLEND_RGBA_MULT)
    return changing_color

class Player(pygame.sprite.Sprite):
    def __init__(self, walk, jump):
        super().__init__()
        self.walk_1 = walk
        self.jump_1 = jump
        self.player_walk = walk
        self.player_index = 0
        self.player_jump = jump
        self.image = self.player_walk[self.player_index]
        self.rect = self.image.get_rect(midbottom = (80, 300))
        self.gravity = 0
        self.jump_sound = pygame.mixer.Sound('audio/jump.mp3')
        self.jump_sound.set_volume(0.5)

    def change_olor(self, color):
        self.player_walk = []
        for img in self.walk_1:
            img_color = image_color(img, color)
            self.player_walk.append(img_color)

        self.player_jump = img_color(self.jump_1, color)
    
    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 300:
            self.gravity = -20
            self.jump_sound.play()

    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 300:
            self.rect.bottom = 300

    def animation_state(self):
        if self.rect.bottom < 300:
            self.image = self.player_jump
        else:
            self.player_index += 0.1
            if self.player_index >= len(self.player_walk):
                self.player_index = 0
            self.image = self.player_walk[int(self.player_index)]
    
    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animation_state()

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()
        if type == 'fly':
            fly_1 = pygame.image.load('graphics/fly/fly1.png').convert_alpha()
            fly_2 = pygame.image.load('graphics/fly/fly2.png').convert_alpha()
            self.frames = [fly_1, fly_2]
            y_pos = 210
        else:
            snail_1 = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
            snail_2 = pygame.image.load('graphics/snail/snail2.png').convert_alpha()
            self.frames = [snail_1, snail_2]
            y_pos = 210
        
        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom = (randint(900, 1100), y_pos))
    
    def animation_state(self):
        self.animatiion_index += 0.1
        if self.animation_index >= len(self.frames):
            self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]
    
    def update(self):
        self.animation_state()
        self.rect.x -= min(12, 6 + (level - 1))
        self.destroy()
    
    def destroy(self):
        if self.rect.x <= -100:
            self.kill()

class Heart(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        heart_img = pygame.image.load('graphics/heart.png').convert_alpha()
        self.image = pygame.transform.scale(heart_img, (48, 48))
        y_pos = choice([200, 250, 300])
        self.rect = self.image.get_rect(midbottom = (randint(900, 1100), y_pos))
    
    def update(self):
        self.rect.x -= min(12, 6 + (level - 1))
        if self.rect.right < 0:
            self.kill()
    
def display_score():
    global level, last_level
    current_time = int(pygame.time.get_ticks() / 1000) - start_time
    score_surf = test_font.render(f'Score: {current_time}', False, (64, 64, 64))
    score_rect = score_surf.get_rect(center = (400, 50))
    screen.blit(score_surf, score_rect)

    level = current_time // 10 + 1
    if level != last_level:
        last_level = level
        new_color = player_colors[(level - 1) % len(player_colors)]
        player.sprite.change_color(new_color)
    return current_time

def collision_sprite():
    global lives, game_active
    if pygame.sprite.spritecollide(player.sprite, obstacle_group, True):
        lives -= 1
        if lives <= 0:
            obstacle_group.empty()
            heart.empty()
            game_active = False
    if pygame.sprite.spritecollide(player.sprite, heart, True):
        lives = min(lives + 1, 3)
    return game_active

pygame.init()
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption('Astronaut Game')
clock = pygame.time.Clock()
test_font = pygame.font.Font('font/Pixeltype.ttf', 50)
game_active = False
paused = False
score = 0
start_time = 0
lives = 3
level = 1
last_level = 1
player_colors = [(255, 255, 255), (153, 226, 180), (24, 78, 119), (217, 237, 146), (0, 109, 119), (255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0)]
bg_music = pygame.mixer.Sound('audio/music.wav')
bg_music.play(loops = -1)
player_walk_1 = pygame.image.load('graphics/player/player_walk_1.png').convert_alpha()
player_walk_2 = pygame.image.load('graphics/player/player_walk_2.png').convert_alpha()
player_walk = [player_walk_1, player_walk_2]
player_jump = pygame.image.load('graphics/player/jump.png').convert_alpha()
player = pygame.sprite.GroupSingle()
player.add(Player(player_walk, player_jump))
obstacle_group = pygame.sprite.Group()
heart = pygame.sprite.Group()
sky_surface = pygame.image.load('graphics/Sky.png').convert()
ground_surface = pygame.image.load('graphics/ground.png').convert()
player_stand = pygame.image.load('graphics/player/player_stand.png').convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand, 0, 2)
player_stand_rect = player_stand.get_rect(center = (400, 200))
game_name = test_font.render('Astronaut Runner', False, (111, 196, 169))
game_name_rect = game_name.get_rect(center = (400, 80))
game_message = test_font.render('Press space to play', False, (111, 196, 169))
game_message_rect = game_message.get_rect(center = (400, 340))
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1500)
pause_button = pygame.Rect(10, 10, 55, 40)
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if game_active:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pause_button.collidepoint(event.pos):
                    paused = not paused
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        paused = not paused
