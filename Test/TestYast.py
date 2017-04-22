import unittest
from pandas import json
from unittest.mock import patch, MagicMock, _patch_object

import numpy

from yast import load_dictionary, process_file, transcode_str_line


class TestYast(unittest.TestCase):
    @patch("yast.count_line")
    @patch("yast.get_file_iterator")
    def test_load_dictionary(self, mocked_file_iterator, mocked_count_line):
        mocked_file_iterator.return_value = iter(["a 0", "b 1", "c 2"])
        mocked_count_line.return_value = 3

        # load method with mocked open method
        loaded_dict = load_dictionary("/toto")
        expected_dict = {
            "a": numpy.array([0]),
            "b": numpy.array([1]),
            "c": numpy.array([2])
        }

        self.assertEqual(loaded_dict, expected_dict, "The loaded dict should be like the mocked one")

    def test_transcode_str_line(self):
        transcode_dict = {
            "a": numpy.array([0]),
            "b": numpy.array([1]),
            "c": numpy.array([2])
        }

        actual_array = transcode_str_line(sequence="a b c", separator="\ |\.|\,", transcode_dict=transcode_dict)
        self.assertTrue(numpy.array_equal(actual_array, numpy.array([[0], [1], [2]])),
                        "sequence transcoded should return the same array as the mocked one")


if __name__ == '__main__':
    unittest.main()
