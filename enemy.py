import pygame
from settings import *
from entity import Entity
from sound import SoundPlayer
from support import *
from particle import Shadow

class Enemy(Entity):
    def __init__(self,monster_name,pos,groups,shadow_sprites,obstacle_sprites,damage_player,death_particles,add_exp):
        super().__init__(groups)
        self.sprite_type = f'{monster_name}'
        self.import_graphics(monster_name)
        self.status = 'idle'

        self.image = self.animation[self.status][self.frame_index]
        
        if monster_name == 'raccoon':
            self.rect = self.image.get_rect(topleft = pos).inflate(-70,-70)
            self.hitbox = self.rect
        else:
            self.rect = self.image.get_rect(topleft = pos)
            self.hitbox = self.rect.inflate(0,-10)
        
        self.monster_name = monster_name
        monster_info = monster_data[self.monster_name]
        self.health = monster_info['health']
        self.exp = monster_info['exp']
        self.speed = monster_info['speed']
        self.attack_damage = monster_info['damage']
        self.resistance = monster_info['resistance']
        self.attack_radius = monster_info['attack_radius']
        self.notice_radius = monster_info['notice_radius']
        self.attack_type = monster_info['attack_type']

        self.can_attack = True
        self.attack_time = 0
        self.attack_cooldown = 1500
        self.damage_player = damage_player

        self.death_particles = death_particles
        self.add_exp = add_exp

        self.hit_react = False
        self.hit_cooldown = 400
        self.hit_time = 0
        
        self.can_knockback = True
        self.knockback_cooldown = 1000
        
        '''sprite'''
        self.obstacle_sprites = obstacle_sprites 
        
        '''shadow'''
        self.shadow = Shadow(self.rect,shadow_sprites,self.sprite_type)

    def import_graphics(self,name):
        self.animation = {'idle':[], 'move':[], 'attack':[]}
        main_path = f'graphics/monsters/{name}/'
        for animation in self.animation:
            self.animation[animation] = import_folder(main_path + animation)
    def get_direction_distance(self,player):
        enemy_vec = pygame.math.Vector2(self.rect.center)
        player_vec = pygame.math.Vector2(player.rect.center)
        distance = (enemy_vec - player_vec).magnitude()
        if distance != 0:    
            direction = (player_vec - enemy_vec).normalize()
        else:
            direction = pygame.math.Vector2()
        return(distance,direction)
    def get_status(self,player):
        distance = self.get_direction_distance(player)[0]
        if distance <= self.attack_radius and self.can_attack:
            if self.status != 'attack':
                self.frame_index = 0
            self.status = 'attack'
        elif distance <= self.notice_radius:
            self.status = 'move'
        else:
            self.status = 'idle'
    def action(self,player):
        if self.status == 'attack':
            self.attack_time = pygame.time.get_ticks()
        elif self.status == 'move':
            self.direction = self.get_direction_distance(player)[1]
        else:
            self.direction = pygame.math.Vector2()
    def animate(self):
        animation = self.animation[self.status]
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation): 
            if self.status == 'attack':
                self.can_attack = False
                self.damage_player(self.attack_damage,self.attack_type)
                self.sound = SoundPlayer(self.monster_name)
            self.frame_index = 0
        self.image = animation[int(self.frame_index)]    
        self.rect = self.image.get_rect(center = self.hitbox.center)
        if not self.can_knockback:
            alpha = self.togle()
            self.image.set_alpha(alpha)
        else:
            self.image.set_alpha(255)
    def cooldown(self):
        self.current_time = pygame.time.get_ticks()
        if not self.can_attack:    
            if self.current_time - self.attack_time >= self.attack_cooldown:
                self.can_attack = True
        if self.hit_react:    
            if self.current_time - self.hit_time >= self.hit_cooldown:
                self.hit_react = False
        elif not self.can_knockback:
            if self.current_time - self.hit_time >= self.knockback_cooldown:
                self.can_knockback = True
    def get_damage(self,player,attack_type):    
        self.hit_sound = SoundPlayer('hit')
        if attack_type == 'weapon':
            self.health -= player.get_full_weapon_damage()
            if self.can_knockback:    
                self.hit_react = True
                self.can_knockback = False
                self.hit_time = pygame.time.get_ticks()
        else:
            self.health -= player.get_full_magic_damage()
            if self.can_knockback:    
                self.hit_react = True
                self.can_knockback = False
                self.hit_time = pygame.time.get_ticks()
    def check_death(self):
        if self.health <= 0:
            self.death_particles(self.rect.center,self.monster_name)
            self.shadow.kill()
            self.kill()
            self.add_exp(self.exp)
            self.death_sound = SoundPlayer('death')
    def hit_reaction(self,player):
        if self.hit_react:
            if self.speed > 0:
                self.speed /= - self.resistance
        elif not self.hit_react:        
            self.speed = monster_data[self.monster_name]['speed']
    def update(self,player):
        self.get_status(player)
        self.action(player)
        self.hit_reaction(player)
        self.move(self.speed)
        self.cooldown()
        self.update_shadow()
        self.animate()
        self.check_death()        

        
        
