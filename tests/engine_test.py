from __future__ import annotations

from pathlib import Path

import chess

from osmanthus.engine import get_engine_move


def test_mate_in_one() -> None:
    """
    This function tests if the engine can find a
    checkmate in two moves in various board states.
    """

    dir_path = Path(__file__).resolve().parent
    fen_path = dir_path / "test_files" / "mate1.fen"

    # Load FEN positions from a file
    with open(fen_path, encoding="utf-8") as file:
        mate1_puzzles = (line.strip() for line in file.readlines())

    # Iterate through each board position and test if engine can find mate-in-1
    for fen in mate1_puzzles:
        board = chess.Board(fen)
        for _ in range(1):
            # Get engine move with a maximum search depth of 2 ply
            board.push(get_engine_move(board, 2))

        # Check if engine move resulted in a checkmate
        assert board.is_checkmate()


def test_mate_in_two() -> None:
    """
    This function tests if the engine can find a
    checkmate in two moves in various board states.
    """

    dir_path = Path(__file__).resolve().parent
    fen_path = dir_path / "test_files" / "mate2.fen"

    # Load FEN positions from a file
    with open(fen_path, encoding="utf-8") as file:
        mate2_puzzles = (line.strip() for line in file.readlines())

    # Iterate through each board position and test if engine can find mate-in-2
    for fen in mate2_puzzles:
        board = chess.Board(fen)
        for _ in range(3):
            # Get engine move with a maximum search depth of 3 ply
            board.push(get_engine_move(board, 3))

        # Check if engine move resulted in a checkmate
        assert board.is_checkmate()


def test_mate_in_three() -> None:
    """
    This function tests if the engine can find a
    checkmate in two moves in various board states.
    """

    # Test a specific board state
    # https://lichess.org/training/yFfBn
    # 1. Rxf8+ Rxf8 2. Qg8+ Rxg8 3. Nf7#
    board = chess.Board("r4q1k/1b4bp/4Q2N/p7/Pp6/3P4/1PP1p1PP/5RK1 w - - 0 29")

    # Get engine move with a maximum search depth of 4 ply
    assert get_engine_move(board, 4).uci() == "f1f8"

    # Test 2: disabled, as there are no mate-in-3 puzzles (yet)
    # with open("tests/test_files/mate3.fen") as f:
    #     mate3_puzzles = (line.strip() for line in f.readlines())
    #
    # for fen in mate3_puzzles:
    #     board = chess.Board(fen)
    #     # Try the first three returned engine moves
    #     for _ in range(3):
    #         board.push(get_engine_move(board, 3))
    #     assert board.is_checkmate()


# The following tests are commented out, as they are currently not in use.

# def test_stalemate() -> None:
#     """
#     This function tests if get_engine_move returns None when there
#     are no legal moves that can be made and the game is a stalemate.
#     """
#
#     # Stalemate puzzle
#     board = chess.Board("8/7k/8/5Q2/8/8/6K1/8 w - - 0 1")
#     move = get_engine_move(3, board)
#     assert move is None
#
# def test_no_legal_moves() -> None:
#     """
#     This function tests if get_engine_move returns None when there
#     are no legal moves that can be made.
#     """
#
#     # Test when there are no legal moves for the current player
#     board = chess.Board("8/8/8/8/8/1k6/8/K7 w - - 0 1")
#     move = get_engine_move(3, board)
#     assert move is None
#
# def test_promotion() -> None:
#     # Test a promotion move
#     board = chess.Board("7k/8/8/5P2/8/8/8/7K w - - 0 1")
#     move = get_engine_move(3, board)
#     assert move.uci() == "f7f8q"
