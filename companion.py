# IMPORT
import os
import pygame
import screeninfo
import abc


# Classes
class Scene(abc.ABC) :
    def __init__(self, name:str, scene_w, scene_h):
        self.name = name
        self.scene_w = scene_w
        self.scene_h = scene_h
        self.focus = False

    def set_focus(self, is_main_scene:bool): # Sets the focus - if focus is true, then draw works
        pass

    @abc.abstractmethod
    def update(self) -> None:
        pass

    @abc.abstractmethod
    def draw(self) -> None:
        pass
    pass


# GLOBAL VARIABLES - FUNCTIONS
for monitor in screeninfo.get_monitors():
    if (monitor.is_primary == True):
        main_monitor = monitor
        break
screen_width = 200
screen_height = 400
pos_x = main_monitor.width - screen_width
pos_y = main_monitor.height - screen_height
os.environ['SDL_VIDEO_WINDOW_POS'] = '%d,%d' % (pos_x, pos_y)

scenes:list[Scene] = []


# PYGAME-CE
pygame.init() 
py_screen = pygame.display.set_mode((200, 400), pygame.RESIZABLE) # pygame.NOFRAME once
clock = pygame.time.Clock()
title = 'Companion by Prynaaa'
pygame.display.set_caption(title)


# LOOP
running = True
while running:
    py_screen.fill((0, 0, 0)) # clears screen every frame
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update Scenes
    for scene in scenes:
        scene.update()

    # Draw scenes
    for scene in scenes:
        scene.draw

    clock.tick(60) # 60 fps

    pygame.display.update()


# QUIT / END
pygame.quit()