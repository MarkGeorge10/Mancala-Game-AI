from typing import Tuple
import copy
from actions.action import move_piece,getMove
from transition_model.transitionmodel import STARTING_NUMBER_OF_SEEDS, PLAYER_1_SIDE, PLAYER_2_SIDE, PLAYER_1_SCORE, \
    PLAYER_2_SCORE
from agent.minimaxPruningAgent import MinimaxPruningAgent
from agent.qLearning import QlearningRL
import os


class Board:

    def __init__(self, reinforcementLearning=False, other=None):

        if reinforcementLearning:
            self.loaded_agent = QlearningRL(load_agent_path=None)
            self.RLVSRL()
        else:
            print('''Start playing Mancala''')
            input('Press Enter to begin...')

            choice = input(
                'If you would like to play multiplier press 1, or vs computer press 2, or press 3 to play with learner computer')

            if choice == str(1):
                print('''Multiplier Game''')
                self.playerVSPlayer(self)
            elif choice == str(2):
                print('''Human vs Computer Game''')
                print('''Computer is the player 1''')
                print('''Human is the player 2''')
                self.playerVSAI(self)
            elif choice == str(3):  # reinforcement_learning == True:

                base_cwd = os.getcwd()
                model_dir = base_cwd + "\\model"
                if not os.path.exists(model_dir):
                    os.mkdir(model_dir)
                model_path = "\\mancala_agent.pkl"

                self.loaded_agent = QlearningRL(load_agent_path=model_path)
                self.PlayerVSRL()

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
                move = getMove(board, PLAYER1)

                # Updating the board
                board, go_again = move_piece(board, move, PLAYER1)

            # AI's move
            elif turn == PLAYER2:
                # Getting the players move
                move = getMove(board, PLAYER2)

                # Updating the board
                board, go_again = move_piece(board, move, PLAYER2)

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

    def RLVSRL(self):
        # Default board, feel free to update if you know what you're doing and want a more interesting game.
        # The code should be set up mostly generic enough to handle different boards / piece amount

        # difficulty_level = input('Please, select the difficulty level from 1 (very easy) to 6 (very hard): ')
        # if not difficulty_level.isdigit():
        #     difficulty_level = 6

        board = self.buildBoard()
        agent = MinimaxPruningAgent()

        # Mapping for how confident the algorithm is on winning the game (ballpark)
        # total_pieces = sum(board[PLAYER_1_SIDE]) + sum(board[PLAYER_2_SIDE])
        # winning_confidence_mapping = {
        #     -(total_pieces // 8): "Terrible",
        #     -(total_pieces // total_pieces): "Bad",
        #     total_pieces // 16: "Possible",
        #     total_pieces // 8: "Good",
        #     total_pieces + 1: "Certain",
        # }

        # Displaying the board so the user know what they are selecting
        self.printBoard(board)

        # Collecting what type the user is
        AI1 = PLAYER_1_SIDE  # get_player_type()
        AI2 = PLAYER_2_SIDE
        MAX_DEPTH = 6
        # MAX_DEPTH = int(difficulty_level) if 0 < int(difficulty_level) < 7 else 6
        # print(MAX_DEPTH)

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
                # Getting the AI's move with the Minimax function
                # best_score, move = agent.minimaxPruning(board, AI1, turn, 6)
                #
                # # Visual aid to show of confident the minimax algorithm is in winning
                # winning_confidence = ""
                # for score, confidence in winning_confidence_mapping.items():
                #     if score < best_score:
                #         continue
                #     winning_confidence = confidence
                #     break
                # ai_printed_moves.append(f"AI Moved : {move + 1}\tChance of Winning : {winning_confidence}")
                #
                # # Updating the board
                # board, go_again = action.move_piece(board, move, AI1)

                #move = self.loaded_agent.take_action(self.get_state(board, player=AI1), board, AI1)

                move = self.loaded_agent.getMoveAIV2(self.get_state(board, player=AI1), board, AI1)

                self.loaded_agent.update_q(self.get_state(board, player=AI1), board[PLAYER_1_SCORE])
                board, go_again = move_piece(board, move, AI1)

            # AI's move
            elif turn == AI2:
                # Getting the AI's move with the q learning
                move = self.loaded_agent.getMoveAIV2(self.get_state(board, player=AI2), board, AI2)
                self.loaded_agent.update_q(self.get_state(board, player=AI2),  board[PLAYER_2_SCORE])

                # Updating the board
                board, go_again = move_piece(board, move, AI2)

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
                f"Congrats! You won when the AI looks {MAX_DEPTH} moves ahead. For more of a challenge try increasing the MAX_DEPTH value."
            )
        elif board[f"{AI1}_score"] < board[f"{AI2}_score"]:
            print(
                f"Nice try, but the machines win this time! For an easier game try decreasing the MAX_DEPTH value."
            )
        else:
            print(f"DRAW! Are you too looking {MAX_DEPTH} moves ahead?")

    def AIVSRL(self):

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
        AI1 = PLAYER_1_SIDE  # get_player_type()
        AI2 = PLAYER_2_SIDE
        MAX_DEPTH = 6

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
                # Getting the AI's move with the Minimax function
                best_score, move = agent.minimaxPruning(board, AI1, turn, 6)

                # Visual aid to show of confident the minimax algorithm is in winning
                winning_confidence = ""
                for score, confidence in winning_confidence_mapping.items():
                    if score < best_score:
                        continue
                    winning_confidence = confidence
                    break
                ai_printed_moves.append(f"AI Moved : {move + 1}\tChance of Winning : {winning_confidence}")

                # Updating the board
                board, go_again = move_piece(board, move, AI1)

            # AI's move
            elif turn == AI2:
                # Getting the AI's move with the q learning
                move = self.loaded_agent.take_action(board[AI2])

                self.loaded_agent.update_q(self.get_state(board, player=AI2), board[PLAYER_2_SCORE])

                # Updating the board
                board, go_again = move_piece(board, move, AI2)

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
                f"Congrats! You won when the AI looks {MAX_DEPTH} moves ahead. For more of a challenge try increasing the MAX_DEPTH value."
            )
        elif board[f"{AI1}_score"] < board[f"{AI2}_score"]:
            print(
                f"Nice try, but the machines win this time! For an easier game try decreasing the MAX_DEPTH value."
            )
        else:
            print(f"DRAW! Are you too looking {MAX_DEPTH} moves ahead?")

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
                move = getMove(board, PLAYER)

                # Updating the board
                board, go_again = move_piece(board, move, PLAYER)

            # AI's move
            elif turn == AIRL:

                # Getting the AI's move with the q learning
                move = self.loaded_agent.getMoveAIV2(self.get_state(board, player=AIRL), board, AIRL)
                self.loaded_agent.update_q(self.get_state(board, player=AIRL), board[PLAYER_2_SCORE])

                print('Machine choose pocket ', move)
                # Updating the board
                board, go_again = move_piece(board, move, AIRL)

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

    @staticmethod
    def AIVSAI(self):
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
        AI1 = PLAYER_2_SIDE  # get_player_type()

        # Some final inits before starting the game
        PRINT_P1 = "CPU"
        PRINT_P2 = "YOU"
        AI2 = PLAYER_1_SIDE
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
            if turn == AI1:
                # Getting the AI's move with the Minimax function
                best_score, move = agent.minimaxPruning(board, AI1, turn, 6)

                # Visual aid to show of confident the minimax algorithm is in winning
                winning_confidence = ""
                for score, confidence in winning_confidence_mapping.items():
                    if score < best_score:
                        continue
                    winning_confidence = confidence
                    break
                ai_printed_moves.append(f"AI Moved : {move + 1}\tChance of Winning : {winning_confidence}")

                # Updating the board
                board, go_again = move_piece(board, move, AI1)

            # AI's move
            elif turn == AI2:
                # Getting the AI's move with the Minimax function
                best_score, move = agent.minimaxPruning(board, AI2, turn, MAX_DEPTH)

                # Visual aid to show of confident the minimax algorithm is in winning
                winning_confidence = ""
                for score, confidence in winning_confidence_mapping.items():
                    if score < best_score:
                        continue
                    winning_confidence = confidence
                    break
                ai_printed_moves.append(f"AI Moved : {move + 1}\tChance of Winning : {winning_confidence}")

                # Updating the board
                board, go_again = move_piece(board, move, AI2)

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
                f"Congrats! You won when the AI looks {MAX_DEPTH} moves ahead. For more of a challenge try increasing the MAX_DEPTH value."
            )
        elif board[f"{AI1}_score"] < board[f"{AI2}_score"]:
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
                move = getMove(board, PLAYER)

                # Updating the board
                board, go_again = move_piece(board, move, PLAYER)

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
                board, go_again = action.move_piece(board, move, AI)

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
