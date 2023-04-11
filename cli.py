import chess
import argparse
import logging
from engine import get_engine_move


# Set up the command line argument parser
parser = argparse.ArgumentParser(description="Play chess against an engine in the terminal.")
parser.add_argument("--debug", action="store_true", help="Enable debug logging.")
parser.add_argument("--selfplay", action="store_true", help="Engine plays against itself.")
parser.add_argument("--depth", type=int, default=3, help="Engine search depth. Defaults to 3")
parser.add_argument("--fen", type=str, default="", help="Starting position in FEN notation.")


def main() -> None:
    """
    Parse command line arguments, initialize the game board, and enter the main
    game loop. The game loop alternates between the user and the AI making moves.
    If playing against the AI, the user can specify their desired difficulty level
    with the `depth argument`. The game ends when a checkmate or stalemate occurs,
    and the final board state and result are printed.
    """

    # Parse command line arguments
    args = parser.parse_args()

    # Set logging level based on the `--debug` flag
    logging.basicConfig(level=logging.DEBUG if args.debug else logging.ERROR)

    # Determine whether the user is playing as white or black
    sides = {"w": chess.WHITE, "b": chess.BLACK}
    user_color = chess.WHITE if args.selfplay else None
    while user_color is None:
        user_color = sides.get(input("Play as [w]hite or [b]lack? ").strip().lower()[:1])

    # Create the starting board, either from the FEN string or the default
    try:
        board = chess.Board(args.fen)
    except ValueError:
        board = chess.Board()

    # Main game loop
    while not board.is_game_over():
        # Display the current state of the board
        print_fancy_board(board, user_color)

        # Determine the next move, either from user input or engine calculation
        if not args.selfplay and board.turn == user_color:
            while not (move := get_user_move(board)):
                print("Illegal Move.")
        else:
            move = get_engine_move(max(1, args.depth), board, debug=args.debug)
            print(f" My move: {board.san(move)}")

        # Push the move to the board
        board.push(move)

    # Print the final state of the board and the result of the game
    print_fancy_board(board, user_color)
    print(f"Result: [w] {board.result()} [b]")


def print_fancy_board(board: chess.Board, user_color=chess.WHITE) -> None:
    """
    Print the current state of a chess board in a visually appealing way,
    Inspired by Sunfish.

    Args:
        board (chess.Board): The chess board to be printed.
        user_color (chess.Color, optional): The color of the player who is
        viewing the board. Defaults to chess.WHITE.

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
    ROWS = range(8) if user_color == chess.BLACK else range(8)[::-1]
    COLS = range(8) if user_color == chess.WHITE else range(8)[::-1]


    # Iterate over the rows and columns to print the board
    for r in ROWS:
        line = [f"{start_color} {r+1}"]
        for c in COLS:
            # Determine the background color for the square
            if (r + c) % 2:
                bg_color = dark_square_color
            else:
                bg_color = light_square_color

            # Highlight the square if it was involved in the last move
            if board.move_stack:
                last_move = board.peek()
                if 8 * r + c in {last_move.from_square, last_move.to_square}:
                    bg_color = highlight_color

            # Get the piece at the current square (if any)
            piece = board.piece_at(8 * r + c)
            symbol = chess.UNICODE_PIECE_SYMBOLS[piece.symbol()] if piece else " "
            line.append(bg_color + symbol)

        # Print the row and add the row number label
        print(f" {' '.join(line)} {start_color} {end_color}")

    # Print the column labels at the bottom of the board
    if user_color == chess.WHITE:
        print(f" {start_color}   a b c d e f g h  {end_color}\n")
    else:
        print(f" {start_color}   h g f e d c b a  {end_color}\n")


def get_user_move(board: chess.Board):
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
    san_option = next(iter(board.san(m) for m in board.legal_moves))
    uci_option = next(iter(m.uci() for m in board.legal_moves))

    # Prompt user for input.
    uci = input(f"Your move (e.g. {san_option} or {uci_option}): ")

    # Try to parse input as SAN or UCI format and check if it is a legal move.
    for parse in (board.parse_san, chess.Move.from_uci):
        try:
            if (move := parse(uci)) in board.legal_moves:
                return move
        except ValueError:
            pass


if __name__ == "__main__":
    try:
        main()
    # Exit gracefully on C-c
    except KeyboardInterrupt:
        pass
