from metripy.LangAnalyzer.Generic.CodeSmell.Detectors.NamingConventionDetector import (
    NamingConventionDetector,
)
from metripy.LangAnalyzer.Generic.CodeSmell.CodeSmell import (
    CodeSmellType,
    CodeSmellSeverity,
)


class TypescriptNamingConventionDetector(NamingConventionDetector):
    def _get_naming_rules(self) -> dict[str, dict]:
        return {
            "class": {
                "pattern": r"^[A-Z][a-zA-Z0-9]*$",
                "description": "PascalCase",
                "smell_type": CodeSmellType.PASCAL_CASE_VIOLATION_CLASS,
                "severity": CodeSmellSeverity.MINOR,
                "excludes": [],
            },
            "function": {
                "pattern": r"^[a-z][a-zA-Z0-9]*$",
                "description": "camelCase",
                "smell_type": CodeSmellType.SNAKE_CASE_VIOLATION_FUNCTION,
                "severity": CodeSmellSeverity.MINOR,
                "excludes": [],
            },
            "variable": {
                "pattern": r"^[a-z][a-zA-Z0-9]*$",
                "description": "camelCase",
                "smell_type": CodeSmellType.SNAKE_CASE_VIOLATION_VARIABLE,
                "severity": CodeSmellSeverity.INFO,
                "excludes": [],
            },
            "constant": {
                "pattern": r"^[A-Z][A-Z0-9_]*$",
                "description": "SCREAMING_SNAKE_CASE",
                "smell_type": CodeSmellType.SCREAMING_SNAKE_CASE_VIOLATION_CONSTANT,
                "severity": CodeSmellSeverity.MINOR,
                "excludes": [],
            },
        }
