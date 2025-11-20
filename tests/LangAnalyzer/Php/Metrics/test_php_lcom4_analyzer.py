from unittest import TestCase

from metripy.LangAnalyzer.Php.Ast.PhpAstParser import PhpAstParser
from metripy.LangAnalyzer.Php.Metrics.PhpLcom4Analyzer import PhpLcom4Analyzer


class TestPhpLcom4Analyzer(TestCase):
    CODE_LCOM4_0 = """
    <?php
    class Example {
        public function __construct() {
            $this->a = 0;
            $this->b = 0;
        }
    }
    """

    CODE_LCOM4_1 = """
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
            return $this->b;
        }

        public function method3() {
            return $this->a + $this->b;
        }

        public function method4() {
            return $this->method1() + $this->method2();
        }
    }
    """
    CODE_LCOM4_1_2 = """
    <?php
    class Example {
        def __init__(self):
            $this->a = 0;
        }

        public function method1() {
            return $this->a;
        }

        public function method2() {
            return $this->a;
        }
    }
    """

    CODE_LCOM4_2 = """
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
            return $this->b;
        }
    """

    def setUp(self):
        self.analyzer = PhpLcom4Analyzer()

    """
    def test_get_lcom4_value_0(self):
        parser = PhpAstParser()
        parser.parse(self.CODE_LCOM4_0)
        result = self.analyzer.get_lcom4(parser)
        self.assertEqual(result["Example"], 0)
    """

    def test_get_lcom4_value_1(self):
        parser = PhpAstParser()
        parser.parse(self.CODE_LCOM4_1)
        result = self.analyzer.get_lcom4(parser)
        self.assertEqual(result["Example"], 1)

    """
    def test_get_lcom4_value_1_example_2(self):
        parser = PhpAstParser()
        parser.parse(self.CODE_LCOM4_1_2)
        result = self.analyzer.get_lcom4(parser)
        self.assertEqual(result["Example"], 1)

    def test_get_lcom4_value_2(self):
        parser = PhpAstParser()
        parser.parse(self.CODE_LCOM4_2)
        result = self.analyzer.get_lcom4(parser)
        self.assertEqual(result["Example"], 2)
    """
