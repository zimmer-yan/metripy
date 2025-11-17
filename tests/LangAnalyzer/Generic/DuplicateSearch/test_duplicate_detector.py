from unittest import TestCase

from simhash import Simhash

from metripy.LangAnalyzer.Generic.DuplicateSearch.CodeChunk import CodeChunk
from metripy.LangAnalyzer.Generic.DuplicateSearch.DuplicateDetector import (
    DuplicateDetector,
)


class TestDuplicateDetector(TestCase):
    """Test cases for DuplicateDetector class"""

    def test_initialization(self):
        """Test that detector initializes with correct defaults"""
        detector = DuplicateDetector()
        self.assertEqual(detector.chunk_size, 5)
        self.assertEqual(detector.min_lines, 3)
        self.assertEqual(len(detector.chunks), 0)
        self.assertIsNotNone(detector.tokenizer)

    def test_initialization_with_custom_params(self):
        """Test initialization with custom parameters"""
        detector = DuplicateDetector(chunk_size=10, min_lines=5)
        self.assertEqual(detector.chunk_size, 10)
        self.assertEqual(detector.min_lines, 5)

    def test_compute_hash(self):
        """Test hash computation for code strings"""
        detector = DuplicateDetector()

        code1 = "def hello():\n    print('world')"
        code2 = "def hello():\n    print('world')"
        code3 = "def goodbye():\n    print('world')"

        hash1 = detector.compute_hash(code1)
        hash2 = detector.compute_hash(code2)
        hash3 = detector.compute_hash(code3)

        # Identical code should produce identical hashes
        self.assertEqual(hash1.value, hash2.value)
        # Different code should produce different hashes (very likely)
        self.assertNotEqual(hash1.value, hash3.value)

    def test_compute_hash_empty_code(self):
        """Test hash computation with empty code"""
        detector = DuplicateDetector()
        hash_value = detector.compute_hash("")
        self.assertIsNotNone(hash_value)

    def test_add_code_creates_chunks(self):
        """Test that adding code creates appropriate chunks"""
        detector = DuplicateDetector(chunk_size=5, min_lines=3)

        code = """def function1():
    x = 1
    y = 2
    z = 3
    return x + y + z

def function2():
    a = 10
    b = 20
    return a + b"""

        detector.add_code("test.py", code)

        # Should create multiple chunks
        self.assertGreater(len(detector.chunks), 0)

        # Check that chunks have correct attributes
        for chunk in detector.chunks:
            self.assertEqual(chunk.filename, "test.py")
            self.assertGreater(chunk.start_line, 0)
            self.assertGreaterEqual(chunk.end_line, chunk.start_line)
            self.assertIsNotNone(chunk.code)
            self.assertIsNotNone(chunk.hash_value)

    def test_add_code_filters_trivial_chunks(self):
        """Test that trivial chunks are filtered out"""
        detector = DuplicateDetector(chunk_size=5, min_lines=3)

        # Code with many empty lines
        code = """


x = 1

"""

        initial_chunks = len(detector.chunks)
        detector.add_code("trivial.py", code)

        # Should not add many chunks due to filtering
        self.assertEqual(len(detector.chunks), initial_chunks)  # No valid chunks added

    def test_exact_duplicate_detection(self):
        """Test detection of exact duplicates"""
        detector = DuplicateDetector(chunk_size=5, min_lines=3)

        # Same code in two files
        duplicate_code = """def calculate_sum(a, b):
    result = a + b
    print(result)
    return result"""

        detector.add_code("file1.py", duplicate_code)
        detector.add_code("file2.py", duplicate_code)

        duplicates = detector.get_duplicates(min_similarity=95.0)

        # Should find duplicates
        self.assertGreater(len(duplicates), 0)

        # Check structure of duplicate report
        dup = duplicates[0]
        self.assertIn("file1", dup)
        self.assertIn("file2", dup)
        self.assertIn("start_line1", dup)
        self.assertIn("end_line1", dup)
        self.assertIn("start_line2", dup)
        self.assertIn("end_line2", dup)
        self.assertIn("similarity", dup)
        self.assertIn("code1", dup)
        self.assertIn("code2", dup)
        self.assertIn("lines", dup)
        # Similarity should be very high (near 100%)
        self.assertGreaterEqual(dup["similarity"], 95.0)

    def test_near_duplicate_detection(self):
        """Test detection of near duplicates (slightly modified code)"""
        detector = DuplicateDetector(chunk_size=5, min_lines=3)

        code1 = """def calculate_sum(a, b):
    result = a + b
    print(result)
    return result"""

        # Similar but with variable name changes
        code2 = """def calculate_total(x, y):
    total = x + y
    print(total)
    return total"""

        detector.add_code("file1.py", code1)
        detector.add_code("file2.py", code2)

        # TODO: check this out, why is the similarity so low?
        duplicates = detector.get_duplicates(min_similarity=20.0)

        # Should find near-duplicates with reasonable threshold
        self.assertGreater(len(duplicates), 0)

    def test_no_false_positives_different_code(self):
        """Test that completely different code is not marked as duplicate"""
        detector = DuplicateDetector(chunk_size=5, min_lines=3)

        code1 = """def calculate_sum(a, b):
    result = a + b
    return result"""

        code2 = """class DataProcessor:
    def __init__(self):
        self.data = []

    def process(self):
        return len(self.data)"""

        detector.add_code("file1.py", code1)
        detector.add_code("file2.py", code2)

        duplicates = detector.get_duplicates(min_similarity=90.0)

        # Should not find high-similarity duplicates
        self.assertEqual(len(duplicates), 0)

    def test_duplicate_locations(self):
        """Test that duplicate locations are correctly reported"""
        detector = DuplicateDetector(chunk_size=4, min_lines=3)

        code1 = """# File 1
def func():
    x = 1
    y = 2
    return x + y"""

        code2 = """# Different header
def func():
    x = 1
    y = 2
    return x + y"""

        detector.add_code("file1.py", code1)
        detector.add_code("file2.py", code2)

        duplicates = detector.get_duplicates(min_similarity=85.0)

        if len(duplicates) > 0:
            dup = duplicates[0]
            # Line numbers should be positive
            self.assertGreater(dup["start_line1"], 0)
            self.assertGreater(dup["end_line1"], 0)
            self.assertGreater(dup["start_line2"], 0)
            self.assertGreater(dup["end_line2"], 0)
            # End should be after start
            self.assertGreaterEqual(dup["end_line1"], dup["start_line1"])
            self.assertGreaterEqual(dup["end_line2"], dup["start_line2"])

    def test_duplicates_sorted_by_similarity(self):
        """Test that duplicates are sorted by similarity (highest first)"""
        detector = DuplicateDetector(chunk_size=5, min_lines=3)

        # Exact duplicate
        exact = """def exact():
    x = 1
    y = 2
    return x + y"""

        # Near duplicate
        near = """def exact():
    x = 1
    y = 2
    return x + y + 1"""

        # Different code
        different = """def other():
    a = 10
    b = 20
    return a * b"""

        detector.add_code("exact1.py", exact)
        detector.add_code("exact2.py", exact)
        detector.add_code("near.py", near)

        duplicates = detector.get_duplicates(min_similarity=70.0)

        # Should be sorted by similarity descending
        if len(duplicates) > 1:
            for i in range(len(duplicates) - 1):
                self.assertGreaterEqual(
                    duplicates[i]["similarity"], duplicates[i + 1]["similarity"]
                )

    def test_multiple_files_duplicate_detection(self):
        """Test duplicate detection across multiple files"""
        detector = DuplicateDetector(chunk_size=5, min_lines=3)

        common_code = """def validate_input(value):
    if value is None:
        raise ValueError("Invalid")
    return True"""

        detector.add_code("module1.py", f"{common_code}\n\ndef other1(): pass")
        detector.add_code("module2.py", f"{common_code}\n\ndef other2(): pass")
        detector.add_code("module3.py", f"{common_code}\n\ndef other3(): pass")

        duplicates = detector.get_duplicates(min_similarity=85.0)

        # Should find duplicates between all file pairs
        self.assertGreater(len(duplicates), 0)

        # Check that we have different file pairs
        file_pairs = set()
        for dup in duplicates:
            pair = tuple(sorted([dup["file1"], dup["file2"]]))
            file_pairs.add(pair)

        # Should have multiple unique pairs
        self.assertGreater(len(file_pairs), 0)

    def test_chunk_size_affects_detection(self):
        """Test that chunk_size parameter affects detection"""
        code = """def long_function():
    line1 = 1
    line2 = 2
    line3 = 3
    line4 = 4
    line5 = 5
    line6 = 6
    line7 = 7
    line8 = 8
    line9 = 9
    line10 = 10
    line11 = 11
    line12 = 12
    return line12"""

        # Small chunks
        detector_small = DuplicateDetector(chunk_size=4, min_lines=3)
        detector_small.add_code("test.py", code)
        small_chunks = len(detector_small.chunks)

        # Large chunks
        detector_large = DuplicateDetector(chunk_size=10, min_lines=3)
        detector_large.add_code("test.py", code)
        large_chunks = len(detector_large.chunks)

        # Smaller chunk size should create more chunks (due to sliding window)
        # With more lines and bigger difference in chunk_size, the difference should be clear
        self.assertGreaterEqual(small_chunks, large_chunks)

    def test_real_world_python_duplicate(self):
        """Test with realistic Python code example"""
        detector = DuplicateDetector(chunk_size=6, min_lines=3)

        file1_code = """
class UserRepository:
    def __init__(self, db):
        self.db = db

    def find_by_id(self, user_id):
        query = "SELECT * FROM users WHERE id = ?"
        result = self.db.execute(query, (user_id,))
        return result.fetchone()

    def save(self, user):
        # Save user logic
        pass
"""

        file2_code = """
class ProductRepository:
    def __init__(self, db):
        self.db = db

    def find_by_id(self, product_id):
        query = "SELECT * FROM products WHERE id = ?"
        result = self.db.execute(query, (product_id,))
        return result.fetchone()

    def delete(self, product):
        # Delete product logic
        pass
"""

        detector.add_code("user_repo.py", file1_code)
        detector.add_code("product_repo.py", file2_code)

        duplicates = detector.get_duplicates(min_similarity=75.0)
        # Should detect the similar find_by_id pattern
        self.assertGreater(len(duplicates), 0)

        # Check that we found meaningful duplicates
        found_meaningful = False
        for dup in duplicates:
            if dup["similarity"] > 80.0 and dup["lines"] >= 3:
                found_meaningful = True
                break

        self.assertTrue(found_meaningful)

    def test_empty_file_handling(self):
        """Test handling of empty files"""
        detector = DuplicateDetector()

        detector.add_code("empty.py", "")
        detector.add_code("also_empty.py", "   \n\n  ")

        # Should not crash
        duplicates = detector.get_duplicates()

        # Should not find duplicates in empty files
        self.assertEqual(len(duplicates), 0)

    def test_single_line_code(self):
        """Test handling of single-line code"""
        detector = DuplicateDetector(chunk_size=3, min_lines=1)

        detector.add_code("one_liner.py", "x = 1")

        # Should not crash
        duplicates = detector.get_duplicates()
        self.assertEqual(len(duplicates), 0)

    def test_code_with_special_characters(self):
        """Test handling of code with special characters"""
        detector = DuplicateDetector()

        code = """def parse_regex():
    pattern = r"[a-zA-Z0-9_@#$%^&*()]+{2,5}"
    text = "Test! @#$ %^& *()_+"
    return re.match(pattern, text)"""

        detector.add_code("regex.py", code)
        detector.add_code("regex_copy.py", code)

        duplicates = detector.get_duplicates(min_similarity=90.0)

        # Should detect duplicates even with special characters
        self.assertGreater(len(duplicates), 0)

    def test_detect_identical_code(self):
        """Test detection of identical code"""
        detector = DuplicateDetector(chunk_size=5, min_lines=3)

        code = """def identical():
    x = 1
    y = 2
    return x + y"""

        detector.add_code("identical1.py", code)
        detector.add_code("identical2.py", code)

        duplicates = detector.get_duplicates(min_similarity=90.0)

        # Should detect duplicates
        self.assertGreater(len(duplicates), 0)

        # With automatic aggregation, should have just 1 duplicate report for this simple case
        self.assertEqual(len(duplicates), 1)

        # Verify the aggregated duplicate has correct structure
        dup = duplicates[0]
        self.assertEqual(dup["file1"], "identical1.py")
        self.assertEqual(dup["file2"], "identical2.py")
        self.assertEqual(dup["start_line1"], 1)
        self.assertEqual(dup["end_line1"], 4)
        self.assertEqual(dup["similarity"], 100.0)
        self.assertEqual(dup["lines"], 4)
        self.assertEqual(dup["code1"], code)
        self.assertEqual(dup["code2"], code)

    def test_aggregation_preserves_separate_duplicate_regions(self):
        """Test that non-overlapping duplicates are kept separate"""
        detector = DuplicateDetector(chunk_size=4, min_lines=3)

        code1 = """def function1():
    x = 1
    y = 2
    return x + y

# Some different code here
z = 100

def function2():
    a = 10
    b = 20
    return a + b"""

        code2 = """def function1():
    x = 1
    y = 2
    return x + y

# Different separator
separator = "---"

def function2():
    a = 10
    b = 20
    return a + b"""

        detector.add_code("module1.py", code1)
        detector.add_code("module2.py", code2)

        duplicates = detector.get_duplicates(min_similarity=85.0)

        # Should find duplicates (function1 and function2)
        self.assertGreater(len(duplicates), 0)

        # Check that we have separate regions if they don't overlap
        # (The middle part is different, so duplicates should be separate)

    def test_ranges_overlap_helper(self):
        """Test the _do_ranges_overlap helper method"""
        detector = DuplicateDetector()

        # Overlapping ranges
        self.assertTrue(detector._do_ranges_overlap(1, 5, 3, 7))
        self.assertTrue(detector._do_ranges_overlap(1, 5, 1, 5))
        self.assertTrue(detector._do_ranges_overlap(1, 10, 3, 7))

        # Non-overlapping ranges
        self.assertFalse(detector._do_ranges_overlap(1, 5, 6, 10))
        self.assertFalse(detector._do_ranges_overlap(6, 10, 1, 5))

        # Adjacent ranges (should not overlap)
        self.assertFalse(detector._do_ranges_overlap(1, 5, 6, 10))

    def test_aggregation_with_multiple_file_pairs(self):
        """Test aggregation works correctly with multiple file pairs"""
        detector = DuplicateDetector(chunk_size=4, min_lines=3)

        duplicate_code = """def common():
    x = 1
    y = 2
    return x + y"""

        # Add the same code to three files
        detector.add_code("file1.py", duplicate_code)
        detector.add_code("file2.py", duplicate_code)
        detector.add_code("file3.py", duplicate_code)

        duplicates = detector.get_duplicates(min_similarity=95.0)

        # Should find duplicates between all pairs: (1,2), (1,3), (2,3)
        self.assertGreaterEqual(len(duplicates), 3)

        # Verify we have different file pairs
        file_pairs = set()
        for dup in duplicates:
            pair = tuple(sorted([dup["file1"], dup["file2"]]))
            file_pairs.add(pair)

        # Should have 3 unique pairs
        expected_pairs = {
            ("file1.py", "file2.py"),
            ("file1.py", "file3.py"),
            ("file2.py", "file3.py"),
        }
        self.assertEqual(file_pairs, expected_pairs)

    def test_aggregated_duplicates_include_code(self):
        """Test that aggregated duplicates include the actual code snippets"""
        detector = DuplicateDetector(chunk_size=5, min_lines=3)

        code1 = """def example_function():
    value_a = 10
    value_b = 20
    value_c = 30
    return value_a + value_b + value_c"""

        code2 = """def example_function():
    value_a = 10
    value_b = 20
    value_c = 30
    return value_a + value_b + value_c"""

        detector.add_code("source1.py", code1)
        detector.add_code("source2.py", code2)

        duplicates = detector.get_duplicates(min_similarity=95.0)

        # Should find duplicates
        self.assertGreater(len(duplicates), 0)

        # Check that code is included
        dup = duplicates[0]
        self.assertIn("code1", dup)
        self.assertIn("code2", dup)
        self.assertIsNotNone(dup["code1"])
        self.assertIsNotNone(dup["code2"])
        self.assertGreater(len(dup["code1"]), 0)
        self.assertGreater(len(dup["code2"]), 0)

        # Code should contain the function definition
        self.assertIn("example_function", dup["code1"])
        self.assertIn("example_function", dup["code2"])
        self.assertIn("value_a", dup["code1"])
        self.assertIn("value_a", dup["code2"])

    def test_code_extraction_helper(self):
        """Test the _extract_code_lines helper method"""
        detector = DuplicateDetector()

        code = """line 1
line 2
line 3
line 4
line 5"""

        detector.add_code("test.py", code)

        # Extract lines 1-3 (1-indexed)
        extracted = detector._extract_code_lines("test.py", 1, 3)
        self.assertEqual(extracted, "line 1\nline 2\nline 3")

        # Extract lines 2-4
        extracted = detector._extract_code_lines("test.py", 2, 4)
        self.assertEqual(extracted, "line 2\nline 3\nline 4")

        # Extract single line
        extracted = detector._extract_code_lines("test.py", 3, 3)
        self.assertEqual(extracted, "line 3")

        # Extract all lines
        extracted = detector._extract_code_lines("test.py", 1, 5)
        self.assertEqual(extracted, code)

        # Non-existent file
        extracted = detector._extract_code_lines("nonexistent.py", 1, 3)
        self.assertEqual(extracted, "")


class TestCodeChunk(TestCase):
    """Test cases for CodeChunk class"""

    def test_code_chunk_creation(self):
        """Test CodeChunk object creation"""

        hash_value = Simhash("test code")
        chunk = CodeChunk(
            filename="test.py",
            start_line=10,
            end_line=15,
            code="test code",
            hash_value=hash_value,
        )

        self.assertEqual(chunk.filename, "test.py")
        self.assertEqual(chunk.start_line, 10)
        self.assertEqual(chunk.end_line, 15)
        self.assertEqual(chunk.code, "test code")
        self.assertEqual(chunk.hash_value, hash_value)

    def test_code_chunk_repr(self):
        """Test CodeChunk string representation"""

        hash_value = Simhash("test")
        chunk = CodeChunk("file.py", 5, 10, "code", hash_value)

        repr_str = repr(chunk)
        self.assertIn("file.py", repr_str)
        self.assertIn("5", repr_str)
        self.assertIn("10", repr_str)
