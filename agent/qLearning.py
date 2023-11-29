import pickle
import random


class QlearningRL:

    def __init__(self, load_agent_path):
        self.state_map = {}
        try:
            if load_agent_path is not None:
                with open(load_agent_path, 'rb') as infile:
                    self.state_map = pickle.load(infile)
        except FileNotFoundError:
            print("No pretrained agent exists. Creating new agent")
            self.state_map = {}
        # Parameters not saved in pkl file
        self.max_actions = 6
        self.previous_state = 0
        self.previous_action = 0
        self.alpha = 0.5
        self.gamma = 0.5
        self.epsilon = 0.9

    def update_q(self, current_state, reward=0):

        # Assume no reward unless explicitly specified
        print("current_state")
        print(current_state)
        # Convert state to a unique identifier
        hashed_current_state = hash(''.join(map(str, str(current_state))))
        print("hashed_current_state")
        print(hashed_current_state)
        hashed_previous_state = hash(''.join(map(str, self.previous_state)))

        current_q_set = self.state_map.get(hashed_current_state)
        previous_q_set = self.state_map.get(hashed_previous_state)

        # Add new dictionary key/value pairs for new states seen
        if current_q_set is None:
            self.state_map[hashed_current_state] = [0] * self.max_actions
            current_q_set = [0] * self.max_actions
        if previous_q_set is None:
            self.state_map[hashed_previous_state] = [0] * self.max_actions

        # Q update formula
        q_s_a = self.state_map[hashed_previous_state][self.previous_action]
        q_s_a = q_s_a + self.alpha * (reward + self.gamma * max(current_q_set) - q_s_a)

        # Update Q
        self.state_map[hashed_previous_state][self.previous_action] = q_s_a

        # Track previous state for r=delayed reward assignment problem
        self.previous_state = current_state

        return True

    def save_agent(self, save_path):
        with open(save_path, 'wb') as outfile:
            pickle.dump(self.state_map, outfile)
