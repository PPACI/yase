# coding=UTF8
import argparse
from yast import process_file

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Yet Another Sequence Translator')
    parser.add_argument('--input', metavar="input.txt", type=str, help='Path to file to transcode', required=True)
    parser.add_argument('--output', metavar="output.txt", type=str, help='Path to output file', required=True)
    parser.add_argument('--mapping', metavar="mapping.vec", type=str, help='Path to mapping file', required=True)
    parser.add_argument('--separator', metavar="\ |\.|\,", type=str,
                        help='regular expression used to split the input sequence', required=False, default="\ ")
    args = parser.parse_args()
    process_file(path_to_file=args.input,
                 path_to_dict=args.mapping,
                 path_output_file=args.output,
                 separator=args.separator)
