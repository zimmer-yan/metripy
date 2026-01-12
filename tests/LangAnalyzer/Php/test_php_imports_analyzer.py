from unittest import TestCase

from metripy.LangAnalyzer.Php.PhpImportsAnalyzer import PhpImportsAnalyzer
from metripy.LangAnalyzer.Php.Ast.PhpAstParser import PhpAstParser


class TestPhpImportsAnalyzer(TestCase):

    SIMPLE_SCRIPT = """
    <?php
    namespace App\\Test;
    use App\\Test\\TestClass2;
    use App\\Test\\TestClass3;

    class TestClass1 {
    }
    """

    def setUp(self):
        self.analyzer = PhpImportsAnalyzer()

    def test_extract_import_name(self):
        parser = PhpAstParser()
        parser.parse(self.SIMPLE_SCRIPT)
        self.assertEqual(
            self.analyzer.extract_import_name("test.php", parser),
            "App\\Test\\TestClass1",
        )
        self.assertEqual(
            self.analyzer.extract_imports("test.php", parser),
            ["App\\Test\\TestClass2", "App\\Test\\TestClass3"],
        )
