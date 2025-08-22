import functools
import logging
import time
from collections.abc import Callable
from datetime import datetime
from enum import Enum
from typing import ParamSpec, TypeVar

P = ParamSpec("P")
T = TypeVar("T")


class TimingOutput(Enum):
    """Output destinations for timing information."""

    PRINT = "print"
    LOG = "log"
    BOTH = "both"


class TimingFormatter:
    """Handles formatting of timing messages."""

    @staticmethod
    def format_datetime(dt: datetime) -> str:
        """Format datetime with milliseconds."""
        return dt.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]

    @staticmethod
    def format_duration(seconds: float) -> str:
        """Format duration in a human-readable way."""
        if seconds < 1:
            return f"{seconds*1000:.1f}ms"
        elif seconds < 60:
            return f"{seconds:.3f}s"
        else:
            minutes = int(seconds // 60)
            remaining_seconds = seconds % 60
            return f"{minutes}m {remaining_seconds:.3f}s"


def timing(
    output: TimingOutput = TimingOutput.PRINT,
    logger: logging.Logger | None = None,
    log_level: int = logging.INFO,
    include_args: bool = False,
):
    """
    A decorator that measures and logs the execution time of a function.

    Args:
        output: Where to send timing output (PRINT, LOG, or BOTH)
        logger: Custom logger to use (if None, creates a default one)
        log_level: Log level for timing messages
        include_args: Whether to include function arguments in timing logs

    Shows:
    - Function start time
    - Function end time
    - Total execution time

    Usage:
        @timing()
        def my_function():
            pass

        @timing(output=TimingOutput.LOG, include_args=True)
        def my_function_with_logging(param1, param2):
            pass
    """

    def decorator(func: Callable[P, T]) -> Callable[P, T]:
        @functools.wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
            # Setup logger if needed
            if output in [TimingOutput.LOG, TimingOutput.BOTH]:
                log = logger or logging.getLogger(f"timing.{func.__module__}.{func.__name__}")

            # Get function name and arguments
            func_name = func.__name__
            args_str = ""
            if include_args and (args or kwargs):
                args_repr = [repr(arg) for arg in args]
                kwargs_repr = [f"{k}={repr(v)}" for k, v in kwargs.items()]
                all_args = args_repr + kwargs_repr
                args_str = f"({', '.join(all_args)})"

            # Record start time
            start_time = time.time()
            start_datetime = datetime.now()

            start_msg = (
                f"{func_name}{args_str} started at: "
                f"{TimingFormatter.format_datetime(start_datetime)}"
            )

            # Output start message
            if output in [TimingOutput.PRINT, TimingOutput.BOTH]:
                print(f"[TIMING] {start_msg}")
            if output in [TimingOutput.LOG, TimingOutput.BOTH]:
                log.log(log_level, f"[START] {start_msg}")

            try:
                # Execute the function
                result = func(*args, **kwargs)

                # Record end time
                end_time = time.time()
                end_datetime = datetime.now()
                execution_time = end_time - start_time

                end_msg = (
                    f"{func_name}{args_str} ended at: "
                    f"{TimingFormatter.format_datetime(end_datetime)}"
                )
                duration_msg = (
                    f"{func_name}{args_str} took {TimingFormatter.format_duration(execution_time)}"
                )

                # Output end messages
                if output in [TimingOutput.PRINT, TimingOutput.BOTH]:
                    print(f"[TIMING] {end_msg}")
                    print(f"[TIMING] {duration_msg}")
                if output in [TimingOutput.LOG, TimingOutput.BOTH]:
                    log.log(log_level, f"[END] {end_msg}")
                    log.log(log_level, f"[DURATION] {duration_msg}")

                return result

            except Exception as e:
                # Record end time even if function fails
                end_time = time.time()
                end_datetime = datetime.now()
                execution_time = end_time - start_time

                error_msg = (
                    f"{func_name}{args_str} failed at: "
                    f"{TimingFormatter.format_datetime(end_datetime)}"
                )
                duration_msg = (
                    f"{func_name}{args_str} took "
                    f"{TimingFormatter.format_duration(execution_time)} before failing"
                )

                # Output error messages
                if output in [TimingOutput.PRINT, TimingOutput.BOTH]:
                    print(f"[TIMING] {error_msg}")
                    print(f"[TIMING] {duration_msg}")
                if output in [TimingOutput.LOG, TimingOutput.BOTH]:
                    log.log(logging.ERROR, f"[ERROR] {error_msg}")
                    log.log(logging.ERROR, f"[DURATION] {duration_msg}")

                # Re-raise the exception
                raise e

        return wrapper

    return decorator


def timing_context(
    name: str = "Operation",
    output: TimingOutput = TimingOutput.PRINT,
    logger: logging.Logger | None = None,
    log_level: int = logging.INFO,
):
    """
    A context manager version for timing code blocks.

    Args:
        name: Name of the operation being timed
        output: Where to send timing output (PRINT, LOG, or BOTH)
        logger: Custom logger to use
        log_level: Log level for timing messages

    Usage:
        with timing_context("Database Query"):
            # Your code here
            pass

        with timing_context("API Call", output=TimingOutput.LOG):
            # Your code here
            pass
    """

    class TimingContext:
        def __init__(self, operation_name: str):
            self.name = operation_name
            self.start_time = None
            self.start_datetime = None

            # Setup logger if needed
            if output in [TimingOutput.LOG, TimingOutput.BOTH]:
                self.log = logger or logging.getLogger(f"timing.context.{operation_name}")

        def __enter__(self):
            self.start_time = time.time()
            self.start_datetime = datetime.now()

            start_msg = (
                f"{self.name} started at: {TimingFormatter.format_datetime(self.start_datetime)}"
            )

            if output in [TimingOutput.PRINT, TimingOutput.BOTH]:
                print(f"[TIMING] {start_msg}")
            if output in [TimingOutput.LOG, TimingOutput.BOTH]:
                self.log.log(log_level, f"[START] {start_msg}")

            return self

        def __exit__(self, exc_type, exc_val, exc_tb):
            end_time = time.time()
            end_datetime = datetime.now()
            execution_time = end_time - self.start_time

            if exc_type is None:
                end_msg = f"{self.name} ended at: {TimingFormatter.format_datetime(end_datetime)}"
                duration_msg = f"{self.name} took {TimingFormatter.format_duration(execution_time)}"

                if output in [TimingOutput.PRINT, TimingOutput.BOTH]:
                    print(f"[TIMING] {end_msg}")
                    print(f"[TIMING] {duration_msg}")
                if output in [TimingOutput.LOG, TimingOutput.BOTH]:
                    self.log.log(log_level, f"[END] {end_msg}")
                    self.log.log(log_level, f"[DURATION] {duration_msg}")
            else:
                error_msg = (
                    f"{self.name} failed at: {TimingFormatter.format_datetime(end_datetime)}"
                )
                duration_msg = (
                    f"{self.name} took "
                    f"{TimingFormatter.format_duration(execution_time)} before failing"
                )

                if output in [TimingOutput.PRINT, TimingOutput.BOTH]:
                    print(f"[TIMING] {error_msg}")
                    print(f"[TIMING] {duration_msg}")
                if output in [TimingOutput.LOG, TimingOutput.BOTH]:
                    self.log.log(logging.ERROR, f"[ERROR] {error_msg}")
                    self.log.log(logging.ERROR, f"[DURATION] {duration_msg}")

    return TimingContext(name)
