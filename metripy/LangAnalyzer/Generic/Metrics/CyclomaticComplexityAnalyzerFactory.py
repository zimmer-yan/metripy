from metripy.LangAnalyzer.Generic.Metrics.GenericCyclomaticComplexityAnalyzer import (
    GenericCyclomaticComplexityAnalyzer,
)
from metripy.LangAnalyzer.Php.Metrics.PhpCyclomaticComplexityAnalyzer import (
    PhpCyclomaticComplexityAnalyzer,
)
from metripy.LangAnalyzer.Python.Metrics.PythonCyclomaticComplexityAnalyzer import (
    PythonCyclomaticComplexityAnalyzer,
)
from metripy.LangAnalyzer.Typescript.Metrics.TypescriptCyclomaticComplexityAnalyzer import (
    TypescriptCyclomaticComplexityAnalyzer,
)

class CyclomaticComplexityAnalyzerFactory:
    _ANALYZERS = {
        "Python": PythonCyclomaticComplexityAnalyzer(),
        "PHP": PhpCyclomaticComplexityAnalyzer(),
        "Typescript": TypescriptCyclomaticComplexityAnalyzer(),
    }

    @staticmethod
    def get_cyclomatic_complexity_analyzer(
        language: str,
    ) -> GenericCyclomaticComplexityAnalyzer:
        try:
            return CyclomaticComplexityAnalyzerFactory._ANALYZERS[language]
        except KeyError:
            raise ValueError(
                f"No cyclomatic complexity analyzer found for language: {language}"
            )
