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
        if self.in_check_after_move(o, d):
            return

        self.board.move_piece(o, d)

    def can_move_to(self, origin_square, destination_square):
        piece = self.board.piece_at(origin_square)
        destination_piece = self.board.piece_at(destination_square)
        row_diff = destination_square.row - origin_square.row
        file_diff = ord(destination_square.file) - ord(origin_square.file)

        if not piece.legal_movement(origin_square, destination_square):
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


