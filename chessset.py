from grid import Grid, GridError
from enum import Enum
from collections import namedtuple


class PieceType(Enum):
    PAWN = 1
    ROOK = 2
    KNIGHT = 3
    BISHOP = 4
    QUEEN = 5
    KING = 6


class PieceColor(Enum):
    WHITE = 1
    BLACK = 2


Square = namedtuple('Square', ['file', 'row'])


class Piece:
    def __init__(self, color, piece_type):
        self.color = color
        self.type = piece_type

    def __str__(self):
        return str(self.color) + ', ' + str(self.type)


class ChessBoardError(Exception):
    pass


class ChessBoard:
    def __init__(self):
        self.board = Grid(8, 8)

    def put_piece(self, square, piece):
        # Test coord for validity
        self.board[square] = piece

    def clear_square(self, square):
        piece = self.board[square]
        try:
            del self.board[square]
        except KeyError as ke:
            print("ChessBoard.clear_square(): KeyError")
        return piece

    def move_piece(self, origin, destination):
        if origin == destination:
            return
        try:
            piece = self.board[origin]
        except KeyError as ke:
            raise ChessBoardError("move_piece(): Error : " + str(ke))

        try:
            self.put_piece(destination, piece)
        except GridError as ge:
            raise ChessBoardError("move_piece(): Error : " + str(ge))

        self.clear_square(origin)

    def piece_at(self, square):
        return self.board[square] if square in self.board else None

    def __iter__(self):
        return iter(self.board)
