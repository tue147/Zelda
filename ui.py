import pygame
from settings import *

class UI():
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font(UI_FONT,UI_FONT_SIZE)

        self.health_bar_rect = pygame.Rect(10,10,HEALTH_BAR_WIDTH,BAR_HEIGHT)
        self.energy_bar_rect = pygame.Rect(10,34,ENERGY_BAR_WIDTH,BAR_HEIGHT)

        self.weapon_graphics = []
        for weapon in weapon_data.values():
            path = weapon['graphic']
            weapon = pygame.image.load(path).convert_alpha()
            self.weapon_graphics.append(weapon)
        self.magic_graphics = []
        for magic in magic_data.values():
            path = magic['graphic']
            magic = pygame.image.load(path).convert_alpha()
            self.magic_graphics.append(magic)
    def show_bar(self,current,max,bg_rect,color):
        ratio = current/max
        width = (bg_rect.width - 6) * ratio
        height = bg_rect.height - 6
        pygame.draw.rect(self.display_surface,UI_BG_COLOR,bg_rect)
        pygame.draw.rect(self.display_surface,UI_BORDER_COLOR,bg_rect,3)
        bar = pygame.Rect(bg_rect.x + 3,bg_rect.y + 3,width,height)
        pygame.draw.rect(self.display_surface,color,bar)
    def show_exp(self,exp):
        text_surf = self.font.render(str(int(exp)),False,TEXT_COLOR)
        x = self.display_surface.get_size()[0] - 20
        y = self.display_surface.get_size()[1] - 20
        text_rect = text_surf.get_rect(bottomright = (x,y))
        pygame.draw.rect(self.display_surface,UI_BG_COLOR,text_rect.inflate(20,10))
        pygame.draw.rect(self.display_surface,UI_BORDER_COLOR,text_rect.inflate(20,10),3)
        self.display_surface.blit(text_surf,text_rect)
    def selection_box(self,left,top,switch_weapon):
        bg_rect = pygame.Rect(left,top,ITEM_BOX_SIZE,ITEM_BOX_SIZE)
        pygame.draw.rect(self.display_surface,UI_BG_COLOR,bg_rect)
        if switch_weapon:
            pygame.draw.rect(self.display_surface,UI_BORDER_COLOR_ACTIVE,bg_rect,3)
        else:
            pygame.draw.rect(self.display_surface,UI_BORDER_COLOR,bg_rect,3)
        return bg_rect
    def show_weapon(self,weapon_index,switch_weapon):
        bg_rect = self.selection_box(10,580,switch_weapon)
        weapon_surf = pygame.transform.scale(self.weapon_graphics[weapon_index],(20,40))
        weapon_surf_rect = weapon_surf.get_rect(center = bg_rect.center)
        self.display_surface.blit(weapon_surf,weapon_surf_rect)
    def show_magic(self,magic_index,switch_magic):
        bg_rect = self.selection_box(60,580,switch_magic)
        magic_surf = pygame.transform.scale(self.magic_graphics[magic_index],(20,40))
        magic_surf_rect = magic_surf.get_rect(center = bg_rect.center)
        self.display_surface.blit(magic_surf,magic_surf_rect)    
    def display(self,player):
        self.show_bar(player.health,player.stats['health'],self.health_bar_rect,HEALTH_COLOR)
        self.show_bar(player.energy,player.stats['energy'],self.energy_bar_rect,ENERGY_COLOR)
        self.show_exp(player.exp)
        self.show_weapon(player.weapon_index,player.switch_weapon)
        self.show_magic(player.magic_index,player.switch_magic)