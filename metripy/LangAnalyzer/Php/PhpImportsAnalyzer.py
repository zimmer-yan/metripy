from metripy.LangAnalyzer.Generic.Metrics.GenericImportsAnalyzer import (
    GenericImportsAnalyzer,
)
from metripy.LangAnalyzer.Generic.Ast.AstParser import AstParser


class PhpImportsAnalyzer(GenericImportsAnalyzer):
    def extract_import_name(self, filename: str, parser: AstParser) -> str:
        return parser.get_fqcn(filename)

    def extract_imports(self, filename: str, parser: AstParser) -> list[str]:
        imports = []
        for node in parser.get_import_nodes():
            imports.append(parser.extract_import_qualified_name(node))
        return imports
