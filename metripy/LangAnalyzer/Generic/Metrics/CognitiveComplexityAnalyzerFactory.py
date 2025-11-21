from metripy.LangAnalyzer.Generic.Metrics.GenericCognitiveComplexityAnalyzer import (
    GenericCognitiveComplexityCalculator,
)
from metripy.LangAnalyzer.Php.Metrics.PhpCognitiveComplexityCalculator import (
    PhpCognitiveComplexityCalculator,
)
from metripy.LangAnalyzer.Python.Metrics.PythonCognitiveComplexityCalculator import (
    PythonCognitiveComplexityCalculator,
)


class CognitiveComplexityAnalyzerFactory:
    _ANALYZERS = {
        "Python": PythonCognitiveComplexityCalculator(),
        "PHP": PhpCognitiveComplexityCalculator(),
        "Typescript": None,
    }

    @staticmethod
    def get_cognitive_complexity_analyzer(
        language: str,
    ) -> GenericCognitiveComplexityCalculator:
        try:
            return CognitiveComplexityAnalyzerFactory._ANALYZERS[language]
        except KeyError:
            raise ValueError(
                f"No cognitive complexity analyzer found for language: {language}"
            )
