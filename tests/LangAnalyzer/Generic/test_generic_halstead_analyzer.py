from unittest import TestCase

from metripy.LangAnalyzer.Generic.Metrics.GenericHalSteadAnalyzer import (
    GenericHalSteadAnalyzer,
)


class DummyHalSteadAnalyzer(GenericHalSteadAnalyzer):
    def get_operators(self) -> list[str]:
        return [
            "+",
            "=",
            "def",
            "return",
            "for",
            "in",
            "print",
            ":",
            "(",
            ")",
        ]


class TestGenericHalSteadAnalyzer(TestCase):
    EXAMPLE_CODE = """
    def add(a, b):
        return a + b

    def multiply(a, b):
        result = 0
        for _ in range(b):
            result = add(result, a)
        return result

    x = 5
    y = 3
    sum_result = add(x, y)
    product_result = multiply(x, y)
    print("Sum:", sum_result)
    print("Product:", product_result)
    """

    def setUp(self):
        self.analyzer = DummyHalSteadAnalyzer()

    def test_analysis(self):
        metrics = self.analyzer.calculate_halstead_metrics(self.EXAMPLE_CODE)

        self.assertIsInstance(metrics, dict)

        self.assertEqual(metrics["n1"], 10)
        self.assertEqual(metrics["n2"], 16)
        self.assertEqual(metrics["N1"], 36)
        self.assertEqual(metrics["N2"], 34)
        self.assertEqual(metrics["vocabulary"], 26)
        self.assertEqual(metrics["length"], 70)
        self.assertEqual(metrics["volume"], 329.0307802698764)
        self.assertEqual(metrics["difficulty"], 10.625)
        self.assertEqual(metrics["effort"], 3495.952040367437)
        self.assertEqual(metrics["calculated_length"], 97.21928094887363)
        self.assertEqual(metrics["bugs"], 0.07678134626668279)
        self.assertEqual(metrics["time"], 194.21955779819095)
