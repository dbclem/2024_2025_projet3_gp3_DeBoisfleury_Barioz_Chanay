from tools import read_from_pickle_file, write_in_pickle_file

def create_q_table(largeur, hauteur, actions):
    """
    Create a Q-table with all possible states and actions.
    """
    q_table = {}
    for x in range(largeur):
        for y in range(hauteur):
            etat = (x, y)
            q_table[etat] = {}
            for action in actions:
                q_table[etat][action] = 0.0  # Q-value initiale

    print("Q-table created with dimensions:", largeur, "x", hauteur)
    print(q_table)
    return q_table

# actions = ["up", "down", "left", "right"]
# q_table = create_q_table(50, 50, actions)
# write_in_pickle_file(q_table, "q_table.pickle")
q_table_read = read_from_pickle_file("q_table.pickle")
print(q_table_read)