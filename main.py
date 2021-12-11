#!/usr/bin/env python

from typing import AnyStr, List, Tuple, Dict

import chess
from chess import Board, parse_square, Piece

from fake_endgame import make_fake_endgame, get_encoding_piece, PIECE_WATERFALL
from util import render

UNKNOWN_CHAR = '❏'

CHARS = [
    'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j',
    'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
    'u', 'v', 'w', 'x', 'y', 'z', '1', '2', '3', '4',
    '5', '6', '7', '8', '9', '0', '.', ',', '!', '?',
    ':', '#', '@', '{', '}', '(', ')', '[', ']', '/',
    '*', ';', '$', '_', '=', '|', '/', '^', '%', '❏',
    '-', '+', ' ', '\r'
]

def create_char_map() -> Tuple[Dict[str, str], Dict[int, str]]:
    square_to_char_map = {}
    char_to_square_map = {}
    c_i = 0
    for square in chess.SQUARES:
        square_to_char_map[c_i] = CHARS[square]
        char_to_square_map[CHARS[c_i]] = square
        c_i += 1
    return char_to_square_map, square_to_char_map

def normalize(message: AnyStr) -> str:
    _message = message.lower()

    return _message

def decode(fens: List[str]) -> str:
    black_queen = Piece(chess.Piece.from_symbol('q').piece_type, False)

    decoded_chars = []

    _, square_to_char_map = create_char_map()

    for fen in fens:
        board = Board()

        board.set_fen(fen)

        pieces = []
        for piece in PIECE_WATERFALL:
            pieces.extend([piece]*len(board.pieces(piece.piece_type, piece.color)))
        encoding_piece = get_encoding_piece(pieces, PIECE_WATERFALL)

        eff_square = -1
        for square in chess.SQUARES:
            if encoding_piece == board.piece_at(square):
                eff_square = square
                break

        c = square_to_char_map.get(eff_square, UNKNOWN_CHAR)

        print(f"Character: {c}")
        print(render(board))

        decoded_chars.append(c)

    return ''.join(decoded_chars)

def encode(message: AnyStr) -> List[str]:
    encoded_message = []

    char_to_square_map, _ = create_char_map()

    normalized_message = normalize(message)

    for c in normalized_message:
        board = Board()

        board.clear_board()

        square = char_to_square_map.get(c)
        if square is None:
            square = char_to_square_map[UNKNOWN_CHAR]

        #board.set_piece_at(square, Piece.from_symbol('q'))
        board = make_fake_endgame(board, square)

        print(f"Character: {c}")
        print(render(board))
        print(board.fen())

        encoded_message.append(board.fen())

    return encoded_message


if __name__ == "__main__":
    encoded = encode("Hi Martin, would you like to have a nice cup of tea with Santas? Thanks, Jean-François")
    print(encoded)

    decoded = decode(encoded)
    print(decoded)

    # for i in range(64):
    #     board = make_fake_endgame(Board(), i)
