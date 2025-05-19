from tools import read_from_numpy_file, write_in_numpy_file
import numpy as np


def create_q_table(largeur, hauteur, actions):
    """
    Create a Q-table using a NumPy array.
    Shape: (largeur, hauteur, len(actions))
    """
    q_table = np.zeros((largeur, hauteur, len(actions)))

    print("Q-table created with dimensions:", largeur, "x", hauteur)
    return q_table

def find_biggest_q_value(state):
    """
    Find the action with the highest Q-value for a given state.
    """
    max_action = None
    max_value = float('-inf')
    for action, value in state.items():
        if value > max_value:
            max_value = value
            max_action = action
    return max_action



"""creation de la q_table"""
actions = ["up", "down", "left", "right"]
q_table = create_q_table(5, 5, actions)  # Exemple de dimensions, à adapter si besoin
q_table[0, 2, 3] = 2
write_in_numpy_file("q_table.npy", q_table)
print (read_from_numpy_file("q_table.npy"))