from __future__ import annotations

import io
import sys

import chess

from osmanthus.cli import get_user_move
from osmanthus.cli import print_fancy_board


def test_fancy_board() -> None:
    """
    Test that all chess characters are properly rendered
    """

    board = chess.Board(chess.STARTING_FEN)
    black_pieces = "♖♘♗♕♔♙"
    white_pieces = "♜♞♝♛♚♟"
    ranks = "12345678"
    files = "abcdefgh"

    with io.StringIO() as buffer:
        # Redirect standard output to the string buffer
        sys.stdout = buffer

        # Call the function that prints the chess board
        print_fancy_board(board)

        # Get the output from the string buffer
        output = buffer.getvalue()

    # Assert that the output contains the expected emoji
    for char in black_pieces + white_pieces + ranks + files:
        assert char in output


def test_get_user_move(monkeypatch):
    """
    Unit test for the get_user_move function.

    Tests whether the function can correctly parse user input and return the
    corresponding move object, or None if the input is not a legal move.
    """

    # Set up legal and illegal moves
    all_legal_moves = chess.Board(chess.STARTING_FEN).legal_moves
    impossible_moves = ["e5", "d6", "h6", "Qf8", "Bc3"]
    board = chess.Board(chess.STARTING_FEN)

    # Test legal moves
    for move in all_legal_moves:
        # Use lambda function to simulate user input
        monkeypatch.setattr('builtins.input', lambda _: str(move))
        # Assert that returned move object matches the input
        assert get_user_move(board) == move

    # Test illegal moves
    for move in impossible_moves:
        # Use lambda function to simulate user input
        monkeypatch.setattr('builtins.input', lambda _: move)
        # Assert that returned move object is None
        assert get_user_move(board) is None
