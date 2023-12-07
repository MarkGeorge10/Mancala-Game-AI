from typing import Tuple
import copy
from actions.action import Action
from transition_model.transitionmodel import STARTING_NUMBER_OF_SEEDS, PLAYER_1_SIDE, PLAYER_2_SIDE, PLAYER_1_SCORE, \
    PLAYER_2_SCORE
from agent.minimaxPruningAgent import MinimaxPruningAgent
from agent.qLearning import QlearningRL
import os


class Board:

    def __init__(self, reinforcementLearning=False, other=None):
        self.loaded_agent = QlearningRL(load_agent_path=None)
        self.action = Action(qlearningAgent=self.loaded_agent)
        self.model_save_path = 'mancala_agent.pkl'
        if reinforcementLearning:
            n_games = 10000
            games_per_checkpoint = 2500
            while n_games > 0:
                self.RLVsRL()
                # Checkpoint
                if n_games % games_per_checkpoint == 0:
                    self.loaded_agent.save_agent(self.model_save_path)
                    print('Saved RL Agent Model!')
                    print('Remaining Games: ', n_games)
                n_games -= 1
                # Save final agent model
            self.loaded_agent.save_agent(self.model_save_path)
        else:


            choice = input(
                'If you would like to play multiplier press 1, or vs computer with Minimax pruning Algorithm press 2, or  play with reinforecement computer press 3')

            if choice == str(1):
                print('''Multiplier Game''')
                self.playerVSPlayer()
            elif choice == str(2):
                print('''Human vs Computer Game''')
                print('''Computer is the player 1''')
                print('''Human is the player 2''')
                self.playerVSAI()
            elif choice == str(3):  # reinforcement_learning == True:

                base_cwd = os.getcwd()
                model_dir = base_cwd
                if not os.path.exists(model_dir):
                    os.mkdir(model_dir)
                model_path = "mancala_agent.pkl"

                self.loaded_agent = QlearningRL(load_agent_path=model_path)
                self.PlayerVSRL()

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
        self.printBoard(board)
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
                move = self.action.getMove(board, PLAYER1)

                # Updating the board
                board, go_again = self.action.move_piece(board, move, PLAYER1)

            # AI's move
            elif turn == PLAYER2:
                # Getting the players move
                move = self.action.getMove(board, PLAYER2)

                # Updating the board
                board, go_again = self.action.move_piece(board, move, PLAYER2)

            # 4. If the last piece you drop is in your own Mancala, you take another turn.
            if not go_again:
                turn = PLAYER_2_SIDE if turn == PLAYER_1_SIDE else PLAYER_1_SIDE

            # Shows the new baord
            self.clearScreen()
            if (turn == PLAYER1) and ai_printed_moves:
                [print(move) for move in ai_printed_moves]
                ai_printed_moves = []
            self.printBoard(board, PRINT_P1, PRINT_P2)

        # WIN / LOSS / DRAW
        if board[f"{PLAYER1}_score"] > board[f"{PLAYER2}_score"]:
            print(
                f"Congrats! player 1 is the winner."
            )
        elif board[f"{PLAYER1}_score"] < board[f"{PLAYER2}_score"]:
            print(
                f"Congrats! player 2 is the winner."
            )
        else:
            print(f"DRAW! Are you too looking {MAX_DEPTH} moves ahead?")

    def playerVSAI(self):
        # Default board, feel free to update if you know what you're doing and want a more interesting game.
        # The code should be set up mostly generic enough to handle different boards / piece amount

        # difficulty_level = input('Please, select the difficulty level from 1 (very easy) to 6 (very hard): ')
        # if not difficulty_level.isdigit():
        #     difficulty_level = 6

        board = self.buildBoard()

        agent = MinimaxPruningAgent()

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
        self.printBoard(board)
        # Collecting what type the user is
        PLAYER = PLAYER_2_SIDE  # get_player_type()

        # Some final inits before starting the game
        PRINT_P1 = "CPU"
        PRINT_P2 = "YOU"
        AI = PLAYER_1_SIDE
        MAX_DEPTH = 6
        # MAX_DEPTH = int(difficulty_level) if 0 < int(difficulty_level) < 7 else 6
        # print(MAX_DEPTH)

        # Top always goes first, feel free to change if you want to be a reble
        turn = PLAYER_1_SIDE

        # visual for what the AI did
        ai_printed_moves = []

        # While the games not over!!!
        while not ((not any(board[PLAYER_1_SIDE])) or (not any(board[PLAYER_2_SIDE]))):
            # Players move
            if turn == PLAYER:
                # Getting the players move
                move = self.action.getMove(board, PLAYER)

                # Updating the board
                board, go_again = self.action.move_piece(board, move, PLAYER)

            # AI's move
            elif turn == AI:
                # Getting the AI's move with the Minimax function
                best_score, move = agent.minimaxPruning(board, AI, turn, MAX_DEPTH)

                # Visual aid to show of confident the minimax algorithm is in winning
                winning_confidence = ""
                for score, confidence in winning_confidence_mapping.items():
                    if score < best_score:
                        continue
                    winning_confidence = confidence
                    break
                ai_printed_moves.append(f"AI Moved : {move + 1}\tChance of Winning : {winning_confidence}")

                # Updating the board
                board, go_again = self.action.move_piece(board, move, AI)

            # 4. If the last piece you drop is in your own Mancala, you take another turn.
            if not go_again:
                turn = PLAYER_2_SIDE if turn == PLAYER_1_SIDE else PLAYER_1_SIDE

            # Shows the new baord
            self.clearScreen()
            if (turn == PLAYER) and ai_printed_moves:
                [print(move) for move in ai_printed_moves]
                ai_printed_moves = []
            self.printBoard(board, PRINT_P1, PRINT_P2)

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

    def RLVsRL(self):

        board = self.buildBoard()

        # Displaying the board so the user know what they are selecting
        self.printBoard(board)

        # Collecting what type the user is
        AI1 = PLAYER_1_SIDE  # get_player_type()
        AI2 = PLAYER_2_SIDE

        self.loaded_agent.previous_state = self.get_state(board, player=AI1)

        # Some final inits before starting the game
        PRINT_P1 = "CPU1"
        PRINT_P2 = "CPU2"

        # Top always goes first, feel free to change if you want to be a reble
        turn = AI1

        # visual for what the AI did
        ai_printed_moves = []

        # While the games not over!!!
        while not ((not any(board[PLAYER_1_SIDE])) or (not any(board[PLAYER_2_SIDE]))):
            # Players move
            if turn == AI1:

                move = self.action.getMoveRL(self.get_state(board, player=AI1), board, AI1)

                self.loaded_agent.update_q(self.get_state(board, player=AI1), board[PLAYER_1_SCORE])
                board, go_again = self.action.move_piece(board, move, AI1)

            # AI's move
            elif turn == AI2:
                # Getting the AI's move with the q learning
                move = self.action.getMoveRL(self.get_state(board, player=AI2), board, AI2)
                self.loaded_agent.update_q(self.get_state(board, player=AI2), board[PLAYER_2_SCORE])

                # Updating the board
                board, go_again = self.action.move_piece(board, move, AI2)

            # 4. If the last piece you drop is in your own Mancala, you take another turn.
            if not go_again:
                turn = PLAYER_2_SIDE if turn == PLAYER_1_SIDE else PLAYER_1_SIDE

            # Shows the new baord
            self.clearScreen()
            if (turn == AI1) and ai_printed_moves:
                [print(move) for move in ai_printed_moves]
                ai_printed_moves = []
            self.printBoard(board, PRINT_P1, PRINT_P2)

        # WIN / LOSS / DRAW
        if board[f"{AI1}_score"] > board[f"{AI2}_score"]:
            print(
                f"Congrats! {AI1} won "
            )
        elif board[f"{AI1}_score"] < board[f"{AI2}_score"]:
            print(
                f"Congrats! {AI2} won "
            )
        else:
            print(f"DRAW!")

    def PlayerVSRL(self):

        board = self.buildBoard()

        self.printBoard(board)

        # Collecting what type the user is
        PLAYER = PLAYER_1_SIDE  # get_player_type()
        AIRL = PLAYER_2_SIDE

        self.loaded_agent.previous_state = self.get_state(board, player=AIRL)

        # Some final inits before starting the game
        PRINT_P1 = "P 1"
        PRINT_P2 = "CPU"

        # Top always goes first, feel free to change if you want to be a reble
        turn = PLAYER

        # visual for what the AI did
        ai_printed_moves = []

        # While the games not over!!!
        while not ((not any(board[PLAYER_1_SIDE])) or (not any(board[PLAYER_2_SIDE]))):
            # Players move
            if turn == PLAYER:
                # Getting the players move
                move = self.action.getMove(board, PLAYER)

                # Updating the board
                board, go_again = self.action.move_piece(board, move, PLAYER)

            # AI's move
            elif turn == AIRL:

                # Getting the AI's move with the q learning
                move = self.action.getMoveRL(self.get_state(board, player=AIRL), board, AIRL)
                self.loaded_agent.update_q(self.get_state(board, player=AIRL), board[PLAYER_2_SCORE])

                print('Machine choose pocket ', move+1)
                # Updating the board
                board, go_again = self.action.move_piece(board, move, AIRL)

            # 4. If the last piece you drop is in your own Mancala, you take another turn.
            if not go_again:
                turn = PLAYER_2_SIDE if turn == PLAYER_1_SIDE else PLAYER_1_SIDE

            # Shows the new baord
            self.clearScreen()
            if (turn == PLAYER) and ai_printed_moves:
                [print(move) for move in ai_printed_moves]
                ai_printed_moves = []
            self.printBoard(board, PRINT_P1, PRINT_P2)

        # WIN / LOSS / DRAW
        if board[f"{PLAYER}_score"] > board[f"{AIRL}_score"]:
            print(
                f"Congrats! You are the winner and beat Reinforcement learning computer."
            )
        elif board[f"{PLAYER}_score"] < board[f"{AIRL}_score"]:
            print(
                f"Nice try, but the machines win this time."
            )
        else:
            print(f"DRAW!")
        self.loaded_agent.save_agent(self.model_save_path)

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
    def printBoard(board: dict, player_1: str = "P 1", player_2: str = "P 2") -> None:
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
    def clearScreen() -> None:
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
    def get_state(board, player):
        """ Returns the unique numeric state of the board for each player from
            the players own perspective. Mancala pockets not necessary but they
            can act as the reward to the computer at the end of the game.
        """
        # Flip the board interpretation if player 2
        if player == "top":
            relevant_pockets = board["top"] + board["bottom"]
        else:
            relevant_pockets = board["bottom"] + board["top"]

        print(relevant_pockets)

        return relevant_pockets
