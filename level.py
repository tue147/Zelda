import pygame
from settings import *
from sound import SoundPlayer
from tile import Tile
from player import Player
from support import *
from random import choice, randint
from weapon import Weapon
from ui import UI
from enemy import Enemy
from particle import *
from magic import MagicPlayer
from menu import Menu
class Level():
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.game_pause = False
        #sprite group setup
        self.visible_sprites = YSortCameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()
        self.enemy_sprites = YSortCameraGroup()
        self.attack_sprites = pygame.sprite.Group()
        self.attackable_sprites = pygame.sprite.Group()

        self.create_map()
        self.current_attack = None

        self.ui = UI()
        self.menu = Menu(self.player)
        
        self.animationplayer = AnimationPlayer()
        self.magic_player = MagicPlayer(self.animationplayer)
    
    def create_map(self):
        layouts = {
            'boudaries' : import_csv_layout('graphics/CREATING MAP 2/map2_blocker.csv'),
            'grass' : import_csv_layout('graphics/CREATING MAP 2/map2_grass.csv'),
            'object' : import_csv_layout('graphics/CREATING MAP 2/map2_tree.csv'),
            'entity' : import_csv_layout('graphics/CREATING MAP 2/map2_player.csv'),
            'fence' : import_csv_layout('graphics/CREATING MAP 2/map2_floor 2.csv'),
            'detail' : import_csv_layout('graphics/CREATING MAP 2/map2_floor 3.csv'),
        }
        graphics = {
            'grass' : import_folder('graphics/grass'),
            'object' : import_folder('graphics/objects'),
            'fence' : import_folder('graphics/fence'),
            'detail' : import_folder('graphics/fence'),
            
        }
        for style, layout in layouts.items():
            for row_index, row in enumerate(layout):
                for col_index, col in enumerate(row):
                    if col != '-1': 
                        x = col_index * TILESIZE
                        y = row_index * TILESIZE
                        if style == 'boudaries':
                            Tile((x,y),[self.obstacle_sprites],'invisible')
                        elif style == 'grass':
                            random_grass_image = choice(graphics['grass'])
                            Tile((x,y),
                            [self.visible_sprites,self.obstacle_sprites,self.attackable_sprites],
                            'grass',
                            random_grass_image)
                        elif style == 'object':
                            surf = graphics['object'][int(col)]
                            Tile((x,y),[self.visible_sprites,self.obstacle_sprites],'tree',surf)
                        elif style == 'entity':
                            if col == '394':
                                self.player = Player((x,y),
                                [self.visible_sprites],
                                self.obstacle_sprites,
                                self.create_attack,
                                self.destroy_attack,
                                self.create_magic)
                            else: 
                                if col == '390':
                                    enemy_name = 'bamboo'
                                elif col == '391':
                                    enemy_name = 'spirit'
                                elif col == '392':
                                    enemy_name = 'raccoon'
                                elif col == '393':
                                    enemy_name = 'squid'
                                Enemy(enemy_name,(x,y),
                                [self.enemy_sprites,self.attackable_sprites],
                                self.obstacle_sprites,
                                self.damage_player,
                                self.enemy_death_particles,
                                self.add_exp)
                        elif style == 'fence':
                            if int(col) == 156:
                                fen = graphics['fence'][2]
                                Tile((x,y),[self.visible_sprites,self.obstacle_sprites],'fence',fen)
                            elif int(col) == 155:
                                fen = graphics['fence'][1]
                                Tile((x,y),[self.visible_sprites,self.obstacle_sprites],'fence',fen)
                            elif int(col) == 126:
                                fen = graphics['fence'][0]
                                Tile((x,y),[self.visible_sprites,self.obstacle_sprites],'fence',fen)
                            elif int(col) == 124:
                                fen = graphics['fence'][3]
                                Tile((x,y),[self.visible_sprites,self.obstacle_sprites],'fence_special',fen)
                            elif int(col) == 125:
                                fen = graphics['fence'][4]
                                Tile((x,y),[self.visible_sprites,self.obstacle_sprites],'fence_special',fen)
                            elif int(col) == 153:
                                fen = graphics['fence'][7]
                                Tile((x,y),[self.visible_sprites,self.obstacle_sprites],'fence_special',fen)
                            elif int(col) == 154:
                                fen = graphics['fence'][8]
                                Tile((x,y),[self.visible_sprites,self.obstacle_sprites],'fence_special',fen)  
                            elif int(col) == 127:
                                fen = graphics['fence'][6]
                                Tile((x,y),[self.visible_sprites,self.obstacle_sprites],'fence_special',fen)  
                        elif style == 'detail':
                            if int(col) == 394:    
                                detail = graphics['fence'][5]
                                Tile((x,y),[self.visible_sprites,self.obstacle_sprites],'detail',detail)
    def create_attack(self):
        if self.player.energy >=  weapon_data[self.player.weapon]['energy']:    
            self.current_attack = Weapon(self.player,[self.visible_sprites,self.attack_sprites])
            self.player.energy -= weapon_data[self.player.weapon]['energy']
    def destroy_attack(self):
        if self.current_attack:
            self.current_attack.kill()
        self.current_attack = None
    def create_magic(self,style,strength,cost):
        if style == 'heal':
            self.magic_player.heal(self.player,strength,cost,[self.visible_sprites])
        elif style == 'flame':
            self.magic_player.flame(self.player,strength,cost,[self.visible_sprites,self.attack_sprites])
    
    def player_attack_logic(self,player):
        if self.attack_sprites:
            for attack_sprite in self.attack_sprites:
                collision_sprites = pygame.sprite.spritecollide(attack_sprite,self.attackable_sprites,False)
                if collision_sprites:
                    for target_sprite in collision_sprites:
                        if target_sprite.sprite_type == 'grass':
                            pos = target_sprite.rect.center + pygame.math.Vector2(0,-30)
                            for leaf in range(randint(3,5)):
                                self.animationplayer.create_grass_particles(pos,[self.visible_sprites])
                            target_sprite.kill()
                        else:
                            if target_sprite not in attack_sprite.hitted:
                                target_sprite.get_damage(self.player,attack_sprite.sprite_type)
                                attack_sprite.hitted.append(target_sprite)
    def damage_player(self,amount,attack_type):
        if self.player.vulnerable:
            self.player.health -= amount
            self.player.vulnerable = False
            self.player.hurt_time = pygame.time.get_ticks()
            self.animationplayer.create_particles(attack_type,self.player.rect.center,[self.visible_sprites])
            self.hit_sound = SoundPlayer('hit')
    def enemy_death_particles(self,pos,particle_type):
        self.animationplayer.create_particles(particle_type,pos,[self.visible_sprites])
    def add_exp(self,amount):
        self.player.exp += amount
    def levelup(self):
        if not self.game_pause:
            self.game_pause = True
        else:
            self.game_pause = False
    def run(self):
        self.visible_sprites.custom_draw(self.player)
        self.enemy_sprites.custom_draw_enemy(self.player)
        self.ui.display(self.player)
        if self.game_pause:
            self.menu.display()
        else:
            self.visible_sprites.update()
            self.enemy_sprites.update(self.player)
            self.player_attack_logic(self.player)
            

class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.half_w = self.display_surface.get_size()[0] / 2
        self.half_h = self.display_surface.get_size()[1] / 2
        self.offset = pygame.math.Vector2()

        self.floor_surf = pygame.image.load('graphics/CREATING MAP 2/map2.png').convert()
        self.floor_rect = self.floor_surf.get_rect(topleft = (0,0))
    def get_offset(self,player):
        self.offset.x = player.rect.x - self.half_w
        self.offset.y = player.rect.y - self.half_h
    def custom_draw(self,player):
        self.get_offset(player)
        self.floor_offset_pos = self.floor_rect.topleft - self.offset
        self.display_surface.blit(self.floor_surf,self.floor_offset_pos)
        for sprite in sorted(self.sprites(), key = lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image,offset_pos)
    def custom_draw_enemy(self,player):
        self.get_offset(player)
        for sprite in sorted(self.sprites(), key = lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image,offset_pos)

    
