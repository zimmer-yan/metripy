from metripy.LangAnalyzer.Generic.Metrics.GenericLcom4Analyzer import (
    GenericLcom4Analyzer,
)
from metripy.LangAnalyzer.Php.Metrics.PhpLcom4Analyzer import PhpLcom4Analyzer
from metripy.LangAnalyzer.Python.Metrics.PythonLcom4Analyzer import PythonLcom4Analyzer
from metripy.LangAnalyzer.Typescript.Metrics.TypescriptLcom4Analyzer import (
    TypescriptLcom4Analyzer,
)


class Lcom4AnalyzerFactory:
    _ANALYZERS = {
        "Python": PythonLcom4Analyzer(),
        "PHP": PhpLcom4Analyzer(),
        "Typescript": TypescriptLcom4Analyzer(),
    }

    @staticmethod
    def get_lcom4_analyzer(language: str) -> GenericLcom4Analyzer:
        try:
            return Lcom4AnalyzerFactory._ANALYZERS[language]
        except KeyError:
            raise ValueError(f"No lcom4 analyzer found for language: {language}")
