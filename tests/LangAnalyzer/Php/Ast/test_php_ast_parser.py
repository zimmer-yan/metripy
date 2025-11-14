from unittest import TestCase

from metripy.LangAnalyzer.Php.Ast.PhpAstParser import PhpAstParser


class TestPhpAstParser(TestCase):
    SIMPLE_SCRIPT = """
    <?php
    namespace App\\Test;
    use App\\ParentClass;
    use App\\Interface1;
    
    class TestClass extends ParentClass implements Interface1 {
        public function testMethod(int $x, string $y): bool {
            echo 'Hello, World!';
            return true;
        }
    }
    """

    def setUp(self):
        self.parser = PhpAstParser()
        self.parser.parse(self.SIMPLE_SCRIPT)

    def test_get_fqcn(self):
        fqcn = self.parser.get_fqcn("for_fallback")
        self.assertEqual(fqcn, "App\\Test\\TestClass")

    def test_get_import_nodes(self):
        import_nodes = self.parser.get_import_nodes()
        self.assertEqual(len(import_nodes), 2)

        self.assertEqual(
            self.parser.extract_import_name(import_nodes[0]), "ParentClass"
        )
        self.assertEqual(self.parser.extract_import_name(import_nodes[1]), "Interface1")
        self.assertEqual(
            self.parser.extract_import_qualified_name(import_nodes[0]),
            "App\\ParentClass",
        )
        self.assertEqual(
            self.parser.extract_import_qualified_name(import_nodes[1]),
            "App\\Interface1",
        )

    def test_get_class_nodes(self):
        class_nodes = self.parser.get_class_nodes()
        self.assertEqual(len(class_nodes), 1)
        self.assertEqual(self.parser.extract_class_name(class_nodes[0]), "TestClass")

    def test_get_class_methods(self):
        class_node = self.parser.get_class_nodes()[0]

        methods = self.parser.get_class_methods(class_node)
        self.assertEqual(len(methods), 1)
        self.assertEqual(methods[0], "testMethod")
