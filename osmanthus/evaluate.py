# This file implements Tomasz Michniewski's Simplified Evaluation Function
# https://www.chessprogramming.org/Simplified_Evaluation_Function
from __future__ import annotations

import chess

PIECE_VALUE = {
    chess.PAWN: 100,
    chess.KNIGHT: 320,
    chess.BISHOP: 330,
    chess.ROOK: 500,
    chess.QUEEN: 900,
    chess.KING: 20_000,
}

PST = {
    chess.PAWN: [
        0, 0, 0, 0, 0, 0, 0, 0,
        50, 50, 50, 50, 50, 50, 50, 50,
        10, 10, 20, 30, 30, 20, 10, 10,
        5, 5, 10, 25, 25, 10, 5, 5,
        0, 0, 0, 20, 20, 0, 0, 0,
        5, -5, -10, 0, 0, -10, -5, 5,
        5, 10, 10, -20, -20, 10, 10, 5,
        0, 0, 0, 0, 0, 0, 0, 0,
    ],

    chess.KNIGHT: [
        -50, -40, -30, -30, -30, -30, -40, -50,
        -40, -20, 0, 0, 0, 0, -20, -40,
        -30, 0, 10, 15, 15, 10, 0, -30,
        -30, 5, 15, 20, 20, 15, 5, -30,
        -30, 0, 15, 20, 20, 15, 0, -30,
        -30, 5, 10, 15, 15, 10, 5, -30,
        -40, -20, 0, 5, 5, 0, -20, -40,
        -50, -40, -30, -30, -30, -30, -40, -50,
    ],

    chess.BISHOP: [
        -20, -10, -10, -10, -10, -10, -10, -20,
        -10, 5, 0, 0, 0, 0, 5, -10,
        -10, 10, 10, 10, 10, 10, 10, -10,
        -10, 0, 10, 10, 10, 10, 0, -10,
        -10, 5, 5, 10, 10, 5, 5, -10,
        -10, 0, 5, 10, 10, 5, 0, -10,
        -10, 0, 0, 0, 0, 0, 0, -10,
        -20, -10, -10, -10, -10, -10, -10, -20,
    ],

    chess.ROOK: [
        0, 0, 0, 0, 0, 0, 0, 0,
        5, 10, 10, 10, 10, 10, 10, 5,
        -5, 0, 0, 0, 0, 0, 0, -5,
        -5, 0, 0, 0, 0, 0, 0, -5,
        -5, 0, 0, 0, 0, 0, 0, -5,
        -5, 0, 0, 0, 0, 0, 0, -5,
        -5, 0, 0, 0, 0, 0, 0, -5,
        0, 0, 0, 5, 5, 0, 0, 0,
    ],

    chess.QUEEN: [
        -20, -10, -10, -5, -5, -10, -10, -20,
        -10, 0, 0, 0, 0, 0, 0, -10,
        -10, 0, 5, 5, 5, 5, 0, -10,
        -5, 0, 5, 5, 5, 5, 0, -5,
        -5, 0, 5, 5, 5, 5, 0, -5,
        -10, 0, 5, 5, 5, 5, 0, -10,
        -10, 0, 0, 0, 0, 0, 0, -10,
        -20, -10, -10, -5, -5, -10, -10, -20,
    ],

    chess.KING: [
        -30, -40, -40, -50, -50, -40, -40, -30,
        -30, -40, -40, -50, -50, -40, -40, -30,
        -30, -40, -40, -50, -50, -40, -40, -30,
        -30, -40, -40, -50, -50, -40, -40, -30,
        -20, -30, -30, -40, -40, -30, -30, -20,
        -10, -20, -20, -20, -20, -20, -20, -10,
        20, 20, 0, 0, 0, 0, 20, 20,
        20, 30, 10, 0, 0, 10, 30, 20,
    ],
}

KING_ENDGAME = [
    -50, -40, -30, -20, -20, -30, -40, -50,
    -30, -20, -10, 0, 0, -10, -20, -30,
    -30, -10, 20, 30, 30, 20, -10, -30,
    -30, -10, 30, 40, 40, 30, -10, -30,
    -30, -10, 30, 40, 40, 30, -10, -30,
    -30, -10, 20, 30, 30, 20, -10, -30,
    -30, -30, 0, 0, 0, 0, -30, -30,
    -50, -30, -30, -30, -30, -30, -30, -50,
]


def is_favorable_move(board: chess.Board, move: chess.Move) -> bool:
    """
    Determines whether a move is favorable or not.

    Args:
        board (chess.Board): The current state of the chess board.
        move (chess.Move): An object representing the move to be evaluated.

    Returns:
        bool: True if the move is favorable, false otherwise.
    """

    # Check if the move is a capture move, and not an en passant move
    if board.is_capture(move) and not board.is_en_passant(move):
        to_piece_type = board.piece_type_at(move.to_square)
        from_piece_type = board.piece_type_at(move.from_square)

        # Make sure there are pieces at both the destination and source squares
        if not (to_piece_type and from_piece_type):
            raise ValueError(
                f"Pieces were expected at both {move.to_square}"
                f"and {move.from_square}",
            )

        # Is this move a good trade?
        if PIECE_VALUE[from_piece_type] < PIECE_VALUE[to_piece_type]:
            return True

        # Does the moving player have more initiative?
        attackers = board.attackers(board.turn, move.to_square)
        defenders = board.attackers(not board.turn, move.to_square)
        return len(attackers) > len(defenders)

    # Check if the move is a promotion move
    return bool(move.promotion)


def get_pst(piece: chess.Piece, square: chess.Square, endgame: bool) -> int:
    """
    Evaluates the given chess piece on the given square.

    Args:
        piece (chess.Piece): The chess piece to evaluate.
        square (chess.Square): The square on which the piece is located.
        endgame (bool): Whether the game is in the endgame or not.

    Returns:
        int: The evaluation score for the given piece on the given square.
    """

    # Get the appropriate PST mapping based on the piece and endgame status.
    if endgame and piece.piece_type == chess.KING:
        mapping = KING_ENDGAME[::(-1)**piece.color]
    else:
        mapping = PST[piece.piece_type][::(-1)**piece.color]

    # Return the evaluation score for the given piece on the given square.
    return mapping[square]


def evaluate_board(board: chess.Board) -> int:
    """
    Evaluates the current state of the chess board by assigning a numerical
    score based on the value of the pieces and their position.

    Args:
        board (chess.Board): The current state of the chess board.

    Returns:
        int: The numerical score of the board evaluation.
    """

    # Initialize the result and check if the game is in the endgame phase
    res: int = 0
    endgame: bool = check_endgame(board)

    # Evaluate each piece on the board and add its value to the result
    for square, piece in board.piece_map().items():
        val = PIECE_VALUE[piece.piece_type] + get_pst(piece, square, endgame)
        res += val * (-1)**bool(not piece.color)

    # Return the final evaluation score
    return res


def check_endgame(board: chess.Board) -> bool:
    """
    Determines if the game has reached the endgame. From Michniewski:

    "We should define where the ending begins. For me it might be either if:
        1. Both sides have no queens or
        2. Every side which has a queen has additionally no other
           pieces or one minor piece maximum."

    Args:
        board (chess.Board): The current state of the chess board.

    Returns:
        bool: True if the game has reached the endgame, False otherwise.
    """

    # Count the number of queens and minor pieces on each side
    white_queens, black_queens = 0, 0
    white_minor, black_minor = 0, 0
    for piece in board.piece_map().values():
        if piece.piece_type == chess.QUEEN:
            white_queens += piece.color == chess.WHITE
            black_queens += piece.color == chess.BLACK
        elif piece.piece_type not in {chess.PAWN, chess.KING}:
            white_minor += piece.color == chess.WHITE
            black_minor += piece.color == chess.BLACK

    # Evaluate if both sides meet the threshold to be in an end game
    white_endgame = (white_queens == 0) or (
        white_queens == 1 and white_minor <= 1
    )
    black_endgame = (black_queens == 0) or (
        black_queens == 1 and black_minor <= 1
    )
    return white_endgame and black_endgame
