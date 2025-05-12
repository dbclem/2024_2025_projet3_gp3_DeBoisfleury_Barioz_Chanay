import json
import pickle

"""  json  """

def read_from_json_file(json_file_name):
    print("use fct : read_from_json_file")
    with open(json_file_name, "r") as f:
        if f.read(1):  # Check if file is not empty --> lit une lettre
            f.seek(0)  # Reset file pointer to the beginning
            loaded_data = json.load(f)
        else:
            loaded_data = [] # si le fichier est vide
    return loaded_data

def write_in_json_file ( data , json_file_name ):
    print("use fct : write_in_json_file")
    with open ( json_file_name , "w") as f :
        json . dump ( data , f , indent =4 , ensure_ascii = False ) # ensure_ascii = False pour les accents

def delete_all_elements_from_json_file(json_file_name):
    print("use fct : delete_all_elements_from_json_file")
    write_in_json_file([], json_file_name)


""" Pickle"""

def read_from_pickle_file(pickle_file_name):
    with open(pickle_file_name, "rb") as f:
        q_table = pickle.load(f)
    return q_table

def write_in_pickle_file(q_table, pickle_file_name):
    with open(pickle_file_name, "wb") as f:
        pickle.dump(q_table, f)


"""projet"""

def adding_one(nombre):
    print(nombre)
    return nombre + 1 