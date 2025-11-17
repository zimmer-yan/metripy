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
