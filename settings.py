WIDTH = 1024
HEIGHT = 640
FPS = 60
TILESIZE = 64
HITBOX_OFFSET_Y = {
    'player': -26,
    'tree': -40,
    'grass': -10,
    'detail':-10,
    'fence':-20,
    'fence_special':-20,
    'invisible': 0}
HITBOX_OFFSET_X = {
    'player': -6,
    'tree': -4,
    'grass': -2,
    'detail':-2,
    'fence': 0,
    'fence_special': -40,
    'invisible': 0}


weapon_data = {
    'sword': {'cooldown': 100, 'damage': 15,'graphic':'graphics/weapons/sword/full.png'},
    'lance': {'cooldown': 400, 'damage': 30,'graphic':'graphics/weapons/lance/full.png'},
    'axe': {'cooldown': 300, 'damage': 20, 'graphic':'graphics/weapons/axe/full.png'},
    'rapier':{'cooldown': 50, 'damage': 8, 'graphic':'graphics/weapons/rapier/full.png'},
    'sai':{'cooldown': 80, 'damage': 10, 'graphic':'graphics/weapons/sai/full.png'}}
magic_data = {
    'flame': {'strength': 5,'cost': 20,'graphic':'graphics/particles/flame/fire.png'},
    'heal' : {'strength': 2.5,'cost': 10,'graphic':'graphics/particles/heal/heal.png'}}
monster_data = {
    'squid': {'health': 100,'exp':100,'damage':20,'attack_type': 'slash', 
    'speed': 3, 'resistance': 1.2, 
    'attack_radius': 80, 'notice_radius': 360},
    
    'raccoon': {'health': 300,'exp':250,'damage':40,'attack_type': 'claw',  
    'speed': 3.5, 'resistance': 1.5,
    'attack_radius': 150, 'notice_radius': 450},
    
    'spirit': {'health': 100,'exp':110,'damage':8,'attack_type': 'thunder', 
    'speed': 4, 'resistance': 1, 
    'attack_radius': 60, 'notice_radius': 350},
    
    'bamboo': {'health': 70,'exp':120,'damage':6,'attack_type': 'leaf_attack', 
    'speed': 3, 'resistance': 1.2, 
    'attack_radius': 70, 'notice_radius': 300}}
sound_dict = {
    'flame':'audio/flame.wav',
    'heal':'audio/heal.wav',
    'squid':'audio/attack/slash.wav',
    'raccoon':'audio/attack/claw.wav',
    'spirit':'audio/attack/fireball.wav',
    'bamboo':'audio/attack/slash.wav',
    'player':'audio/sword.wav',
    'hit':'audio/hit.wav',
    'death':'audio/death.wav',
    'main':'audio/main.ogg',
}

BAR_HEIGHT = 20
HEALTH_BAR_WIDTH = 200
ENERGY_BAR_WIDTH = 140
ITEM_BOX_SIZE = 50
UI_FONT = 'graphics/font/joystix.ttf'
UI_FONT_SIZE = 18
HEALTH_COLOR = 'red'
ENERGY_COLOR = 'blue'
UI_BORDER_COLOR_ACTIVE = 'gold'

WATER_COLOR = '#71ddee'
UI_BG_COLOR = '#222222'
UI_BORDER_COLOR = '#111111'
TEXT_COLOR = '#EEEEEE'
#menu settings
TEXT_COLOR_SELECTED = '#111111'
BAR_COLOR = '#EEEEEE'
BAR_COLOR_SELECTED = '#111111'
UPGRADE_BG_COLOR_SELECTED = '#EEEEEE'
 

