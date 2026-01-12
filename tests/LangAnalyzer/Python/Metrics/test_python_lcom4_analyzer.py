from unittest import TestCase

from metripy.LangAnalyzer.Python.Ast.PythonAstParser import PythonAstParser
from metripy.LangAnalyzer.Python.Metrics.PythonLcom4Analyzer import PythonLcom4Analyzer


class TestPythonLcom4Analyzer(TestCase):
    CODE_LCOM4_0 = """
    class Example:
        def __init__(self):
            self.a = 0
            self.b = 0
    """

    CODE_LCOM4_1 = """
    class Example:
        def __init__(self):
            self.a = 0
            self.b = 0

        def method1(self):
            return self.a

        def method2(self):
            return self.b

        def method3(self):
            return self.a + self.b

        def method4(self):
            return self.method1() + self.method2()
    """
    CODE_LCOM4_1_2 = """
    class Example:
        def __init__(self):
            self.a = 0

        def method1(self):
            return self.a

        def method2(self):
            return self.a
    """

    CODE_LCOM4_2 = """
    class Example:
        def __init__(self):
            self.a = 0
            self.b = 0

        def method1(self):
            return self.a

        def method2(self):
            return self.b
    """

    def setUp(self):
        self.analyzer = PythonLcom4Analyzer()

    def test_get_lcom4_value_0(self):
        parser = PythonAstParser()
        parser.parse(self.CODE_LCOM4_0)
        result = self.analyzer.get_lcom4(parser)
        self.assertEqual(result["Example"], 0)

    def test_get_lcom4_value_1(self):
        parser = PythonAstParser()
        parser.parse(self.CODE_LCOM4_1)
        result = self.analyzer.get_lcom4(parser)
        self.assertEqual(result["Example"], 1)

    def test_get_lcom4_value_1_example_2(self):
        parser = PythonAstParser()
        parser.parse(self.CODE_LCOM4_1_2)
        result = self.analyzer.get_lcom4(parser)
        self.assertEqual(result["Example"], 1)

    def test_get_lcom4_value_2(self):
        parser = PythonAstParser()
        parser.parse(self.CODE_LCOM4_2)
        result = self.analyzer.get_lcom4(parser)
        self.assertEqual(result["Example"], 2)
