from chessset import Square
from chessgame import ChessGame
from boardcanvas import BoardCanvas
from tkinter import Tk
from gametree import do_depth_two


class Controller(Tk):
    """ Top level GUI class, catches inputs from the user and dispatches the
    appropriate requests to the model and vies classes """
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        self.bind('<Key>', self.key_event)
        self.view = BoardCanvas(self)
        self.minsize(400,400)
        self.view.place(relwidth=1.0, relheight=1.0)
        self.model = ChessGame()

    def move_submit(self, o, d):
        self.model.play_move(o, d)
        self.view.draw_position()

    def key_event(self, event):
        if event.char == ' ':
            self.model.setup_problem()
            self.view.board = self.model.board
            self.view.draw_position()
        else:
            do_depth_two(self.model)

    def run(self):
        self.view.board = self.model.board
        self.mainloop()

move_number = 0
moves = [
    (Square('e', 2), Square('e', 4)),
    (Square('e', 7), Square('e', 5)),
    (Square('g', 1), Square('f', 3)),
    (Square('d', 7), Square('d', 6)),
    (Square('d', 2), Square('d', 4)),
    (Square('c', 8), Square('g', 4)),
    (Square('d', 4), Square('e', 5)),
    (Square('g', 4), Square('f', 3)),
    (Square('d', 1), Square('f', 3)),
    (Square('d', 6), Square('e', 5)),
    (Square('f', 1), Square('c', 4)),
    (Square('g', 8), Square('f', 6)),
    (Square('f', 3), Square('b', 3)),
    (Square('d', 8), Square('e', 7)),
    (Square('b', 1), Square('c', 3)),
    (Square('c', 7), Square('c', 6)),
    (Square('c', 1), Square('g', 5)),
    (Square('b', 7), Square('b', 5)),
    (Square('c', 3), Square('b', 5)),
    (Square('c', 6), Square('b', 5)),
    (Square('c', 4), Square('b', 5)),
    (Square('b', 8), Square('d', 7)),
    (Square('e', 1), Square('c', 1)),
    (Square('a', 1), Square('d', 1)),
    (Square('a', 8), Square('d', 8)),
    (Square('d', 1), Square('d', 7)),
    (Square('d', 8), Square('d', 7)),
    (Square('h', 1), Square('d', 1)),
    (Square('e', 7), Square('e', 6)),
    (Square('b', 5), Square('d', 7)),
    (Square('f', 6), Square('d', 7)),
    (Square('b', 3), Square('b', 8)),
    (Square('d', 7), Square('b', 8)),
    (Square('d', 1), Square('d', 8))]


if __name__ == "__main__":
    ctrl = Controller()
    ctrl.run()