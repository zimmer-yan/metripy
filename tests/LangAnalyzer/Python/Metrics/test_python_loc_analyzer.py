from unittest import TestCase

from metripy.LangAnalyzer.Python.Metrics.PythonLocAnalyzer import PythonLocAnalyzer


class TestPythonLocAnalyzer(TestCase):

    SIMPLE_SCRIPT = """print("Hello, World!")
    # This is a comment
    x = 1
    """

    MEDIUM_SCRIPT = """import foobar
    def test_function(x):
        '''this function does soemthing'''
        if foobar.evaluate(x):
            print("x is valid")
        else:
            # this is bad
            raise ValueError("x is invalid")

        return x
    """

    COMPLEX_SCRIPT = """import foo
    class ComplexClass:
        '''this class is complex'''

        def __init__(self, x):
            self.x = x

        def complex_method(self):
            '''
            this method is very complex
            it needs a lot of comments
            '''
            if foo.evaluate(self.x):
                print("x is valid")
            else:
                # this is bad
                print("error"); raise ValueError("x is invalid")

            return self.x
        """

    def setUp(self):
        self.analyzer = PythonLocAnalyzer()

    def test_analyze_simple_script(self):
        result = self.analyzer.analyze(self.SIMPLE_SCRIPT)
        self.assertEqual(result["loc"], 4)
        self.assertEqual(result["sloc"], 2)
        self.assertEqual(result["lloc"], 2)
        self.assertEqual(result["comments"], 1)
        self.assertEqual(result["single_comments"], 1)
        self.assertEqual(result["multiline_comments"], 0)
        self.assertEqual(result["blank_lines"], 1)

    def test_analyze_medium_script(self):
        result = self.analyzer.analyze(self.MEDIUM_SCRIPT)
        self.assertEqual(result["loc"], 11)
        self.assertEqual(result["sloc"], 7)
        self.assertEqual(result["lloc"], 7)
        self.assertEqual(result["comments"], 2)
        self.assertEqual(result["single_comments"], 2)
        self.assertEqual(result["multiline_comments"], 0)
        self.assertEqual(result["blank_lines"], 2)

    def test_analyze_complex_script(self):
        result = self.analyzer.analyze(self.COMPLEX_SCRIPT)
        self.assertEqual(result["loc"], 20)
        self.assertEqual(result["sloc"], 10)
        self.assertEqual(result["lloc"], 11)
        self.assertEqual(result["comments"], 6)
        self.assertEqual(result["single_comments"], 2)
        self.assertEqual(result["multiline_comments"], 4)
        self.assertEqual(result["blank_lines"], 4)
