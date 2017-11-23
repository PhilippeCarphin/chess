from tkinter import Tk, Canvas

from chessgame import ChessGame
from chessset import ChessBoard, Square, PieceType, PieceColor

white_unicode = {PieceType.KING: u'\u2654',
                 PieceType.QUEEN: u'\u2655',
                 PieceType.ROOK: u'\u2656',
                 PieceType.BISHOP: u'\u2657',
                 PieceType.KNIGHT: u'\u2658',
                 PieceType.PAWN: u'\u2659'}

black_unicode = {PieceType.KING: u'\u265A',
                 PieceType.QUEEN: u'\u265B',
                 PieceType.ROOK: u'\u265C',
                 PieceType.BISHOP: u'\u265D',
                 PieceType.KNIGHT: u'\u265E',
                 PieceType.PAWN: u'\u265F'}


class BoardCanvas(Canvas):
    def __init__(self, master):
        Canvas.__init__(self, master, bd=0, cursor='circle', relief='sunken')
        self.master = master
        self.bind('<Configure>', self.configure_event)
        self.bind('<Button>', self.button_event)
        self.bind('<ButtonRelease>', self.button_release_event)
        self.bind('<Motion>', self.motion_event)
        self.board = ChessBoard()
        self.side = int(master.winfo_width() / 8)
        self.move = 0  # For testing
        self.cursor_piece = None
        self.origin_square = None

    def motion_event(self, event):
        if self.cursor_piece is not None:
            self.draw_position()
            self.draw_piece(event.x -30, event.y-30, self.cursor_piece)

    def coord_to_square(self, x, y):
        file = chr(ord('a') + int(x / self.side))
        row = 8 - int(y / self.side)
        return Square(file, row)

    def button_event(self, event):
        if self.cursor_piece is None:
            self.origin_square = self.coord_to_square(event.x, event.y)
            self.cursor_piece = self.board.piece_at(self.origin_square)

    def button_release_event(self, event):
        self.cursor_piece = None
        destination_square = self.coord_to_square(event.x, event.y)
        self.master.move_submit(self.origin_square, destination_square)
        self.draw_position()

    def draw_symbol(self, x, y, symbol):
        x_offset = 0.5 * self.side
        y_offset = 0.55 * self.side
        self.create_text(x+x_offset, y+y_offset, text=symbol, font=('Arial', int(0.8 * self.side)), fill='black', activefill='red')

    def draw_square(self, file, row, color):
        x0 = (ord(file) - ord('a')) * self.side
        y0 = (8 - row) * self.side
        self.create_rectangle(x0, y0, x0 + self.side, y0 + self.side, outline="black", fill=color, width=2)

    def square_to_coord(self, file, row):
        return (ord(file) - ord('a')) * self.side, (8 - row) * self.side

    def draw_piece(self, x, y, piece):
        if piece.color == PieceColor.WHITE:
            symbol = white_unicode[piece.type]
        else:
            symbol = black_unicode[piece.type]
        self.draw_symbol(x, y, symbol)

    def draw_pieces(self):
        for square in self.board:
            piece = self.board.piece_at(square)
            if piece is self.cursor_piece:
                continue
            x, y = self.square_to_coord(square.file, square.row)
            self.draw_piece(x, y, piece)

    def clear_square(self, file, row):
        if (ord(file) - ord('a') + row) % 2 == 0:
            color = 'grey'
        else:
            color = 'white'
        self.draw_square(file, row, color)

    def draw_board(self):
        for file in 'abcdefgh':
            for row in range(1, 9):
                self.clear_square(file, row)

    def draw_position(self):
        self.delete('all')
        self.draw_board()
        self.draw_pieces()

    def configure_event(self, event):
        self.side = int(min(event.width, event.height) / 8)
        print(event)
        self.draw_position()

    def key_event(self, event):
        global move_number
        try:
            self.board.move_piece(moves[move_number][0], moves[move_number][1])
        except IndexError as ie:
            pass
        move_number += 1
        self.draw_position()


def display_board(board):
    """ Used for displaying positions in other modules for testing
    purposes"""
    root = Tk()
    root.minsize(400, 400)
    bc = BoardCanvas(root)
    root.bind('<Key>', bc.key_event)
    bc.place(relwidth=1.0, relheight=1.0)
    bc.board = board
    bc.draw_position()
    root.mainloop()



