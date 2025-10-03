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
