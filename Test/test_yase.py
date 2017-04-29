import json
import unittest
from collections import OrderedDict
from unittest.mock import patch, MagicMock, _patch_object

import numpy

import yase


class test_yast(unittest.TestCase):
    @patch("yase.count_line")
    @patch("yase.get_file_iterator")
    def test_load_dictionary(self, mocked_file_iterator, mocked_count_line):
        mocked_file_iterator.return_value = iter(["a 0", "b 1", "c 2"])
        mocked_count_line.return_value = 3

        # load method with mocked open method
        loaded_dict = yase.load_dictionary("/toto", encoding="UTF8")
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

        actual_array = yase.transcode_str_line(sequence="a b c", separator="\ |\.|\,", transcode_dict=transcode_dict,
                                               replacements={})
        self.assertTrue(numpy.array_equal(actual_array, numpy.array([[0], [1], [2]])),
                        "sequence transcoded should return the same array as the mocked one")

    def test_transcode_str_line_with_replacements(self):
        input_str = "a. b. c +"
        transcode_dict = {
            "a": numpy.array([0]),
            "b": numpy.array([1]),
            "c": numpy.array([2]),
            ".": numpy.array([4])
        }
        dict_repl = yase.get_replacement_dict(path="Ressources/replacement.json", no_replace=False)

        actual_array = yase.transcode_str_line(sequence=input_str,
                                               separator="\ ",
                                               transcode_dict=transcode_dict,
                                               replacements=dict_repl)
        self.assertTrue(numpy.array_equal(actual_array, numpy.array([[0], [4], [1], [4], [2]])),
                        "sequence transcoded should return the same array as the mocked one")

    def test_list_replace(self):
        bad_str = "\"\"a\"\".."
        dict_repl = yase.get_replacement_dict(path="Ressources/replacement.json", no_replace=False)
        actual_str = yase.apply_list_replace(input_str=bad_str, replacements=dict_repl)
        self.assertEqual(actual_str, "a . . ", "str should have been transformed")

    def test_get_replacement_dict(self):
        with open("Ressources/replacement.json") as f:
            expected_dict = json.load(f, object_pairs_hook=OrderedDict)
        dict_repl = yase.get_replacement_dict(path="Ressources/replacement.json", no_replace=False)
        self.assertEqual(dict_repl, expected_dict, msg="returned dict should be like supplied one")

        dict_repl = yase.get_replacement_dict(path=None, no_replace=False)
        self.assertEqual(dict_repl, expected_dict, msg="returned dict should be like supplied one, with default dict")

        dict_repl = yase.get_replacement_dict(path="Ressources/replacement.json", no_replace=True)
        self.assertEqual(dict_repl, {}, msg="returned dict should be empty")


if __name__ == '__main__':
    unittest.main()
