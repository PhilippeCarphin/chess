from chessset import ChessBoard, PieceType, PieceColor, Piece, Square


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
                    self.board.put_piece(Square(file, row), Piece(c,t))

    def play_move(self, origin_square, destination_square):
        if self.is_legal(origin_square, destination_square):
            self.board.move_piece(origin_square, destination_square)

    def is_legal(self, origin_square, destination_square):
        piece = self.board.piece_at(origin_square)
        dest_piece = self.board.piece_at(destination_square)
        if dest_piece is not None and dest_piece.color == piece.color:
            return False
        if piece is None:
            return
        if origin_square == destination_square:
            return False

        if piece.type == PieceType.ROOK:
            return self.rook_move_legal(origin_square, destination_square)
        elif piece.type == PieceType.PAWN:
            return self.pawn_move_legal(origin_square, destination_square)

        return True


    def rook_move_legal(self, o, d):
        if d.file != o.file and o.row != d.row:
            return False
        if o.file != d.file:
            for ord_file in range(ord(o.file), ord(d.file)):
                if ord_file == ord(o.file):
                    continue
                if self.board.piece_at(Square(chr(ord_file), d.row)) is not None:
                    return False
        if o.row != d.row:
            for row in range(o.row, d.row):
                if row == o.row:
                    continue
                if self.board.piece_at(Square(d.file, row)) is not None:
                    return False
        return True

    def pawn_move_legal(self, origin_square, destination_square):
        return True
