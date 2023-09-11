# flake8: noqa
from __future__ import annotations

import sys
import time
from collections import defaultdict
from pathlib import Path

import chess
from chess import polyglot

from osmanthus.evaluate import evaluate_board
from osmanthus.evaluate import is_favorable_move
# from functools import cache
# from osmanthus.evaluate import check_endgame


# chess.Board.__hash__ = chess.polyglot.zobrist_hash

DEBUG_INFO: dict[str, float] = {}
TIMEOUT_SECONDS: int
QUIESCENCE_SEARCH_DEPTH: int = 20

best_move: chess.Move
global_best_move: chess.Move
DEPTH = 0
IS_TIMEOUT = False
move_scores: dict = defaultdict(dict)
start_time: float


def get_engine_move(board: chess.Board, depth=3, limit=15, debug=False) -> chess.Move:
    """
    Given the current state of the board, returns the best move for the engine.

    Args:
        board (chess.Board): The current state of the chess board.
        depth (int, optional): The maximum depth to search the game tree.
        limit (int, optional): The maximum time to search the game tree.
        debug (bool, optional): If set to True, prints debug information.

    Returns:
        chess.Move: The best move for the current player.
    """

    global start_time
    global TIMEOUT_SECONDS

    TIMEOUT_SECONDS = max(1, limit)

    # Clear debug info and set up a timer
    DEBUG_INFO["nodes"] = 0
    start_time = time.time()

    # Call the minimax algorithm to get the best move
    if not (move := get_opening_database_moves(board)):
        move = iterative_deepening(board, max(1, depth), debug)

    # Calculate the time taken and print debug info if requested
    DEBUG_INFO["time"] = time.time() - start_time
    if debug:  # pragma: no cover
        print(f"debug info: {DEBUG_INFO}")
    return move


def get_opening_database_moves(board: chess.Board) -> chess.Move | None:
    """
    Get a move from the opening book using Polyglot library.

    Args:
        board (chess.Board): The current state of the chess board.

    Returns:
        chess.Move | None: A move from the opening book, if available.
    """

    dir_path = Path(__file__).resolve().parent
    book_path = dir_path / "performance.bin"

    # Open the opening book file with Polyglot
    with polyglot.open_reader(book_path) as reader:
        try:
            # Get a random move from the opening book
            return reader.weighted_choice(board).move
        except IndexError:
            # Return None if no moves are available in the opening book
            return None


def iterative_deepening(board: chess.Board, depth: int, debug: bool) -> chess.Move:
    """
    This function performs an iterative deepening search on the given chess
    board using the minimax algorithm.

    Args:
        board (chess.Board): The current state of the chess board.
        depth (int): The maximum depth to search to.
        debug (bool): If True, print debug information during the search.

    Returns:
        chess.Move: The best move found after the search.
    """

    # Initialize global variables
    global DEPTH
    global IS_TIMEOUT
    global global_best_move

    IS_TIMEOUT = False
    current_score = 0

    # Loop through depths from 0 up to the maximum depth
    for DEPTH in range(depth + 1):

        # Exit loop if timeout or maximum score has been reached
        if IS_TIMEOUT or current_score in {-sys.maxsize, sys.maxsize}:
            break

        # Run minimax algorithm with the current depth
        current_score = minimax(board, -sys.maxsize, sys.maxsize, DEPTH)

        # Update best move if a new one is found
        if DEPTH and not IS_TIMEOUT:
            global_best_move = best_move

            # Print debug information if requested
            if debug:  # pragma: no cover
                print(
                    f"Completed search with depth {DEPTH}. "
                    f"Best move so far: {board.san(global_best_move)} "
                    f"(Score: {current_score})",
                )

    return global_best_move

# @cache


def minimax(board: chess.Board, alpha: int, beta: int, depth: int) -> int:
    """
    Compute the best move using the minimax algorithm with alpha-beta pruning.

    Args:
        board (chess.Board): The current chess board state.
        alpha (int): The alpha value for alpha-beta pruning.
        beta (int): The beta value for alpha-beta pruning.
        depth (int): The maximum depth to search to.

    Returns:
        int: The best move score found.
    """

    global best_move
    global IS_TIMEOUT

    DEBUG_INFO["nodes"] += 1

    # Check if the time limit has been reached
    if time.time() - start_time > TIMEOUT_SECONDS:
        IS_TIMEOUT = True
        return alpha if board.turn else beta

    # Check for checkmate or stalemate
    if board.is_game_over():
        return sys.maxsize * (-1)**board.turn * (not board.is_stalemate())

    # Apply quiescence search if the maximum depth is reached
    if depth < 1:
        return quiescence_search(board, alpha, beta, 1)

    # Initialize the score based on the current player's color
    score = alpha if board.turn else beta

    # Get the scores for each legal move for the current board position
    board_scores = move_scores.get(board.fen(), {})

    # Sort the legal moves based on the scores
    moves = sorted(
        board.legal_moves, key=lambda move: board_scores.get(move, 0) *
        (-1)**board.turn,
    )

    # Loop through each legal move and update the score if necessary
    for move in moves:
        board.push(move)

        # Recursively call minimax for the next depth
        if board.turn:
            move_score = minimax(board, alpha, score, depth - 1)
        else:
            move_score = minimax(board, score, beta, depth - 1)

        # Update the move_scores dictionary with the new move score
        move_scores[board.fen()][move] = move_score
        board.pop()

        # Update the score and best_move if necessary, and perform alpha-beta pruning
        if (board.turn and move_score > score) or ((not board.turn) and move_score < score):
            score = move_score
            if depth == DEPTH:
                best_move = move
            if (board.turn and score >= beta) or ((not board.turn) and score <= alpha):
                break

    return score


# @cache
def quiescence_search(board: chess.Board, alpha: int, beta: int, depth: int) -> int:
    """
    Quiescence Search algorithm used for alpha-beta pruning of chess board.

    Args:
        board (chess.Board): current chess board state
        alpha (int): best score of maximizer
        beta (int): best score of minimizer
        depth (int): current depth in search tree

    Returns:
        int: evaluated score of the current chess board
    """

    # increment node counter for debugging purposes
    DEBUG_INFO["nodes"] += 1

    # if maximum depth is reached or no favorable moves available, return evaluated score
    if depth == QUIESCENCE_SEARCH_DEPTH or not board.legal_moves:
        return evaluate_board(board)

    # determine favorable moves
    favorable_moves = [
        move for move in board.legal_moves if is_favorable_move(board, move)
    ]

    # if no favorable moves available, return evaluated score
    if not favorable_moves:
        return evaluate_board(board)

    # initialize score based on which player's turn it is
    score = alpha if board.turn else beta

    # loop through favorable moves
    for move in favorable_moves:
        # make the move and recursively evaluate the resulting board
        board.push(move)
        if board.turn:
            move_score = quiescence_search(board, alpha, score, depth + 1)
        else:
            move_score = quiescence_search(board, score, beta, depth + 1)
        board.pop()

        # update best score and alpha/beta values
        score = max(score, move_score) if board.turn else min(
            score, move_score,
        )

        if (board.turn and score >= beta) or ((not board.turn) and score <= alpha):
            break

    return score
