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
    function testFunction() {
        echo 'Hello, World!';
        return true;
    }
    """

    ATTRIBUTE_SCRIPT = """
    <?php
    class Example {
        public function __construct() {
            $this->a = 0;
            $this->b = 0;
        }

        public function method1() {
            return $this->a;
        }

        public function method2() {
            return $this->method1();
        }
    }
    """

    USAGE_SCRIPT = """
    <?
    namespace App\\Test;
    
    class TestClass {
        /**
         * @var Bar
         */
        private $bar;

        /**
         * @param Baz[] $y
         * @return Qux
         * @throws Quux
         */
        public function testMethod(Foo $x, array $y): mixed {
            return $x;
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
        self.assertEqual(self.parser.extract_function_name(methods[0]), "testMethod")

    def test_get_function_nodes(self):
        function_nodes = self.parser.get_function_nodes()
        self.assertEqual(len(function_nodes), 2)
        self.assertEqual(
            self.parser.extract_function_name(function_nodes[1]), "testMethod"
        )
        self.assertEqual(
            self.parser.extract_function_name(function_nodes[0]), "testFunction"
        )

    def test_get_function_attributes(self):
        parser = PhpAstParser()
        parser.parse(self.ATTRIBUTE_SCRIPT)
        function_nodes = parser.get_function_nodes()
        self.assertEqual(len(function_nodes), 3)
        self.assertEqual(
            parser.get_function_attributes(function_nodes[0]), ["$this->a", "$this->b"]
        )
        self.assertEqual(
            parser.get_function_attributes(function_nodes[1]), ["$this->a"]
        )
        self.assertEqual(parser.get_function_attributes(function_nodes[2]), [])

    def test_get_function_self_calls(self):
        parser = PhpAstParser()
        parser.parse(self.ATTRIBUTE_SCRIPT)
        function_nodes = parser.get_function_nodes()
        self.assertEqual(len(function_nodes), 3)
        self.assertEqual(parser.get_function_self_calls(function_nodes[0]), [])
        self.assertEqual(parser.get_function_self_calls(function_nodes[1]), [])
        self.assertEqual(parser.get_function_self_calls(function_nodes[2]), ["method1"])

    def test_get_identifier_nodes_usage(self):
        parser = PhpAstParser()
        parser.parse(self.USAGE_SCRIPT)
        from metripy.DebugUtils.AstDumper import AstDumper
        dumper = AstDumper(parser)
        #dumper.dump_all()
        identifier_nodes = parser.get_identifier_nodes("usage")
        names = [parser.get_node_text(node) for node in identifier_nodes]
        self.assertIn("Foo", names)
        self.assertIn("Bar", names)
        self.assertIn("Baz", names)
        self.assertIn("Qux", names)
        self.assertIn("Quux", names)
