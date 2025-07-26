import os
import tempfile
import time
import pytest
from pathlib import Path

from lib.fss.fss_output_parser import OutputParser, parse_output
from tests.tests_utils import get_abs_path


class TestOutputParserCaching:
    """Test class for OutputParser caching functionality"""

    @classmethod
    def setup_class(cls):
        """Setup test environment"""
        # Clear the cache before running tests
        OutputParser._cache.clear()

        # Get the test.fss file path
        cls.test_fss_path = get_abs_path("tests/test.fss")
        assert os.path.exists(cls.test_fss_path), f"Test file not found: {cls.test_fss_path}"

    @classmethod
    def teardown_class(cls):
        """Clean up after all tests"""
        # Clear the cache after tests
        OutputParser._cache.clear()

    def setup_method(self):
        """Reset cache before each test"""
        OutputParser._cache.clear()

    def test_initial_cache_is_empty(self):
        """Test that the cache starts empty"""
        assert len(OutputParser._cache) == 0

    def test_first_parse_populates_cache(self):
        """Test that first parse of a file populates the cache"""
        # First parse
        output1 = parse_output(self.test_fss_path)

        # Check that cache is populated
        assert len(OutputParser._cache) == 1
        assert self.test_fss_path in OutputParser._cache

        # Check cache structure
        cached_mtime, cached_output = OutputParser._cache[self.test_fss_path]
        assert isinstance(cached_mtime, (int, float))  # Modification time
        assert isinstance(cached_output, dict)  # Parsed output
        assert "metadata" in cached_output
        assert "dimensions" in cached_output
        assert "models" in cached_output

    def test_second_parse_uses_cache(self):
        """Test that second parse of the same file uses cache"""
        # First parse
        output1 = parse_output(self.test_fss_path)

        # Get initial cache state
        initial_cache_entry = OutputParser._cache[self.test_fss_path]

        # Second parse (should use cache)
        output2 = parse_output(self.test_fss_path)

        # Check that outputs are identical
        assert output1 == output2

        # Check that cache entry is the same (not recreated)
        assert OutputParser._cache[self.test_fss_path] == initial_cache_entry

    def test_cache_invalidation_on_file_modification(self):
        """Test that cache is invalidated when file modification time changes"""
        # Create a temporary file for testing
        with tempfile.NamedTemporaryFile(mode='w', suffix='.fss', delete=False) as temp_file:
            temp_path = temp_file.name
            # Write some basic FSS content
            temp_file.write("NAME OF THE JOB ........................Test\n")
            temp_file.write("NUMBER OF VARIABLES ....................  30\n")
            temp_file.write("MINIMAL DIMENSIONALITY .................   2\n")
            temp_file.write("MAXIMAL DIMENSIONALITY .................   4\n")
            temp_file.write("SIMILARITY DATA  (CORRELATIONS)\n")
            temp_file.write("VALUES REPRESENTING MISSING CELLS.......(99.0    ,99.0    )  ,\n")
            temp_file.write("TIED VALUES WITH A TOLERANCE OF ........   0.000\n")
            temp_file.write("WEIGHTING PARAMETER FOR LOCALITY .......   2\n")
            temp_file.write("\x0c\n")  # End block

        try:
            # First parse
            output1 = parse_output(temp_path)
            initial_cache_entry = OutputParser._cache[temp_path]

            # Wait a moment and modify the file
            time.sleep(0.1)  # Ensure modification time changes
            with open(temp_path, 'a') as f:
                f.write("# Modified content\n")

            # Second parse (should re-parse due to modification)
            output2 = parse_output(temp_path)
            new_cache_entry = OutputParser._cache[temp_path]

            # Check that cache entry changed (different modification time)
            assert new_cache_entry != initial_cache_entry

        finally:
            # Clean up
            os.unlink(temp_path)

    def test_multiple_files_cached_separately(self):
        """Test that different files are cached separately"""
        # Create two temporary files
        with tempfile.NamedTemporaryFile(mode='w', suffix='.fss', delete=False) as temp_file1:
            temp_path1 = temp_file1.name
            temp_file1.write("NAME OF THE JOB ........................Test1\n")
            temp_file1.write("NUMBER OF VARIABLES ....................  10\n")
            temp_file1.write("\x0c\n")

        with tempfile.NamedTemporaryFile(mode='w', suffix='.fss', delete=False) as temp_file2:
            temp_path2 = temp_file2.name
            temp_file2.write("NAME OF THE JOB ........................Test2\n")
            temp_file2.write("NUMBER OF VARIABLES ....................  20\n")
            temp_file2.write("\x0c\n")

        try:
            # Parse both files
            output1 = parse_output(temp_path1)
            output2 = parse_output(temp_path2)

            # Check that both files are cached
            assert len(OutputParser._cache) == 2
            assert temp_path1 in OutputParser._cache
            assert temp_path2 in OutputParser._cache

            # Check that cache entries are different
            assert OutputParser._cache[temp_path1] != OutputParser._cache[temp_path2]

        finally:
            # Clean up
            os.unlink(temp_path1)
            os.unlink(temp_path2)

    def test_direct_parser_instantiation_uses_cache(self):
        """Test that direct OutputParser instantiation also uses cache"""
        # First parse using parse_output function
        output1 = parse_output(self.test_fss_path)

        # Clear the cache to simulate fresh start
        OutputParser._cache.clear()

        # Parse again to populate cache
        output2 = parse_output(self.test_fss_path)

        # Now create OutputParser directly
        parser = OutputParser(self.test_fss_path)
        output3 = parser.get_output()

        # Check that all outputs are identical
        assert output1 == output2 == output3

    def test_cache_persistence_across_instances(self):
        """Test that cache is shared across different OutputParser instances"""
        # First instance
        parser1 = OutputParser(self.test_fss_path)
        output1 = parser1.get_output()

        # Check cache is populated
        assert len(OutputParser._cache) == 1

        # Second instance (should use cache)
        parser2 = OutputParser(self.test_fss_path)
        output2 = parser2.get_output()

        # Check outputs are identical
        assert output1 == output2

        # Check that both instances have the same data
        assert parser1.metadata == parser2.metadata
        assert parser1.dim_data == parser2.dim_data
        assert parser1.models == parser2.models

    def test_cache_handles_missing_file(self):
        """Test that cache handles missing files gracefully"""
        non_existent_path = "non_existent_file.fss"

        with pytest.raises(FileNotFoundError):
            parse_output(non_existent_path)

        # Check that cache is not polluted
        assert non_existent_path not in OutputParser._cache

    def test_cache_structure_integrity(self):
        """Test that cached data structure is correct"""
        output = parse_output(self.test_fss_path)

        # Check cache entry structure
        cached_mtime, cached_output = OutputParser._cache[self.test_fss_path]

        # Check modification time is reasonable
        assert cached_mtime > 0
        assert cached_mtime <= time.time()

        # Check output structure
        assert isinstance(cached_output, dict)
        assert "metadata" in cached_output
        assert "dimensions" in cached_output
        assert "models" in cached_output

        # Check that cached output matches returned output
        assert cached_output == output

    def test_cache_clearing(self):
        """Test that cache can be cleared"""
        # Parse a file to populate cache
        parse_output(self.test_fss_path)
        assert len(OutputParser._cache) > 0

        # Clear cache
        OutputParser._cache.clear()
        assert len(OutputParser._cache) == 0

        # Parse again (should re-populate cache)
        parse_output(self.test_fss_path)
        assert len(OutputParser._cache) == 1


if __name__ == "__main__":
    pytest.main([__file__])