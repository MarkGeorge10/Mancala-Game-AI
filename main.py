# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

from transitionmodel import getNewBoard


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print('''Start playing Mancala''')

    input('Press Enter to begin...')
    gameBoard = getNewBoard()
    playerTurn = '1'  # Player 1 goes first.

    # while True:  # Run a player's turn.
    #     # "Clear" the screen by printing many newlines, so the old
    #     # board isn't visible anymore.
    #     print('\n' * 60)
    #     # Display board and get the player's move:
    #     displayMancalaBoard(gameBoard)
    #     # playerMove = askForPlayerMove(playerTurn, gameBoard)
    #     #
    #     # # Carry out the player's move:
    #     # playerTurn = makeMove(gameBoard, playerTurn, playerMove)
    #     #
    #     # # Check if the game ended and a player has won:
    #     # winner = checkForWinner(gameBoard)
    #     # if winner == '1' or winner == '2':
    #     #     displayBoard(gameBoard)  # Display the board one last time.
    #     #     print('Player ' + winner + ' has won!')
    #     #     sys.exit()
    #     # elif winner == 'tie':
    #     #     displayBoard(gameBoard)  # Display the board one last time.
    #     #     print('There is a tie!')
    #     #     sys.exit()





# See PyCharm help at https://www.jetbrains.com/help/pycharm/
