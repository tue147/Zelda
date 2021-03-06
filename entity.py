import pygame
from math import sin


class Entity(pygame.sprite.Sprite):
    def __init__(self,groups):
        super().__init__(groups)
        
        self.frame_index = 0
        self.animation_speed = 0.15
        
        self.direction = pygame.math.Vector2()
        
        self.display_surface = pygame.display.get_surface()
    def move(self,speed):
        if self.direction.magnitude() > 0:
            self.direction = self.direction.normalize()
        self.hitbox.centerx += self.direction.x * speed
        self.colision('horizontal')
        self.hitbox.centery += self.direction.y * speed
        self.colision('vertical')
        self.rect.center = self.hitbox.center
    def colision(self,direction):
        if direction == 'horizontal':
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.speed > 0:    
                        if self.direction.x > 0:
                            self.hitbox.right = sprite.hitbox.left
                        elif self.direction.x < 0:
                            self.hitbox.left = sprite.hitbox.right
                    else:
                        if self.direction.x < 0:
                            self.hitbox.right = sprite.hitbox.left
                        elif self.direction.x > 0:
                            self.hitbox.left = sprite.hitbox.right
        elif direction == 'vertical':
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.speed > 0:    
                        if self.direction.y > 0:
                            self.hitbox.bottom = sprite.hitbox.top
                        elif self.direction.y < 0:
                            self.hitbox.top = sprite.hitbox.bottom
                    else:
                        if self.direction.y < 0:
                            self.hitbox.bottom = sprite.hitbox.top
                        elif self.direction.y > 0:
                            self.hitbox.top = sprite.hitbox.bottom
    def togle(self):
        value = sin(pygame.time.get_ticks())
        if value >= 0:
            return 255
        else:
            return 0
    def update_shadow(self):
        if self.sprite_type == 'spirit':
            self.shadow.rect.center = self.rect.midbottom - pygame.math.Vector2(0,6)
        elif self.sprite_type == 'raccoon':
            self.shadow.rect.center = self.rect.midbottom - pygame.math.Vector2(0,25)
        elif self.sprite_type == 'squid':
            self.shadow.rect.center = self.rect.midbottom - pygame.math.Vector2(0,6)
        elif self.sprite_type == 'bamboo':
            self.shadow.rect.center = self.rect.midbottom - pygame.math.Vector2(0,4)
        else:
            self.shadow.rect.center = self.rect.midbottom
        
        
        
    