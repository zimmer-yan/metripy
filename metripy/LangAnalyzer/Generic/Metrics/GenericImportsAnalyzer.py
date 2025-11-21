from metripy.LangAnalyzer.Generic.Ast.AstParser import AstParser
from abc import ABC, abstractmethod


class GenericImportsAnalyzer(ABC):
    def get_import_data(
        self, filename: str, parser: AstParser
    ) -> tuple[str, list[str]]:
        return (
            self.extract_import_name(filename, parser),
            self.extract_imports(filename, parser),
        )

    @abstractmethod
    def extract_import_name(self, filename: str, parser: AstParser) -> str:
        """Extract the name of this file with which it is imported"""
        pass

    @abstractmethod
    def extract_imports(self, filename: str, parser: AstParser) -> list[str]:
        """Extract the names of the imports of this file"""
        pass
