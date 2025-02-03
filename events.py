import pygame
import time

class Events:
    events_object = None
    
    def __new__(cls, *args, **kwargs):
        if not cls.events_object:
            cls.events_object = super().__new__(cls)

        return cls.events_object
    
    def __init__(self):
        self.__time = time.time()
        self.__keys = []
        self.__mouse = (-1, -1)
        self.running = True

    @property
    def time(self):
        return self.__time
    
    @property
    def keys(self):
        return self.__keys
    
    @property
    def mouse(self):
        return self.__mouse    

    def update(self):
        self.__events()
        self.__upd_time()
        self.__upd_mouse()
        pygame.time.Clock().tick(10000)

    def __events(self):
        self.__keys.clear()
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                self.__keys.append(event.unicode if event.unicode else event.key)

            if event.type == pygame.QUIT:
                self.running = False

    def __upd_time(self):
        self.__time = time.time()

    def __upd_mouse(self):
        self.__mouse = pygame.mouse.get_cursor()