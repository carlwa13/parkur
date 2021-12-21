import pygame, sys, time # import pygame and sys

clock = pygame.time.Clock() # set up the clock

from pygame.locals import * # import pygame modules
pygame.init() # initiate pygame
pygame.mixer.init()
WINDOW_SIZE = (600,400) # set up window size
pygame.display.set_caption('yeeeeeeeet') # set the window name
screen = pygame.display.set_mode(WINDOW_SIZE,0,32) # initiate screen

pygame.mixer.music.load('start.ogg')
pygame.mixer.music.play()
time.sleep(4.5)

main_music = pygame.mixer.music.load('main.mp3')


display = pygame.Surface((1000, 600))

pygame.mixer.music.load('main.mp3')
pygame.mixer.music.play(0)

player_image = pygame.image.load('player_right.png').convert()
player_image.set_colorkey((255, 255, 255))

grass_image = pygame.image.load('grass.png')
TILE_SIZE = grass_image.get_width()

dirt_image = pygame.image.load('dirt.png')

game_map = [['0','0','0','0','0','0','0','0','0','0','0','0','2','0','0','0','0','0','0','0','0','0','0','0'],
            ['0','0','0','0','0','0','0','0','0','0','2','2','1','2','2','0','0','0','0','0','0','0','0','0'],
            ['2','0','0','0','0','0','0','0','0','0','0','1','1','1','0','0','0','0','0','0','0','0','0','0'],
            ['1','2','0','0','0','0','0','0','0','0','0','1','0','1','0','0','0','0','0','0','2','2','1','0'],
            ['0','0','0','0','0','0','0','0','0','0','0','1','0','1','0','0','0','0','0','0','0','1','0','0'],
            ['0','0','0','0','0','0','0','0','0','0','0','0','0','1','0','2','2','0','0','0','0','0','0','0'],
            ['0','0','0','0','0','0','0','0','2','2','2','0','0','0','0','1','1','0','0','0','0','0','0','0'],
            ['0','0','0','0','0','0','0','0','0','1','0','0','0','0','2','1','1','0','0','0','0','0','0','0'],
            ['0','0','0','0','0','0','0','0','0','0','0','0','0','0','1','1','1','0','0','0','0','2','2','0'],
            ['0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','2','1','0','0'],
            ['0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','1','0','0','0'],
            ['0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','2','2','1','0','0','0'],
            ['0','0','0','0','0','2','2','2','0','0','0','0','0','0','2','2','2','0','0','0','0','0','0','0']]

def collision_test(rect, tiles):
    hit_list = []
    for tile in tiles:
        if rect.colliderect(tile):
            hit_list.append(tile)
    return hit_list

def move(rect, movement, tiles):
    collision_types = {'top': False, 'bottom': False, 'right': False, 'left': False}
    rect.x += movement[0]
    hit_list = collision_test(rect, tiles)
    for tile in hit_list:
        if movement[0] > 0:
            rect.right = tile.left
            collision_types['right'] = True
        elif movement[0] < 0:
            rect.left = tile.right
            collision_types['left'] = True
    rect.y += movement[1]
    hit_list = collision_test(rect, tiles)
    for tile in hit_list:
        if movement[1] > 0:
            rect.bottom = tile.top
            collision_types['bottom'] = True
        elif movement[1] < 0:
            rect.top = tile.bottom
            collision_types['top'] = True
    return rect, collision_types

moving_right = False
moving_left = False

player_y_momentum = 0
air_timer = 0

player_rect = pygame.Rect(50, 50, player_image.get_width(), player_image.get_height())
test_rect = pygame.Rect(100,100,100,50)

while True: # game loop
    display.fill((146,244,255))

    tile_rects = []
    y = 0
    for row in game_map:
        x = 0
        for tile in row:
            if tile == '1':
                display.blit(dirt_image, (x * TILE_SIZE, y * TILE_SIZE))
            if tile == '2':
                display.blit(grass_image, (x * TILE_SIZE, y * TILE_SIZE))
            if tile != '0':
                tile_rects.append(pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))
            x += 1
        y += 1

    player_movement = [0, 0]
    if moving_right:
        player_movement[0] += 4
    if moving_left:
        player_movement[0] -= 4
    player_movement[1] += player_y_momentum
    player_y_momentum += 0.2
    if player_y_momentum > 4:
        player_y_momentum = 15

    player_rect, collisions = move(player_rect, player_movement, tile_rects)

    if collisions['bottom']:
        player_y_momentum = 0
        air_timer = 0
    else:
        air_timer += 1
    to_left = player_movement[0]
    display.blit(player_image, (player_rect.x, player_rect.y))
    
    for event in pygame.event.get(): # event loop
        if event.type == QUIT: # check for window quit
            pygame.quit()
            pygame.mixer.quit() # stop pygame
            sys.exit() # stop script
            
        if event.type == KEYDOWN:
            if event.key == K_RIGHT and to_left <= 20:
                moving_right = True
                player_image = pygame.image.load('player_right.png').convert()
                player_image.set_colorkey((255, 255, 255))
            if event.key == K_LEFT and to_left <= 260:
                moving_left = True
                player_image = pygame.image.load('player_left.png').convert()
                player_image.set_colorkey((255, 255, 255))
            if event.key == K_UP:
                if air_timer < 10:
                    player_y_momentum = -10
        if event.type == KEYUP:
            if event.key == K_RIGHT and to_left <= 20:
                moving_right = False
                player_image = pygame.image.load('player_right.png').convert()
                player_image.set_colorkey((255, 255, 255))
            if event.key == K_LEFT and to_left <= 260:
                player_image = pygame.image.load('player_left.png').convert()
                moving_left = False
                player_image.set_colorkey((255, 255, 255))
    surf = pygame.transform.scale(display, WINDOW_SIZE)
    screen.blit(surf, (0, 0))
    pygame.display.update() # update display
    clock.tick(60) # maintain 60 fps
