# IMPORT
import os
import pygame
import pygame_gui
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

def get_position_coordinations(pos:Position, width, height):
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

def get_position_coordinations_inside_window(pos:Position, scene:Scene, width, height):
    match pos:
        case Position.LEFT_UPPER:
            return 0, 0
        case Position.LEFT_LOWER:
            return 0, scene.scene_h - height
        case Position.RIGHT_UPPER:
            return scene.scene_w - width, 0
        case Position.RIGHT_LOWER:
            return scene.scene_w - width, scene.scene_h - height
        case Position.CENTER:
            return (scene.scene_w - width) // 2, (scene.scene_h - height) // 2
        case _:
            return 0, 0

def changeCompanionPosition():
    global companion_position
    match companion_position:
        case Position.LEFT_UPPER:
            companion_position = Position.LEFT_LOWER
        case Position.LEFT_LOWER:
            companion_position = Position.RIGHT_UPPER
        case Position.RIGHT_UPPER:
            companion_position = Position.RIGHT_LOWER
        case Position.RIGHT_LOWER:
            companion_position = Position.LEFT_UPPER
        case _:
            companion_position = Position.LEFT_UPPER

def changeActiveScene(scene_from:Scene, scene_to:Scene):
    scene_from.set_focus(False)
    scene_to.set_focus(True)
    pygame.display.set_mode((scene_to.scene_w, scene_to.scene_h))
    manager.set_window_resolution((scene_to.scene_w, scene_to.scene_h))
    pass

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
        screen.blit(image_position, get_position_coordinations_inside_window(companion_position, self, image_position.width, image_position.height)) # see image_companion comment
        pass
    pass

class Companion(Scene):
    def __init__(self, title: str, w: int, h: int, x: int, y: int):
                super().__init__(title, w, h, x, y)
    
    def update(self):
        # print(f'{self.title}: updated...')
        pass

    def draw(self, screen:pygame.display.set_mode): 
        pygame.display.set_window_position((self.window_position_x, self.window_position_y))
        screen.blit(image_companion, Position.LEFT_UPPER) 
        pass
    pass

# GLOBAL VARIABLES - FUNCTIONS
companion_position = Position.RIGHT_LOWER
screen_width = 400
screen_height = 800
pos_x = main_monitor.width - screen_width
pos_y = main_monitor.height - screen_height
os.environ['SDL_VIDEO_WINDOW_POS'] = '%d,%d' % (pos_x, pos_y)

scenes:list[Scene] = []

# STARTUP MENU
menu_width = 400
menu_height = 800
menu = Menu("Startup Menu", menu_width, menu_height, *get_position_coordinations(Position.CENTER, menu_width, menu_height))
menu.set_focus(True)
scenes.append(menu)

# COMPANION SCENE
scene_companion_width = 320
scene_companion_height = 320
companion = Companion("Companion Scene", scene_companion_width, scene_companion_height, *get_position_coordinations(companion_position, scene_companion_width, scene_companion_width))

# PYGAME-CE & PYGAME_GUI
pygame.init() 

manager = pygame_gui.UIManager((screen_width, screen_height))

font_title_size = 32
title_font = pygame.font.Font(None, 32)
text_font = pygame.font.Font(None, 16)

py_screen = pygame.display.set_mode((screen_width, screen_height)) # pygame.NOFRAME once
clock = pygame.time.Clock()
title = 'Companion by Prynaaa'
pygame.display.set_caption(title)

# message_box = pygame.display.message_box('test', 'testing this is crazy', 'info') # info, warn, error
button_companion_position_w = 120
button_companion_position_h = 40
button_companion_position = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect(get_position_coordinations_inside_window(Position.CENTER, menu, button_companion_position_w, button_companion_position_h), (button_companion_position_w, button_companion_position_h)), 
    text='Change Position', manager=manager)

button_done_position_x = 120
button_done_position_y = 40
button_done_width = 120
button_done_height = -40
button_done = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect(get_position_coordinations_inside_window(Position.CENTER, menu, button_done_width, button_done_height), (button_done_position_x, button_done_position_y)), 
    text='DONE', manager=manager)


# IMAGES
image_companion = pygame.image.load(os.path.join('resources/default', 'plum_companion_320x320.png')).convert()
image_position = pygame.image.load(os.path.join('resources/default', 'companion_position.png')).convert()

# LOOP
running = True
while running:
    py_screen.fill(BLACK) # clears screen every frame
    time_delta = clock.tick(24)/1000

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if(event.ui_element == button_companion_position):
                changeCompanionPosition()
            if(event.ui_element == button_done):
                changeActiveScene(menu, companion)
                button_done.hide()
                button_companion_position.hide()
        manager.process_events(event)

    # Update Scenes
    manager.update(time_delta)
    for scene in scenes:
        if(scene.focus):
            scene.update()

    # Draw scenes
    for scene in scenes:
        if(scene.focus):
            scene.draw(py_screen)

    manager.draw_ui(py_screen)
    pygame.display.update()
    clock.tick(24) # 24 fps


# QUIT / END
pygame.quit()