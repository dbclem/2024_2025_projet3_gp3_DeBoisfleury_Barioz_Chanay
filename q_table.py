from tools import read_from_numpy_file, write_in_numpy_file
import numpy as np


def create_q_table(largeur, hauteur, actions):
    """
    Create a Q-table using a NumPy array.
    Shape: (largeur, hauteur, len(actions))
    """
    q_table = np.zeros((largeur, hauteur, len(actions)))

    print(" ---- \n Q-table created with dimensions:", largeur, "x", hauteur, "\n ----")
    return q_table

def find_biggest_q_value_with_numpy(q_values):
    return np.argmax(q_values)  # retourne l'indice de la plus grande valeur




"""creation de la q_table"""
# actions = ["up", "down", "left", "right"]
# q_table = create_q_table(5, 5, actions)  # Exemple de dimensions, à adapter si besoin
# q_table[0, 2, 3] = 2
# state = (0, 2)
# print("valeur", q_table[state])
# write_in_numpy_file("q_table.npy", q_table)
# print (read_from_numpy_file("q_table.npy"))