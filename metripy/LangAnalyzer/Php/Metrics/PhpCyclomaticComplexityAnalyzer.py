from metripy.LangAnalyzer.Generic.Metrics.GenericCyclomaticComplexityAnalyzer import (
    GenericCyclomaticComplexityAnalyzer,
)
from typing import List
from tree_sitter import Node


class PhpCyclomaticComplexityAnalyzer(GenericCyclomaticComplexityAnalyzer):
    def get_decision_types(self) -> List[str]:
        return [
            "if",
            "else",
            "elseif",
            "for",
            "foreach",
            "do",
            "while",
            "try",
            "catch",
            "finally",
            "throw",
            "switch",
            "case",
            "match",
            "match_block",
            "default",
            "yield_expression",
            "break",
            "continue",
            "return",
            "binary_expression",
            "conditional_expression",
            "coalesce_operator",
        ]

    def has_special_rule(self, type: str) -> bool:
        return type == "binary_expression"

    def eval_special_rule(self, node: Node) -> int:
        if node.type == "binary_expression":
            if node.children[1].type in [
                "??",
                "&&",
                "||",
                "xor",
                "&",
                "|",
                "^",
                "~",
                ">>",
                "<<",
            ]:
                return 1
        return 0
