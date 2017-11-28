from chessset import ChessBoard, PieceType, PieceColor, Piece, Square, make_piece, King
from movement import get_path
from copy import deepcopy

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

        self.board.move_piece(o, d)
        print("in_check() == " + str(self.in_check(PieceColor.WHITE)))

    def can_move_to(self, origin_square, destination_square):
        piece = self.board.piece_at(origin_square)
        if not piece.legal_movement(origin_square, destination_square):
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

        other_color = PieceColor.WHITE if color == PieceColor.BLACK else PieceColor.BLACK

        for square in self.board:
            piece = self.board.piece_at(square)
            if piece.color == other_color and self.can_move_to(square, king_square):
                return True

        return False



