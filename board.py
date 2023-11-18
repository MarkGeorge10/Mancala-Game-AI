from typing import Tuple
import copy
from actions import action
from agent import minimaxalphabeta
from transition_model.transitionmodel import STARTING_NUMBER_OF_SEEDS, PLAYER_1_SIDE, PLAYER_2_SIDE, PLAYER_1_SCORE, \
    PLAYER_2_SCORE


class Board:
    def __init__(self, other=None):

        print('''Start playing Mancala''')
        input('Press Enter to begin...')

        choice = input('If you would like to play multiplier press 1, or vs computer press 2')

        if choice == str(1):
            print('''Multiplier Game''')
            self.playerVSPlayer(self)
        elif choice == str(2):
            print('''Human vs Computer Game''')
            print('''Computer is the player 1''')
            print('''Human is the player 2''')
            print('''Please wait computer plays''')
            self.playerVSAI(self)

    @staticmethod
    def playerVSPlayer(self):

        board = self.buildBoard()

        # Mapping for how confident the algorithm is on winning the game (ballpark)
        total_pieces = sum(board[PLAYER_1_SIDE]) + sum(board[PLAYER_2_SIDE])
        winning_confidence_mapping = {
            -(total_pieces // 8): "Terrible",
            -(total_pieces // total_pieces): "Bad",
            total_pieces // 16: "Possible",
            total_pieces // 8: "Good",
            total_pieces + 1: "Certain",
        }

        # Displaying the board so the user know what they are selecting
        self.print_board(board)
        # Collecting what type the user is
        PLAYER1 = PLAYER_1_SIDE  # get_player_type()

        # Some final inits before starting the game
        PRINT_P1 = "P 1"
        PRINT_P2 = "P 2"
        PLAYER2 = PLAYER_2_SIDE
        MAX_DEPTH = 6

        # Top always goes first, feel free to change if you want to be a reble
        turn = PLAYER_1_SIDE

        # visual for what the AI did
        ai_printed_moves = []

        # While the games not over!!!
        while not ((not any(board[PLAYER_1_SIDE])) or (not any(board[PLAYER_2_SIDE]))):
            # Players move
            if turn == PLAYER1:
                # Getting the players move
                move = self.get_player_move(board, PLAYER1)

                # Updating the board
                board, go_again = action.move_piece(board, move, PLAYER1)

            # AI's move
            elif turn == PLAYER2:
                # Getting the players move
                move = self.get_player_move(board, PLAYER2)

                # Updating the board
                board, go_again = action.move_piece(board, move, PLAYER2)

            # 4. If the last piece you drop is in your own Mancala, you take another turn.
            if not go_again:
                turn = PLAYER_2_SIDE if turn == PLAYER_1_SIDE else PLAYER_1_SIDE

            # Shows the new baord
            self.clear_screen()
            if (turn == PLAYER1) and ai_printed_moves:
                [print(move) for move in ai_printed_moves]
                ai_printed_moves = []
            self.print_board(board, PRINT_P1, PRINT_P2)

        # WIN / LOSS / DRAW
        if board[f"{PLAYER1}_score"] > board[f"{PLAYER2}_score"]:
            print(
                f"Congrats! You won when the AI looks {MAX_DEPTH} moves ahead. For more of a challenge try increasing the MAX_DEPTH value."
            )
        elif board[f"{PLAYER1}_score"] < board[f"{PLAYER2}_score"]:
            print(
                f"Nice try, but the machines win this time! For an easier game try decreasing the MAX_DEPTH value."
            )
        else:
            print(f"DRAW! Are you too looking {MAX_DEPTH} moves ahead?")

    @staticmethod
    def playerVSAI(self):
        # Default board, feel free to update if you know what you're doing and want a more interesting game.
        # The code should be set up mostly generic enough to handle different boards / piece amount
        board = self.buildBoard()

        # Mapping for how confident the algorithm is on winning the game (ballpark)
        total_pieces = sum(board[PLAYER_1_SIDE]) + sum(board[PLAYER_2_SIDE])
        winning_confidence_mapping = {
            -(total_pieces // 8): "Terrible",
            -(total_pieces // total_pieces): "Bad",
            total_pieces // 16: "Possible",
            total_pieces // 8: "Good",
            total_pieces + 1: "Certain",
        }

        # Displaying the board so the user know what they are selecting
        self.print_board(board)
        # Collecting what type the user is
        PLAYER = PLAYER_2_SIDE  # get_player_type()

        # Some final inits before starting the game
        PRINT_P1 = "CPU"
        PRINT_P2 = "YOU"
        AI = PLAYER_1_SIDE
        MAX_DEPTH = 6

        # Top always goes first, feel free to change if you want to be a reble
        turn = PLAYER_1_SIDE

        # visual for what the AI did
        ai_printed_moves = []

        # While the games not over!!!
        while not ((not any(board[PLAYER_1_SIDE])) or (not any(board[PLAYER_2_SIDE]))):
            # Players move
            if turn == PLAYER:
                # Getting the players move
                move = self.get_player_move(board, PLAYER)

                # Updating the board
                board, go_again = action.move_piece(board, move, PLAYER)

            # AI's move
            elif turn == AI:
                # Getting the AI's move with the Minimax function
                best_score, move = minimaxalphabeta.minimax_mancala(board, AI, turn, MAX_DEPTH)

                # Visual aid to show of confident the minimax algorithm is in winning
                winning_confidence = ""
                for score, confidence in winning_confidence_mapping.items():
                    if score < best_score:
                        continue
                    winning_confidence = confidence
                    break
                ai_printed_moves.append(f"AI Moved : {move + 1}\tChance of Winning : {winning_confidence}")

                # Updating the board
                board, go_again = action.move_piece(board, move, AI)

            # 4. If the last piece you drop is in your own Mancala, you take another turn.
            if not go_again:
                turn = PLAYER_2_SIDE if turn == PLAYER_1_SIDE else PLAYER_1_SIDE

            # Shows the new baord
            self.clear_screen()
            if (turn == PLAYER) and ai_printed_moves:
                [print(move) for move in ai_printed_moves]
                ai_printed_moves = []
            self.print_board(board, PRINT_P1, PRINT_P2)

        # WIN / LOSS / DRAW
        if board[f"{PLAYER}_score"] > board[f"{AI}_score"]:
            print(
                f"Congrats! You won when the AI looks {MAX_DEPTH} moves ahead. For more of a challenge try increasing the MAX_DEPTH value."
            )
        elif board[f"{PLAYER}_score"] < board[f"{AI}_score"]:
            print(
                f"Nice try, but the machines win this time! For an easier game try decreasing the MAX_DEPTH value."
            )
        else:
            print(f"DRAW! Are you too looking {MAX_DEPTH} moves ahead?")

    @staticmethod
    def buildBoard():
        """Displays the game board as ASCII-art based on the board
          dictionary."""

        board = {
            PLAYER_1_SIDE: [STARTING_NUMBER_OF_SEEDS] * 6,
            PLAYER_2_SIDE: [STARTING_NUMBER_OF_SEEDS] * 6,
            PLAYER_1_SCORE: 0,
            PLAYER_2_SCORE: 0,
        }
        return board

    @staticmethod
    def print_board(board: dict, player_1: str = "P 1", player_2: str = "P 2") -> None:
        """A function to display the board

        Args:
            board (dict): Schema
            {
                "top"          : [4, 4, 4, 4, 4, 4],
                "bottom"       : [4, 4, 4, 4, 4, 4],
                "top_score"    : 0,
                "bottom_score" : 0
            }
            :param player_2:
            :param board:
            :param player_1:
        """
        print(
            f"""
       {''.join(f'{(len(board["top"]) - num):3}' for num in range(len(board['top'])))}
    +---+{'--+' * len(board['top'])}---+
    |{player_1}|{'|'.join(f'{item:2}' for item in reversed(board['top']))}|   | <- PLAYER 1
    |{board["top_score"]:3}+{'--+' * len(board['top'])}{board["bottom_score"]:3}|
    |   |{'|'.join(f'{item:2}' for item in board['bottom'])}|{player_2}| PLAYER 2 ->
    +---+{'--+' * len(board['bottom'])}---+
       {''.join(f'{(num + 1):3}' for num in range(len(board['bottom'])))}
    """
        )
        return

    @staticmethod
    def get_player_move(board: dict, turn: str) -> int:
        """A function to get the players move

        Args:
            board (dict): Schema
            {
                "top"          : [4, 4, 4, 4, 4, 4],
                "bottom"       : [4, 4, 4, 4, 4, 4],
                "top_score"    : 0,
                "bottom_score" : 0
            }
            turn (str): 'top' or 'bottom'

        Returns:
            int: a valid move of the player
        """
        while True:
            playerturn = "Player 1 turn" if turn == PLAYER_1_SIDE else "Player 2 turn"
            print(playerturn)
            player_move = input("Please Select A Move.\n:")
            if "quit" in player_move.lower():
                quit()
            try:
                player_move = int(player_move) - 1
            except ValueError:
                print("Please Make Sure To Enter A Valid Number.")
                continue

            if action.is_legal_move(board, player_move, turn):
                return player_move

            print("Sorry, That Is Not A Valid Move.")

    @staticmethod
    def clear_screen() -> None:
        """
        *NOTE*
        some terminals may not work well with this code, please feel free to try out this instead...

        # IMPORT THIS AT THE TOP OF THE FILE
        import os
        os.system('cls' if os.name == 'nt' else 'clear')
        """
        # Clearing screen to make the game visually appealing when updating
        print("\033c", end="")

    @staticmethod
    def get_player_type() -> str:
        """A function to get the players type (top goes first)

        Returns:
            str: 'top' or 'bottom'
        """
        while True:
            player_input = input(
                "Please Enter Which Player You Want To Be :\n1. Player 1\n2. Player 2\n:"
            )
            if "quit" in player_input.lower():
                quit()
            elif "1" in player_input:
                return PLAYER_1_SIDE
            elif "2" in player_input:
                return PLAYER_2_SIDE
            print("Please Make Sure You Are Entering One Of The Two Options Listed.")
