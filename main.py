from draw import Window, Field
from pygame import Color, init
import parameters
from events import Events
from snake import Snake, Food, Grid, Score, HistoryScore
from text import Text
from text import RecordText
import os
os.system('cls')

init()
game_score = Score(0, 50, (10, 5), parameters.SCORE_COLOR, name='g')
max_score = Score(0, 50, (100, 5), parameters.SCORE_COLOR, image_name='kubok.png', name='m')
field = Field((20, 20), parameters.CELLS_COLORS)

grid = Grid(field)
window = Window([field, game_score, max_score])
food = Food(grid, height_in_pixels=parameters.CELL_SIZE)
field.rect.center = window.rect.center
snake = Snake(grid, food, game_score)
field.add_objects([snake, food])
events = Events()
history_score = HistoryScore()
# record_text = RecordText(str(history_score.read_scores()[
#                          0][1]), 50, (10, 70), parameters.SCORE_COLOR)
# window.add_objects([record_text])
max_score.add(history_score.best_score)

while events.running:
    snake.update()
    food.update()
    events.update()
    if game_score.score > history_score.best_score:
        history_score.update_record(game_score.score)
        max_score.add()
    window.update()
