# coding=UTF8

import re
from concurrent import futures
from typing import Dict, List
import numpy

from itertools import islice


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


def transcode_token(token: str, transcode_dict: Dict[str, List[float]]) -> List[float]:
    """
    Take a token contained in a sequence and transcode it to a vector of values using the provided transcode_dict.
    
    :param token: the token to transcode as str
    :param transcode_dict: the dict used for transcoding
    :return: the vector associated with this token
    """

    return transcode_dict.get(token)


def transcode_sequence(sequence: str, transcode_dict: Dict[str, List[float]]) -> List[List[float]]:
    raise NotImplementedError


def load_dictionnary(path: str, encoding="UTF8") -> Dict[str, List[float]]:
    """
    Load the transcoding dict. It process the file chunk by chunk so very large file should not be a problem.
    
    :param path: path to the dict
    :return: the transcoding dict
    """
    with open(path, encoding=encoding) as file:
        transcode_dict = {}
        from tqdm import tqdm
        for text_line in tqdm(file):
            splitted_line = text_line.split(" ")
            vectors = []
            for value in splitted_line[1:]:
                try:
                    vectors.append(float(value))
                except ValueError:
                    pass
            transcode_dict[splitted_line[0]] = numpy.array(vectors, dtype=numpy.float16)
    return transcode_dict


if __name__ == '__main__':
    transcode_dict = load_dictionnary("C:\\Users\pierr\OneDrive\Developpement\Spacy Word Vector\wiki.fr.vec")
    import sys

    print(sys.getsizeof(transcode_dict) / 1e6)
    print(len(transcode_dict))
    print(transcode_dict["bonjour"])
