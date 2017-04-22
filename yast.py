import csv
import json
import re
from typing import List, Dict, Iterator

import numpy
import time

from numpy import ndarray

from tqdm import tqdm


def split_sequence(sequence: str, separator: str, *args, **kwargs) -> List[str]:
    """
    Take a sequence as string and split it with the provided regex separator
    Sequence, separator, args and kwargs are passed to re.split() method.    
    
    :param sequence: Sequence to split
    :param separator: Regex used to split sequence
    :return: List of token in the sequence
    """

    tokens = re.split(separator, sequence, *args, **kwargs)
    if len(tokens) == 0:
        raise ValueError("No tokens are returned after split")
    else:
        return tokens


def apply_list_replace(input_str: str, replacements: Dict[str, str]) -> str:
    """
    Apply a series of replacement on the input.
    
    :param input_str: the string to be modified
    :param replacements: a Dict regex -> replacement. Each item will be passed to re.sub()
    :return: the modified string
    """
    temp = input_str
    if isinstance(replacements, dict):
        for replacement in replacements.items():
            temp = re.sub(replacement[0], replacement[1], temp)
    return temp


def transcode_token(token: str, transcode_dict: Dict[str, ndarray]) -> ndarray:
    """
    Take a token contained in a sequence and transcode it to a vector of values using the provided transcode_dict.
    
    :param token: the token to transcode as str
    :param transcode_dict: the dict used for transcoding
    :return: the vector associated with this token
    """

    return transcode_dict.get(token)


def get_replacement_dict(path: str, *args, **kwargs) -> Dict[str, str]:
    # Todo: Read a CSV file "regex", "replacement" and return it as dict
    raise NotImplementedError


def transcode_str_line(sequence: str, separator: str, transcode_dict: Dict[str, ndarray],
                       replacements: Dict[str, str] = None) -> ndarray:
    replaced = apply_list_replace(input_str=sequence, replacements=replacements)
    splitted = [token for token in split_sequence(replaced.strip().lower(), separator=separator) if token != '']
    tokens = []
    for word in splitted:
        token = transcode_token(token=word, transcode_dict=transcode_dict)
        if token is not None:
            tokens.append(token)
    return numpy.stack(tokens, axis=0)  # TODO: return a fixed sized array


def load_dictionary(path: str, encoding="UTF8") -> Dict[str, ndarray]:
    """
    Load the transcoding dict. It process the file chunk by chunk so very large file should not be a problem.

    :param path: path to the dict
    :param encoding: Encoding of the transcode dictionary
    :return: the transcoding dict
    """
    total = count_line(encoding, path)

    transcode_dict = {}
    time.sleep(0.01)  # Workaround for tqdm (windows only ?)
    for text_line in tqdm(get_file_iterator(path), total=total, mininterval=0.5):
        splitted_line = text_line.strip().split(" ")
        vectors = []
        for value in splitted_line[1:]:
            try:
                vectors.append(float(value))
            except ValueError:
                pass
        transcode_dict[splitted_line[0].lower()] = numpy.array(splitted_line[1:], dtype=numpy.float16)

        # TODO: the creation of a numpy array at each iteration is very slow, it should be refactored.
    return transcode_dict


def count_line(encoding, path):
    with open(path, encoding=encoding) as file:
        total = sum([1 for _ in file])
    return total


def get_file_iterator(path: str, *args, **kwargs) -> Iterator[str]:
    """
    Read a file and yield each line.
    Pass additional args and kwargs to builtin open method
    
    :param path: path to file to read
    :return: an iterator over each line in file
    """
    with open(path, *args, **kwargs) as file:
        for line in file:
            yield line


def process_file(path_to_file: str, path_to_dict: str, path_output_file: str, separator: str,
                 file_encoding: str = "UTF8",
                 dict_encoding: str = "UTF8"):
    # Loading transcoding ding
    print("loading dict...")
    transcode_dict = load_dictionary(path_to_dict, encoding=dict_encoding)

    # Sleep for tqdm
    time.sleep(0.01)
    print("transcoding file...")

    # Counting total line in input file for tqdm
    total = count_line(path=path_to_file, encoding=file_encoding)

    with open(path_output_file, encoding="UTF8", newline="", mode="w") as csv_output:
        fields = ["inputs", "vectors"]
        writer = csv.DictWriter(csv_output, fieldnames=fields)
        writer.writeheader()
        time.sleep(0.01)
        for line in tqdm(get_file_iterator(path_to_file), total=total, mininterval=0.5):
            csv_line = {"inputs": line.strip(),
                        "vectors": transcode_str_line(sequence=line,
                                                      separator=separator,
                                                      transcode_dict=transcode_dict).tolist()}
            writer.writerow(csv_line)
    time.sleep(0.01)
    print("done !")
