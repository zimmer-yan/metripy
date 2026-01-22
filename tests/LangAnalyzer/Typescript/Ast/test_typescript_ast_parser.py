from unittest import TestCase
from metripy.LangAnalyzer.Typescript.Ast.TypescriptAstParser import TypescriptAstParser


class TestTypescriptAstParser(TestCase):
    CLASS_SCRIPT = """
    class TestClass {
        constructor() {
            this.a = 0;
        }
        public testMethod() {
            console.log("Hello, World!");
        }
    }
    function testFunction() {
        console.log("Hello, World!");
    }
    """

    EXPORT_ARROW_FUNCTION_SCRIPT = """
    export const foo = () => {
        console.log("Hello, World!");
    }
    """

    ATTRIBUTE_SCRIPT = """
    class Example {
        constructor() {
            this.a = 0;
            this.b = 0;
        }
        public method1() {
            return this.a;
        }
        public method2() {
            return this.method1();
        }
    """

    def setUp(self):
        self.parser = TypescriptAstParser()

    def test_get_class_nodes(self):
        self.parser.parse(self.CLASS_SCRIPT)
        nodes = self.parser.get_class_nodes()
        self.assertEqual(len(nodes), 1)
        self.assertEqual(self.parser.extract_class_name(nodes[0]), "TestClass")

    def test_get_function_nodes(self):
        self.parser.parse(self.CLASS_SCRIPT)
        nodes = self.parser.get_function_nodes()
        self.assertEqual(len(nodes), 3)
        self.assertEqual(self.parser.extract_function_name(nodes[0]), "testFunction")
        self.assertEqual(self.parser.extract_function_name(nodes[1]), "constructor")
        self.assertEqual(self.parser.extract_function_name(nodes[2]), "testMethod")

    def test_get_class_methods(self):
        self.parser.parse(self.CLASS_SCRIPT)
        nodes = self.parser.get_class_nodes()
        self.assertEqual(len(nodes), 1)
        methods = self.parser.get_class_methods(nodes[0])
        self.assertEqual(len(methods), 2)
        self.assertEqual(self.parser.extract_function_name(methods[0]), "constructor")
        self.assertEqual(self.parser.extract_function_name(methods[1]), "testMethod")

    def test_get_export_arrow_function(self):
        self.parser.parse(self.EXPORT_ARROW_FUNCTION_SCRIPT)
        nodes = self.parser.get_function_nodes()
        self.assertEqual(len(nodes), 1)
        self.assertEqual(self.parser.extract_function_name(nodes[0]), "foo")

    def test_get_function_attributes(self):
        self.parser.parse(self.ATTRIBUTE_SCRIPT)
        function_nodes = self.parser.get_function_nodes()
        self.assertEqual(len(function_nodes), 3)
        self.assertEqual(
            self.parser.get_function_attributes(function_nodes[0]), ["this.a", "this.b"]
        )
        self.assertEqual(
            self.parser.get_function_attributes(function_nodes[1]), ["this.a"]
        )
        self.assertEqual(self.parser.get_function_attributes(function_nodes[2]), [])

    def test_get_function_self_calls(self):
        self.parser.parse(self.ATTRIBUTE_SCRIPT)
        function_nodes = self.parser.get_function_nodes()
        self.assertEqual(len(function_nodes), 3)
        self.assertEqual(self.parser.get_function_self_calls(function_nodes[0]), [])
        self.assertEqual(self.parser.get_function_self_calls(function_nodes[1]), [])
        self.assertEqual(
            self.parser.get_function_self_calls(function_nodes[2]), ["method1"]
        )


if __name__ == "__main__":
    filename = "./../../PhpstormProjects/ymmd-ddev-stack/talent-ui/src/helpers.ts"
    parser = TypescriptAstParser()
    parser.parse(open(filename, "r").read())
    from metripy.DebugUtils.AstDumper import AstDumper

    dumper = AstDumper(parser)
    dumper.dump_all()
    exit()
    functions = parser.get_identifier_nodes("usage")
