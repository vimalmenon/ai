"""
Function caching utility with invalidation support.

This module provides a caching decorator that can cache function results
and invalidate the cache when the function is updated or when explicitly cleared.
"""

import functools
import hashlib
import inspect
import pickle
import threading
from collections.abc import Callable
from typing import Any, TypeVar

F = TypeVar("F", bound=Callable[..., Any])

# Global cache storage
_cache_store: dict[str, Any] = {}
_cache_lock = threading.RLock()
_function_signatures: dict[str, str] = {}
_cached_functions: set[str] = set()


def _get_function_signature(func: Callable) -> str:
    """Get a hash of the function's source code and signature."""
    try:
        source = inspect.getsource(func)
        signature = str(inspect.signature(func))
        combined = f"{source}{signature}"
        return hashlib.sha256(combined.encode()).hexdigest()
    except (OSError, TypeError):
        # Fallback to function name and module if source is not available
        return f"{func.__module__}.{func.__qualname__}"


def _get_cache_key(func: Callable, args: tuple, kwargs: dict) -> str:
    """Generate a cache key for the function call."""
    func_name = f"{func.__module__}.{func.__qualname__}"

    # Normalize arguments by binding them to the function signature
    try:
        sig = inspect.signature(func)
        bound_args = sig.bind(*args, **kwargs)
        bound_args.apply_defaults()

        # Create a normalized representation
        normalized_kwargs = dict(bound_args.arguments)

        # Create a deterministic key from normalized arguments
        try:
            sorted_items = tuple(sorted(normalized_kwargs.items()))
            args_key = pickle.dumps(sorted_items)
            args_hash = hashlib.sha256(args_key).hexdigest()
        except (pickle.PicklingError, TypeError):
            # Fallback to string representation if pickling fails
            sorted_items_list = sorted(normalized_kwargs.items())
            args_str = str(sorted_items_list)
            args_hash = hashlib.sha256(args_str.encode()).hexdigest()

    except (TypeError, ValueError):
        # Fallback to original method if signature binding fails
        try:
            # Sort kwargs to ensure consistent ordering
            sorted_kwargs = tuple(sorted(kwargs.items())) if kwargs else ()
            combined_args = (args, sorted_kwargs)
            args_key = pickle.dumps(combined_args)
            args_hash = hashlib.sha256(args_key).hexdigest()
        except (pickle.PicklingError, TypeError):
            # Fallback to string representation if pickling fails
            sorted_kwargs_list = sorted(kwargs.items()) if kwargs else []
            args_str = f"{args}{sorted_kwargs_list}"
            args_hash = hashlib.sha256(args_str.encode()).hexdigest()

    return f"{func_name}:{args_hash}"


def _is_function_updated(func: Callable) -> bool:
    """Check if the function has been updated since last cached."""
    func_id = f"{func.__module__}.{func.__qualname__}"
    current_signature = _get_function_signature(func)

    if func_id not in _function_signatures:
        _function_signatures[func_id] = current_signature
        return False

    if _function_signatures[func_id] != current_signature:
        _function_signatures[func_id] = current_signature
        return True

    return False


def cache_with_invalidation(
    ttl: float | None = None, maxsize: int | None = None, typed: bool = False
) -> Callable[[F], F]:
    """
    A decorator that caches function results with automatic invalidation.

    The cache is automatically invalidated when:
    1. The function code is updated
    2. The cache is explicitly cleared
    3. TTL expires (if specified)
    4. Max size is reached (if specified)

    Args:
        ttl: Time to live in seconds. If None, cache never expires.
        maxsize: Maximum number of cached items. If None, unlimited cache size.
        typed: If True, function arguments with different types will be cached separately.

    Returns:
        The decorated function with caching capabilities.

    Example:
        @cache_with_invalidation(ttl=3600, maxsize=100)
        def expensive_function(x, y):
            return x + y
    """

    def decorator(func: F) -> F:
        func_id = f"{func.__module__}.{func.__qualname__}"
        _cached_functions.add(func_id)

        # Initialize function signature
        _function_signatures[func_id] = _get_function_signature(func)

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Check if function has been updated
            if _is_function_updated(func):
                clear_cache(func)

            cache_key = _get_cache_key(func, args, kwargs)

            # Add type information if typed=True
            if typed:
                type_info = tuple(type(arg).__name__ for arg in args)
                type_info += tuple(f"{k}:{type(v).__name__}" for k, v in kwargs.items())
                cache_key += f":types:{hash(type_info)}"

            with _cache_lock:
                # Check if we have a cached result
                if cache_key in _cache_store:
                    cached_item = _cache_store[cache_key]

                    # Check TTL if specified
                    if ttl is not None:
                        import time

                        if time.time() - cached_item["timestamp"] > ttl:
                            del _cache_store[cache_key]
                        else:
                            # Update timestamp for LRU behavior
                            cached_item["timestamp"] = time.time()
                            return cached_item["result"]
                    else:
                        # Update timestamp for LRU behavior
                        import time

                        cached_item["timestamp"] = time.time()
                        return cached_item["result"]

                # If we get here, we need to call the function
                # Check maxsize and evict if necessary (before adding new entry)
                if maxsize is not None:
                    func_cache_keys = [
                        k for k, v in _cache_store.items() if v["function_id"] == func_id
                    ]
                    if len(func_cache_keys) >= maxsize:
                        # Find least recently used entry for this function
                        oldest_key = min(
                            func_cache_keys, key=lambda k: _cache_store[k]["timestamp"]
                        )
                        del _cache_store[oldest_key]

                # Release lock to call function (avoid holding lock during function execution)

            # Call the function (outside of lock)
            result = func(*args, **kwargs)

            # Store result in cache
            with _cache_lock:
                import time

                _cache_store[cache_key] = {
                    "result": result,
                    "timestamp": time.time(),
                    "function_id": func_id,
                }

            return result

        # Add cache management methods to the wrapper
        wrapper._cache_info = lambda: {  # type: ignore[attr-defined]
            "cache_size": len([k for k, v in _cache_store.items() if v["function_id"] == func_id]),
            "function_id": func_id,
            "ttl": ttl,
            "maxsize": maxsize,
            "typed": typed,
        }

        wrapper._clear_cache = lambda: clear_cache(func)  # type: ignore[attr-defined]

        return wrapper  # type: ignore[return-value]

    return decorator


def clear_cache(func: Callable) -> int:
    """
    Clear the cache for a specific function.

    Args:
        func: The function whose cache should be cleared.

    Returns:
        The number of cache entries that were cleared.
    """
    func_id = f"{func.__module__}.{func.__qualname__}"
    cleared_count = 0

    with _cache_lock:
        keys_to_remove = [
            key for key, value in _cache_store.items() if value["function_id"] == func_id
        ]

        for key in keys_to_remove:
            del _cache_store[key]
            cleared_count += 1

    return cleared_count


def clear_all_caches() -> int:
    """
    Clear all cached function results.

    Returns:
        The number of cache entries that were cleared.
    """
    with _cache_lock:
        cleared_count = len(_cache_store)
        _cache_store.clear()
        _function_signatures.clear()

    return cleared_count


def get_cache_stats() -> dict[str, Any]:
    """
    Get statistics about the current cache state.

    Returns:
        A dictionary containing cache statistics.
    """
    with _cache_lock:
        total_entries = len(_cache_store)
        functions_cached = len(set(v["function_id"] for v in _cache_store.values()))

        function_stats = {}
        for value in _cache_store.values():
            func_id = value["function_id"]
            if func_id not in function_stats:
                function_stats[func_id] = 0
            function_stats[func_id] += 1

        return {
            "total_cache_entries": total_entries,
            "cached_functions_count": functions_cached,
            "registered_functions": list(_cached_functions),
            "function_cache_counts": function_stats,
        }
