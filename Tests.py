
import unittest
import os

import spreadsheet
from Exceptions import *
from Cell import Cell

class ReadTests(unittest.TestCase):

    def setUp(self):
        spreadsheet.spreadsheet = {}

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

    def test_read_command__success_lowercase(self):
        cell = Cell("B8")
        cell.type = "TEXT"
        cell.value = 42
        spreadsheet.spreadsheet = {"V7":Cell("V7"),"B8":cell}
        result = spreadsheet.read_command("b8")
        self.assertEqual(result,42)

class WriteTests(unittest.TestCase):

    def setUp(self):
        spreadsheet.spreadsheet = {}

    def test_write_command__malformatted_args(self):
        with self.assertRaises(InputException):
            spreadsheet.write_command("a1")

    def test_write_command__success_int(self):
        result = spreadsheet.write_command("a1 1")
        self.assertEqual(result, 1)
        self.assertEqual(type(result), int)

    def test_write_command__success_lowercase(self):
        spreadsheet.write_command("a1 hi")
        self.assertTrue("A1" in spreadsheet.spreadsheet)

    def test_write_command__success_float(self):
        result = spreadsheet.write_command("a1 1.2")
        self.assertEqual(result, 1.2)
        self.assertEqual(type(result), float)

    def test_write_command__success_text(self):
        result = spreadsheet.write_command("a1 hi")
        self.assertEqual(result, "hi")
        self.assertEqual(type(result), str)

    def test_write_command__formula_constant_number(self):
        result = spreadsheet.write_command("a1 =1")
        self.assertEqual(result, 1.0)
        self.assertEqual(type(result), float)

    def test_write_command__formula_constant_text(self):
        result = spreadsheet.write_command("a1 =\"hi\"")
        self.assertEqual(result, "hi")
        self.assertEqual(type(result), str)

    def test_write_command__formula_reference(self):
        spreadsheet.write_command("a1 =666")
        result = spreadsheet.write_command("a2 =~a1")
        self.assertEqual(result, 666)

    def test_write_command__formula_reference_doesnt_exist(self):
        with self.assertRaises(FormulaException):
            spreadsheet.write_command("a2 =~a1")

    def test_write_command__formula_reference_cyclic_dep(self):
        try:
            spreadsheet.write_command("a1 =~a2")
        except FormulaException:
            pass

        with self.assertRaises(FormulaException):
            spreadsheet.write_command("a2 =~a1")

    def test_write_command__formula_func_min(self):
        result = spreadsheet.write_command("a1 =MIN(1,2)")
        self.assertEqual(result, 1)

    def test_write_command__formula_func_max(self):
        result = spreadsheet.write_command("a1 =MAX(1,2)")
        self.assertEqual(result, 2)

    def test_write_command__formula_func_concat(self):
        result = spreadsheet.write_command("a1 =CONCAT(\"hi\",\"ho\")")
        self.assertEqual(result, "hiho")

    def test_write_command__formula_func_lookup(self):
        spreadsheet.write_command("a1 1")
        spreadsheet.write_command("a2 2")
        spreadsheet.write_command("b1 10")
        spreadsheet.write_command("b2 20")
        result = spreadsheet.write_command("c1 =LOOKUP(\"A1:B2\",1,1)")
        self.assertEqual(result, 10)

    def test_write_command__formula_func_lookup_lowercase(self):
        spreadsheet.write_command("a1 1")
        spreadsheet.write_command("a2 2")
        spreadsheet.write_command("b1 10")
        spreadsheet.write_command("b2 20")
        result = spreadsheet.write_command("c1 =LOOKUP(\"a1:B2\",1,1)")
        self.assertEqual(result, 10)

    def test_write_command__formula_func_sum(self):
        spreadsheet.write_command("a1 1")
        spreadsheet.write_command("a2 2")
        spreadsheet.write_command("a3 10")
        result = spreadsheet.write_command("a4 =SUM(\"A1:A3\")")
        self.assertEqual(result, 13)

    def test_write_command__formula_func_mean(self):
        spreadsheet.write_command("a1 2")
        spreadsheet.write_command("a2 3")
        spreadsheet.write_command("a3 10")
        result = spreadsheet.write_command("a4 =MEAN(\"A1:A3\")")
        self.assertEqual(result, 5)

    def test_write_command__formula_add(self):
        result = spreadsheet.write_command("a1 =1+2")
        self.assertEqual(result, 3)

    def test_write_command__formula_multiply(self):
        result = spreadsheet.write_command("a1 =3*5")
        self.assertEqual(result, 15)

    def test_write_command__formula_bracketed(self):
        result = spreadsheet.write_command("a1 =(3*5)")
        self.assertEqual(result, 15)

    def test_write_command__formula_spaced(self):
        spreadsheet.write_command("h1 9")
        result = spreadsheet.write_command("a1 = 2 * ( 3 + 5 ) + MIN( 3 , 2 ) * ~H1")
        self.assertEqual(result, 34)

class SaveTests(unittest.TestCase):

    def setUp(self):
        spreadsheet.spreadsheet = {}

    def test_save_and_open(self):
        filename = "file.out"
        spreadsheet.write_command("a1 hi")
        spreadsheet.save_sheet(filename)
        spreadsheet.spreadsheet = {}
        self.assertTrue("A1" not in spreadsheet.spreadsheet)
        spreadsheet.open_sheet(filename)
        result = spreadsheet.read_command("a1")
        self.assertEqual(result, "hi")
        os.remove(filename)

if __name__ == '__main__':
    unittest.main()
    
        
