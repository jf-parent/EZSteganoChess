#!/usr/bin/env python

from typing import AnyStr, List, Tuple, Dict

# pip install chess
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
    '*', ';', '$', '_', '=', '|', '/', '^', '%', UNKNOWN_CHAR,
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

        board = make_fake_endgame(board, square)

        print(f"Character: {c}")
        print(render(board))
        print(board.fen())

        encoded_message.append(board.fen())

    return encoded_message


if __name__ == "__main__":
    encoded = encode("Hi Bob, would you like to have a nice cup of tea with Ïgor? Thanks, Alice")
    print(encoded)

    decoded = decode(encoded)
    print(decoded)
    assert decoded == "hi bob, would you like to have a nice cup of tea with ❏gor? thanks, alice"
