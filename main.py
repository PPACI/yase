# coding=UTF8
from yast import *

if __name__ == '__main__':
    process_file(path_to_file="Ressources/test_input.txt",
                 path_to_dict="Ressources/test_dict",
                 path_output_file="Ressources/test_output.csv",
                 separator=" |\.|,")
