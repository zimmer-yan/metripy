from metripy.LangAnalyzer.Generic.Metrics.GenericImportsAnalyzer import GenericImportsAnalyzer
from metripy.LangAnalyzer.Generic.Ast.AstParser import AstParser
from pathlib import Path

class TypescriptImportsAnalyzer(GenericImportsAnalyzer):
    def extract_imports(self, filename: str, parser: AstParser) -> list[str]:
        imports = []
        for node in parser.get_import_nodes():
            for child in parser.walk_tree(node):
                if child.type == "string_fragment":
                    path = parser.get_node_text(child)
                    imports.append(path)

        filename_path = Path(filename)
        full_imports = []
        for import_name in imports:
            dir_path = filename_path.parent
            if import_name.startswith("./"):
                rel = filename_path.parent / Path(import_name[2:])
            elif import_name.startswith("../"):
                while import_name.startswith("../"):
                    dir_path = dir_path.parent
                    import_name = import_name[3:]
                rel = dir_path / Path(import_name)
            elif import_name.startswith("@"):
                # skip package imports
                continue
            else:
                rel = filename_path.parent / Path(import_name)
            rel_name = rel.__str__()
            if (filename.startswith("./")):
                rel_name = "./" + rel_name
            full_imports.append(self.extract_import_name(rel_name, parser))
        return full_imports

    def extract_import_name(self, filename: str, parser: AstParser) -> str:
        """Extract the name of this file with which it is imported"""
        project_root = [
            p for p in Path(filename).parts if not p.startswith(".")
        ][0]

        path = Path(filename)

        # Get all parts of the path
        parts = path.parts

        # Find where the project root starts
        try:
            root_index = parts.index(project_root)
            # Get parts from project root onwards, excluding the file extension
            module_parts = list(parts[root_index:])
            if filename.endswith((".ts", ".js")):
                module_parts[-1] = path.stem
            # Join with dots to create import name
            return "./" + "/".join(module_parts)
        except ValueError:
            raise ValueError(f"Failed to extract import name for {filename}")
