# This is a sample Python script.
from board import Board

if __name__ == '__main__':
    print('''Start Program''')

    choice = input(
        'if you want to start playing press Y, if you want to train machine press T')

    if choice.lower() == 'y':
        board = Board(reinforcementLearning=False)
    elif choice.lower() == 't':
        board = Board(reinforcementLearning=True)
    else:
        quit()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
