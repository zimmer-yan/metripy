"""TypeScript-specific AST parser implementation using tree-sitter"""

from typing import List, Optional

from tree_sitter import Node

from metripy.LangAnalyzer.Generic.Ast.AstParser import AstParser


class TypescriptAstParser(AstParser):
    """TypeScript-specific implementation of AST parser"""

    def __init__(self):
        super().__init__("typescript")

    def get_import_nodes(self) -> List[Node]:
        """Get all import statements"""
        return self.find_nodes_by_type("import_statement")

    def get_function_nodes(self) -> List[Node]:
        """Get all function and method definitions"""
        functions = self.find_nodes_by_type("function_declaration")
        functions.extend(self.find_nodes_by_type("method_definition"))

        arrow_function_nodes = self.find_nodes_by_type("arrow_function")
        for arrow_function_node in arrow_function_nodes:
            for child in reversed(arrow_function_node.parent.children):
                # only if parent has another child called identifier are we assigning this function, else its just a lambda expression
                if child.type == "identifier":
                    functions.append(arrow_function_node)
                    break
        return functions

    def get_class_nodes(self) -> List[Node]:
        """Get all class definitions"""
        return self.find_nodes_by_type("class_declaration")

    def get_variable_assignment_nodes(self) -> List[Node]:
        """Get all variable declarations"""
        nodes = self.find_nodes_by_type("lexical_declaration")
        nodes.extend(self.find_nodes_by_type("variable_declaration"))
        return nodes

    def get_identifier_nodes(self, context: str = "usage") -> List[Node]:
        """Get identifier nodes"""
        nodes = self.find_nodes_by_type("identifier")
        nodes.extend(self.find_nodes_by_type("type_identifier"))
        return nodes

    def extract_function_name(self, node: Node) -> Optional[str]:
        """Extract function name"""
        if node.type == "function_declaration":
            for child in node.children:
                if child.type == "identifier":
                    return self.get_node_text(child)
        elif node.type == "method_definition":
            for child in node.children:
                if child.type == "property_identifier":
                    return self.get_node_text(child)
        elif node.type == "arrow_function":
            for child in reversed(node.parent.children):
                if child.type == "identifier":
                    return self.get_node_text(child)
        return None

    def extract_class_name(self, node: Node) -> Optional[str]:
        """Extract class name"""
        for child in node.children:
            if child.type == "type_identifier":
                return self.get_node_text(child)
        return None

    def extract_variable_name(self, node: Node) -> Optional[str]:
        """Extract variable name from declaration"""
        for child in node.children:
            if child.type == "variable_declarator":
                for grandchild in child.children:
                    if grandchild.type == "identifier":
                        return self.get_node_text(grandchild)
        return None

    def extract_import_name(self, node: Node) -> Optional[str]:
        """Extract imported names from import statement"""
        names = []
        for child in node.children:
            if child.type == "import_clause":
                for grandchild in child.children:
                    if grandchild.type == "identifier":
                        names.append(self.get_node_text(grandchild))
                    elif grandchild.type == "named_imports":
                        for import_spec in grandchild.children:
                            if import_spec.type == "import_specifier":
                                for part in import_spec.children:
                                    if part.type == "identifier":
                                        names.append(self.get_node_text(part))
        return ", ".join(names) if names else None

    def get_function_parameters(self, function_node: Node) -> List[str]:
        """Extract parameter names from function definition"""
        params = []
        for child in function_node.children:
            if child.type == "formal_parameters":
                for param_node in child.children:
                    if (
                        param_node.type == "required_parameter"
                        or param_node.type == "optional_parameter"
                    ):
                        for grandchild in param_node.children:
                            if grandchild.type == "identifier":
                                params.append(self.get_node_text(grandchild))
                                break
                    elif param_node.type == "identifier":
                        params.append(self.get_node_text(param_node))
        return params

    def get_operator_types(self) -> List[str]:
        raise NotImplementedError

    def get_operand_types(self) -> List[str]:
        raise NotImplementedError

    def get_function_attributes(self, function_node: Node) -> List[str]:
        self_calls = []
        for child in self.walk_tree(function_node):
            if (
                child.type == "member_expression"
                and not child.parent.type == "call_expression"
            ):
                self_calls.append(self.get_node_text(child))
        return self_calls

    def get_function_self_calls(self, function_node: Node) -> List[str]:
        self_calls = []
        for child in self.walk_tree(function_node):
            if (
                child.type == "member_expression"
                and child.parent.type == "call_expression"
            ):
                # cut of "this." prefix
                self_calls.append(self.get_node_text(child)[5:])
        return self_calls

    def get_class_methods(self, class_node: Node) -> List[Node]:
        functions = self.find_nodes_by_type("function_declaration", class_node)
        functions.extend(self.find_nodes_by_type("method_definition", class_node))
        functions.extend(self.find_nodes_by_type("arrow_function", class_node))
        return functions

    def extract_import_qualified_name(self, node: Node) -> Optional[str]:
        for child in self.walk_tree(node):
            if child.type == "qualified_name":
                return self.get_node_text(child)
        return None
