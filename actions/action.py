import random
from typing import Tuple, List

from agent.qLearning import QlearningRL
from transition_model.transitionmodel import STARTING_NUMBER_OF_SEEDS, PLAYER_1_SIDE, PLAYER_2_SIDE, PLAYER_1_SCORE, \
    PLAYER_2_SCORE


class Action:
    def __init__(self, qlearningAgent: QlearningRL):
        self.loaded_agent = qlearningAgent

    def is_legal_move(self,board: dict, tile: int, turn: str) -> bool:
        """A validation function to determin if a move is viable
        Args:
            board (dict): Schema
            {
                "top"          : [4, 4, 4, 4, 4, 4],
                "bottom"       : [4, 4, 4, 4, 4, 4],
                "top_score"    : 0,
                "bottom_score" : 0
            }
            tile (int): the index of the list
            turn (str): 'top' or 'bottom'

        Returns:
            bool: if the space is a valid space to choose
        """
        if tile >= len(board[turn]) or tile < 0:
            return False
        return bool(board[turn][tile])

    def move_piece(self, board: dict, tile: int, turn: str) -> Tuple[dict, bool]:
        """A function to preform the moves of the user

                Args:
                    board (dict): Schema
                    {
                        "top"          : [4, 4, 4, 4, 4, 4],
                        "bottom"       : [4, 4, 4, 4, 4, 4],
                        "top_score"    : 0,
                        "bottom_score" : 0
                    }
                    tile (int): the index of the list
                    turn (str): 'top' or 'bottom'

                Returns:
                    Tuple[dict, bool]:
                        board (dict): Schema
                        {
                            "top"          : [4, 4, 4, 4, 4, 4],
                            "bottom"       : [4, 4, 4, 4, 4, 4],
                            "top_score"    : 0,
                            "bottom_score" : 0
                        }
                        go_again (bool): indicats if the user is able ot make another turn
                """

        pieces = board[turn][tile]
        board[turn][tile] = 0
        location = turn
        go_again = False

        # 2. Moving counter-clockwise, the player deposits one of the stones in each pocket until the stones run out.
        while pieces > 0:
            go_again = False
            pieces -= 1
            tile += 1

            if tile < len(board[location]):
                board[location][tile] += 1
                continue

            # 3. If you run into your own Mancala (store), deposit one piece in it.
            # If you run into your opponent's Mancala, skip it and continue moving to the next pocket.
            # 4. If the last piece you drop is in your own Mancala, you take another turn.
            if location == turn:
                board[f"{turn}_score"] += 1
                go_again = True
            else:
                pieces += 1

            location = PLAYER_2_SIDE if location == PLAYER_1_SIDE else PLAYER_1_SIDE
            tile = -1

        # OPTIONAL RULE :
        # Some people like to play where if you land on a populated space on your side, you get to go again using that tile
        # If that is the rules that you like, please uncomment the codeblock below
        """
                if (location == turn) and (board[location][tile] > 1):
                    return move_piece(board, tile, turn)
                """

        # 5. If the last piece you drop is in an empty pocket on your side,
        # you capture that piece and any pieces in the pocket directly opposite.
        # UNLESS, theres nothing directly in the pocket next to it
        # 6. Always place all captured pieces in your Mancala (store).
        inverse_location = PLAYER_2_SIDE if location == PLAYER_1_SIDE else PLAYER_1_SIDE
        if (
                (location == turn)
                and (board[location][tile] == 1)
                and (board[inverse_location][len(board[inverse_location]) - 1 - tile] != 0)
        ):
            board[f"{turn}_score"] += (
                    1 + board[inverse_location][len(board[inverse_location]) - 1 - tile]
            )
            board[location][tile] = 0
            board[inverse_location][len(board[inverse_location]) - 1 - tile] = 0

        # 7. The game ends when all six pockets on one side of the Mancala board are empty.
        # 8. The player who still has pieces on his/her side of the board when the game ends captures all of those pieces.
        if (not any(board[PLAYER_1_SIDE])) or (not any(board[PLAYER_2_SIDE])):
            board[PLAYER_1_SCORE] += sum(board[PLAYER_1_SIDE])
            board[PLAYER_2_SCORE] += sum(board[PLAYER_2_SIDE])

            board[PLAYER_1_SIDE] = [0] * len(board[PLAYER_1_SIDE])
            board[PLAYER_2_SIDE] = [0] * len(board[PLAYER_2_SIDE])

            go_again = False

        return board, go_again

    def getMove(self, board: dict, turn: str) -> int:
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

            if self.is_legal_move(board, player_move, turn):
                return player_move

            print("Sorry, That Is Not A Valid Move.")

    def getMoveAI(self, board, turn) -> List[int]:
        possible_moves = [
            move for move in range(len(board[turn])) if self.is_legal_move(board, move, turn)
        ]
        return possible_moves

    def getMoveRL(self, current_state, board: dict, turn: str) -> int:
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

            player_move = self.take_action(current_state)

            try:
                player_move = player_move
            except ValueError:
                print("Please Make Sure To Enter A Valid Number.")
                self.loaded_agent.update_q(current_state, -100000000000)
                continue

            if self.is_legal_move(board, player_move, turn):
                return player_move

            print("Sorry, That Is Not A Valid Move.")

    def take_action(self, current_state):
        # Random action 1-epsilon percent of the time

        if random.random() > self.loaded_agent.epsilon:
            action = random.randint(0, 5)
        else:
            # Greedy action taking
            hashed_current_state = hash(''.join(map(str, current_state)))
            current_q_set = self.loaded_agent.state_map.get(hashed_current_state)
            if current_q_set is None:
                self.loaded_agent.state_map[hashed_current_state] = [0] * self.loaded_agent.max_actions
                current_q_set = [0] * self.loaded_agent.max_actions
            action = current_q_set.index(max(current_q_set))  # Argmax of Q

        self.loaded_agent.previous_action = action

        # # Convert computer randomness to appropriate action for mancala usage
        # converted_action = action

        print("machine action")
        print(action)

        return action
