from unittest import TestCase

from metripy.LangAnalyzer.Python.Ast.PythonAstParser import PythonAstParser
from metripy.LangAnalyzer.Python.Metrics.PythonCognitiveComplexityCalculator import (
    PythonCognitiveComplexityCalculator,
)


class TestPythonCognitiveComplexityCalculator(TestCase):

    SIMPLE_SCRIPT = """
    def test_function():
        if True:
            print("Hello, World!")
        else:
            print("Hello, World!")
    """
    MEDIUM_SCRIPT = """
    def test_function():
        for i in range(10):
            print(i)
            if i % 2 == 0:
                print("Even")
            else:
                print("Odd")
        try:
            print("Hello, World!")
        except Exception as e:
            print(e)
    """
    COMPLEX_SCRIPT = """
    def test_function(data):
        for i in range(len(data)):                     # +1
            if data[i] > 0:                            # +1 + nesting (+1)
                for j in range(data[i]):               # +1 + nesting (+2)
                    if j % 2 == 0:                     # +1 + nesting (+3)
                        print("Even")
                    else:
                        print("Odd")
                    if j > 5:                          # +1 + nesting (+3)
                        print("Large")
                    else:
                        print("Small")
                if data[i] > 100:                      # +1 + nesting (+2)
                    try:                                # +1 + nesting (+3)
                        if data[i] % 10 == 0:          # +1 + nesting (+4)
                            print("Divisible by 10")
                        else:
                            print("Not divisible by 10")
                    except Exception as e:             # +1 + nesting (+4)
                        print(e)
                    finally:
                        print("Cleanup")
            else:
                print("Non-positive")
    """

    def setUp(self):
        self.calculator = PythonCognitiveComplexityCalculator()

    def test_simple_script(self):
        parser = PythonAstParser()
        parser.parse(self.SIMPLE_SCRIPT)
        result = self.calculator.calculate_for_all_functions(parser)
        self.assertEqual(result["test_function"], 1)

    def test_medium_script(self):
        parser = PythonAstParser()
        parser.parse(self.MEDIUM_SCRIPT)
        result = self.calculator.calculate_for_all_functions(parser)
        self.assertEqual(result["test_function"], 6)

    def test_complex_script(self):
        parser = PythonAstParser()
        parser.parse(self.COMPLEX_SCRIPT)
        result = self.calculator.calculate_for_all_functions(parser)
        self.assertEqual(result["test_function"], 31)
