import unittest

from pybuilder_prettySetup import build_string_from_array
from pybuilder_prettySetup import build_string_from_dict

TEST_KEY = "foobar"
TEST_IDENT = 6


class StrinUtilsTest(unittest.TestCase):
  
  def test_single_item_array(self):
    expected = "['item']"

    items = ['item']

    string = build_string_from_array(items, TEST_KEY)
    self.assertEqual(string, expected)

  def test_multiple_item_array(self):
    expected = "[\n"
    expected += " " * TEST_IDENT
    expected += "'item1',\n"
    expected += " " * TEST_IDENT
    expected += "'item2'\n"
    expected += " " * (TEST_IDENT - 2)
    expected += "]"

    string = build_string_from_array(['item1','item2'], TEST_KEY)
    self.assertEqual(string, expected)
       
