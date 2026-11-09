# IMPORT
import os
import pygame
import screeninfo
import abc
import enum

# Colors
BLACK = ( 0, 0, 0)
WHITE = (255, 255, 255)

# Monitor
for monitor in screeninfo.get_monitors():
    if (monitor.is_primary):
        main_monitor = monitor
        break

# Classes - Functions
class Position(enum.Enum):
    LEFT_UPPER = ("left_upper")
    LEFT_LOWER = ("left_lower")
    RIGHT_UPPER = ("right_upper")
    RIGHT_LOWER = ("right_lower")
    CENTER = ("center")

def get_position_coordinations(pos, width, height):
    match pos:
        case Position.LEFT_UPPER:
            return 0, 0
        case Position.LEFT_LOWER:
            return 0, main_monitor.height - height
        case Position.RIGHT_UPPER:
            return main_monitor.width - width, 0
        case Position.RIGHT_LOWER:
            return main_monitor.width - width, main_monitor.height - height
        case Position.CENTER:
            return (main_monitor.width - width) // 2, (main_monitor.height - height) // 2
        case _:
            return 0, 0


class Scene(abc.ABC) :
    def __init__(self, title:str, scene_w, scene_h, default_window_position_x, default_window_position_y):
        self.title = title
        self.scene_w = scene_w
        self.scene_h = scene_h
        self.focus = False
        self.window_position_x = default_window_position_x
        self.window_position_y = default_window_position_y

    def set_focus(self, is_main_scene:bool): # Sets the focus - if focus is true, then draw works
        self.focus = is_main_scene
        pass

    @abc.abstractmethod
    def update(self) -> None:
        pass

    @abc.abstractmethod
    def draw(self, screen:pygame.display.set_mode) -> None:
        pass
    pass

class Menu(Scene):
    def __init__(self, title: str, w: int, h: int, x: int, y: int):
            super().__init__(title, w, h, x, y)

    def update(self):
        # print(f'{self.title}: updated...')
        pass

    def draw(self, screen:pygame.display.set_mode):
        pygame.display.set_window_position((self.window_position_x, self.window_position_y))
        title_text = title_font.render(f'Companion by Prynaaa', True, WHITE)
        screen.blit(title_text, title_text.get_rect(center=(self.scene_w/2, font_title_size))) # center at the top of the scene
        pass
    pass

# GLOBAL VARIABLES - FUNCTIONS
screen_width = 200
screen_height = 400
pos_x = main_monitor.width - screen_width
pos_y = main_monitor.height - screen_height
os.environ['SDL_VIDEO_WINDOW_POS'] = '%d,%d' % (pos_x, pos_y)

scenes:list[Scene] = []

# STARTUP MENU
menu_width = 400
menu_height = 400
menu = Menu("Startup Menu", menu_width, menu_height, *get_position_coordinations(Position.CENTER, menu_width, menu_height))
menu.set_focus(True)
scenes.append(menu)

# PYGAME-CE
pygame.init() 

font_title_size = 32
title_font = pygame.font.Font(None, 32)
text_font = pygame.font.Font(None, 16)

py_screen = pygame.display.set_mode((200, 400)) # pygame.NOFRAME once
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
        if(scene.focus):
            scene.update()

    # Draw scenes
    for scene in scenes:
        if(scene.focus):
            screen = pygame.display.set_mode((scene.scene_w, scene.scene_h))
            scene.draw(screen)

    pygame.display.update()
    clock.tick(60) # 120 fps


# QUIT / END
pygame.quit()