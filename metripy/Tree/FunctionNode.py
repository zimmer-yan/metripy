class FunctionNode:
    def __init__(
        self, full_name: str, name: str, lineno: int, col_offset: int, complexity: int
    ):
        self.full_name = full_name
        self.name = name
        self.lineno = lineno
        self.line_end = 0
        self.col_offset = col_offset
        self.complexity = complexity
        self.h1 = 0
        self.h2 = 0
        self.N1 = 0
        self.N2 = 0
        self.vocabulary = 0
        self.length = 0
        self.calculated_length = 0
        self.volume = 0
        self.difficulty = 0
        self.effort = 0
        self.time = 0
        self.bugs = 0
        self.maintainability_index = 0

    def to_dict(self) -> dict:
        """Convert FunctionNode to a dictionary for JSON serialization."""
        return {
            "full_name": self.full_name,
            "name": self.name,
            "lineno": self.lineno,
            "col_offset": self.col_offset,
            "complexity": self.complexity,
            "h1": self.h1,
            "h2": self.h2,
            "N1": self.N1,
            "N2": self.N2,
            "vocabulary": self.vocabulary,
            "length": self.length,
            "calculated_length": self.calculated_length,
            "volume": self.volume,
            "difficulty": self.difficulty,
            "effort": self.effort,
            "time": self.time,
            "bugs": self.bugs,
            "maintainability_index": self.maintainability_index,
        }

    def __dict__(self) -> dict:
        return self.to_dict()
