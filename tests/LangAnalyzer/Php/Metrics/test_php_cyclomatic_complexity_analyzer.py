from unittest import TestCase
from metripy.LangAnalyzer.Php.Metrics.PhpCyclomaticComplexityAnalyzer import (
    PhpCyclomaticComplexityAnalyzer,
)
from metripy.LangAnalyzer.Php.Ast.PhpAstParser import PhpAstParser


class TestPhpCyclomaticComplexityAnalyzer(TestCase):

    SIMPLE_SCRIPT = """
    <?php
    class Example {
        public function test_method() {
            if (true) {
                echo "Hello, World!";
            } else {
                echo "Hello, World!";
            }
        }
    }
    """

    MEDIUM_SCRIPT = """
    <?php
    class Example {
        public function test_method() {
            for ($i = 0; $i < 10; $i++) {
                echo $i;
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
    }
    function test_function() {
        if (true) {
            echo "Hello, World!";
        }
    }
    """
    COMPLEX_SCRIPT = """
    <?php
    class Example {
        public function test_method($data) {
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
                    } else {
                        echo "Non-positive";
                    }
                }
            }
        }
    }
    function test_function($data) {
        for ($i = 0; $i < count($data); $i++) {
            if ($data[$i] > 0) {
                for ($j = 0; $j < $data[$i]; $j++) {
                    if ($j % 2 == 0) {
                        echo "Even";
                    } else {
                        echo "Odd";
                    }
                }
            }
        }
    }
    """

    MULTIPLE_FUNCTIONS_SCRIPT = """
    <?php
    class Example {
        public function test_method_1() {
            if (true) {
                echo "Hello, World!";
            }
        }
        public function test_method_2() {
            if (false) {
                echo "Hello, World!";
            }
        }
    }
    function test_function() {
        if (true) {
            echo "Hello, World!";
        }
    }
    function test_function_2() {
        if (false) {
            echo "Hello, World!";
        }
    }
    """

    def setUp(self):
        self.analyzer = PhpCyclomaticComplexityAnalyzer()

    def test_calculate_simple_script(self):
        parser = PhpAstParser()
        parser.parse(self.SIMPLE_SCRIPT)
        result = self.analyzer.calculate(parser)
        self.assertEqual(len(result["classes"]), 1)
        self.assertEqual(len(result["functions"]), 0)
        self.assertEqual(result["classes"][0]["methods"][0]["complexity"], 3)
        self.assertEqual(result["classes"][0]["methods"][0]["line_start"], 3)
        self.assertEqual(result["classes"][0]["methods"][0]["line_end"], 10)

    def test_calculate_medium_script(self):
        parser = PhpAstParser()
        parser.parse(self.MEDIUM_SCRIPT)
        result = self.analyzer.calculate(parser)
        self.assertEqual(len(result["classes"]), 1)
        self.assertEqual(len(result["functions"]), 1)
        self.assertEqual(result["classes"][0]["name"], "Example")
        self.assertEqual(result["classes"][0]["methods"][0]["complexity"], 6)
        self.assertEqual(result["classes"][0]["methods"][0]["line_start"], 3)
        self.assertEqual(result["classes"][0]["methods"][0]["line_end"], 18)
        self.assertEqual(result["functions"][0]["name"], "test_function")
        self.assertEqual(result["functions"][0]["complexity"], 2)
        self.assertEqual(result["functions"][0]["line_start"], 19)
        self.assertEqual(result["functions"][0]["line_end"], 24)

    def test_calculate_complex_script(self):
        parser = PhpAstParser()
        parser.parse(self.COMPLEX_SCRIPT)
        result = self.analyzer.calculate(parser)
        self.assertEqual(len(result["classes"]), 1)
        self.assertEqual(len(result["functions"]), 1)
        self.assertEqual(result["classes"][0]["name"], "Example")
        self.assertEqual(result["classes"][0]["methods"][0]["complexity"], 15)
        self.assertEqual(result["classes"][0]["methods"][0]["line_start"], 3)
        self.assertEqual(result["classes"][0]["methods"][0]["line_end"], 36)
        self.assertEqual(result["functions"][0]["name"], "test_function")
        self.assertEqual(result["functions"][0]["complexity"], 6)
        self.assertEqual(result["functions"][0]["line_start"], 37)
        self.assertEqual(result["functions"][0]["line_end"], 50)

    def test_calculate_multiple_functions_script(self):
        parser = PhpAstParser()
        parser.parse(self.MULTIPLE_FUNCTIONS_SCRIPT)
        result = self.analyzer.calculate(parser)
        self.assertEqual(len(result["classes"]), 1)
        self.assertEqual(len(result["functions"]), 2)
        self.assertEqual(result["classes"][0]["name"], "Example")
        self.assertEqual(result["classes"][0]["methods"][0]["complexity"], 2)
        self.assertEqual(result["classes"][0]["methods"][0]["line_start"], 3)
        self.assertEqual(result["classes"][0]["methods"][0]["line_end"], 8)
        self.assertEqual(result["classes"][0]["methods"][1]["complexity"], 2)
        self.assertEqual(result["classes"][0]["methods"][1]["line_start"], 8)
        self.assertEqual(result["classes"][0]["methods"][1]["line_end"], 13)
        self.assertEqual(result["functions"][0]["name"], "test_function")
        self.assertEqual(result["functions"][0]["complexity"], 2)
        self.assertEqual(result["functions"][0]["line_start"], 14)
        self.assertEqual(result["functions"][0]["line_end"], 19)
        self.assertEqual(result["functions"][1]["name"], "test_function_2")
        self.assertEqual(result["functions"][1]["complexity"], 2)
        self.assertEqual(result["functions"][1]["line_start"], 19)
        self.assertEqual(result["functions"][1]["line_end"], 24)

    def test_empty_class(self):
        parser = PhpAstParser()
        parser.parse(
            """
        <?php
        class Example {
        }
        """
        )
        result = self.analyzer.calculate(parser)
        self.assertEqual(len(result["classes"]), 1)
        self.assertEqual(len(result["functions"]), 0)
        self.assertEqual(result["classes"][0]["name"], "Example")
        self.assertEqual(result["classes"][0]["methods"], [])

    def test_if_decision_types(self):
        parser = PhpAstParser()
        parser.parse(
            """
        <?php
        function test_function() {
            if (true) {
                echo "Hello, World!";
            } elseif (false) {
                echo "Hello, World!";
            } else {
                echo "Hello, World!";
            }
        }
        """
        )
        result = self.analyzer.calculate(parser)
        self.assertEqual(len(result["functions"]), 1)
        self.assertEqual(result["functions"][0]["name"], "test_function")
        self.assertEqual(result["functions"][0]["complexity"], 4)
        self.assertEqual(result["functions"][0]["line_start"], 2)
        self.assertEqual(result["functions"][0]["line_end"], 11)

    def test_loop_decision_types(self):
        parser = PhpAstParser()
        parser.parse(
            """
        <?php
        function test_function() {
            for ($i = 0; $i < 10; $i++) {
                echo $i;
            }
            foreach ($array as $value) {
                echo $value;
            }
            do {
                echo "Hello, World!";
            } while (true);
        }
        """
        )
        result = self.analyzer.calculate(parser)
        self.assertEqual(len(result["functions"]), 1)
        self.assertEqual(result["functions"][0]["name"], "test_function")
        self.assertEqual(result["functions"][0]["complexity"], 5)
        self.assertEqual(result["functions"][0]["line_start"], 2)
        self.assertEqual(result["functions"][0]["line_end"], 13)

    def test_try_catch_decision_types(self):
        parser = PhpAstParser()
        parser.parse(
            """
        <?php
        function test_function() {
            try {
                throw new Exception("Hello, World!");
            } catch (Exception $e) {
                echo $e;
            } finally {
                echo "Hello, World!";
            }
        }
        """
        )
        result = self.analyzer.calculate(parser)
        self.assertEqual(len(result["functions"]), 1)
        self.assertEqual(result["functions"][0]["name"], "test_function")
        self.assertEqual(result["functions"][0]["complexity"], 5)
        self.assertEqual(result["functions"][0]["line_start"], 2)
        self.assertEqual(result["functions"][0]["line_end"], 11)

    def test_switch_decision_types(self):
        parser = PhpAstParser()
        parser.parse(
            """
        <?php
        function test_function() {
            switch ($x) {
                case 1:
                    echo "Hello, World!";
                default:
                    echo "Hello, World!";
            }
            match ($x) {
                1 => "Hello, World!",
            }
        }
        """
        )
        result = self.analyzer.calculate(parser)
        self.assertEqual(len(result["functions"]), 1)
        self.assertEqual(result["functions"][0]["name"], "test_function")
        self.assertEqual(result["functions"][0]["complexity"], 6)
        self.assertEqual(result["functions"][0]["line_start"], 2)
        self.assertEqual(result["functions"][0]["line_end"], 13)

    def test_loop_control_decision_types(self):
        parser = PhpAstParser()
        parser.parse(
            """
        <?php
        function test_function() {
            for ($i = 0; $i < 10; $i++) {
                break;
                continue;
                return;
                yield "Hello, World!";
            }
        }
        """
        )
        result = self.analyzer.calculate(parser)
        self.assertEqual(len(result["functions"]), 1)
        self.assertEqual(result["functions"][0]["name"], "test_function")
        self.assertEqual(result["functions"][0]["complexity"], 6)
        self.assertEqual(result["functions"][0]["line_start"], 2)
        self.assertEqual(result["functions"][0]["line_end"], 10)

    def test_boolean_decision_types(self):
        parser = PhpAstParser()
        parser.parse(
            """
        <?php
        function test_function() {
            $a = true || false;
            $a = true && false;
            $a = true xor false;
            $a = true & false;
            $a = null | true;
        }
        """
        )
        result = self.analyzer.calculate(parser)
        self.assertEqual(len(result["functions"]), 1)
        self.assertEqual(result["functions"][0]["name"], "test_function")
        self.assertEqual(result["functions"][0]["complexity"], 6)
        self.assertEqual(result["functions"][0]["line_start"], 2)
        self.assertEqual(result["functions"][0]["line_end"], 9)

    def test_question_mark_operator_decision_types(self):
        parser = PhpAstParser()
        parser.parse(
            """
        <?php
        function test_function() {
            $a = true ? "Hello, World!" : "Hello, World!";
            $a = null ?? "Hello, World!";
        }
        """
        )
        result = self.analyzer.calculate(parser)
        self.assertEqual(len(result["functions"]), 1)
        self.assertEqual(result["functions"][0]["name"], "test_function")
        self.assertEqual(result["functions"][0]["complexity"], 3)
        self.assertEqual(result["functions"][0]["line_start"], 2)
        self.assertEqual(result["functions"][0]["line_end"], 6)
