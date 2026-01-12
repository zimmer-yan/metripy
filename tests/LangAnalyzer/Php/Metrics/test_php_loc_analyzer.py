from unittest import TestCase

from metripy.LangAnalyzer.Php.Metrics.PhpLocAnalyzer import PhpLocAnalyzer


class TestPhpLocAnalyzer(TestCase):

    SIMPLE_SCRIPT = """<?php
    // This is a comment
    $x = 1;
    """

    MEDIUM_SCRIPT = """<?php
    function test_function($x) {
        /* this is a comment */
        if ($x > 0) {
            echo "x is greater than 0";
        } else {
            // this is bad
            throw new Exception("x is invalid");
        }

        return $x;
    }
    """

    COMPLEX_SCRIPT = """<?php
    /** this class is complex */
    class ComplexClass {

        public function __construct($x) {
            $this->x = $x;
        }

        public function complex_method() {
            /* 
            this method is very complex
            it needs a lot of comments
            */
            if ($this->x > 0) {
                echo "x is greater than 0";
            } else {
                # this is bad
                echo "error"; throw new Exception("x is invalid");
            }

            return $this->x;
        }
    }
    """

    def setUp(self):
        self.analyzer = PhpLocAnalyzer()

    def test_analyze_simple_script(self):
        result = self.analyzer.analyze(self.SIMPLE_SCRIPT)
        self.assertEqual(result["loc"], 4)
        self.assertEqual(result["sloc"], 2)
        self.assertEqual(result["lloc"], 2)
        self.assertEqual(result["comments"], 1)
        self.assertEqual(result["single_comments"], 1)
        self.assertEqual(result["multiline_comments"], 0)
        self.assertEqual(result["blank_lines"], 1)

    def test_analyze_medium_script(self):
        result = self.analyzer.analyze(self.MEDIUM_SCRIPT)
        self.assertEqual(result["loc"], 13)
        self.assertEqual(result["sloc"], 9)
        self.assertEqual(result["lloc"], 9)
        self.assertEqual(result["comments"], 2)
        self.assertEqual(result["single_comments"], 2)
        self.assertEqual(result["multiline_comments"], 0)
        self.assertEqual(result["blank_lines"], 2)

    def test_analyze_complex_script(self):
        result = self.analyzer.analyze(self.COMPLEX_SCRIPT)
        self.assertEqual(result["loc"], 24)
        self.assertEqual(result["sloc"], 14)
        self.assertEqual(result["lloc"], 15)
        self.assertEqual(result["comments"], 6)
        self.assertEqual(result["single_comments"], 2)
        self.assertEqual(result["multiline_comments"], 4)
        self.assertEqual(result["blank_lines"], 4)
