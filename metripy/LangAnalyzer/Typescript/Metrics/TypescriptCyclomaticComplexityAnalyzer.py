from metripy.LangAnalyzer.Generic.Metrics.GenericCyclomaticComplexityAnalyzer import (
    GenericCyclomaticComplexityAnalyzer,
)

class TypescriptCyclomaticComplexityAnalyzer(GenericCyclomaticComplexityAnalyzer):
    def get_decision_types(self) -> list[str]:
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
        ]
