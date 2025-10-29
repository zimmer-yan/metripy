from metripy.Tree.FunctionNode import FunctionNode


class ClassNode:
    def __init__(
        self,
        full_name: str,
        name: str,
        lineno: int,
        col_offset: int,
        real_complexity: int,
    ):
        self.full_name = full_name
        self.name = name
        self.lineno = lineno
        self.col_offset = col_offset
        self.real_complexity = real_complexity
        self.functions: list[FunctionNode] = []

    def to_dict(self) -> dict:
        """Convert ClassNode to a dictionary for JSON serialization."""
        return {
            "full_name": self.full_name,
            "name": self.name,
            "lineno": self.lineno,
            "col_offset": self.col_offset,
            "real_complexity": self.real_complexity,
            "functions": [func.to_dict() for func in self.functions],
        }

    def __dict__(self) -> dict:
        return self.to_dict()
