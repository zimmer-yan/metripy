from abc import ABC, abstractmethod
from collections import defaultdict

from tree_sitter import Node

from metripy.LangAnalyzer.Generic.Ast.AstParser import AstParser


class GenericLcom4Analyzer(ABC):
    @abstractmethod
    def get_methods_to_ignore(self) -> list[str]:
        pass

    def get_lcom4(self, parser: AstParser) -> dict[str, int]:
        class_nodes = parser.get_class_nodes()
        if not class_nodes:
            return {}

        class_data = {}
        for class_node in class_nodes:
            class_data[parser.extract_class_name(class_node)] = self._get_class_lcom4(
                parser, class_node
            )

        return class_data

    def _get_class_lcom4(self, parser: AstParser, class_node: Node) -> int:
        method_attributes = defaultdict(set)
        for method_node in parser.get_class_methods(class_node):
            method_attributes[parser.extract_function_name(method_node)].update(
                parser.get_function_self_calls(method_node)
            )
            method_attributes[parser.extract_function_name(method_node)].update(
                parser.get_function_attributes(method_node)
            )

        for method in self.get_methods_to_ignore():
            if method in method_attributes:
                del method_attributes[method]

        # Build graph of connected methods
        methods = list(method_attributes.keys())
        connected_components = []
        visited = set()

        def dfs(method, component):
            visited.add(method)
            component.add(method)
            for other_method in methods:
                sharing_attributes = (
                    method_attributes[method] & method_attributes[other_method]
                )
                using_method = other_method in method_attributes[method]
                if other_method not in visited and (sharing_attributes or using_method):
                    dfs(other_method, component)

        for method in reversed(methods):
            if method not in visited:
                component = set()
                dfs(method, component)
                connected_components.append(component)

        return len(connected_components)
