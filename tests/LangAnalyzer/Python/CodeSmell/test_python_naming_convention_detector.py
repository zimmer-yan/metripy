from unittest import TestCase

from metripy.Application.Config.CodeSmellConfig import CodeSmellConfig
from metripy.LangAnalyzer.Generic.CodeSmell.CodeSmell import (
    CodeSmellSeverity,
    CodeSmellType,
)
from metripy.LangAnalyzer.Python.Ast.PythonAstParser import PythonAstParser
from metripy.LangAnalyzer.Python.CodeSmell.PythonNamingConventionDetector import (
    PythonNamingConventionDetector,
)


class TestPythonNamingConventionDetector(TestCase):
    def test_no_naming_convention_violations(self):
        code = """
        class TestClass:
            def test_method(self):
                print('Hello, World!')
        """
        parser = PythonAstParser()
        parser.parse(code)
        detector = PythonNamingConventionDetector(
            filename="test.py", parser=parser, config=CodeSmellConfig()
        )
        smells = detector.detect()
        assert len(smells) == 0

    def test_class_name_not_pascal_case(self):
        code = """
class testClass:
    def test_method(self):
        print('Hello, World!')
"""
        parser = PythonAstParser()
        parser.parse(code)
        detector = PythonNamingConventionDetector(
            filename="test.py", parser=parser, config=CodeSmellConfig()
        )
        smells = detector.detect()
        assert len(smells) == 1
        assert smells[0].smell_type == CodeSmellType.PASCAL_CASE_VIOLATION_CLASS
        assert smells[0].severity == CodeSmellSeverity.MINOR
        assert smells[0].message == "Class name 'testClass' should use PascalCase"
        assert smells[0].line_number == 2
        assert smells[0].column == 0
        assert smells[0].filename == "test.py"

    def test_function_name_not_snake_case(self):
        code = """
class TestClass:
    def testMethod(self):
        print('Hello, World!')
"""
        parser = PythonAstParser()
        parser.parse(code)
        detector = PythonNamingConventionDetector(
            filename="test.py", parser=parser, config=CodeSmellConfig()
        )
        smells = detector.detect()
        assert len(smells) == 1
        assert smells[0].smell_type == CodeSmellType.SNAKE_CASE_VIOLATION_FUNCTION
        assert smells[0].severity == CodeSmellSeverity.MINOR
        assert smells[0].message == "Function name 'testMethod' should use snake_case"
        assert smells[0].line_number == 3
        assert smells[0].column == 4
        assert smells[0].filename == "test.py"
