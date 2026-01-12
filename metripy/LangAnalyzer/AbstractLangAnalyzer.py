from abc import ABC, abstractmethod

from metripy.Application.Config.ProjectConfig import ProjectConfig
from metripy.Component.Output.ProgressBar import ProgressBar
from metripy.LangAnalyzer.Generic.CodeSmell.CodeSmellDetectorFactory import (
    CodeSmellDetectorFactory,
)
from metripy.LangAnalyzer.Generic.DuplicateSearch.DuplicateDetector import (
    DuplicateDetector,
)
from metripy.LangAnalyzer.Generic.DuplicateSearch.TokenizerFactory import (
    TokenizerFactory,
)
from metripy.LangAnalyzer.Generic.Metrics.GenericHalSteadAnalyzer import (
    GenericHalSteadAnalyzer,
)
from metripy.LangAnalyzer.Generic.Metrics.GenericLcom4Analyzer import (
    GenericLcom4Analyzer,
)
from metripy.LangAnalyzer.Generic.Metrics.GenericLocAnalyzer import GenericLocAnalyzer
from metripy.LangAnalyzer.Generic.Metrics.HalSteadAnalyzerFactory import (
    HalSteadAnalyzerFactory,
)
from metripy.LangAnalyzer.Generic.Metrics.Lcom4AnalyzerFactory import (
    Lcom4AnalyzerFactory,
)
from metripy.LangAnalyzer.Generic.Metrics.CyclomaticComplexityAnalyzerFactory import (
    CyclomaticComplexityAnalyzerFactory,
)
from metripy.LangAnalyzer.Generic.Metrics.GenericCyclomaticComplexityAnalyzer import (
    GenericCyclomaticComplexityAnalyzer,
)
from metripy.LangAnalyzer.Generic.Metrics.LocAnalyzerFactory import LocAnalyzerFactory
from metripy.Metric.Code.FileMetrics import FileMetrics
from metripy.Tree.ModuleNode import ModuleNode
from metripy.Tree.FunctionNode import FunctionNode
from metripy.Tree.ClassNode import ClassNode

from metripy.LangAnalyzer.Generic.Ast.AstParserFactory import AstParserFactory
from metripy.LangAnalyzer.Generic.Ast.AstParser import AstParser
from metripy.LangAnalyzer.Generic.Metrics.GenericCognitiveComplexityAnalyzer import (
    GenericCognitiveComplexityCalculator,
)
from metripy.LangAnalyzer.Generic.Metrics.CognitiveComplexityAnalyzerFactory import (
    CognitiveComplexityAnalyzerFactory,
)
from metripy.LangAnalyzer.Generic.Metrics.ImportsAnalyzerFactory import (
    ImportsAnalyzerFactory,
)
from metripy.LangAnalyzer.Generic.Metrics.GenericImportsAnalyzer import (
    GenericImportsAnalyzer,
)
import math


class AbstractLangAnalyzer(ABC):
    def __init__(self, project_config: ProjectConfig):
        self.config = project_config
        self.files: list[str] = []
        self.modules: dict[str, ModuleNode] = {}
        self.ast_parser: AstParser = AstParserFactory.get_ast_parser(
            self.get_lang_name()
        )
        self.loc_analyzer: GenericLocAnalyzer = LocAnalyzerFactory.get_loc_analyzer(
            self.get_lang_name()
        )
        self.cyclomatic_complexity_analyzer: GenericCyclomaticComplexityAnalyzer = (
            CyclomaticComplexityAnalyzerFactory.get_cyclomatic_complexity_analyzer(
                self.get_lang_name()
            )
        )
        self.cognitive_complexity_analyzer: GenericCognitiveComplexityCalculator = (
            CognitiveComplexityAnalyzerFactory.get_cognitive_complexity_analyzer(
                self.get_lang_name()
            )
        )
        self.halstead_analyzer: GenericHalSteadAnalyzer = (
            HalSteadAnalyzerFactory.get_halstead_analyzer(self.get_lang_name())
        )
        self.lcom4_analyzer: GenericLcom4Analyzer = (
            Lcom4AnalyzerFactory.get_lcom4_analyzer(self.get_lang_name())
        )
        self.imports_analyzer: GenericImportsAnalyzer = (
            ImportsAnalyzerFactory.get_imports_analyzer(self.get_lang_name())
        )
        self.code_smell_detector = CodeSmellDetectorFactory.get_code_smell_detector(
            self.get_lang_name(), self.config.code_smells
        )
        self.duplicate_detector = DuplicateDetector(
            tokenizer=TokenizerFactory.get_tokenizer(self.get_lang_name())
        )

    # need to be implemented by sub analyzers
    @abstractmethod
    def get_lang_name(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def get_supported_extensions(self) -> tuple[str]:
        raise NotImplementedError

    # can be overridden by sub analyzers
    def before_run(self) -> None:
        # build cache
        pass

    def after_run(self) -> None:
        # clear cache
        pass

    def set_files(self, files: list[str]) -> None:
        self.files = list(
            filter(lambda file: file.endswith(self.get_supported_extensions()), files)
        )

    def is_needed(self) -> bool:
        return len(self.files) > 0

    def run(self, progress_bar: ProgressBar) -> None:
        for file in self.files:
            with open(file, "r") as f:
                code = f.read()
                self.analyze(code, file)
            progress_bar.advance()

    def create_module_node(self, filename: str, code: str) -> ModuleNode:
        loc_data = self.loc_analyzer.analyze(code)
        full_name = self.full_name(filename)
        return ModuleNode(
            full_name,
            loc_data.get("loc", 0),
            loc_data.get("lloc", 0),
            loc_data.get("sloc", 0),
            loc_data.get("comments", 0),
            loc_data.get("multiline_comments", 0),
            loc_data.get("blank_lines", 0),
            loc_data.get("single_comments", 0),
        )

    def add_function_halstead_metrics(
        self, function_node: FunctionNode, function_code: str
    ) -> None:
        function_metrics = self.halstead_analyzer.calculate_halstead_metrics(
            function_code
        )
        function_node.h1 = function_metrics["n1"]
        function_node.h2 = function_metrics["n2"]
        function_node.N1 = function_metrics["N1"]
        function_node.N2 = function_metrics["N2"]
        function_node.vocabulary = function_metrics["vocabulary"]
        function_node.length = function_metrics["length"]
        function_node.calculated_length = function_metrics["calculated_length"]
        function_node.volume = function_metrics["volume"]
        function_node.difficulty = function_metrics["difficulty"]
        function_node.effort = function_metrics["effort"]
        function_node.bugs = function_metrics["bugs"]
        function_node.time = function_metrics["time"]
        function_node.calc_mi()

    @staticmethod
    def full_name(
        filename: str, item_name: str | None = None, class_name: str | None = None
    ) -> str:
        if class_name is None:
            if item_name is None:
                return filename
            return f"{filename}:{item_name}"
        return f"{filename}:{class_name}:{item_name}"

    def get_duplicates(self) -> list[dict]:
        return self.duplicate_detector.get_duplicates()

    def get_metrics(self) -> list[FileMetrics]:
        metrics: dict[str, FileMetrics] = {}

        efferent_coupling = {}
        afferent_coupling = {}

        for module in self.modules.values():
            full_name = module.full_name

            if len(module.functions) > 0:
                totalCc = sum(function.complexity for function in module.functions)
                avgCcPerFunction = totalCc / len(module.functions)
                avgLocPerFunction = sum(
                    function.get_loc() for function in module.functions
                ) / len(module.functions)
                total_cog_complexity = sum(
                    function.cognitive_complexity for function in module.functions
                )
                avg_cog_complexity_per_function = total_cog_complexity / len(
                    module.functions
                )
            else:
                totalCc = 0
                avgCcPerFunction = 0
                avgLocPerFunction = 0
                total_cog_complexity = 0
                avg_cog_complexity_per_function = 0
            maintainabilityIndex = module.maintainability_index

            if self.lcom4_analyzer is not None and len(module.classes) > 0:
                total_lcom4 = sum(class_node.lcom4 for class_node in module.classes)
                avg_lcom4_per_class = total_lcom4 / len(module.classes)
            else:
                total_lcom4 = 0
                avg_lcom4_per_class = 0

            file_metric = FileMetrics(
                full_name=full_name,
                loc=module.loc,
                totalCc=totalCc,
                avgCcPerFunction=avgCcPerFunction,
                maintainabilityIndex=maintainabilityIndex,
                avgLocPerFunction=avgLocPerFunction,
                class_nodes=module.classes,
                function_nodes=module.functions,
                import_name=module.import_name,
                imports=module.imports,
                code_smells=module.code_smells,
                total_cog_complexity=total_cog_complexity,
                avg_cog_complexity_per_function=avg_cog_complexity_per_function,
                avg_lcom4_per_class=avg_lcom4_per_class,
            )
            metrics[full_name] = file_metric

            if not module.import_name or not module.imports:
                continue
            efferent_coupling[module.import_name] = len(module.imports)
            for import_name in module.imports:
                if import_name not in afferent_coupling:
                    afferent_coupling[import_name] = []
                afferent_coupling[import_name].append(module.import_name)

        for file_metric in metrics.values():
            imported_by = afferent_coupling.get(file_metric.import_name, [])
            ca = len(imported_by)
            ce = efferent_coupling.get(file_metric.import_name, 0)
            file_metric.imported_by = imported_by
            file_metric.afferent_coupling = ca
            file_metric.efferent_coupling = ce
            file_metric.instability = (ce / (ca + ce)) if (ca + ce) > 0 else 0

        return list(metrics.values())

    def analyze(self, code: str, filename: str) -> None:
        self.ast_parser.parse(code)
        cyclomatic_complexity_data = self.cyclomatic_complexity_analyzer.calculate(
            self.ast_parser
        )

        classes: dict[str, ClassNode] = {}
        functions: dict[str, FunctionNode] = {}
        for data_item in cyclomatic_complexity_data["classes"]:
            class_node = ClassNode(
                self.full_name(filename, data_item["name"]),
                data_item["name"],
                data_item["line_start"],
                data_item["line_end"],
                sum(
                    [method_data["complexity"] for method_data in data_item["methods"]]
                ),
            )
            classes[class_node.full_name] = class_node
            for method_data in data_item["methods"]:
                function_node = FunctionNode(
                    self.full_name(filename, method_data["name"]),
                    method_data["name"],
                    method_data["line_start"],
                    method_data["line_end"],
                    method_data["complexity"],
                )
                class_node.functions.append(function_node)
                functions[function_node.full_name] = function_node
        for data_item in cyclomatic_complexity_data["functions"]:
            function_node = FunctionNode(
                self.full_name(filename, data_item["name"]),
                data_item["name"],
                data_item["line_start"],
                data_item["line_end"],
                data_item["complexity"],
            )
            functions[function_node.full_name] = function_node

        module_node = self.create_module_node(filename, code)
        module_node.classes.extend(classes.values())
        module_node.functions.extend(functions.values())

        code_lines = code.split("\n")
        for func_name, function_node in functions.items():
            lines = code_lines[function_node.lineno : function_node.line_end]
            self.add_function_halstead_metrics(function_node, "\n".join(lines))

        maintainability_index = self._calculate_maintainability_index(
            functions.values(), module_node
        )
        module_node.maintainability_index = maintainability_index
        self.modules[module_node.full_name] = module_node

        # ignore for now - maybe only pass class code, so we dont get import duplicates
        # self.duplicate_detector.add_code(filename, code)

        module_node.import_name, module_node.imports = (
            self.imports_analyzer.get_import_data(filename, self.ast_parser)
        )

        module_node.code_smells = self.code_smell_detector.detect_all(filename, code)

        cognitive_complexities = (
            self.cognitive_complexity_analyzer.calculate_for_all_functions(
                self.ast_parser
            )
        )
        for func_name, complexity in cognitive_complexities.items():
            full_name = self.full_name(filename, func_name)
            function_node = functions.get(full_name)
            if function_node is not None:
                function_node.cognitive_complexity = complexity
            else:
                raise ValueError(f"Function node not found for function {full_name}")

        lcom4 = self.lcom4_analyzer.get_lcom4(self.ast_parser)
        for class_name, lcom4_value in lcom4.items():
            full_name = self.full_name(filename, class_name)
            class_node = classes.get(full_name)
            if class_node is not None:
                class_node.lcom4 = lcom4_value
            else:
                raise ValueError(f"Class node not found for class {full_name}")

        # for classes that dont have lcom4, interface, set to number of methods
        for class_node in classes.values():
            if class_node.lcom4 is None:
                class_node.lcom4 = len(class_node.functions)

    def _calculate_maintainability_index(
        self, functions: list[FunctionNode], module_node: ModuleNode
    ) -> float:
        """Calculate maintainability index for PHP"""
        if not functions:
            return 100.0

        total_volume = sum(func.volume for func in functions)
        total_complexity = sum(func.complexity for func in functions)
        total_length = sum(func.length for func in functions)

        if total_volume == 0 or total_length == 0:
            return 100.0

        # PHP maintainability index calculation
        mi_base = max(
            (
                171
                - 5.2 * math.log(total_volume)
                - 0.23 * total_complexity
                - 16.2 * math.log(total_length)
            )
            * 100
            / 171,
            0,
        )

        # Comment weight
        comment_weight = 0
        if module_node.loc > 0:
            comment_ratio = module_node.single_comments / module_node.loc
            comment_weight = 50 * math.sin(math.sqrt(2.4 * comment_ratio))

        return mi_base + comment_weight
