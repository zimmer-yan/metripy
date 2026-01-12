from unittest import TestCase
from metripy.LangAnalyzer.Typescript.TypescriptImportsAnalyzer import TypescriptImportsAnalyzer
from metripy.LangAnalyzer.Typescript.Ast.TypescriptAstParser import TypescriptAstParser
class TestTypescriptImportsAnalyzer(TestCase):
    SIMPLE_SCRIPT = """
    import { TestClass } from "./test.ts";
    import { TestClass2 } from "../test2.ts";

    class Foo {
    }
    """

    COMPLEX_SCRIPT = """
    import { TestClass } from "./test.service"

    class Foo {
    }
    """

    def setUp(self):
        self.analyzer = TypescriptImportsAnalyzer()

    def test_get_import_data(self):
        parser = TypescriptAstParser()
        parser.parse(self.SIMPLE_SCRIPT)
        name, imports = self.analyzer.get_import_data("./src/foo.ts", parser)
        self.assertEqual(name, "./src/foo")
        self.assertEqual(imports, ["./src/test", "./test2"])

    def test_get_import_data_complex(self):
        parser = TypescriptAstParser()
        parser.parse(self.COMPLEX_SCRIPT)
        name, imports = self.analyzer.get_import_data("./src/foo.service.ts", parser)
        self.assertEqual(name, "./src/foo.service")
        self.assertEqual(imports, ["./src/test.service"])
