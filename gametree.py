from copy import deepcopy

from chessgame import ChessGame, GameState
from chessset import PieceColor


class Node:
    def __init__(self):
        self.children = []
        self.game = None
        self.origin_square = None
        self.destination_square = None
        self.parent = None

    def add_child(self, child):
        self.children.append(child)
        child.parent = self

    def print(self):
        print("Move : " + str(self.origin_square) + " ---> " + str(self.destination_square))


class GameTree:
    def __init__(self):
        self.root = Node()


def make_game_tree(game, depth):
    assert isinstance(game, ChessGame)
    tree = GameTree()
    tree.root.game = game
    legal_moves = tree.root.game.get_legal_moves()
    for m in legal_moves:
        new_node = Node()
        new_game = deepcopy(tree.root.game)
        new_game.play_move(m)
        new_node.game = new_game
        tree.root.children.append(new_node)


def append_legal_moves(node, color):
    for origin_square in node.game.board:
        piece = node.game.board.piece_at(origin_square)
        legal_moves = node.game.get_legal_moves(color)
        for m in legal_moves:
            child = Node()
            child.game = deepcopy(node.game)
            child.game.play_move(m[0], m[1])
            child.origin_square = m[0]
            child.destination_square = m[1]
            node.add_child(child)


def do_depth_two(original_game):
    root = Node()
    root.game = original_game
    leaves = 0
    append_legal_moves(root, PieceColor.WHITE)

    for n in root.children:
        append_legal_moves(n, PieceColor.BLACK)
        for m in n.children:
            append_legal_moves(m, PieceColor.WHITE)
            leaves += len(m.children)
            for leaf in m.children:
                if leaf.game.game_state(PieceColor.BLACK) == GameState.CHECKMATE:
                    last_node = leaf
                    black_move = leaf.parent
                    first_move = leaf.parent.parent
                    print("CHECKMATE_FOUND")
            print("Done with level 2 move (nodes = " + str(leaves))
        print("Done with level 1 move")
