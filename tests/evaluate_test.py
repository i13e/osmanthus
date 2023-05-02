from __future__ import annotations

import chess

from osmanthus.evaluate import check_endgame
from osmanthus.evaluate import evaluate_board
from osmanthus.evaluate import is_favorable_move
# from pathlib import Path


def test_favorable_move() -> None:
    """
    Test the is_favorable_move function with various board states and moves.
    Ensure that the function always finds a good move. A move is "favorable"
    if it leads to a clear advantage for the current player.
    """

    # Open the positions file
    with open("tests/test_files/positions.fen", encoding="utf-8") as file:
        # Read each line (position) in the file and remove trailing whitespace
        positions = (line.strip() for line in file.readlines())

    # Test each position
    for fen in positions:
        # Create a new chess board using the FEN string
        board = chess.Board(fen)
        # Check if any of the legal moves are favorable
        assert any(
            is_favorable_move(board, move)
            for move in board.legal_moves
        )


def test_is_endgame() -> None:
    """
    Test the check_endgame function with various board states.
    Ensure that the function correctly identifies endgame states.
    """

    # Test the starting position (not an endgame)
    board = chess.Board(chess.STARTING_FEN)
    assert check_endgame(board) is False

    # Open the endgame file
    with open("tests/test_files/endgame.fen", encoding="utf-8") as file:
        # Read each line (position) in the file and remove trailing whitespace
        endgame = (line.strip() for line in file.readlines())

    # Test each endgame position
    for fen in endgame:
        # Create a new chess board using the FEN string
        board = chess.Board(fen)
        # Check if the board is in an endgame state
        assert check_endgame(chess.Board(fen)) is True


def test_evaluate_board() -> None:
    """
    Test the evaluate_board function with various board states.
    Ensure that the function correctly evaluates the board position.
    """

    # Test a position where white is down one pawn
    white_down_one_pawn = chess.Board(
        "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPP1/RNBQKBNR w KQkq - 0 1",
    )
    assert evaluate_board(white_down_one_pawn) < 0

    # Test a position where white has played e4
    white_played_e4 = chess.Board(
        "rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq - 0 1",
    )
    assert evaluate_board(white_played_e4) > 0
