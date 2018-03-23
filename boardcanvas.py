from tkinter import Tk, Canvas
from chessset import ChessBoard, Square, PieceType, PieceColr

white_unicode = {
        PieceType.KNG: u'\u2654',
        PieceType.QUN: u'\u2655',
        PieceType.ROK: u'\u2656',
        PieceType.BSP: u'\u2657',
        PieceType.NIT: u'\u2658',
        PieceType.PWN: u'\u2659'
}

black_unicode = {
        PieceType.KNG: u'\u265A',
        PieceType.QUN: u'\u265B',
        PieceType.ROK: u'\u265C',
        PieceType.BSP: u'\u265D',
        PieceType.NIT: u'\u265E',
        PieceType.PWN: u'\u265F'
}

pieces_unicode = {
        PieceColr.WHT: white_unicode,
        PieceColr.BLK: black_unicode}


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
        self.x_cursor_offset = 0
        self.y_cursor_offset = 0
        self.highlight_square = None

    def motion_event(self, event):
        if self.cursor_piece is not None:
            self.draw_position()
            self.draw_piece(event.x + self.x_cursor_offset, event.y + self.y_cursor_offset, self.cursor_piece)
            destination_square = self.coord_to_square(event.x, event.y)
            if self.cursor_piece.legal_movement(self.origin_square, destination_square):
                self.highlight_square = self.coord_to_square(event.x, event.y)
            else:
                self.highlight_square = None

    def coord_to_square(self, x, y):
        file = chr(ord('a') + int(x / self.side))
        row = 8 - int(y / self.side)
        return Square(file, row)

    def button_event(self, event):
        self.x_cursor_offset = - (event.x % self.side)
        self.y_cursor_offset = - (event.y % self.side)
        if self.cursor_piece is None:
            self.origin_square = self.coord_to_square(event.x, event.y)
            piece = self.board.piece_at(self.origin_square)
            if piece is not None and self.master.model.turn == piece.color:
                self.cursor_piece = piece
                self.motion_event(event)

    def button_release_event(self, event):
        self.cursor_piece = None
        destination_square = self.coord_to_square(event.x, event.y)
        self.master.move_submit(self.origin_square, destination_square)
        self.highlight_square = None
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
        self.draw_symbol(x, y, pieces_unicode[piece.color][piece.type])

    def draw_pieces(self):
        for square in self.board:
            piece = self.board.piece_at(square)
            if piece is self.cursor_piece:
                continue
            x, y = self.square_to_coord(square.file, square.row)
            self.draw_piece(x, y, piece)

    def clear_square(self, file, row):
        if (ord(file) - ord('a') + row) % 2 == 0:
            color = 'white'
        else:
            color = 'grey'
        if Square(file,row) == self.highlight_square:
            color = 'blue'
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



