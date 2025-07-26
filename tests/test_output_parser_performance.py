import time
import pytest
from lib.fss.fss_output_parser import OutputParser, parse_output
from tests.tests_utils import get_abs_path
import os


class TestOutputParserPerformance:
    """Test class for OutputParser performance with caching"""

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

    def test_caching_performance_improvement(self):
        """Test that second parse is significantly faster due to caching"""
        # First parse (should be slower)
        start_time = time.time()
        output1 = parse_output(self.test_fss_path)
        first_parse_time = time.time() - start_time

        # Second parse (should be faster due to cache)
        start_time = time.time()
        output2 = parse_output(self.test_fss_path)
        second_parse_time = time.time() - start_time

        # Verify outputs are identical
        assert output1 == output2

        # Verify second parse is significantly faster
        # The second parse should be at least 10x faster
        assert second_parse_time < first_parse_time / 10, \
            f"Second parse ({second_parse_time:.4f}s) should be much faster than first parse ({first_parse_time:.4f}s)"

        print(f"First parse time: {first_parse_time:.4f}s")
        print(f"Second parse time: {second_parse_time:.4f}s")

        # Handle division by zero case (when second parse is extremely fast)
        if second_parse_time > 0:
            speed_improvement = first_parse_time / second_parse_time
            print(f"Speed improvement: {speed_improvement:.1f}x faster")
        else:
            print("Speed improvement: Extremely fast (cached parse took ~0 seconds)")

    def test_cache_hit_vs_miss_performance(self):
        """Test performance difference between cache hit and cache miss scenarios"""
        # Clear cache and parse (cache miss)
        OutputParser._cache.clear()
        start_time = time.time()
        output1 = parse_output(self.test_fss_path)
        cache_miss_time = time.time() - start_time

        # Parse again (cache hit)
        start_time = time.time()
        output2 = parse_output(self.test_fss_path)
        cache_hit_time = time.time() - start_time

        # Verify outputs are identical
        assert output1 == output2

        # Verify cache hit is much faster
        assert cache_hit_time < cache_miss_time / 5, \
            f"Cache hit ({cache_hit_time:.4f}s) should be much faster than cache miss ({cache_miss_time:.4f}s)"

        print(f"Cache miss time: {cache_miss_time:.4f}s")
        print(f"Cache hit time: {cache_hit_time:.4f}s")

        # Handle division by zero case
        if cache_hit_time > 0:
            performance_ratio = cache_miss_time / cache_hit_time
            print(f"Performance ratio: {performance_ratio:.1f}x faster with cache")
        else:
            print("Performance ratio: Extremely fast (cached parse took ~0 seconds)")

    def test_cache_effectiveness(self):
        """Test that cache is working by measuring multiple parses"""
        # Clear cache
        OutputParser._cache.clear()

        # First parse (cache miss)
        start_time = time.time()
        output1 = parse_output(self.test_fss_path)
        first_time = time.time() - start_time

        # Multiple subsequent parses (cache hits)
        cache_times = []
        for i in range(5):
            start_time = time.time()
            output = parse_output(self.test_fss_path)
            cache_time = time.time() - start_time
            cache_times.append(cache_time)
            assert output == output1  # All outputs should be identical

        avg_cache_time = sum(cache_times) / len(cache_times)

        print(f"First parse (cache miss): {first_time:.4f}s")
        print(f"Average cached parse: {avg_cache_time:.4f}s")

        # Verify caching is effective
        assert avg_cache_time < first_time / 5, \
            f"Cached parses ({avg_cache_time:.4f}s) should be much faster than first parse ({first_time:.4f}s)"

        if avg_cache_time > 0:
            improvement = first_time / avg_cache_time
            print(f"Average improvement: {improvement:.1f}x faster")
        else:
            print("Average improvement: Extremely fast (cached parses took ~0 seconds)")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])