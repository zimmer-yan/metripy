from metripy.LangAnalyzer.Generic.Metrics.GenericCyclomaticComplexityAnalyzer import (
    GenericCyclomaticComplexityAnalyzer,
)
from typing import List


class PythonCyclomaticComplexityAnalyzer(GenericCyclomaticComplexityAnalyzer):
    def get_decision_types(self) -> List[str]:
        return [
            "if_statement",
            "elif_clause",
            "else_clause",
            "for_statement",
            "while_statement",
            "try_statement",
            "except_clause",
            "switch_statement",
            "case_statement",
            "conditional_expression",
            "logical_operator",
        ]
