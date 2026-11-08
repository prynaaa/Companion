# IMPORT
import os
import pygame
import screeninfo


# GLOBAL VARIABLES - FUNCTIONS
monitors = screeninfo.get_monitors()
for monitor in monitors :
    if (monitor.is_primary == True) :
        main_monitor = monitor
        break
screen_width = 200
screen_height = 400
pos_x = main_monitor.width - screen_width
pos_y = main_monitor.height - screen_height
os.environ['SDL_VIDEO_WINDOW_POS'] = '%d,%d' % (pos_x, pos_y)


# PYGAME-CE
pygame.init() 
py_screen = pygame.display.set_mode((200, 400), pygame.RESIZABLE) # pygame.NOFRAME once
clock = pygame.time.Clock()
title = 'Companion by Prynaaa'
pygame.display.set_caption(title)

# LOOP
running = True
while running:
    py_screen.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    clock.tick(60) # 60 fps

    pygame.display.update()


# QUIT / END
pygame.quit()