import unittest
from pandas import json
from unittest.mock import patch, MagicMock, _patch_object

import numpy

from yast import load_dictionary, process_file, transcode_sequence


class TestYast(unittest.TestCase):
    @patch("yast.open")
    def test_load_dictionary(self, mocked_open):
        self.mock_open(mocked_open, ["a 0", "b 1", "c 2"])

        # load method with mocked open method
        loaded_dict = load_dictionary("/toto")
        expected_dict = {
            "a": numpy.array([0]),
            "b": numpy.array([1]),
            "c": numpy.array([2])
        }

        self.assertEqual(loaded_dict, expected_dict, "The loaded dict should be like the mocked one")

    @staticmethod
    def mock_open(mocked_open, results):
        # Mock the file behaviour
        mock_file = MagicMock()
        mock_file.__iter__.return_value = results
        # Mock the file context manager
        mock_context = MagicMock()
        mock_context.__enter__.return_value = mock_file
        # Mock the open method to return the mocked context manager
        mocked_open.return_value = mock_context

    def test_transcode_sequence(self):
        transcode_dict = {
            "a": numpy.array([0]),
            "b": numpy.array([1]),
            "c": numpy.array([2])
        }

        actual_array = transcode_sequence(sequence="a b c", separator="\ |\.|\,", transcode_dict=transcode_dict)
        self.assertTrue(numpy.array_equal(actual_array, numpy.array([[0], [1], [2]])),
                        "sequence transcoded should return the same array as the mocked one")


if __name__ == '__main__':
    unittest.main()
