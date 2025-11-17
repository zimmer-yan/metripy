from unittest import TestCase

from metripy.LangAnalyzer.Php.Ast.PhpAstParser import PhpAstParser
from metripy.LangAnalyzer.Php.Metrics.PhpCognitiveComplexityCalculator import (
    PhpCognitiveComplexityCalculator,
)


class TestPhpCognitiveComplexityCalculator(TestCase):

    SIMPLE_SCRIPT = """
    <?php
    function test_function() {
        if (true) {
            echo "Hello, World!";
        } else {
            echo "Hello, World!";
        }
    }
    """
    MEDIUM_SCRIPT = """
    <?php
    function test_function() {
        for ($i = 0; $i < 10; $i++) {
            echo $i
            if ($i % 2 == 0) {
                echo "Even";
            } else {
                echo "Odd";
            }
        }
        try {
            echo "Hello, World!";
        } catch (Exception $e) {
            echo $e;
        }
    }
    """
    COMPLEX_SCRIPT = """
    <?php
    function test_function($data) {
        for ($i = 0; $i < count($data); $i++) {
            if ($data[$i] > 0) {
                for ($j = 0; $j < $data[$i]; $j++) {
                    if ($j % 2 == 0) {
                        echo "Even";
                    } else {
                        echo "Odd";
                    }
                    if ($j > 5) {
                        echo "Large";
                    } else {
                        echo "Small";
                    }
                if ($data[$i] > 100) {
                    try {
                        if ($data[$i] % 10 == 0) {
                            echo "Divisible by 10";
                        } else {
                            echo "Not divisible by 10";
                        }
                    } catch (Exception $e) {
                        echo $e;
                    } finally {
                        echo "Cleanup";
                    }
                }
            } else {
                echo "Non-positive";
            }
        }
    }
    """

    def test_simple_script(self):
        parser = PhpAstParser()
        parser.parse(self.SIMPLE_SCRIPT)
        calculator = PhpCognitiveComplexityCalculator(parser)
        result = calculator.calculate_for_all_functions()
        self.assertEqual(result["test_function"], 1)

    def test_medium_script(self):
        parser = PhpAstParser()
        parser.parse(self.MEDIUM_SCRIPT)
        calculator = PhpCognitiveComplexityCalculator(parser)
        result = calculator.calculate_for_all_functions()
        self.assertEqual(result["test_function"], 6)

    def test_complex_script(self):
        parser = PhpAstParser()
        parser.parse(self.COMPLEX_SCRIPT)
        calculator = PhpCognitiveComplexityCalculator(parser)
        result = calculator.calculate_for_all_functions()
        # why 35 not 31?
        self.assertEqual(result["test_function"], 35)
