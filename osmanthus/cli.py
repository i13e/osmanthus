from __future__ import annotations

import argparse
import logging
import os

import chess

from osmanthus.engine import get_engine_move
# from chess import pgn


# Set up the command line argument parser
parser = argparse.ArgumentParser(
    description="Play chess against an engine in the terminal.",
)
parser.add_argument(
    "--debug", action="store_true",
    help="Enable debug logging.",
)
parser.add_argument(
    "--selfplay", action="store_true",
    help="Engine plays against itself.",
)
parser.add_argument(
    "--depth", type=int, default=3,
    help="Engine search depth. Defaults to 3.",
)
parser.add_argument(
    "--limit", type=int, default=15,
    help="Engine time limit. Defaults to 15.",
)
parser.add_argument(
    "--fen", type=str, default=chess.STARTING_FEN,
    help="Starting position in FEN notation.",
)


def main() -> int:
    """
    Parse command line arguments, initialize the game board, and enter the main
    game loop. The game loop alternates between the user and the AI making
    moves. If playing against the AI, the user can specify their desired
    difficulty level with the `depth argument`. The game ends when a checkmate
    or stalemate occurs, and the final board state and result are printed.
    """

    # Parse command line arguments
    args = parser.parse_args()

    # Set logging level based on the `--debug` flag
    logging.basicConfig(level=logging.DEBUG if args.debug else logging.ERROR)

    # Create the starting board, either from the FEN string or the default
    try:
        board = chess.Board(args.fen)
    except ValueError:
        board = chess.Board()

    # Determine whether the user is playing as white or black
    sides = {"w": chess.WHITE, "b": chess.BLACK}
    user_color = chess.WHITE if args.selfplay else None
    while user_color is None:
        user_color = sides.get(
            input("Play as [w]hite or [b]lack? ").strip().lower()[:1],
        )

    # Main game loop
    try:
        while not board.is_game_over():
            # Clear screen
            os.system("clear")

            # Display the current state of the board
            print_fancy_board(board, user_color)

            move = None
            # Get user/engine move
            if not args.selfplay and board.turn == user_color:
                while not (move := get_user_move(board)):
                    print("Illegal Move.")
            else:
                move = get_engine_move(
                    board, args.depth, args.limit, args.debug,
                )
                # print(f"{board.turn}'s move: {board.san(move)}")

            # Push the move to the board
            board.push(move)

    # Exit gracefully on C-c
    except KeyboardInterrupt:
        return 1

    # Print the final position and game result
    print_fancy_board(board, user_color)
    print(f"Result: [w] {board.result()} [b]")
    # print(pgn.Game.from_board(board))
    return 0


def print_fancy_board(board: chess.Board, user_color=chess.WHITE) -> None:
    """
    Print the current state of a chess board in a visually appealing way.
    Inspired by Sunfish.

    Args:
        board (chess.Board): The chess board to be printed.
        user_color (chess.Color, optional): The color of the player
        who is viewing the board. Defaults to chess.WHITE.

    Returns:
        None.
    """

    # Define color codes for the console output
    start_color = "\x1b[0;30;107m"
    end_color = "\x1b[0m"
    light_square_color = "\x1b[48;5;253m"
    dark_square_color = "\x1b[48;5;255m"
    highlight_color = "\x1b[48;5;153m"

    # Determine row and column ranges based on user's color preference
    rows = range(8)[::(-1)**(user_color)]
    cols = range(8)[::(-1)**(not user_color)]

    # Iterate over the rows and columns to print the board
    for row in rows:
        line = [f"{start_color} {row + 1}"]
        for col in cols:
            square = chess.square(col, row)

            # Determine the background color for the square
            if (row + col) % 2:
                bg_color = dark_square_color
            else:
                bg_color = light_square_color

            # Highlight the square if it was involved in the last move
            if board.move_stack:
                last_move = board.peek()
                if square in {last_move.from_square, last_move.to_square}:
                    bg_color = highlight_color

            # Get the piece at the current square (if any)
            if piece := board.piece_at(square):
                symbol = chess.UNICODE_PIECE_SYMBOLS[piece.symbol()]
            else:
                symbol = " "

            line.append(bg_color + symbol)

        # Print the row and add the row number label
        print(f" {' '.join(line)} {start_color} {end_color}")

    # Print the column labels at the bottom of the board
    file_names = " ".join(chess.FILE_NAMES)[::(-1)**(not user_color)]
    print(f" {start_color}   {file_names}  {end_color}\n")


def get_user_move(board: chess.Board) -> chess.Move | None:
    """
    Prompts the user to enter a move in Standard Algebraic Notation (SAN) or
    Universal Chess Interface (UCI) format, validates the input against the
    legal moves of the given chess board, and returns the corresponding move
    object.

    Args:
        board (chess.Board): The chess board to get the user's move for.

    Returns:
        chess.Move: The move object corresponding to the user's input,
        or None if the input is invalid or not a legal move.
    """

    # Choose a random legal move to suggest to the user.
    san_option = next(board.san(m) for m in board.legal_moves)
    uci_option = next(board.uci(m) for m in board.legal_moves)

    # Prompt user for input.
    uci = input(f"Your move (e.g. {san_option} or {uci_option}): ")

    # Try to parse input as SAN or UCI and check if it is a legal move.
    for parse in (board.parse_san, chess.Move.from_uci):
        try:
            if board.is_legal(move := parse(uci)):
                return move
        except ValueError:
            pass
    return None


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
