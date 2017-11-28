from chessset import ChessBoard, PieceType, PieceColor, Piece, Square, make_piece
from chessrules import get_path

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
        piece = self.board.piece_at(o)
        if not piece.legal_movement(o, d):
            return

        path = get_path(o, d)
        for square in get_path(o, d):
            if self.board.piece_at(square) is not None:
                return

        self.board.move_piece(o, d)
