from metripy.LangAnalyzer.Generic.Ast.AstParser import AstParser
from metripy.LangAnalyzer.Php.Ast.PhpAstParser import PhpAstParser
from metripy.LangAnalyzer.Python.Ast.PythonAstParser import PythonAstParser
from metripy.LangAnalyzer.Typescript.Ast.TypescriptAstParser import TypescriptAstParser


class AstParserFactory:
    _PARSERS = {
        "Python": PythonAstParser(),
        "PHP": PhpAstParser(),
        "Typescript": TypescriptAstParser(),
    }

    @staticmethod
    def get_ast_parser(language: str) -> AstParser:
        try:
            return AstParserFactory._PARSERS[language]
        except KeyError:
            raise ValueError(f"No ast parser found for language: {language}")
