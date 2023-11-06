import sys

from transitionmodel import STARTING_NUMBER_OF_SEEDS, PLAYER_1_PITS, PLAYER_2_PITS, NEXT_PIT, OPPOSITE_PIT


class Board:
    def __init__(self, other=None):
        print('''Start playing Mancala''')

        input('Press Enter to begin...')
        game_board = self.get_new_Board()
        playerTurn = '1'  # Player 1 goes first.

        while True:  # Run a player's turn.
            # "Clear" the screen by printing many newlines, so the old
            # board isn't visible anymore.
            print('\n' * 60)
            # Display board and get the player's move:
            self.displayBoard(game_board)
            playerMove = self.ask_player_move(playerTurn, game_board)

            # Carry out the player's move:
            playerTurn = self.make_move(game_board, playerTurn, playerMove)

            # Check if the game ended and a player has won:
            winner = self.check_winner(game_board)
            if winner == '1' or winner == '2':
                self.displayBoard(game_board)  # Display the board one last time.
                print('Player ' + winner + ' has won!')
                sys.exit()
            elif winner == 'tie':
                self.displayBoard(game_board)  # Display the board one last time.
                print('There is a tie!')
                sys.exit()

    @staticmethod
    def get_new_Board():
        """Return a dictionary representing a Mancala board in the starting
        state: 4 seeds in each pit and 0 in the stores."""

        # Syntactic sugar - Use a shorter variable name:

        s = STARTING_NUMBER_OF_SEEDS

        # Create the data structure for the board, with 0 seeds in the
        # stores and the starting number of seeds in the pits:

        return {'1': 0, '2': 0, 'A': s, 'B': s, 'C': s, 'D': s, 'E': s,
                'F': s, 'G': s, 'H': s, 'I': s, 'J': s, 'K': s, 'L': s}

    @staticmethod
    def displayBoard(board):
        """Displays the game board as ASCII-art based on the board
          dictionary."""

        seedAmounts = []
        # This 'GHIJKL21ABCDEF' string is the order of the pits left to
        # right and top to bottom:
        for pit in 'GHIJKL21ABCDEF':
            numSeedsInThisPit = str(board[pit]).rjust(2)
            seedAmounts.append(numSeedsInThisPit)

        print("""
         +------+------+--<<<<<-Player 2----+------+------+------+
         2      |G     |H     |I     |J     |K     |L     |      1
                |  {}  |  {}  |  {}  |  {}  |  {}  |  {}  |
         S      |      |      |      |      |      |      |      S
         T  {}  +------+------+------+------+------+------+  {}  T
         O      |A     |B     |C     |D     |E     |F     |      O
         R      |  {}  |  {}  |  {}  |  {}  |  {}  |  {}  |      R
         E      |      |      |      |      |      |      |      E
         +------+------+------+-Player 1->>>>>-----+------+------+
         
         """.format(*seedAmounts))

    @staticmethod
    def ask_player_move(playerTurn, game_board):
        """Asks the player which pit on their side of the board they
         select to sow seeds from. Returns the uppercase letter label of the
         selected pit as a string."""
        while True:  # Keep asking the player until they enter a valid move.
            # Ask the player to select a pit on their side:
            if playerTurn == '1':
                print('Player 1, choose move: A-F (or QUIT)')
            elif playerTurn == '2':
                print('Player 2, choose move: G-L (or QUIT)')
            response = input('> ').upper().strip()

            # Check if the player wants to quit:
            if response == 'QUIT':
                print('Thanks for playing!')
                sys.exit()

            # Make sure it is a valid pit to select:
            if (playerTurn == '1' and response not in PLAYER_1_PITS) or (
                    playerTurn == '2' and response not in PLAYER_2_PITS):
                print('Please pick a letter on your side of the board.')
                continue  # Ask player again for their move.
            if game_board.get(response) == 0:
                print('Please pick a non-empty pit.')
                continue  # Ask player again for their move.
            return response

    @staticmethod
    def make_move(game_board, playerTurn, pit):
        """Modify the board data structure so that the player 1 or 2 in
        turn selected pit as their pit to sow seeds from. Returns either
        '1' or '2' for whose turn it is next."""

        seeds_to_sow = game_board[pit]  # Get number of seeds from selected pit.
        game_board[pit] = 0  # Empty out the selected pit.

        while seeds_to_sow > 0:  # Continue sowing until we have no more seeds.
            pit = NEXT_PIT[pit]  # Move on to the next pit.
            if (playerTurn == '1' and pit == '2') or (playerTurn == '2' and pit == '1'):
                continue  # Skip opponent's store.
            game_board[pit] += 1
            seeds_to_sow -= 1

        # If the last seed went into the player's store, they go again.
        if (pit == playerTurn == '1') or (pit == playerTurn == '2'):
            # The last seed landed in the player's store; take another turn.
            return playerTurn

        # Check if last seed was in an empty pit; take opposite pit's seeds.
        if playerTurn == '1' and pit in PLAYER_1_PITS and game_board[pit] == 1:
            opposite_pit = OPPOSITE_PIT[pit]
            game_board['1'] += game_board[opposite_pit]
            game_board[opposite_pit] = 0
        elif playerTurn == '2' and pit in PLAYER_2_PITS and game_board[pit] == 1:
            opposite_pit = OPPOSITE_PIT[pit]
            game_board['2'] += game_board[opposite_pit]
            game_board[opposite_pit] = 0

        # Return the other player as the next player:
        if playerTurn == '1':
            return '2'
        elif playerTurn == '2':
            return '1'

    @staticmethod
    def check_winner(game_board):
        """Looks at board and returns either '1' or '2' if there is a
        winner or 'tie' or 'no winner' if there isn't. The game ends when a
        player's pits are all empty; the other player claims the remaining
        seeds for their store. The winner is whoever has the most seeds."""

        player1Total = game_board['A'] + game_board['B'] + game_board['C']
        player1Total += game_board['D'] + game_board['E'] + game_board['F']
        player2Total = game_board['G'] + game_board['H'] + game_board['I']
        player2Total += game_board['J'] + game_board['K'] + game_board['L']

        if player1Total == 0:
            # Player 2 gets all the remaining seeds on their side:
            game_board['2'] += player2Total
            for pit in PLAYER_2_PITS:
                game_board[pit] = 0  # Set all pits to 0.
        elif player2Total == 0:
            # Player 1 gets all the remaining seeds on their side:
            game_board['1'] += player1Total
            for pit in PLAYER_1_PITS:
                game_board[pit] = 0  # Set all pits to 0.
        else:
            return 'no winner'  # No one has won yet.

        # Game is over, find player with the largest score.
        if game_board['1'] > game_board['2']:
            return '1'
        elif game_board['2'] > game_board['1']:
            return '2'
        else:
            return 'tie'
