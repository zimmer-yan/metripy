from unittest import TestCase
from metripy.LangAnalyzer.Php.PhpBasicLocAnalyzer import PhpBasicLocAnalyzer

class TestPhpBasicLocAnalyzer(TestCase):

    SIMPLE_SCRIPT = """
    <?php
    $x = 1;
    $y = 2;
    $z = $x + $y;

    // echo the result
    echo $z;
    """

    MEDIUM_SCRIPT = """
    <?php
    // asignment
    $x = 1;
    $y = 2;
    $z = $x + $y;

    // check here if z is greater than 3
    if ($z > 3) {
        echo 'z is greater than 3';
    } else {
        echo 'z is less than or equal to 3';
    }

    echo "done";
    """

    def test_get_loc_metrics_single_line_script(self):
        analyzer = PhpBasicLocAnalyzer()
        metrics = analyzer.get_loc_metrics("<?php echo 'Hello, World!'; ?>", "test.php")
        self.assertEqual(metrics["lines"], 1)
        self.assertEqual(metrics["linesOfCode"], 1)
        self.assertEqual(metrics["logicalLinesOfCode"], 1)
        self.assertEqual(metrics["commentLines"], 0)
        self.assertEqual(metrics["blankLines"], 0)

    def test_get_loc_metrics_simple_script(self):
        analyzer = PhpBasicLocAnalyzer()
        metrics = analyzer.get_loc_metrics(self.SIMPLE_SCRIPT, "test.php")
        self.assertEqual(metrics["lines"], 9)
        self.assertEqual(metrics["linesOfCode"], 5)
        self.assertEqual(metrics["logicalLinesOfCode"], 5)
        self.assertEqual(metrics["commentLines"], 1)
        # 1 in the middle, start and end are blank
        self.assertEqual(metrics["blankLines"], 3)

    def test_get_loc_metrics_medium_script(self):
        analyzer = PhpBasicLocAnalyzer()
        metrics = analyzer.get_loc_metrics(self.MEDIUM_SCRIPT, "test.php")
        self.assertEqual(metrics["lines"], 16)
        self.assertEqual(metrics["linesOfCode"], 10)
        self.assertEqual(metrics["logicalLinesOfCode"], 10)
        self.assertEqual(metrics["commentLines"], 2)
        self.assertEqual(metrics["blankLines"], 4)

    # TODO: more test cases
