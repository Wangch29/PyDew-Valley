import pygame
from setting import *
from support import *
from timer import Timer

""" Animate changing speed """
ANIMATE_FPS_INDEX: int = 4


class Player(pygame.sprite.Sprite):

    def __init__(self, pos: tuple, group: pygame.sprite.Group):
        super().__init__(group)

        self.import_assets()
        self.status: str = "down"
        self.frame_index: float = 0

        # General setup
        self.image = self.animations[self.status][int(self.frame_index)]
        self.rect = self.image.get_rect(center=pos)

        # Movement attributes
        self.direction = pygame.math.Vector2()
        self.pos = pygame.math.Vector2(self.rect.center)
        self.speed: float = 100

        # timers
        self.timers: dict = {
                'tool use': Timer(350, self.use_tool)
        }

        # tools
        self.selected_tool = 'water'

    def use_tool(self):
        print(self.selected_tool)

    def import_assets(self):
        self.animations = {'up': [], 'down': [], 'left': [], 'right': [],
                           'right_idle': [], 'left_idle': [], 'up_idle': [], 'down_idle': [],
                           'right_hoe': [], 'left_hoe': [], 'up_hoe': [], 'down_hoe': [],
                           'right_axe': [], 'left_axe': [], 'up_axe': [], 'down_axe': [],
                           'right_water': [], 'left_water': [], 'up_water': [], 'down_water': []}

        for animation in self.animations.keys():
            full_path = '../graphics/character/' + animation
            self.animations[animation] = import_folder(full_path)

    def animate(self, dt: float):
        # Update frame_index
        self.frame_index = self.frame_index + ANIMATE_FPS_INDEX * dt
        if self.frame_index >= len(self.animations[self.status]):
            self.frame_index = 0
        # Update image
        self.image = self.animations[self.status][int(self.frame_index)]

    def input(self):
        keys = pygame.key.get_pressed()

        if not self.timers['tool use'].active:
            # directions
            if keys[pygame.K_UP]:
                self.direction.y = -1
                self.status = "up"
            elif keys[pygame.K_DOWN]:
                self.direction.y = 1
                self.status = "down"
            else:
                self.direction.y = 0

            if keys[pygame.K_LEFT]:
                self.direction.x = -1
                self.status = "left"
            elif keys[pygame.K_RIGHT]:
                self.direction.x = 1
                self.status = "right"
            else:
                self.direction.x = 0

            # tool use
            if keys[pygame.K_SPACE]:
                self.timers['tool use'].activate()
                self.direction = pygame.math.Vector2(0, 0)
                self.frame_index = 0

    def get_status(self):
        # idle status
        if self.direction.magnitude() == 0:
            self.status = self.status.split('_')[0] + '_idle'

        # tool using status
        if self.timers['tool use'].active:
            # self.status = TOOL_STATUS_MAPPING.get(self.status)
            self.status = self.status.split('_')[0] + '_' + self.selected_tool

    def move(self, dt: float):
        # normalizing a vector
        if self.direction.magnitude() != 0:
            self.direction = self.direction / self.direction.magnitude()

        # horizontal movement
        self.pos.x += self.direction.x * self.speed * dt
        # vertical movement
        self.pos.y += self.direction.y * self.speed * dt
        # update self.rect.center
        self.rect.center = self.pos

    def update_timers(self):
        for timer in self.timers.values():
            timer.update()

    def update(self, dt: float):
        self.update_timers()
        self.input()
        self.get_status()
        self.move(dt)
        self.animate(dt)
