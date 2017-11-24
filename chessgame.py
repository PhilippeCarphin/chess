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
        elif piece.type == PieceType.BISHOP:
            return self.bishop_move_legal(origin_square, destination_square)
        elif piece.type == PieceType.QUEEN:
            return self.queen_move_legal(origin_square, destination_square)
        elif piece.type == PieceType.KING:
            return self.king_move_legal(origin_square, destination_square)
        elif piece.type == PieceType.KNIGHT:
            return self.knight_move_legal(origin_square, destination_square)
        else:
            raise Exception

    def is_diagonal_move(self, o, d):
        if abs(o.row - d.row) != abs(ord(o.file) - ord(d.file)):
            return False
        return True

    def is_latteral_move(self, o, d):
        return self.is_file_move(o, d) or self.is_row_move(o, d)

    def is_row_move(self, o, d):
        return o.file == d.file and o.row != d.row

    def get_file_path(self, o, d):
        if ord(o.file) > ord(d.file):
            file_range = reversed(range(ord(d.file)+1, ord(o.file)+1))
        else:
            file_range = range(ord(o.file), ord(d.file))
        return [Square(file, o.row) for file in map(chr, file_range)][1:]

    def get_row_path(self, o, d):
        if o.row > d.row:
            row_range = reversed(range(d.row, o.row))
        else:
            row_range = range(o.row, d.row)
        return [Square(o.file, row) for row in row_range][1:]

    def get_diag_path(self, o, d):

        if o.row > d.row:
            row_range = reversed(range(d.row, o.row))
        else:
            row_range = range(o.row, d.row)
        if ord(o.file) > ord(d.file):
            file_range = reversed(range(ord(d.file)+1, ord(o.file)+1))
        else:
            file_range = range(ord(o.file), ord(d.file))

        return [Square(file, row) for file, row in zip(map(chr, file_range), row_range)][1:]

    def is_file_move(self, o, d):
        return o.file != d.file and o.row == d.row

    def rook_move_legal(self, o, d):
        if self.is_row_move(o, d):
            path = self.get_row_path(o, d)
        elif self.is_file_move(o, d):
            path = self.get_file_path(o, d)
        else:
            return False

        for square in path:
            if self.board.piece_at(square):
                return False
        return True

    def bishop_move_legal(self, o, d):
        if not self.is_diagonal_move(o, d):
            return False
        for square in self.get_diag_path(o, d):
            if self.board.piece_at(square) is not None:
                return False
        return True

    def queen_move_legal(self, o, d):
        return self.rook_move_legal(o,d) or self.bishop_move_legal(o,d)

    def king_move_legal(self, o, d):
        d_row=o.row - d.row
        d_file=ord(o.file) - ord(d.file)
        if abs(d_row) > 1 or abs(d_file) > 1:
            return False
        return True

    def knight_move_legal(self, o, d):
        d_row=o.row - d.row
        d_file=ord(o.file) - ord(d.file)
        if abs(d_file) == 1 and abs(d_row) == 2:
            return True
        if (abs(d_file), abs(d_row)) in [(1,2),(2,1)]:
            return True
        else:
            return False

    def pawn_move_legal(self, origin_square, destination_square):
        piece = self.board.piece_at(origin_square)
        if piece.color == PieceColor.WHITE:
            return self.white_pawn_move_legal(origin_square, destination_square)
        elif piece.color == PieceColor.BLACK:
            return self.black_pawn_move_legal(origin_square, destination_square)
        else:
            raise Exception("Can't run")

    def black_pawn_move_legal(self, o, d):
        return True

    def white_pawn_move_legal(self, o, d):
        d_row=d.row - o.row
        d_file=ord(d.file) - ord(o.file)
        print("d_file = {}, d_row = {}".format(d_file, d_row))
        destination_piece = self.board.piece_at(d)
        if d_row == 1 and d_file in (1,-1):
            if destination_piece is not None and destination_piece.color == PieceColor.BLACK:
                return True
            # TODO Do en-passant
        elif d_row == 1 and d_file == 0:
            if destination_piece is None:
                return True
        elif o.row == 2 and d_row == 2 and d_file == 0:
            if self.board.piece_at(Square(o.file, o.row+1)) is None and destination_piece is None:
                return True

        return False