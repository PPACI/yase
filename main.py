import argparse
from yast import process_file

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Yet Another Sequence Translator')
    parser.add_argument('--input', metavar="input.txt", type=str, help='Path to file to transcode', required=True)
    parser.add_argument('--input-encoding', metavar="UTF8", type=str, help='encoding of input file. UTF8 by default',
                        required=False, default="UTF8")
    parser.add_argument('--output', metavar="output.txt", type=str, help='Path to output file', required=True)
    parser.add_argument('--mapping', metavar="mapping.vec", type=str, help='Path to mapping file', required=True)
    parser.add_argument('--mapping-encoding', metavar="UTF8", help='encoding of mapping file. UTF8 by default',
                        required=False, default="UTF8", type=str)
    parser.add_argument('--separator', metavar="\ |\.|\,", type=str,
                        help='regular expression used to split the input sequence', required=False, default="\ ")
    args = parser.parse_args()
    process_file(path_to_file=args.input,
                 path_to_dict=args.mapping,
                 path_output_file=args.output,
                 separator=args.separator,
                 file_encoding=args.input_encoding,
                 dict_encoding=args.mapping_encoding)
