from unittest import TestCase
from metripy.LangAnalyzer.Python.Metrics.PythonCyclomaticComplexityAnalyzer import (
    PythonCyclomaticComplexityAnalyzer,
)
from metripy.LangAnalyzer.Python.Ast.PythonAstParser import PythonAstParser


class TestPythonCyclomaticComplexityAnalyzer(TestCase):

    SIMPLE_SCRIPT = """
    class Example:
        def test_method(self):
            if True:
                print("Hello, World!")
            else:
                print("Hello, World!")
    """

    MEDIUM_SCRIPT = """
    class Example:
        def test_method(self):
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
    def test_function():
        if True:
            print("Hello, World!")
    """
    COMPLEX_SCRIPT = """
    class Example:
        def test_method(self, data):
            for i in range(len(data)):
                if data[i] > 0:
                    for j in range(data[i]):
                        if j % 2 == 0:
                            print("Even")
                        else:
                            print("Odd")
                        if j > 5:
                            print("Large")
                        else:
                            print("Small")
                    if data[i] > 100:
                        try:
                            if data[i] % 10 == 0:
                                print("Divisible by 10")
                            else:
                                print("Not divisible by 10")
                        except Exception as e:
                            print(e)
                        finally:
                            print("Cleanup")
                else:
                    print("Non-positive")

    def test_function(data):
        for i in range(len(data)):
            if data[i] > 0:
                for j in range(data[i]):
                    if j % 2 == 0:
                        print("Even")
                    else:
                        print("Odd")
    """

    MULTIPLE_FUNCTIONS_SCRIPT = """
    class Example:
        def test_method_1(self):
            if True:
                print("Hello, World!")
        def test_method_2(self):
            if False:
                print("Hello, World!")
    def test_function():
        if True:
            print("Hello, World!")
    def test_function_2():
        if False:
            print("Hello, World!")
    """

    def setUp(self):
        self.analyzer = PythonCyclomaticComplexityAnalyzer()

    def test_calculate_simple_script(self):
        parser = PythonAstParser()
        parser.parse(self.SIMPLE_SCRIPT)
        result = self.analyzer.calculate(parser)
        self.assertEqual(len(result["classes"]), 1)
        self.assertEqual(len(result["functions"]), 0)
        self.assertEqual(result["classes"][0]["name"], "Example")
        self.assertEqual(result["classes"][0]["methods"][0]["complexity"], 3)
        self.assertEqual(result["classes"][0]["methods"][0]["line_start"], 2)
        self.assertEqual(result["classes"][0]["methods"][0]["line_end"], 7)

    def test_calculate_medium_script(self):
        parser = PythonAstParser()
        parser.parse(self.MEDIUM_SCRIPT)
        result = self.analyzer.calculate(parser)
        self.assertEqual(len(result["classes"]), 1)
        self.assertEqual(len(result["functions"]), 1)
        self.assertEqual(result["classes"][0]["name"], "Example")
        self.assertEqual(result["classes"][0]["methods"][0]["complexity"], 6)
        self.assertEqual(result["classes"][0]["methods"][0]["line_start"], 2)
        self.assertEqual(result["classes"][0]["methods"][0]["line_end"], 13)
        self.assertEqual(result["functions"][0]["name"], "test_function")
        self.assertEqual(result["functions"][0]["complexity"], 2)
        self.assertEqual(result["functions"][0]["line_start"], 13)
        self.assertEqual(result["functions"][0]["line_end"], 16)

    def test_calculate_complex_script(self):
        parser = PythonAstParser()
        parser.parse(self.COMPLEX_SCRIPT)
        result = self.analyzer.calculate(parser)
        self.assertEqual(len(result["classes"]), 1)
        self.assertEqual(len(result["functions"]), 1)
        self.assertEqual(result["classes"][0]["name"], "Example")
        self.assertEqual(result["classes"][0]["methods"][0]["complexity"], 14)
        self.assertEqual(result["classes"][0]["methods"][0]["line_start"], 2)
        self.assertEqual(result["classes"][0]["methods"][0]["line_end"], 26)
        self.assertEqual(result["functions"][0]["name"], "test_function")
        self.assertEqual(result["functions"][0]["complexity"], 6)
        self.assertEqual(result["functions"][0]["line_start"], 27)
        self.assertEqual(result["functions"][0]["line_end"], 35)

    def test_calculate_multiple_functions_script(self):
        parser = PythonAstParser()
        parser.parse(self.MULTIPLE_FUNCTIONS_SCRIPT)
        result = self.analyzer.calculate(parser)
        self.assertEqual(len(result["classes"]), 1)
        self.assertEqual(len(result["functions"]), 2)
        self.assertEqual(result["classes"][0]["name"], "Example")
        self.assertEqual(result["classes"][0]["methods"][0]["complexity"], 2)
        self.assertEqual(result["classes"][0]["methods"][0]["line_start"], 2)
        self.assertEqual(result["classes"][0]["methods"][0]["line_end"], 5)
        self.assertEqual(result["classes"][0]["methods"][1]["complexity"], 2)
        self.assertEqual(result["classes"][0]["methods"][1]["line_start"], 5)
        self.assertEqual(result["classes"][0]["methods"][1]["line_end"], 8)
        self.assertEqual(result["functions"][0]["name"], "test_function")
        self.assertEqual(result["functions"][0]["complexity"], 2)
        self.assertEqual(result["functions"][0]["line_start"], 8)
        self.assertEqual(result["functions"][0]["line_end"], 11)
        self.assertEqual(result["functions"][1]["name"], "test_function_2")
        self.assertEqual(result["functions"][1]["complexity"], 2)
        self.assertEqual(result["functions"][1]["line_start"], 11)
        self.assertEqual(result["functions"][1]["line_end"], 14)
