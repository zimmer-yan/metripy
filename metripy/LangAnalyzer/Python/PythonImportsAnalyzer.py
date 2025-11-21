from pathlib import Path

from metripy.LangAnalyzer.Generic.Metrics.GenericImportsAnalyzer import (
    GenericImportsAnalyzer,
)
from metripy.LangAnalyzer.Generic.Ast.AstParser import AstParser


class PythonImportsAnalyzer(GenericImportsAnalyzer):
    def extract_imports(self, filename: str, parser: AstParser) -> list[str]:
        """Extract the names of the imports of this file"""
        imports = []
        for node in parser.get_import_nodes():
            imports.append(parser.extract_import_qualified_name(node))
        return imports

    def extract_import_name(self, filename: str, parser: AstParser) -> str:
        """Extract the name of this file with which it is imported"""
        project_root = [
            p for p in Path(filename).parts if p.isalpha() and not p.startswith(".")
        ][0]

        path = Path(filename)

        # Get all parts of the path
        parts = path.parts

        # Find where the project root starts
        try:
            root_index = parts.index(project_root)
            # Get parts from project root onwards, excluding the file extension
            module_parts = list(parts[root_index:])
            # Remove .py extension from the last part
            module_parts[-1] = path.stem
            # Join with dots to create import name
            return ".".join(module_parts)
        except ValueError:
            raise ValueError(f"Failed to extract import name for {filename}")
