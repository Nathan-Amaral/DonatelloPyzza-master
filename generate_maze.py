from donatellopyzza import Game
from donatellopyzza import Action
from donatellopyzza import Feedback
from donatellopyzza import MazeGenerator
import pygame
import random
import time


if __name__ == '__main__':
    # generate and save a new random maze
    generator = MazeGenerator()
    maze = generator.create_maze(15, 15)
    fn = "test"
    maze.save(maze, filename=fn)

    # load the new maze
    __ENVIRONMENT__ = "test"
    # display the interface (or not)
    __GUI__ = True

    game = Game(__ENVIRONMENT__, __GUI__)
    # returns a turtle that execute actions on its environment
    turtle = game.start()
    
    # the hard-coded path to find the pizza in the maze environment
    actions = [Action.MOVE_FORWARD, Action.TOUCH, Action.TURN_LEFT, Action.TURN_RIGHT]

    i = 1
    while not game.isWon() :
        time.sleep(0.05)
        rand = random.randint(0, 3)
        actions = [Action.MOVE_FORWARD, Action.TOUCH, Action.TURN_LEFT, Action.TURN_RIGHT]
        squares = game.getSquaresDict()
        for key in squares:
            r = 203
            g = 189
            b = 147
            squares[key] = pygame.Color(r, g, b)
        game.setSquaresColors(squares)
        result = turtle.execute(actions[rand])
        i += 1
    if game.isWon() :
        actions = [Action.TOUCH]
        game.showMessage("Pizza trouvée ! The turtle stops moving.")
