from typing import List
from tree_sitter import Node
from abc import ABC, abstractmethod

from metripy.LangAnalyzer.Generic.Ast.AstParser import AstParser


class GenericCyclomaticComplexityAnalyzer(ABC):

    # implement these to handle special rules for operators that somestimes count
    def has_special_rule(self, type: str) -> bool:
        return False

    def eval_special_rule(self, node: Node) -> int:
        return 0

    @abstractmethod
    def get_decision_types(self) -> List[str]:
        pass

    def _create_object(
        self,
        type: str,
        name: str,
        class_name: str | None,
        cc: int,
        line_start: int,
        line_end: int,
    ) -> dict:
        return {
            "type": type,
            "name": name,
            "class_name": class_name,
            "complexity": cc,
            "line_start": line_start,
            "line_end": line_end,
            "methods": [],
        }

    def calculate(self, parser: AstParser) -> dict[str, any]:
        complexities: dict[str, any] = {"classes": [], "functions": []}
        class_nodes = parser.get_class_nodes()
        visited_nodes = set()
        for class_node in class_nodes:
            class_name = parser.extract_class_name(class_node)
            class_obj = self._create_object(
                type="class",
                name=class_name,
                class_name=None,
                cc=0,
                line_start=class_node.start_point[0],
                line_end=class_node.end_point[0] + 1,
            )
            function_nodes = parser.get_class_methods(class_node)
            for function_node in function_nodes:
                visited_nodes.add(function_node)
                function_name = parser.extract_function_name(function_node)
                class_obj["methods"].append(
                    self._compute_complexity(
                        parser, function_node, function_name, class_name
                    )
                )
            complexities["classes"].append(class_obj)

        all_function_nodes = parser.get_function_nodes()
        for function_node in all_function_nodes:
            if function_node in visited_nodes:
                continue
            function_name = parser.extract_function_name(function_node)
            complexities["functions"].append(
                self._compute_complexity(parser, function_node, function_name)
            )

        return complexities

    def _compute_complexity(
        self,
        parser: AstParser,
        function_node: Node,
        function_name: str,
        class_name: str | None = None,
    ) -> dict[str, int]:
        decision_types = self.get_decision_types()

        count = 1  # Base complexity
        for node in parser.walk_tree(function_node):
            if node.type in decision_types:
                if self.has_special_rule(node.type):
                    # print(node.type)
                    count += self.eval_special_rule(node)
                else:
                    # print(node.type)
                    count += 1

        return self._create_object(
            type="function",
            name=function_name,
            class_name=class_name,
            cc=count,
            line_start=function_node.start_point[0],
            line_end=function_node.end_point[0] + 1,
        )
