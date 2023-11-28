import logging

from agent.qLearning import QlearningRL
from board import Board



def train_agent(n_games=1, games_per_checkpoint=1, model_save_path='mancala_agent.pkl'):
    # If model already exists, expand on it, otherwise start fresh
    loaded_agent = QlearningRL(load_agent_path=model_save_path)
    environment = Board(reinforcementLearning=True)

    while n_games > 0:
        environment.RLVSRL()
        # Checkpoint
        if n_games % games_per_checkpoint == 0:
            loaded_agent.save_agent(model_save_path)
            logging.info('Saved RL Agent Model!')
            print('Remaining Games: ', n_games)
        n_games -= 1

    # Save final agent model
    loaded_agent.save_agent(model_save_path)

    return environment


if __name__ == "__main__":
    environment = train_agent(n_games=1000, games_per_checkpoint=250)