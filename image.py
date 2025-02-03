import pygame
import parameters

class Image:
    def __init__(self, img_path, scale_factor=1, rotate=0):
        self.__draft = pygame.image.load(parameters.IMGS_PATH + '\\' + img_path)
        self.change_size(scale_factor=scale_factor)
        
    def change_size(self, scale_factor):
        img = self.__draft
        width = int(img.get_width() * scale_factor)
        height = int(img.get_height() * scale_factor)
        self.__image = pygame.transform.scale(img, (width, height))
        self.__rect = self.image.get_rect()

    @property
    def image(self):
        return self.__image

    @property
    def size(self):
        draft_width = self.__draft.get_width()
        draft_height = self.__draft.get_height()
        image_width = self.__image.get_width()
        image_height = self.__image.get_height()
        size = {
            'draft': {
                'x': draft_width,
                'y': draft_height
            },
            'image': {
                'x': image_width,
                'y': image_height
            }
        }
        return size
    
    @property
    def rect(self):
        return self.__rect