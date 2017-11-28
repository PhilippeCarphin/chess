from grid import Grid, GridError
from enum import Enum
from chessrules import *


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


class Piece:
    def __init__(self, color, piece_type):
        self.color = color
        self.type = piece_type

    def __str__(self):
        return str(self.color) + ', ' + str(self.type)

    def legal_movement(self, origin_square, destination_square):
        raise Exception("Piece with no type")


class Rook(Piece):
    def __init__(self, color):
        Piece.__init__(self, color, PieceType.ROOK)

    def legal_movement(self, origin_square, destination_square):
        return is_lateral_move(origin_square, destination_square)


class Bishop(Piece):
    def __init__(self, color):
        Piece.__init__(self, color, PieceType.BISHOP)

    def legal_movement(self, origin_square, destination_square):
        return is_diagonal_move(origin_square, destination_square)


class Queen(Piece):
    def __init__(self, color):
        Piece.__init__(self, color, PieceType.QUEEN)

    def legal_movement(self, origin_square, destination_square):
        return is_diagonal_move(origin_square, destination_square) or is_lateral_move(origin_square, destination_square)


class Pawn(Piece):
    def __init__(self, color):
        Piece.__init__(self, color, PieceType.PAWN)

    def legal_movement(self, origin_square, destination_square):
        row_diff = destination_square.row - origin_square.row
        file_diff = ord(destination_square.file) - ord(origin_square.file)
        direction = 1 if self.color == PieceColor.WHITE else -1

        if row_diff == 2*direction and origin_square.row == 2*direction and file_diff == 0:
            return True
        if row_diff == 1*direction and file_diff in (-1, 0, 1):
            return True
        return False


class Knight(Piece):
    def __init__(self, color):
        Piece.__init__(self, color, PieceType.KNIGHT)

    def legal_movement(self, origin_square, destination_square):
        file_difference = ord(destination_square.file) - ord(origin_square.file)
        row_difference = destination_square.row - origin_square.row
        return tuple(map(abs, (file_difference, row_difference))) in ((1, 2), (2, 1))


class King(Piece):
    def __init__(self, color):
        Piece.__init__(self, color, PieceType.KING)

    def legal_movement(self, origin_square, destination_square):
        return distance(origin_square, destination_square) == 1


piece_maker = {PieceType.ROOK: (lambda c: Rook(c)),
               PieceType.BISHOP: (lambda c: Bishop(c)),
               PieceType.KNIGHT: (lambda c: Knight(c)),
               PieceType.QUEEN: (lambda c: Queen(c)),
               PieceType.KING: (lambda c: King(c)),
               PieceType.PAWN: (lambda c: Pawn(c))}


def make_piece(piece_color, piece_type):
    return piece_maker[piece_type](piece_color)

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
