import copy
from typing import Tuple

from actions.action import Action
from transition_model.transitionmodel import PLAYER_1_SIDE, PLAYER_2_SIDE


class MinimaxPruningAgent:


    """A function to calculate the minimax algorithm for a given board

           Args:
               board (dict): Schema
               {
                   "top"          : [4, 4, 4, 4, 4, 4],
                   "bottom"       : [4, 4, 4, 4, 4, 4],
                   "top_score"    : 0,
                   "bottom_score" : 0
               }
               ai_side (str): 'top' or 'bottom'
               turn (str): 'top' or 'bottom'
               depth (int): How deep that you want the AI to look ahead, *WARNING* larger depths require more CPU power

           Returns:
               Tuple[int, int]:
                   score (int): the likelihood of the move being the best move
                       - this is used in recursion for finding the best move
                   move (int) : the recommended minimax move
                       - this is used in decision-making for executing the best move
           """

    def __init__(self):
        self.action = Action(qlearningAgent=None)


    def minimaxPruning(self, board: dict, ai_side: str, turn: str, depth: int) -> Tuple[int, int]:

        AI = ai_side
        PLAYER = PLAYER_2_SIDE if PLAYER_1_SIDE == ai_side else PLAYER_1_SIDE
        best_move = -1

        # If the game is over, or the max depth is reached. The delta of the AI - PLAYER is what I believe to give
        # the best result, as it will cause the algorithm to strive for large number victories
        if (not any(board[AI])) or (not any(board[PLAYER])) or depth <= 0:
            return board[f"{AI}_score"] - board[f"{PLAYER}_score"], best_move

        # Finding the move which will give the most points to the AI
        if AI == turn:
            # only uphill from here
            best_score = float("-inf")

            possible_moves = self.action.getMoveAI(board, AI)

            for move in possible_moves:
                # preforming a deepcopy so we don't accidently overwrite moves by referencing the same list
                board_copy = copy.deepcopy(board)
                board_copy, go_again = self.action.move_piece(board_copy, move, turn)

                # mancala is one of those games where you can get two moves.
                # In testing, I found that not decressing the depth for the multimove results in the best AI
                if go_again:
                    points, _ = self.minimaxPruning(board_copy, AI, AI, depth)
                else:
                    points, _ = self.minimaxPruning(board_copy, AI, PLAYER, depth - 1)

                # The MAX part of minimax. Finding the MAX output for the AI
                if points > best_score:
                    best_move = move
                    best_score = points

        # Finding the move which will give the least points to the PLAYER
        elif PLAYER == turn:
            best_score = float("inf")

            possible_moves = self.action.getMoveAI(board, PLAYER)
            for move in possible_moves:
                # preforming a deepcopy so we don't accidently overwrite moves by referencing the same list
                board_copy = copy.deepcopy(board)
                board_copy, go_again = self.action.move_piece(board_copy, move, turn)

                # mancala is one of those games where you can get two moves.
                # In testing, I found that not decressing the depth for the multimove results in the best AI
                if go_again:
                    points, _ = self.minimaxPruning(board_copy, AI, PLAYER, depth)
                else:
                    points, _ = self.minimaxPruning(board_copy, AI, AI, depth - 1)

                # The MIN part of minimax. Finding the MIN output for the PLAYER
                if points < best_score:
                    best_move = move
                    best_score = points

        return best_score, best_move
