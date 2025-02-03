import pygame
import parameters


class BaseDrawable:
    def __init__(self, size=None, color=None, position=None, objects=None):
        self._width, self._height = (size or [0, 0])
        self._color = color or (0, 0, 0)
        self._rect = pygame.Rect(
            position or [0, 0], (self._width, self._height))
        self._objects = objects or []

    def add_objects(self, objects):
        self._objects.extend(objects)

    def delete_objects(self, objects):
        self._objects = [obj for obj in self._objects if obj not in objects]

    def _draw_objects(self, surface):
        for obj in self._objects:
            if type(obj) is Surface:  # isinstance(obj, Surface)
                surface.blit(obj.surface, obj.rect)
            else:
                obj.draw(surface)


class Window(BaseDrawable):
    __window = None

    def __new__(cls, *args, **kwargs):
        if not cls.__window:
            cls.__window = super().__new__(cls)
        return cls.__window

    def __init__(self, objects=None):
        super().__init__(size=[parameters.WINDOW['width'], parameters.WINDOW['height']],
                         color=parameters.SCREEN_COLOR,
                         objects=objects)
        self.__surface = pygame.display.set_mode((self._width, self._height))

    def update(self):
        self.__surface.fill(self._color)
        self._draw_objects(self.__surface)
        pygame.display.update()

    @property
    def rect(self):
        return self.__surface.get_rect()


class Surface(BaseDrawable):
    def __init__(self, size, color, position=None, objects=None):
        super().__init__(size=size, color=color, position=position, objects=objects)
        self._surface = pygame.Surface((self._width, self._height))

    @property
    def surface(self):
        self._surface.fill(self._color)
        self._draw_objects(self._surface)
        return self._surface

    @property
    def rect(self):
        return self._rect


class Field(Surface):
    def __init__(self, size, colors, position=None, objects=None):
        super().__init__((size[0] * parameters.CELL_SIZE, size[1]
                          * parameters.CELL_SIZE), colors[0], position, objects)
        self.__color = colors
        self.__quantity_cells = size

    def draw(self, surface):
        self._surface.fill(self.__color[0])
        for x in range(self.__quantity_cells[0]):
            for y in range(self.__quantity_cells[1]):
                rect = pygame.Rect(
                    x * parameters.CELL_SIZE,
                    y * parameters.CELL_SIZE,
                    parameters.CELL_SIZE,
                    parameters.CELL_SIZE
                )

                pygame.draw.rect(
                    self._surface, self.__color[(x + y) % 2], rect)
        self._draw_objects(self._surface)
        surface.blit(self._surface, self._rect)
        
    @property
    def quantity_cells(self):
        return self.__quantity_cells