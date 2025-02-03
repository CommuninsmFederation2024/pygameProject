import pygame
from image import Image


class Text:
    def __init__(self, text: str, size: int, tl_position: tuple, color: pygame.Color):
        self._text = text
        self._font = pygame.font.Font(None, size)
        self._color = color
        self._surface = self._font.render(self._text, True, self._color)
        self._rect = self._surface.get_rect()
        self._tl_position = tl_position
        self._rect.topleft = tl_position

    def draw(self, surface):
        surface.blit(self._surface, self._rect)


class RecordText(Text):
    def __init__(self, text: str, size: int, tl_position: tuple, color: pygame.Color, image_name='kubok.png'):
        super().__init__(text, size, tl_position, color)
        self.__image = Image(image_name)
        scale_factor = size / self.__image.image.get_height()
        self.__image.change_size(scale_factor)
        self._rect.x += self.__image.rect.width

    def draw(self, surface):
        surface.blit(self.__image.image, self.__image.rect)
        surface.blit(self._surface, self._rect)
