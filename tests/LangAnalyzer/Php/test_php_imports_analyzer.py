from unittest import TestCase
from metripy.LangAnalyzer.Php.PhpImportsAnalyzer import PhpImportsAnalyzer

class TestPhpImportsAnalyzer(TestCase):

    SIMPLE_SCRIPT = """
    <?php
    namespace App\\Test;
    use App\\Test\\TestClass2;
    use App\\Test\\TestClass3;

    class TestClass1 {
    }
    """

    def test_extract(self):
        analyzer = PhpImportsAnalyzer("test.php", self.SIMPLE_SCRIPT)
        self.assertEqual(analyzer.extract_import_name(), "App\\Test\\TestClass1")
        self.assertEqual(analyzer.extract_imports(), ["App\\Test\\TestClass2", "App\\Test\\TestClass3"])
