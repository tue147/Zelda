import pygame
from settings import *
from support import *
from entity import Entity
from sound import SoundPlayer

class Player(Entity):
    def __init__(self,pos,groups,obstacle_sprites,create_attack,destroy_attack,create_magic):
        super().__init__(groups)
        '''basic'''
        self.image = pygame.image.load('graphics/test/player.png').convert_alpha()
        self.rect = self.image.get_rect(topleft = pos)
        self.import_player_assets()
        self.hitbox = self.rect.inflate(HITBOX_OFFSET_X['player'],HITBOX_OFFSET_Y['player'])
          
        self.status = 'down'
        '''weapons'''
        self.create_attack = create_attack
        self.destroy_attack = destroy_attack
        self.attacking = False
        self.push_back = False
        self.cooldown_attack = 400
        self.attack_time = 0
        
        self.weapon_index = 0
        self.weapon = list(weapon_data.keys())[self.weapon_index]
        self.switch_weapon = True
        self.cooldown_switch_weapon = 2000
        self.switch_weapon_time = 0
        '''magics'''
        self.create_magic = create_magic
        
        self.magic_index = 0
        self.magic = list(magic_data.keys())[self.magic_index]
        self.switch_magic = True
        self.cooldown_switch_magic = 2000
        self.switch_magic_time = 0
        '''stats'''
        self.stats = {'health': 100,'energy':60,'attack': 10,'magic': 4,'speed': 5}
        self.max_stats = {'health': 300, 'energy': 140, 'attack': 20, 'magic' : 10, 'speed': 10}
        self.upgrade_cost = {'health': 100, 'energy': 100, 'attack': 100, 'magic' : 100, 'speed': 100}
        self.health = self.stats['health']
        self.energy = self.stats['energy']
        self.speed = self.stats['speed']
        self.exp = 0
        '''damage'''
        self.vulnerable = True
        self.hurt_time = 0
        self.invulnerable = 500

        '''sprite'''
        self.obstacle_sprites = obstacle_sprites
    def input(self):
        if not self.attacking:
            key = pygame.key.get_pressed()
            if key[pygame.K_UP]:
                self.direction.y = -1
                self.status = 'up'
            elif key[pygame.K_DOWN]:
                self.direction.y = 1
                self.status = 'down'
            else:
                self.direction.y = 0
            if key[pygame.K_RIGHT]:
                self.direction.x = 1
                self.status = 'right'
            elif key[pygame.K_LEFT]:
                self.direction.x = -1
                self.status = 'left'
            else:
                self.direction.x = 0
            
            if key[pygame.K_SPACE]:
                self.attacking = True
                self.attack_time = pygame.time.get_ticks()
                self.create_attack()
                self.soundplayer = SoundPlayer('player')
            elif key[pygame.K_b]:
                self.attacking = True
                self.attack_time = pygame.time.get_ticks()
                style = list(magic_data.keys())[self.magic_index]
                strength = list(magic_data.values())[self.magic_index]['strength'] + self.stats['magic']
                cost = list(magic_data.values())[self.magic_index]['cost']
                self.create_magic(style,strength,cost)
            elif key[pygame.K_v]:
                if self.switch_magic:
                    if self.magic_index < len(list(magic_data.keys())) - 1:    
                        self.magic_index += 1
                    else:
                        self.magic_index = 0
                    self.magic = list(magic_data.keys())[self.magic_index]
                    self.switch_magic_time = pygame.time.get_ticks()
                    self.switch_magic = False
            elif key[pygame.K_c]:
                if self.switch_weapon:
                    if self.weapon_index < len(list(weapon_data.keys())) - 1:    
                        self.weapon_index += 1
                    else:
                        self.weapon_index = 0
                    self.weapon = list(weapon_data.keys())[self.weapon_index]
                    self.switch_weapon_time = pygame.time.get_ticks()
                    self.switch_weapon = False
    def import_player_assets(self):
        character_path = 'graphics/player/'
        self.animation = {'up':[],'down':[],'left':[],'right':[],
        'right_idle':[],'left_idle':[],'up_idle':[],'down_idle':[],
        'right_attack':[],'left_attack':[],'up_attack':[],'down_attack':[]}
        for animation in self.animation:
            full_path = character_path + animation
            self.animation[animation] = import_folder(full_path)
    def get_status(self):
        if self.direction.x == 0 and self.direction.y == 0:
            if not '_idle' in self.status and not '_attack' in self.status:    
                self.status = self.status + '_idle'
        if self.attacking:
            self.direction.x, self.direction.y = 0, 0
            if not'_attack' in self.status:
                if '_idle' in self.status:
                    self.status = self.status.replace('_idle','_attack')
                else:
                    self.status = self.status + '_attack'
        else:
            if '_attack' in self.status:
                self.status = self.status.replace('_attack','')
    def animate(self):
        animation = self.animation[self.status]
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation): 
            self.frame_index = 0
        self.image = animation[int(self.frame_index)]    
        self.rect = self.image.get_rect(center = self.hitbox.center)  
        if not self.vulnerable:
            alpha = self.togle()
            self.image.set_alpha(alpha)
        else:
            self.image.set_alpha(255)         
    def cooldowns(self):
        current_time = pygame.time.get_ticks()
        if self.attacking:    
            if current_time - self.attack_time >= self.cooldown_attack + weapon_data[self.weapon]['cooldown']:
                self.attacking = False 
                self.destroy_attack()
        if not self.switch_weapon:    
            if current_time - self.switch_weapon_time >= self.cooldown_switch_weapon:
                self.switch_weapon = True  
        if not self.switch_magic:    
            if current_time - self.switch_magic_time >= self.cooldown_switch_magic:
                self.switch_magic = True   
        if not self.vulnerable:
            if current_time - self.hurt_time >= self.invulnerable:
                self.vulnerable = True
    def get_full_weapon_damage(self):
        base_damage = self.stats['attack']
        weapon_damage = weapon_data[self.weapon]['damage']
        return base_damage + weapon_damage
    def get_full_magic_damage(self):
        base_damage = self.stats['magic'] * 2.5
        magic_damage = magic_data[self.magic]['strength']
        return base_damage + magic_damage
    def get_value_by_index(self,index):
        return list(self.stats.values())[index]
    def get_cost_by_index(self,index):    
        return list(self.upgrade_cost.values())[index]
    def recover_energy(self):
        if self.energy <= self.stats['energy']:
            self.energy += 0.0003 * self.stats['energy']     

    def update(self):
        self.input()
        self.cooldowns()
        self.get_status()
        self.animate()
        self.move(self.stats['speed'])
        self.recover_energy()
            