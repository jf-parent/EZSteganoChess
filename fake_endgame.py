from typing import List, Dict, Tuple
from random import choice, randint, shuffle, choices

import chess
from chess import Square, Board, Piece, parse_square, SQUARES

from util import render

MAX_ATTEMPT = 50
PIECE_POINTS = {
    "q": 9,
    "r": 5,
    "n": 3,
    "b": 3
}
FILES = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
FILES_IDX = {f:i for i,f in enumerate(FILES)}
IDX_FILES = {i:f for i,f in enumerate(FILES)}
RANKS = range(8)

TENTATIVE_SQUARES = {
    'N': [
        1, 2, 2, 2, 2, 2, 2, 1,
        10, 20, 25, 30, 30, 25, 20, 10,
        10, 20, 25, 30, 30, 25, 20, 10,
        10, 20, 25, 30, 30, 25, 20, 10,
        10, 20, 25, 30, 30, 25, 20, 10,
        10, 20, 25, 30, 30, 25, 20, 10,
        10, 20, 25, 30, 30, 25, 20, 10,
        5, 10, 10, 10, 10, 10, 10, 5
    ],
}

def get_pieces(config: Dict = None) -> Tuple[List[Piece], List[Piece], int, int]:
    if not config:
        config = {}

    white_pieces = []
    black_pieces = []

    # Nb pieces
    nb_white_pieces = config.get('nb_white_pieces') or randint(2, 6)
    nb_black_pieces = config.get('nb_black_pieces') or nb_white_pieces

    # Handicap
    if nb_black_pieces > 4 and nb_white_pieces > 4:
        handicap = config.get('handicap') or randint(-1, 1)

        if handicap == -1:
            nb_black_pieces -= randint(1, 3)
        elif handicap == 1:
            nb_white_pieces -= randint(1, 3)

    # Add kings
    white_pieces.append(Piece.from_symbol('K'))
    black_pieces.append(Piece.from_symbol('k'))
    nb_white_pieces -= 1
    nb_black_pieces -= 1

    # Add pawns
    nb_white_pawns = min(nb_white_pieces, randint(1, 5))
    nb_black_pawns = min(nb_black_pieces, nb_white_pawns)
    white_pieces.extend([Piece.from_symbol('P')]*nb_white_pawns)
    black_pieces.extend([Piece.from_symbol('p')]*nb_black_pawns)
    nb_white_pieces -= nb_white_pawns
    nb_black_pieces -= nb_black_pawns

    # Add minor/major pieces
    pool_pieces = ['q', 'n', 'n', 'b', 'b', 'r', 'r']
    shuffle(pool_pieces)
    white_remaining_point = 10
    while nb_white_pieces > 0 and white_remaining_point > 0:
        piece = pool_pieces.pop()
        white_remaining_point -= PIECE_POINTS[piece]
        nb_white_pieces -= 1
        white_pieces.append(Piece.from_symbol(piece.upper()))

    pool_pieces = ['q', 'n', 'n', 'b', 'b', 'r', 'r']
    shuffle(pool_pieces)
    black_remaining_point = 10
    while nb_black_pieces > 0 and black_remaining_point > 0:
        piece = pool_pieces.pop()
        black_remaining_point -= PIECE_POINTS[piece]
        nb_black_pieces -= 1
        black_pieces.append(Piece.from_symbol(piece))

    return (white_pieces, black_pieces, nb_white_pawns, nb_black_pawns)


def get_pawn_formation(nb_white_pawns: int, nb_black_pawns: int, config: Dict = None) -> str:
    if not config:
        config = {}

    formations = ['1_island']
    if nb_white_pawns > 3 or nb_black_pawns > 3:
        formations.extend([
            '1_island_doubled_pawns',
            '2_islands',
            '2_islands_doubled_pawns'
        ])

    if nb_white_pawns > 5 or nb_black_pawns > 5:
        formations.extend([
            '3_islands',
            '3_islands_doubled_pawns',
            '3_islands_tripled_pawns'
        ])

    shuffle(formations)
    return formations[0]

def pawn_placement(board, pawn_formation, nb_white_pawns, nb_black_pawns) -> Board:
    _board = board.copy()
    _nb_white_pawns = nb_white_pawns
    _nb_black_pawns = nb_black_pawns

    nb_pawns_starting_file = {
        1: FILES.copy(),
        2: ['A', 'B', 'C', 'D', 'E', 'F', 'G'],
        3: ['A', 'B', 'C', 'D', 'E', 'F'],
        4: ['A', 'B', 'C', 'D', 'E'],
        5: ['A', 'B', 'C', 'D'],
        6: ['A', 'B', 'C']
    }
    white_starting_rank = {
        1: range(1, 6),
        2: range(1, 6),
        3: range(1, 6),
        4: range(1, 5),
        5: range(1, 4),
        6: range(1, 4)
    }

    starting_files = nb_pawns_starting_file[nb_white_pawns].copy()
    shuffle(starting_files)
    file_idx = FILES_IDX[starting_files[0]]
    white_rank = choice(white_starting_rank[nb_white_pawns])
    # 1 island
    while _nb_white_pawns > 0 or _nb_black_pawns > 0:
        file_ = IDX_FILES[file_idx].lower()

        white_rank += choice(range(-2, 2))
        white_rank = max(1, min(6, white_rank))

        black_rank = white_rank + choice(range(1, 5))
        black_rank = min(6, black_rank)

        white_square = parse_square(f"{file_}{white_rank+1}")
        black_square = parse_square(f"{file_}{black_rank+1}")
        if _nb_white_pawns:
            _board.set_piece_at(white_square, Piece.from_symbol('P'))
            _nb_white_pawns -= 1

        if _nb_black_pawns:
            _board.set_piece_at(black_square, Piece.from_symbol('p'))
            _nb_black_pawns -= 1

        file_idx += 1

    return _board

def get_encoding_piece(pieces: List[Piece], piece_waterfall: List[Piece]) -> Piece:
    for p in piece_waterfall:
        if pieces.count(p) < 2:
            return p

def get_tentative_square(piece: Piece) -> Square:
    return choices(SQUARES, TENTATIVE_SQUARES.get(piece.symbol()))[0]

def piece_placement(board: Board, char_position: Square, white_pieces: List[Piece], black_pieces: List[Piece], piece_waterfall: List[Piece]) -> Board:
    _board = board.copy()
    _board.castling_rights = 0

    encoding_piece = get_encoding_piece(white_pieces, piece_waterfall)
    if attackers := _board.attackers(True, char_position):
        _board.set_piece_at(char_position, encoding_piece)
    else:
        _board.set_piece_at(char_position, encoding_piece)

    # White King
    white_king = Piece.from_symbol('K')
    for i in range(MAX_ATTEMPT):
        tentative_square = get_tentative_square(white_king)
        if not _board.piece_at(tentative_square):
            _board.set_piece_at(tentative_square, white_king)
            break
    else:
        raise Exception("MAX_ATTEMPT reached: unable to place {piece} on the board!")

    # Black King
    black_king = Piece.from_symbol('k')
    for i in range(MAX_ATTEMPT):
        tentative_square = get_tentative_square(black_king)
        if not _board.piece_at(tentative_square):
            _board.set_piece_at(tentative_square, black_king)
            if not _board.is_valid():
                _board.remove_piece_at(tentative_square)
                continue
            else:
                break
    else:
        raise Exception("MAX_ATTEMPT reached: unable to place {piece} on the board!")

    ignore_pieces = ['k', 'K', encoding_piece.symbol(), 'p', 'P']
    pieces = white_pieces + black_pieces
    while pieces:
        piece = pieces.pop()

        if piece.symbol() in ignore_pieces: continue

        for i in range(MAX_ATTEMPT):
            tentative_square = get_tentative_square(piece)
            if not _board.piece_at(tentative_square):
                _board.set_piece_at(tentative_square, piece)
                if not _board.is_valid():
                    _board.remove_piece_at(tentative_square)
                    continue
                else:
                    break
        else:
            raise Exception("MAX_ATTEMPT reached: unable to place {piece} on the board!")

    return _board


def make_fake_endgame(board: Board, char_position: Square, config: Dict = None) -> Board:
    if not config:
        config = {}

    piece_waterfall = [
        Piece.from_symbol('Q'),
        Piece.from_symbol('R'),
        Piece.from_symbol('B'),
        Piece.from_symbol('N'),
        Piece.from_symbol('K')
    ]
    white_pieces, black_pieces, nb_white_pawns, nb_black_pawns = get_pieces()

    print(f"White: {white_pieces}")
    print(f"Black: {black_pieces}")
    print(f"Nb white pawns: {nb_white_pawns}")
    print(f"Nb black pawns: {nb_black_pawns}")

    pawn_formation = get_pawn_formation(nb_white_pawns, nb_black_pawns)
    print(f"Pawn formation: {pawn_formation}")

    board.clear_board()

    _board = pawn_placement(board, 'far_1_island', nb_white_pawns, nb_black_pawns)

    _board = piece_placement(_board, char_position, white_pieces, black_pieces, piece_waterfall)

    print(render(_board))
    return _board
