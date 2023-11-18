from typing import Tuple
from transition_model.transitionmodel import STARTING_NUMBER_OF_SEEDS, PLAYER_1_SIDE, PLAYER_2_SIDE, PLAYER_1_SCORE, \
    PLAYER_2_SCORE


def is_legal_move(board: dict, tile: int, turn: str) -> bool:
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


def move_piece(board: dict, tile: int, turn: str) -> Tuple[dict, bool]:
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
