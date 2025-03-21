import json

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