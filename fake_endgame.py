from typing import List, Dict, Tuple
from random import choice, randint, shuffle

from chess import Square, Board, Piece

PIECE_POINTS = {
    "q": 9,
    "r": 5,
    "n": 3,
    "b": 3
}

def get_pieces(config: Dict = None) -> Tuple[List[Piece], List[Piece], int, int]:
    if not config:
        config = {}

    white_pieces = []
    black_pieces = []

    # Nb pieces
    nb_white_pieces = config.get('nb_white_pieces') or randint(2, 8)
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
    nb_white_pawns = min(nb_white_pieces, randint(1, 7))
    nb_black_pawns = min(nb_black_pieces, nb_white_pawns)
    white_pieces.extend([Piece.from_symbol('P')]*nb_white_pawns)
    black_pieces.extend([Piece.from_symbol('p')]*nb_black_pawns)
    nb_white_pieces -= nb_white_pawns
    nb_black_pieces -= nb_black_pawns

    # Add minor/major pieces
    pool_pieces = ['q', 'n', 'r', 'b']
    shuffle(pool_pieces)
    white_remaining_point = 10
    while nb_white_pieces > 0 and white_remaining_point > 0:
        piece = pool_pieces.pop()
        white_remaining_point -= PIECE_POINTS[piece]
        nb_white_pieces -= 1
        white_pieces.append(Piece.from_symbol(piece.upper()))

    pool_pieces = ['q', 'n', 'r', 'b']
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

    formations = ['entangled_1_island', 'far_1_island']
    if nb_white_pawns > 3 or nb_black_pawns > 3:
        formations.extend([
            'entangled_2_islands',
            'far_2_islands',
            'mixed_2_islands',
            'entangled_1_island_doubled_pawns',
            'far_1_islaned_doubled_pawns',
            'entangled_2_islands_doubled_pawns',
            'far_2_islands_doubled_pawns',
            'mixed_2_islands_doubled_pawns'
        ])

    if nb_white_pawns > 5 or nb_black_pawns > 5:
        formations.extend([
            'entangled_3_islands',
            'far_3_islands',
            'mixed_3_islands',
            'entangled_3_islands_doubled_pawns',
            'far_3_islands_doubled_pawns',
            'mixed_3_islands_doubled_pawns',
            'entangled_3_islands_tripled_pawns',
            'far_3_islands_tripled_pawns',
            'mixed_3_islands_tripled_pawns'
        ])

    shuffle(formations)
    return formations[0]


def make_fake_endgame(char_position: Square, config: Dict = None) -> Board:
    if not config:
        config = {}

    white_pieces, black_pieces, nb_white_pawns, nb_black_pawns = get_pieces()
    print(f"White: {white_pieces}")
    print(f"Black: {black_pieces}")
    print(f"Nb white pawns: {nb_white_pawns}")
    print(f"Nb black pawns: {nb_black_pawns}")

    pawn_formation = get_pawn_formation(nb_white_pawns, nb_black_pawns)
    print(f"Pawn formation: {pawn_formation}")
