# A tuple of the player's pits:
PLAYER_1_PITS = ('A', 'B', 'C', 'D', 'E', 'F')
PLAYER_2_PITS = ('G', 'H', 'I', 'J', 'K', 'L')

# A dictionary whose keys are pits and values are opposite pit:
OPPOSITE_PIT = {'A': 'G', 'B': 'H', 'C': 'I', 'D': 'J', 'E': 'K',
                'F': 'L', 'G': 'A', 'H': 'B', 'I': 'C', 'J': 'D', 'K': 'E', 'L': 'F'}

# A dictionary whose keys are pits and values are the next pit in order:
NEXT_PIT = {'A': 'B', 'B': 'C', 'C': 'D', 'D': 'E', 'E': 'F', 'F': '1',
            '1': 'L', 'L': 'K', 'K': 'J', 'J': 'I', 'I': 'H', 'H': 'G', 'G': '2', '2': 'A'}

# Every pit label, in counterclockwise order starting with A:
PIT_LABELS = 'ABCDEF1LKJIHG2'

# How many seeds are in each pit at the start of a new game:
STARTING_NUMBER_OF_SEEDS = 4


def getNewBoard():
    """Return a dictionary representing a Mancala board in the starting
    state: 4 seeds in each pit and 0 in the stores."""

    # Syntactic sugar - Use a shorter variable name:
    s = STARTING_NUMBER_OF_SEEDS

    # Create the data structure for the board, with 0 seeds in the
    # stores and the starting number of seeds in the pits:
    assign_seeds_to_pit =  {'1': 0, '2': 0, 'A': s, 'B': s, 'C': s, 'D': s, 'E': s,
            'F': s, 'G': s, 'H': s, 'I': s, 'J': s, 'K': s, 'L': s}
    print(assign_seeds_to_pit)
    return assign_seeds_to_pit


# def displayMancalaBoard(board):
#     """Displays the game board as ASCII-art based on the board
#     dictionary."""
#     seed_amounts = []
#     # This 'GHIJKL21ABCDEF' string is the order of the pits left to
#     # right and top to bottom:
#     for pit in 'GHIJKL21ABCDEF':
#         num_seeds_in_this_pit = str(board[pit]).rjust(2)
#         seed_amounts.append(num_seeds_in_this_pit)
#         print("""
#         +------+------+--<<<<<-Player 2----+------+------+------+
#         |G     |H     |I     |J     |K     |L     |      1
#         |  {}  |  {}  |  {}  |  {}  |  {}  |  {}  |
#         S      |      |      |      |      |      |      |      S
#         T  {}  +------+------+------+------+------+------+  {}  T
#         O      |A     |B     |C     |D     |E     |F     |      O
#         R      |  {}  |  {}  |  {}  |  {}  |  {}  |  {}  |      R
#         E      |      |      |      |      |      |      |      E
#         +------+------+------+-Player 1->>>>>-----+------+------+
#         """.format(*seed_amounts))