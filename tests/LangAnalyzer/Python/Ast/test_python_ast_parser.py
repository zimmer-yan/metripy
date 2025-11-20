from unittest import TestCase

from metripy.LangAnalyzer.Python.Ast.PythonAstParser import PythonAstParser


class TestPythonAstParser(TestCase):
    SIMPLE_SCRIPT = """
    import app.ParentClass
    import app.Interface1
    
    class TestClass(ParentClass, Interface1):
        def test_method(self, x: int, y: str) -> bool:
            print("Hello, World!")
            return True

    def test_function() -> bool:
        print("Hello, World!")
        return True
    """

    ATTRIBUTE_SCRIPT = """
    class Example:
        def __init__(self):
            self.a = 0
            self.b = 0

        def method1(self):
            return self.a

        def method2(self):
            return self.method1()
    """

    def setUp(self):
        self.parser = PythonAstParser()
        self.parser.parse(self.SIMPLE_SCRIPT)

    def test_get_import_nodes(self):
        import_nodes = self.parser.get_import_nodes()
        self.assertEqual(len(import_nodes), 2)
        self.assertEqual(
            self.parser.extract_import_name(import_nodes[0]), "ParentClass"
        )
        self.assertEqual(self.parser.extract_import_name(import_nodes[1]), "Interface1")
        self.assertEqual(
            self.parser.extract_import_qualified_name(import_nodes[0]),
            "app.ParentClass",
        )
        self.assertEqual(
            self.parser.extract_import_qualified_name(import_nodes[1]), "app.Interface1"
        )

    def test_get_function_nodes(self):
        function_nodes = self.parser.get_function_nodes()
        self.assertEqual(len(function_nodes), 2)
        self.assertEqual(
            self.parser.extract_function_name(function_nodes[0]), "test_method"
        )
        self.assertEqual(
            self.parser.extract_function_name(function_nodes[1]), "test_function"
        )

    def test_get_function_attributes(self):
        parser = PythonAstParser()
        parser.parse(self.ATTRIBUTE_SCRIPT)
        function_nodes = parser.get_function_nodes()
        self.assertEqual(len(function_nodes), 3)
        self.assertEqual(
            parser.get_function_attributes(function_nodes[0]), ["self.a", "self.b"]
        )
        self.assertEqual(parser.get_function_attributes(function_nodes[1]), ["self.a"])
        self.assertEqual(parser.get_function_attributes(function_nodes[2]), [])

    def test_get_function_self_calls(self):
        parser = PythonAstParser()
        parser.parse(self.ATTRIBUTE_SCRIPT)
        function_nodes = parser.get_function_nodes()
        self.assertEqual(len(function_nodes), 3)
        self.assertEqual(parser.get_function_self_calls(function_nodes[0]), [])
        self.assertEqual(parser.get_function_self_calls(function_nodes[1]), [])
        self.assertEqual(parser.get_function_self_calls(function_nodes[2]), ["method1"])
