import parameters
# import sqlalchemy
import pygame
import math
from events import Events
from draw import Field
from copy import copy
from image import Image
from random import choice
from text import Text


class Head:
    def __init__(self, direction, size=5):
        pass

    def draw(self):
        pass


class HistoryScore:
    __score = None

    def __new__(cls, *args, **kwargs):
        if not cls.__score:
            cls.__score = super().__new__(cls)

        return cls.__score

    def __init__(self, file_name=None):
        path = parameters.SCORE_PATH
        self.__file_path = path + '\\' + \
            (file_name or parameters.SCORES_FILE_NAME)
        self.__scores = []
        self.__open()
        self.read_scores()

    def __del__(self):
        self.__close()

    def __open(self):
        self.__file = open(self.__file_path, 'r+', encoding='UTF-8')

    def __close(self):
        self.__file.close()

    def read_scores(self):
        for note in self.__file.readlines():
            note = note.replace('\n', '')
            name = note[:note.index(' ')]
            score = int(note[note.index(' ') + 1:])
            self.__scores.append([score, name])

    def update_record(self, new_score):
        self.__scores.insert(0, [new_score, "Player"])
        self.__file.seek(0)
        self.__file.truncate()
        for score, name in self.__scores:
            self.__file.write(f"{name} {score}\n")
        self.__file.flush()
    
    @property
    def scores(self):
        return self.__scores
    
    @property
    def best_score(self):
        if self.__scores:
            return self.__scores[0][0]
        else:
            return 0
        
class Score(Text):
    def __init__(self, score: int, size: int, tl_position: tuple, color: pygame.color, name, image_name='yablako.png'):
        super().__init__(str(score), size, tl_position, color)
        self.name = name
        self.__score = score
        self.__image = Image(image_name)
        scale_factor = size / self.__image.image.get_height()
        self.__image.change_size(scale_factor)
        self.__image.rect.x, self.__image.rect.y = tl_position[0], tl_position[1]
        tl = self.__image.rect.topright
        self._rect.topleft = tl

    @property
    def score(self):
        return self.__score

    def add(self, addition=1):
        self.__score += addition
        tl = self._rect 
        self._surface = self._font.render(str(self.__score), True, self._color)
        print(self.name)
        # self._rect = self._surface.get_rect()
        # self._rect.topleft = self._tl_position
        # self._rect.x += self.__image.rect.width

    def draw(self, surface: pygame.Surface):
        surface.blit(self.__image.image, self.__image.rect)
        surface.blit(self._surface, self._rect)


class Grid:
    def __init__(self, field: Field):
        self.__grid = []
        for x in range(parameters.CELL_SIZE // 2, field.quantity_cells[0] * parameters.CELL_SIZE, parameters.CELL_SIZE):
            for y in range(parameters.CELL_SIZE // 2, field.quantity_cells[1] * parameters.CELL_SIZE, parameters.CELL_SIZE):
                self.__grid.append((x, y))

        self.__edges = [
            [self.__grid[0][0], self.__grid[-1][0]],
            [self.__grid[0][1], self.__grid[-1][1]]
        ]
        self.__unocupated_grid = self.__grid
        self.__grid = tuple(self.__grid)

    @property
    def get(self):
        return self.__grid

    @property
    def edges(self):
        return self.__edges

    @property
    def unocupated_grid(self):
        return self.__unocupated_grid


class Food:
    def __init__(self, grid: Grid, height_in_pixels=None, width_in_pixels=None):
        self.__grid = grid
        self.__food = None
        self.__image = Image('yablako.png')
        ind = None
        if height_in_pixels:
            ind = 'y'
        elif width_in_pixels:
            ind = 'x'
        if not ind is None:
            scale_factor = (
                height_in_pixels if ind else width_in_pixels) / self.__image.size['image'][ind]
            self.__image.change_size(scale_factor=scale_factor)

    @property
    def position(self):
        return self.__image.rect.center

    def eaten(self):
        self.__food = False

    def update(self):
        if not self.__food:
            self.__food = True
            result = choice(self.__grid.unocupated_grid)
            self.__image.rect.center = result
            self.__grid.unocupated_grid.remove(tuple(result))

    def draw(self, surface):
        surface.blit(self.__image.image, self.__image.rect)

class Snake:
    __snake = None

    def __new__(cls, *args, **kwargs):
        if not cls.__snake:
            cls.__snake = super().__new__(cls)

        return cls.__snake

    def __init__(self, grid: Grid, food: Food, score: Score, direction=pygame.K_RIGHT):
        self.__snake_lenght = parameters.SNAKE_LENGHT
        self.__direction = direction
        self.__food = food
        self.__score = score
        self.__events = Events()
        self.__turns = []
        self.__eaten = False
        self.__grid = grid
        self.__color = parameters.SNAKE_COLORS[0]
        self.__height_section = parameters.HEIGHT_SNAKE
        self.__body_dots = []
        self.__append = 0

        start = len(self.__grid.get) // 2
        x = self.__grid.get[start][0]
        y = self.__grid.get[start][1]
        count = 0
        while count < parameters.SNAKE_LENGHT:
            self.__body_dots.append([x - parameters.CELL_SIZE * count, y])
            self.__grid.unocupated_grid.remove(tuple(self.__body_dots[-1]))
            count += 1

    def draw(self, surface):
        change_dots = []
        for dot in self.__body_dots:
            change_dots.append([
                dot[0] - 1,
                dot[1] - 1
            ])
        pygame.draw.lines(surface, self.__color, False,
                          change_dots, self.__height_section[0])

        for dot in self.__body_dots:
            change_dot = [
                dot[0] + 1,
                dot[1] + 1
            ]
            pygame.draw.circle(surface, self.__color, dot,
                               self.__height_section[0] // 2)

    def update(self):
        self.__check_keys()
        self.__change_direction()
        self.__check_eat()
        self.__check_game_over()
        self.__shft_body()

    def __check_keys(self):
        last_move = self.__turns[-2] if len(self.__turns) == 2 else self.__direction if len(
            self.__turns) == 0 else self.__turns[-1]

        for direction in parameters.DIRS:
            if direction in self.__events.keys and last_move not in (parameters.REVERSE_DIRS[direction], direction):
                if len(self.__turns) == 2:
                    self.__turns[-1] = direction
                else:
                    self.__turns.append(direction)

    def __change_direction(self):
        if tuple(self.__body_dots[0]) in self.__grid.get:
            if len(self.__turns):
                self.__direction = self.__turns[0]
                self.__turns = self.__turns[1:]
            self.__body_dots = self.__body_dots[:1] + self.__body_dots
            if tuple(self.__body_dots[0]) in self.__grid.unocupated_grid:
                self.__grid.unocupated_grid.remove(tuple(self.__body_dots[0]))

    def __shft_body(self):
        self.__body_dots[0] = [
            self.__body_dots[0][0] + parameters.SHIFT[self.__direction][0],
            self.__body_dots[0][1] + parameters.SHIFT[self.__direction][1],
        ]
        if not self.__eaten or self.__append == parameters.CELL_SIZE:
            self.__append = 0
            self.__eaten = False
            tail_d = self.__tail_directrion(
                self.__body_dots[-1], self.__body_dots[-2])
            self.__body_dots[-1] = [
                self.__body_dots[-1][0] + parameters.SHIFT[tail_d][0],
                self.__body_dots[-1][1] + parameters.SHIFT[tail_d][1],
            ]
        else:
            self.__append += 1
        if self.__body_dots[-1] == self.__body_dots[-2]:
            del self.__body_dots[-2]
            self.__grid.unocupated_grid.append(tuple(self.__body_dots[-1]))

    @staticmethod
    def __tail_directrion(last, pre_last):
        dx = pre_last[0] - last[0]
        dy = pre_last[1] - last[1]
        if dx > 0:
            return pygame.K_RIGHT
        elif dx < 0:
            return pygame.K_LEFT
        elif dy > 0:
            return pygame.K_DOWN
        else:
            return pygame.K_UP

    def __check_game_over(self):
        head = copy(self.__body_dots[0])
        x = copy(self.__grid.edges[0])
        y = copy(self.__grid.edges[1])
        shadow_move = self.__turns[0] if len(self.__turns) else None

        if x[0] == head[0] + 1 and pygame.K_LEFT in (shadow_move, self.__direction):
            self.__events.running = False
        elif x[1] == head[0] - 1 and pygame.K_RIGHT in (shadow_move, self.__direction):
            self.__events.running = False
        elif y[0] == head[1] + 1 and pygame.K_UP in (shadow_move, self.__direction):
            self.__events.running = False
        elif y[1] == head[1] - 1 and pygame.K_DOWN in (shadow_move, self.__direction):
            self.__events.running = False

        head = self.__check_on_distance(head)

        if head in self.__body_dots[1:]:
            self.__events.running = False

    def __check_on_distance(self, dot: list):
        dot = copy(dot)
        if self.__direction == pygame.K_DOWN:
            dot[1] += parameters.CELL_SIZE
        elif self.__direction == pygame.K_UP:
            dot[1] -= parameters.CELL_SIZE
        elif self.__direction == pygame.K_RIGHT:
            dot[0] += parameters.CELL_SIZE
        elif self.__direction == pygame.K_LEFT:
            dot[0] -= parameters.CELL_SIZE

        return dot

    def __check_eat(self):
        head = self.__body_dots[0]
        head = self.__check_on_distance(head)
        if tuple(head) == self.__food.position:
            self.__eaten = True
            self.__score.add()
            self.__food.eaten()