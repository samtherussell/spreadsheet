
import unittest

import spreadsheet
from Exceptions import *
from Cell import Cell

class Tests(unittest.TestCase):

    def test_read_command__malformatted_arg(self):
        with self.assertRaises(InputException):
            spreadsheet.read_command("1")

    def test_read_command__not_in_spreadsheet(self):
        spreadsheet.spreadsheet = {"V7":Cell("V7")}
        result = spreadsheet.read_command("B8")
        self.assertEqual(result,"<empty>")

    def test_read_command__success(self):
        cell = Cell("B8")
        cell.type = "TEXT"
        cell.value = 42
        spreadsheet.spreadsheet = {"V7":Cell("V7"),"B8":cell}
        result = spreadsheet.read_command("B8")
        self.assertEqual(result,42)

if __name__ == '__main__':
    unittest.main()
    
        
