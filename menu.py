from turtle import bgcolor, up
import pygame
from pygame.constants import K_LEFT, K_SPACE
from settings import *

class Menu():
    def __init__(self,player):
        self.display_surface = pygame.display.get_surface()
        self.player = player
        self.attribute_number = len(self.player.stats)
        self.attribute_name = list(self.player.stats.keys())
        self.max_value = list(player.max_stats.values())
        self.font = pygame.font.Font(UI_FONT,UI_FONT_SIZE)

        self.selection_index = 0
        self.selection_time = 0
        self.can_move = True

        self.height = self.display_surface.get_size()[1] * 0.8
        self.width = self.display_surface.get_size()[0] //6
        self.full_width = self.display_surface.get_size()[0]
        self.increment = self.full_width // self.attribute_number

        self.create_upgrade()
    def input(self):
        keys = pygame.key.get_pressed()
        if self.can_move:    
            if keys[pygame.K_RIGHT] and self.selection_index < self.attribute_number - 1:
                self.selection_index += 1
                self.can_move = False
                self.selection_time = pygame.time.get_ticks()
            elif keys[pygame.K_LEFT] and self.selection_index >= 1:
                self.selection_index -= 1
                self.can_move = False
                self.selection_time = pygame.time.get_ticks()
            if keys[pygame.K_SPACE]:
                self.can_move = False
                self.selection_time = pygame.time.get_ticks()
                self.item_list[self.selection_index].trigger(self.player)
    def create_upgrade(self):
        self.item_list = []
        for item, index in enumerate(range(len(self.attribute_name))):
            top = self.display_surface.get_size()[1] * 0.1
            left = (self.increment * item) + (self.increment - self.width) //2
            item = Item(left,top,self.width,self.height,index,self.font)
            self.item_list.append(item)
    def selection_timer(self):
        if not self.can_move:
            self.current_time = pygame.time.get_ticks()
            if self.current_time - self.selection_time >= 250:
                self.can_move = True
    
    def display(self):
        self.input()
        self.selection_timer()
        for index, item in enumerate(self.item_list):
            name = self.attribute_name[index]
            value = self.player.get_value_by_index(index)
            max_value = self.max_value[index]
            cost = self.player.get_cost_by_index(index)
            item.display(self.display_surface,self.selection_index,name,value,max_value,cost)

class Item():
    def __init__(self,l,t,w,h,index,font):
        self.rect = pygame.Rect(l,t,w,h)
        self.index = index
        self.font = font
    def display_names(self,surface,name,cost,selected):
        color = TEXT_COLOR_SELECTED if selected else TEXT_COLOR

        title_surf = self.font.render(name,False,color)
        title_rect = title_surf.get_rect(midtop = self.rect.midtop - pygame.math.Vector2(0,-20))
        
        cost_surf = self.font.render(str(int(cost)),False,color)
        cost_rect = title_surf.get_rect(midbottom = self.rect.midbottom - pygame.math.Vector2(-20,20))
        
        surface.blit(title_surf,title_rect)
        surface.blit(cost_surf,cost_rect)
    def display_bar(self,surface,value,max_value,selected):
        top = self.rect.midtop + pygame.math.Vector2(0,60)
        bottom = self.rect.midbottom + pygame.math.Vector2(0,-60)
        color = BAR_COLOR_SELECTED if selected else BAR_COLOR
        #bar setup
        full_height = bottom[1] - top[1]
        current_value = (value / max_value) * full_height
        value_rect = pygame.Rect(top[0] - 15,bottom[1] - current_value,30,10)

        pygame.draw.line(surface,color,top,bottom,5)
        pygame.draw.rect(surface,color,value_rect)
    def trigger(self,player):
        upgrade_atribute = list(player.stats.keys())[self.index]
        if player.stats[upgrade_atribute] < player.max_stats[upgrade_atribute]:    
                player.exp -= player.upgrade_cost[upgrade_atribute]
                player.upgrade_cost[upgrade_atribute] *= 1.4
        if player.exp >= player.upgrade_cost[upgrade_atribute]:
            player.stats[upgrade_atribute] *= 1.2
            if player.stats[upgrade_atribute] >= player.max_stats[upgrade_atribute]:
                player.stats[upgrade_atribute] = player.max_stats[upgrade_atribute]
            
                
            

    def display(self,surface,selection_num,name,value,max_value,cost):
        if self.index == selection_num:
            pygame.draw.rect(surface,UPGRADE_BG_COLOR_SELECTED,self.rect)
            pygame.draw.rect(surface,UI_BORDER_COLOR,self.rect,4)
        else:
            pygame.draw.rect(surface,UI_BG_COLOR,self.rect)
            pygame.draw.rect(surface,UI_BORDER_COLOR,self.rect,4)
        self.display_names(surface,name,cost,self.index == selection_num)
        self.display_bar(surface,value,max_value,self.index == selection_num)
