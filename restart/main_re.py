import pygame 
from game_re import Game
from tools import read_from_numpy_file

if __name__ == "__main__":
    old_q_table = read_from_numpy_file("q_table.npy")
    pygame.init()
    game = Game()
    game.run()
    q_table = read_from_numpy_file("q_table.npy")
    state = (22, 48)
    # Affiche les valeurs Q pour les états proches de (22, 48)
    for i in range(state[0] - 2, state[0] + 3):
        for j in range(state[1] - 2, state[1] + 3):
            try:
                print(f"Q[{i},{j}] = {q_table[i, j]}")
            except IndexError:
                print(f"Q[{i},{j}] = hors limites")

    if (old_q_table == q_table).all():
        print("old_q_table et q_table sont identiques.")
    else:
        print("old_q_table et q_table sont différentes.")

    

