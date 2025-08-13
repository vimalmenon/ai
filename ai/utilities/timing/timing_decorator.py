import functools
import time
from collections.abc import Callable
from datetime import datetime
from typing import ParamSpec, TypeVar

P = ParamSpec("P")
T = TypeVar("T")


def timing(func: Callable[P, T]) -> Callable[P, T]:
    """
    A decorator that measures and logs the execution time of a function.

    Shows:
    - Function start time
    - Function end time
    - Total execution time in seconds

    Usage:
        @timing
        def my_function():
            # Your code here
            pass
    """

    @functools.wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
        # Get function name
        func_name = func.__name__

        # Record start time
        start_time = time.time()
        start_datetime = datetime.now()

        print(
            f"[TIMING] {func_name} started at: "
            f"{start_datetime.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]}"
        )

        try:
            # Execute the function
            result = func(*args, **kwargs)

            # Record end time
            end_time = time.time()
            end_datetime = datetime.now()
            execution_time = end_time - start_time

            print(
                f"[TIMING] {func_name} ended at: "
                f"{end_datetime.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]}"
            )
            print(f"[TIMING] {func_name} took {execution_time:.3f} seconds")

            return result

        except Exception as e:
            # Record end time even if function fails
            end_time = time.time()
            end_datetime = datetime.now()
            execution_time = end_time - start_time

            print(
                f"[TIMING] {func_name} failed at: "
                f"{end_datetime.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]}"
            )
            print(f"[TIMING] {func_name} took {execution_time:.3f} seconds before failing")

            # Re-raise the exception
            raise e

    return wrapper


def timing_context(name: str = "Operation"):
    """
    A context manager version for timing code blocks.

    Usage:
        with timing_context("Database Query"):
            # Your code here
            pass
    """

    class TimingContext:
        def __init__(self, operation_name: str):
            self.name = operation_name
            self.start_time = None
            self.start_datetime = None

        def __enter__(self):
            self.start_time = time.time()
            self.start_datetime = datetime.now()
            print(
                f"[TIMING] {self.name} started at: "
                f"{self.start_datetime.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]}"
            )
            return self

        def __exit__(self, exc_type, exc_val, exc_tb):
            end_time = time.time()
            end_datetime = datetime.now()
            execution_time = end_time - self.start_time

            if exc_type is None:
                print(
                    f"[TIMING] {self.name} ended at: "
                    f"{end_datetime.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]}"
                )
                print(f"[TIMING] {self.name} took {execution_time:.3f} seconds")
            else:
                print(
                    f"[TIMING] {self.name} failed at: "
                    f"{end_datetime.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]}"
                )
                print(f"[TIMING] {self.name} took {execution_time:.3f} seconds before failing")

    return TimingContext(name)
