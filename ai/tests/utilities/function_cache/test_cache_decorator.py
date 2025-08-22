"""
Tests for the function caching utility.
"""

import time
from unittest.mock import patch

from ai.utilities.function_cache import cache_with_invalidation, clear_all_caches, clear_cache


class TestFunctionCache:

    def setup_method(self):
        """Clear all caches before each test."""
        clear_all_caches()

    def test_basic_caching(self):
        """Test that function results are cached."""
        call_count = 0

        @cache_with_invalidation()
        def expensive_function(x, y):
            nonlocal call_count
            call_count += 1
            return x + y

        # First call should execute the function
        result1 = expensive_function(1, 2)
        assert result1 == 3
        assert call_count == 1

        # Second call with same arguments should use cache
        result2 = expensive_function(1, 2)
        assert result2 == 3
        assert call_count == 1  # Function should not be called again

        # Call with different arguments should execute the function
        result3 = expensive_function(2, 3)
        assert result3 == 5
        assert call_count == 2

    def test_cache_with_kwargs(self):
        """Test caching works with keyword arguments."""
        call_count = 0

        @cache_with_invalidation()
        def function_with_kwargs(x, y=10, z=20):
            nonlocal call_count
            call_count += 1
            return x + y + z

        result1 = function_with_kwargs(1)
        assert result1 == 31
        assert call_count == 1

        # Same call should use cache
        result2 = function_with_kwargs(1)
        assert result2 == 31
        assert call_count == 1

        # Different kwargs should call function
        result3 = function_with_kwargs(1, y=5)
        assert result3 == 26
        assert call_count == 2

        # Same kwargs in different order should use cache
        result4 = function_with_kwargs(x=1, y=5, z=20)
        assert result4 == 26
        assert call_count == 2

    def test_ttl_expiration(self):
        """Test that TTL expiration works."""
        call_count = 0

        @cache_with_invalidation(ttl=0.1)  # 100ms TTL
        def function_with_ttl(x):
            nonlocal call_count
            call_count += 1
            return x * 2

        result1 = function_with_ttl(5)
        assert result1 == 10
        assert call_count == 1

        # Immediate call should use cache
        result2 = function_with_ttl(5)
        assert result2 == 10
        assert call_count == 1

        # Wait for TTL to expire
        time.sleep(0.2)

        # Call after TTL should execute function again
        result3 = function_with_ttl(5)
        assert result3 == 10
        assert call_count == 2

    def test_maxsize_eviction(self):
        """Test that maxsize eviction works with LRU behavior."""
        call_count = 0

        @cache_with_invalidation(maxsize=2)
        def function_with_maxsize(x):
            nonlocal call_count
            call_count += 1
            return x * 3

        # Fill cache to maxsize
        function_with_maxsize(1)
        function_with_maxsize(2)
        assert call_count == 2

        # Both should still be cached
        function_with_maxsize(1)
        function_with_maxsize(2)
        assert call_count == 2

        # Adding a third item should evict the LRU (item 1 since it was accessed first above)
        function_with_maxsize(3)
        assert call_count == 3

        # First item should have been evicted, so it should call function again
        # This will evict item 2 (now the LRU)
        function_with_maxsize(1)
        assert call_count == 4

        # Second item should now be evicted, so it will call function again
        # This will evict item 3 (now the LRU)
        function_with_maxsize(2)
        assert call_count == 5

        # Third item should now be evicted, so it will call function again
        function_with_maxsize(3)
        assert call_count == 6

    def test_typed_caching(self):
        """Test that typed caching distinguishes between different types."""
        call_count = 0

        @cache_with_invalidation(typed=True)
        def typed_function(x):
            nonlocal call_count
            call_count += 1
            return str(x)

        # Call with int
        result1 = typed_function(5)
        assert result1 == "5"
        assert call_count == 1

        # Call with same int should use cache
        result2 = typed_function(5)
        assert result2 == "5"
        assert call_count == 1

        # Call with float of same value should call function again
        result3 = typed_function(5.0)
        assert result3 == "5.0"
        assert call_count == 2

        # Call with same float should use cache
        result4 = typed_function(5.0)
        assert result4 == "5.0"
        assert call_count == 2

    def test_clear_specific_cache(self):
        """Test clearing cache for a specific function."""
        call_count1 = 0
        call_count2 = 0

        @cache_with_invalidation()
        def function1(x):
            nonlocal call_count1
            call_count1 += 1
            return x * 2

        @cache_with_invalidation()
        def function2(x):
            nonlocal call_count2
            call_count2 += 1
            return x * 3

        # Call both functions
        function1(5)
        function2(5)
        assert call_count1 == 1
        assert call_count2 == 1

        # Cached calls shouldn't increment counters
        function1(5)
        function2(5)
        assert call_count1 == 1
        assert call_count2 == 1

        # Clear cache for function1 only
        cleared = clear_cache(function1)
        assert cleared == 1

        # function1 should call again, function2 should use cache
        function1(5)
        function2(5)
        assert call_count1 == 2
        assert call_count2 == 1

    def test_clear_all_caches(self):
        """Test clearing all caches."""
        call_count1 = 0
        call_count2 = 0

        @cache_with_invalidation()
        def function1(x):
            nonlocal call_count1
            call_count1 += 1
            return x * 2

        @cache_with_invalidation()
        def function2(x):
            nonlocal call_count2
            call_count2 += 1
            return x * 3

        # Call both functions
        function1(5)
        function2(5)
        assert call_count1 == 1
        assert call_count2 == 1

        # Clear all caches
        cleared = clear_all_caches()
        assert cleared == 2

        # Both functions should call again
        function1(5)
        function2(5)
        assert call_count1 == 2
        assert call_count2 == 2

    def test_cache_info(self):
        """Test that cache info is available on decorated functions."""

        @cache_with_invalidation(ttl=60, maxsize=100, typed=True)
        def test_function(x):
            return x * 2

        # Check that cache info is available
        cache_info = test_function._cache_info()
        assert cache_info["ttl"] == 60
        assert cache_info["maxsize"] == 100
        assert cache_info["typed"] is True
        assert cache_info["cache_size"] == 0

        # Call function and check cache size
        test_function(5)
        cache_info = test_function._cache_info()
        assert cache_info["cache_size"] == 1

    def test_function_update_invalidation(self):
        """Test that cache is invalidated when function is updated."""
        # This test is tricky to implement since we can't actually modify
        # function source during test execution. We'll use mocking.

        call_count = 0

        @cache_with_invalidation()
        def dynamic_function(x):
            nonlocal call_count
            call_count += 1
            return x * 2

        # First call
        result1 = dynamic_function(5)
        assert result1 == 10
        assert call_count == 1

        # Cached call
        result2 = dynamic_function(5)
        assert result2 == 10
        assert call_count == 1

        # Mock function signature change
        with patch(
            "ai.utilities.function_cache.cache_decorator._get_function_signature"
        ) as mock_sig:
            mock_sig.return_value = "different_signature"

            # This should invalidate cache and call function again
            result3 = dynamic_function(5)
            assert result3 == 10
            assert call_count == 2
