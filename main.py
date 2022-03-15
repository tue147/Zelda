import sys
import pygame
from settings import *
from level import Level
from sound import SoundPlayer
class Game:
	def __init__(self):
		pygame.init()
		self.screen = pygame.display.set_mode((WIDTH,HEIGHT))
		pygame.display.set_caption('IceVII')
		self.clock = pygame.time.Clock()
		self.level = Level()
	def run(self):
		while True:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_q:
						pygame.quit()
						sys.exit()
					if event.key == pygame.K_x:
						self.level.levelup()
			
			self.screen.fill(WATER_COLOR)
			self.level.run()
			pygame.display.update()
			self.clock.tick(FPS)
if __name__ == '__main__':
	game = Game()
	game.run()
 