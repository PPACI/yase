import csv
import json
import re
from typing import List, Dict

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


def transcode_token(token: str, transcode_dict: Dict[str, ndarray]) -> ndarray:
    """
    Take a token contained in a sequence and transcode it to a vector of values using the provided transcode_dict.
    
    :param token: the token to transcode as str
    :param transcode_dict: the dict used for transcoding
    :return: the vector associated with this token
    """

    return transcode_dict.get(token)


def transcode_sequence(sequence: str, separator: str, transcode_dict: Dict[str, ndarray]) -> ndarray:
    splitted = [token for token in split_sequence(sequence.strip().lower(), separator=separator) if token != '']
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
    with open(path, encoding=encoding) as file:
        total = sum([1 for _ in file])

    with open(path, encoding=encoding) as file:
        # total_stream = file.seek(0,2)
        # file.seek(0,0)  # Return to the start of the file
        transcode_dict = {}
        time.sleep(0.01)  # Workaround for tqdm (windows only ?)
        for text_line in tqdm(file, total=total, mininterval=0.5):
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


def process_file(path_to_file: str, path_to_dict: str, path_output_file: str, separator: str,
                 file_encoding: str = "UTF8",
                 dict_encoding: str = "UTF8"):
    print("loading dict...")
    transcode_dict = load_dictionary(path_to_dict, encoding=dict_encoding)

    time.sleep(0.01)
    print("transcoding file...")
    with open(path_to_file, encoding=file_encoding) as file:
        total = sum([1 for _ in file])
    with open(path_to_file, encoding=file_encoding) as file:
        with open(path_output_file, encoding="UTF8", newline="", mode="w") as csv_output:
            fields = ["inputs", "vectors"]
            writer = csv.DictWriter(csv_output, fieldnames=fields)
            writer.writeheader()
            time.sleep(0.01)
            for line in tqdm(file, total=total, mininterval=0.5):
                csv_line = {"inputs": line.strip(),
                            "vectors": transcode_sequence(sequence=line,
                                                          separator=separator,
                                                          transcode_dict=transcode_dict).tolist()}
                writer.writerow(csv_line)
    time.sleep(0.01)
    print("done !")
