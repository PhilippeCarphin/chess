from chessset import ChessBoard, PieceType, PieceColor, Piece, Square, make_piece, King
from movement import get_path
from copy import deepcopy
from enum import Enum

class GameState(Enum):
    NORMAL = 0
    CHECK = 1
    STALEMATE = 2
    CHECKMATE = 3

class ChessGame:
    def __init__(self):
        self.board = ChessBoard()
        self.setup_standard_board()

    def setup_standard_board(self):
        row_pawn = {PieceColor.BLACK: 7, PieceColor.WHITE: 2}
        row_piece = {PieceColor.BLACK: 8, PieceColor.WHITE: 1}
        file_piece = {PieceType.ROOK: 'ah',
                      PieceType.KNIGHT: 'bg',
                      PieceType.BISHOP: 'cf',
                      PieceType.QUEEN: 'd',
                      PieceType.KING: 'e',
                      PieceType.PAWN: 'abcdefgh'}

        for t in PieceType:
            for c in PieceColor:
                row = row_pawn[c] if t == PieceType.PAWN else row_piece[c]
                for file in file_piece[t]:
                    self.board.put_piece(Square(file, row), make_piece(c, t))

    def play_move(self, o, d):
        if o == d:
            return
        if not self.can_move_to(o, d):
            return
        if self.in_check_after_move(o, d):
            return

        self.board.move_piece(o, d)
        self.has_legal_move(PieceColor.BLACK)
        print("Play_move() : " + str(o) + " -> " + str(d))
        print("GameState(BLACK) : " + str(self.game_state(PieceColor.BLACK)))

    def can_move_to(self, origin_square, destination_square):
        piece = self.board.piece_at(origin_square)
        destination_piece = self.board.piece_at(destination_square)
        row_diff = destination_square.row - origin_square.row
        file_diff = ord(destination_square.file) - ord(origin_square.file)

        if not piece.legal_movement(origin_square, destination_square):
            return False

        if destination_piece is not None and destination_piece.color == piece.color:
            return False

        if piece.type == PieceType.PAWN:
            if abs(file_diff) == 1 and destination_piece is None:
                return False
            if file_diff == 0 and destination_piece is not None:
                return False

        for square in get_path(origin_square, destination_square):
            if self.board.piece_at(square):
                return False

        return True

    def in_check(self, color):
        for square in self.board:
            piece = self.board.piece_at(square)
            if isinstance(piece, King) and piece.color == color:
                king = piece
                king_square = square
                break
        else:
            raise Exception("No king of color " + str(color) + " on board")

        other_color = PieceColor.WHITE if color == PieceColor.BLACK else PieceColor.BLACK

        for square in self.board:
            piece = self.board.piece_at(square)
            if piece.color == other_color and self.can_move_to(square, king_square):
                return True

        return False

    def in_check_after_move(self, origin_square, destination_square):
        temp_game = deepcopy(self)
        mover_color = temp_game.board.piece_at(origin_square).color
        temp_game.board.move_piece(origin_square, destination_square)

        if temp_game.in_check(mover_color):
            return True
        else:
            return False

    def has_legal_move(self, color):
        for origin_square in [s for s in self.board if True and self.board.piece_at(s).color == color]:
            for file in "abcdefgh":
                for row in range(1, 9):
                    destination_square = Square(file, row)
                    if self.can_move_to(origin_square, destination_square) and \
                            (not self.in_check_after_move(origin_square, destination_square)):
                        return True
        return False

    def game_state(self, color):
        if self.has_legal_move(color):
            if self.in_check(color):
                return GameState.CHECK
            else:
                return GameState.NORMAL
        else:
            if self.in_check(color):
                return GameState.CHECKMATE
            else:
                return GameState.STALEMATE


