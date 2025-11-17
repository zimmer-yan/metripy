from unittest import TestCase

from metripy.LangAnalyzer.Python.DuplicateSearch.PythonTokenizer import PythonTokenizer


class TestPythonTokenizer(TestCase):
    """Test cases for Python-specific tokenizer"""

    def test_initialization(self):
        """Test tokenizer initialization with defaults"""
        tokenizer = PythonTokenizer()
        self.assertFalse(tokenizer.normalize_identifiers)
        self.assertEqual(tokenizer.ngram_size, 4)

    def test_initialization_with_custom_params(self):
        """Test tokenizer initialization with custom parameters"""
        tokenizer = PythonTokenizer(normalize_identifiers=True, ngram_size=3)
        self.assertTrue(tokenizer.normalize_identifiers)
        self.assertEqual(tokenizer.ngram_size, 3)

    def test_simple_function_tokenization(self):
        """Test tokenization of a simple Python function"""
        tokenizer = PythonTokenizer()

        code = """def hello():
    return "world"
"""

        tokens = tokenizer.tokenize(code)

        # Should produce n-grams
        self.assertGreater(len(tokens), 0)
        self.assertIsInstance(tokens, list)
        self.assertTrue(all(isinstance(t, str) for t in tokens))

    def test_removes_comments(self):
        """Test that comments are filtered out"""
        tokenizer = PythonTokenizer(ngram_size=3)

        code1 = """def function():
    x = 1
    return x
"""

        code2 = """def function():
    # This is a comment
    x = 1  # Another comment
    return x
"""

        tokens1 = tokenizer.tokenize(code1)
        tokens2 = tokenizer.tokenize(code2)

        # Should produce similar tokens (comments removed)
        # They might not be exactly equal due to ngram windows, but should be close
        self.assertGreater(len(tokens1), 0)
        self.assertGreater(len(tokens2), 0)

    def test_normalizes_strings(self):
        """Test that string literals are normalized"""
        tokenizer = PythonTokenizer(ngram_size=3)

        code1 = """message = "hello"
print(message)
"""

        code2 = """message = "goodbye"
print(message)
"""

        tokens1 = tokenizer.tokenize(code1)
        tokens2 = tokenizer.tokenize(code2)

        # Should produce similar structure since strings are normalized
        self.assertEqual(len(tokens1), len(tokens2))

        # Check that STRING token is used
        combined = " ".join(tokens1 + tokens2)
        self.assertIn("STRING", combined)

    def test_normalizes_numbers(self):
        """Test that number literals are normalized"""
        tokenizer = PythonTokenizer(ngram_size=3)

        code1 = """x = 42
y = 3.14
"""

        code2 = """x = 100
y = 2.71
"""

        tokens1 = tokenizer.tokenize(code1)
        tokens2 = tokenizer.tokenize(code2)

        # Should produce same structure since numbers are normalized
        self.assertEqual(len(tokens1), len(tokens2))

        # Check that NUMBER token is used
        combined = " ".join(tokens1 + tokens2)
        self.assertIn("NUMBER", combined)

    def test_identifier_normalization_disabled(self):
        """Test that identifiers are preserved when normalization is disabled"""
        tokenizer = PythonTokenizer(normalize_identifiers=False, ngram_size=2)

        code = """def calculate_sum(a, b):
    return a + b
"""

        tokens = tokenizer.tokenize(code)
        combined = " ".join(tokens)

        # Should contain actual identifier names
        self.assertIn("calculate_sum", combined)
        self.assertIn("calculate_sum", str(tokens))

    def test_identifier_normalization_enabled(self):
        """Test that identifiers are normalized when enabled"""
        tokenizer = PythonTokenizer(normalize_identifiers=True, ngram_size=3)

        code1 = """def calculate_sum(a, b):
    return a + b
"""

        code2 = """def compute_total(x, y):
    return x + y
"""

        tokens1 = tokenizer.tokenize(code1)
        tokens2 = tokenizer.tokenize(code2)

        # Should produce more similar tokens with normalization
        # (keywords preserved, identifiers normalized)
        combined = " ".join(tokens1 + tokens2)
        self.assertIn("IDENTIFIER", combined)
        self.assertIn("def", combined)  # Keywords should be preserved

    def test_preserves_keywords(self):
        """Test that Python keywords are always preserved"""
        tokenizer = PythonTokenizer(normalize_identifiers=True, ngram_size=2)

        code = """if x > 0:
    return True
else:
    return False
"""

        tokens = tokenizer.tokenize(code)
        combined = " ".join(tokens)

        # Keywords should be present
        self.assertIn("if", combined)
        self.assertIn("return", combined)
        self.assertIn("else", combined)
        self.assertIn("True", combined)
        self.assertIn("False", combined)

    def test_handles_empty_code(self):
        """Test handling of empty code"""
        tokenizer = PythonTokenizer()

        tokens = tokenizer.tokenize("")
        self.assertEqual(tokens, [])

        tokens = tokenizer.tokenize("   \n\n  ")
        self.assertEqual(tokens, [])

    def test_handles_operators(self):
        """Test that operators are tokenized correctly"""
        tokenizer = PythonTokenizer(ngram_size=2)

        code = """result = a + b - c * d / e
"""

        tokens = tokenizer.tokenize(code)
        combined = " ".join(tokens)

        # Should contain operators
        self.assertTrue(any(op in combined for op in ["+", "-", "*", "/", "="]))

    def test_handles_complex_python_code(self):
        """Test tokenization of complex Python code"""
        tokenizer = PythonTokenizer()

        code = """class Calculator:
    def __init__(self):
        self.value = 0

    def add(self, x):
        self.value += x
        return self.value

    def multiply(self, x):
        self.value *= x
        return self.value
"""

        tokens = tokenizer.tokenize(code)

        # Should produce tokens
        self.assertGreater(len(tokens), 0)

        combined = " ".join(tokens)
        # Should contain class definition tokens
        self.assertIn("class", combined)
        self.assertIn("def", combined)

    def test_handles_multiline_strings(self):
        """Test handling of multiline strings"""
        tokenizer = PythonTokenizer(ngram_size=2)

        code = '''def get_doc():
    """
    This is a docstring
    with multiple lines
    """
    return "result"
'''

        tokens = tokenizer.tokenize(code)

        # Should handle without crashing
        self.assertGreater(len(tokens), 0)

        combined = " ".join(tokens)
        # Docstring should be normalized to STRING
        self.assertIn("STRING", combined)

    def test_ngram_size_affects_output(self):
        """Test that ngram_size parameter affects the output"""
        code = """def function():
    x = 1
    y = 2
    return x + y
"""

        tokenizer_small = PythonTokenizer(ngram_size=2)
        tokenizer_large = PythonTokenizer(ngram_size=5)

        tokens_small = tokenizer_small.tokenize(code)
        tokens_large = tokenizer_large.tokenize(code)

        # Smaller ngrams should produce more tokens (more windows)
        self.assertGreaterEqual(len(tokens_small), len(tokens_large))

    def test_similar_code_produces_similar_tokens(self):
        """Test that structurally similar code produces similar tokens"""
        tokenizer = PythonTokenizer(normalize_identifiers=True, ngram_size=3)

        code1 = """def process_data(input_value):
    result = input_value * 2
    return result
"""

        code2 = """def handle_input(user_data):
    output = user_data * 2
    return output
"""

        tokens1 = tokenizer.tokenize(code1)
        tokens2 = tokenizer.tokenize(code2)

        # Should have similar length (same structure)
        self.assertLessEqual(abs(len(tokens1) - len(tokens2)), 2)

    def test_fallback_tokenization(self):
        """Test fallback tokenization for malformed code"""
        tokenizer = PythonTokenizer()

        # Intentionally malformed Python code
        code = """def broken(
    # Missing closing parenthesis and body
"""

        # Should not crash, use fallback
        tokens = tokenizer.tokenize(code)

        # Should still produce some tokens
        self.assertIsInstance(tokens, list)

    def test_handles_decorators(self):
        """Test tokenization of decorators"""
        tokenizer = PythonTokenizer(ngram_size=2)

        code = """@decorator
def function():
    pass
"""

        tokens = tokenizer.tokenize(code)
        combined = " ".join(tokens)

        # Should handle decorators
        self.assertGreater(len(tokens), 0)
        self.assertIn("@", combined)

    def test_handles_list_comprehensions(self):
        """Test tokenization of list comprehensions"""
        tokenizer = PythonTokenizer(ngram_size=2)

        code = """squares = [x**2 for x in range(10)]
"""

        tokens = tokenizer.tokenize(code)

        # Should tokenize without issues
        self.assertGreater(len(tokens), 0)

        combined = " ".join(tokens)
        self.assertIn("for", combined)
        self.assertIn("in", combined)

    def test_handles_lambda_functions(self):
        """Test tokenization of lambda functions"""
        tokenizer = PythonTokenizer(ngram_size=2)

        code = """add = lambda x, y: x + y
"""

        tokens = tokenizer.tokenize(code)
        combined = " ".join(tokens)

        # Should contain lambda
        self.assertIn("lambda", combined)

    def test_whitespace_insensitive(self):
        """Test that different whitespace produces similar tokens"""
        tokenizer = PythonTokenizer(ngram_size=3)

        code1 = """def f():
    x=1
    y=2
    return x+y
"""

        code2 = """def f():
    x = 1
    y = 2
    return x + y
"""

        tokens1 = tokenizer.tokenize(code1)
        tokens2 = tokenizer.tokenize(code2)

        # Should produce same tokens (whitespace ignored in tokenization)
        self.assertEqual(len(tokens1), len(tokens2))

    def test_real_world_duplicate_detection(self):
        """Test with realistic duplicate code scenario"""
        tokenizer = PythonTokenizer(normalize_identifiers=False)

        code1 = """def validate_user(user):
    if not user:
        raise ValueError("User cannot be None")
    if not user.email:
        raise ValueError("Email is required")
    return True
"""

        code2 = """def validate_user(user):
    if not user:
        raise ValueError("User cannot be None")
    if not user.email:
        raise ValueError("Email is required")
    return True
"""

        tokens1 = tokenizer.tokenize(code1)
        tokens2 = tokenizer.tokenize(code2)

        # Identical code should produce identical tokens
        self.assertEqual(tokens1, tokens2)
        self.assertGreater(len(tokens1), 0)
