from chessset import *


def is_legal(board, o, d):
    """ Does a surface check of the legality of a move, checks if a move is
    consistent with the way a piece moves and whether the """
    piece = board.piece_at(o)
    destination_piece = board.piece_at(d)
    if destination_piece is not None and destination_piece.color == piece.color:
        return False
    if piece is None:
        return
    if o == d:
        return False

    if piece.type == PieceType.ROOK:
        return rook_move_legal(board, o, d)
    elif piece.type == PieceType.PAWN:
        return pawn_move_legal(board, o, d)
    elif piece.type == PieceType.BISHOP:
        return bishop_move_legal(board, o, d)
    elif piece.type == PieceType.QUEEN:
        return queen_move_legal(board, o, d)
    elif piece.type == PieceType.KING:
        return king_move_legal(board, o, d)
    elif piece.type == PieceType.KNIGHT:
        return knight_move_legal(board, o, d)
    else:
        raise Exception


def is_diagonal_move(o, d):
    if abs(o.row - d.row) != abs(ord(o.file) - ord(d.file)):
        return False
    return True


def is_lateral_move(o, d):
    return is_file_move(o, d) or is_row_move(o, d)


def is_row_move(o, d):
    return o.file == d.file and o.row != d.row


def get_file_path(o, d):
    if ord(o.file) > ord(d.file):
        file_range = reversed(range(ord(d.file) + 1, ord(o.file) + 1))
    else:
        file_range = range(ord(o.file), ord(d.file))
    file_path = [Square(file, o.row) for file in map(chr, file_range)][1:]
    print(file_path)
    return file_path


def get_row_path(o, d):
    if o.row > d.row:
        row_range = reversed(range(d.row+1, o.row+1))
    else:
        row_range = range(o.row, d.row)
    row_path = [Square(o.file, row) for row in row_range][1:]
    print(row_path)
    return row_path


def get_diagonal_path(o, d):
    if o.row > d.row:
        row_range = reversed(range(d.row, o.row))
    else:
        row_range = range(o.row, d.row)
    if ord(o.file) > ord(d.file):
        file_range = reversed(range(ord(d.file) + 1, ord(o.file) + 1))
    else:
        file_range = range(ord(o.file), ord(d.file))

    return [Square(file, row) for file, row in zip(map(chr, file_range), row_range)][1:]


def is_file_move(o, d):
    return o.file != d.file and o.row == d.row


def rook_move_legal(board, o, d):
    if is_row_move(o, d):
        path = get_row_path(o, d)
    elif is_file_move(o, d):
        path = get_file_path(o, d)
    else:
        return False

    for square in path:
        if board.piece_at(square):
            return False
    return True


def bishop_move_legal(board, o, d):
    if not is_diagonal_move(o, d):
        return False
    for square in get_diagonal_path(o, d):
        if board.piece_at(square) is not None:
            return False
    return True


def queen_move_legal(board, o, d):
    return rook_move_legal(board, o, d) or bishop_move_legal(board, o, d)


def king_move_legal(board, o, d):
    d_row = o.row - d.row
    d_file = ord(o.file) - ord(d.file)
    destination_piece = board.piece_at(d)
    if abs(d_row) > 1 or abs(d_file) > 1:
        return False
    if destination_piece is not None and destination_piece.color == board.piece_at(o).color:
        return False
    return True


def knight_move_legal(board, o, d):
    d_row = o.row - d.row
    d_file = ord(o.file) - ord(d.file)
    if abs(d_file) == 1 and abs(d_row) == 2:
        return True
    if (abs(d_file), abs(d_row)) in [(1, 2), (2, 1)]:
        return True
    else:
        return False


def pawn_move_legal(board, o, d):
    piece = board.piece_at(o)
    if piece.color == PieceColor.WHITE:
        return white_pawn_move_legal(board, o, d)
    elif piece.color == PieceColor.BLACK:
        return black_pawn_move_legal(board, o, d)
    else:
        raise Exception("Can't run")


def black_pawn_move_legal(board, o, d):
    return True


def white_pawn_move_legal(board, o, d):
    row_diff = d.row - o.row
    file_diff = ord(d.file) - ord(o.file)
    print("file_diff = {}, row_diff = {}".format(file_diff, row_diff))
    destination_piece = board.piece_at(d)
    origin_piece = board.piece_at(o)
    en_passant_piece = board.piece_at(Square(d.file, d.row - 1))
    if row_diff == 1 and file_diff in (1, -1):
        if destination_piece is not None and destination_piece.color != origin_piece.color:
            return True
        elif destination_piece is None and en_passant_piece is not None and en_passant_piece.color == PieceColor.BLACK:
            return True
    elif row_diff == 1 and file_diff == 0:
        if destination_piece is None:
            return True
    elif o.row == 2 and row_diff == 2 and file_diff == 0:
        if board.piece_at(Square(o.file, o.row + 1)) is None and destination_piece is None:
            return True

    return False
