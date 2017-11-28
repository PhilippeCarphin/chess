from collections import namedtuple

Square = namedtuple('Square', ['file', 'row'])


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
    return file_path


def get_row_path(o, d):
    if o.row > d.row:
        row_range = reversed(range(d.row+1, o.row+1))
    else:
        row_range = range(o.row, d.row)
    row_path = [Square(o.file, row) for row in row_range][1:]
    return row_path


def get_diagonal_path(o, d):
    if o.row > d.row:
        row_range = reversed(range(d.row+1, o.row+1))
    else:
        row_range = range(o.row, d.row)
    if ord(o.file) > ord(d.file):
        file_range = reversed(range(ord(d.file) + 1, ord(o.file) + 1))
    else:
        file_range = range(ord(o.file), ord(d.file))

    return [Square(file, row) for file, row in zip(map(chr, file_range), row_range)][1:]


def is_file_move(o, d):
    return o.file != d.file and o.row == d.row


def distance(o, d):
    file_diff = ord(o.file) - ord(d.file)
    row_diff = o.row - d.row
    return max(abs(row_diff), abs(file_diff))


def get_lateral_path(o, d):
    if is_row_move(o, d):
        return get_row_path(o, d)
    elif is_file_move(o, d):
        return get_file_path(o, d)
    else:
        return None


def get_path(o, d):
    if is_diagonal_move(o, d):
        return get_diagonal_path(o, d)
    if is_lateral_move(o, d):
        return get_lateral_path(o, d)
    return []
