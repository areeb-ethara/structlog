"""
Type information used throughout *structlog*.

For now, they are considered provisional. Especially `BindableLogger` will
probably change to something more elegant.

.. versionadded:: 22.2.0
"""
from __future__ import annotations
import sys
from collections.abc import Mapping, MutableMapping
from types import TracebackType
from typing import Any, Callable, Optional, Protocol, TextIO, Union, runtime_checkable
if sys.version_info >= (3, 11):
    from typing import Self
else:
    from typing_extensions import Self
WrappedLogger = Any
'\nA logger that is wrapped by a bound logger and is ultimately responsible for\nthe output of the log entries.\n\n*structlog* makes *no* assumptions about it.\n\n.. versionadded:: 20.2.0\n'
Context = Union[dict[str, Any], dict[Any, Any]]
'\nA dict-like context carrier.\n\n.. versionadded:: 20.2.0\n'
EventDict = MutableMapping[str, Any]
"\nAn event dictionary as it is passed into processors.\n\nIt's created by copying the configured `Context` but doesn't need to support\ncopy itself.\n\n.. versionadded:: 20.2.0\n"
ProcessorReturnValue = Union[Mapping[str, Any], str, bytes, bytearray, tuple[Any, ...]]
'\nA value returned by a processor.\n'
Processor = Callable[[WrappedLogger, str, EventDict], ProcessorReturnValue]
'\nA callable that is part of the processor chain.\n\nSee :doc:`processors`.\n\n.. versionadded:: 20.2.0\n'
ExcInfo = tuple[type[BaseException], BaseException, Optional[TracebackType]]
'\nAn exception info tuple as returned by `sys.exc_info`.\n\n.. versionadded:: 20.2.0\n'
ExceptionRenderer = Callable[[TextIO, ExcInfo], None]
'\nA callable that pretty-prints an `ExcInfo` into a file-like object.\n\nUsed by `structlog.dev.ConsoleRenderer`.\n\n.. versionadded:: 21.2.0\n'

@runtime_checkable
class ExceptionTransformer(Protocol):
    """
    **Protocol:** A callable that transforms an `ExcInfo` into another
    datastructure.

    The result should be something that your renderer can work with, e.g., a
    ``str`` or a JSON-serializable ``dict``.

    Used by `structlog.processors.format_exc_info()` and
    `structlog.processors.ExceptionPrettyPrinter`.

    Args:
        exc_info: Is the exception tuple to format

    Returns:
        Anything that can be rendered by the last processor in your chain, for
        example, a string or a JSON-serializable structure.

    .. versionadded:: 22.1.0
    """

    def __call__(self, exc_info: ExcInfo) -> Any:
        ...

@runtime_checkable
class BindableLogger(Protocol):
    """
    **Protocol**: Methods shared among all bound loggers and that are relied on
    by *structlog*.

    .. versionadded:: 20.2.0
    """

    @property
    def _context(self) -> Context:
        pass

    def bind(self, **new_values: Any) -> Self:
        pass

    def unbind(self, *keys: str) -> Self:
        pass

    def try_unbind(self, *keys: str) -> Self:
        pass

    def new(self, **new_values: Any) -> Self:
        pass

class FilteringBoundLogger(BindableLogger, Protocol):
    """
    **Protocol**: A `BindableLogger` that filters by a level.

    The only way to instantiate one is using `make_filtering_bound_logger`.

    .. versionadded:: 20.2.0
    .. versionadded:: 22.2.0 String interpolation using positional arguments.
    .. versionadded:: 22.2.0
       Async variants ``alog()``, ``adebug()``, ``ainfo()``, and so forth.
    .. versionchanged:: 22.3.0
       String interpolation is only attempted if positional arguments are
       passed.
    .. versionadded:: 25.5.0
       String interpolation using dictionary-based arguments if the first and
       only argument is a mapping.

    """

    def bind(self, **new_values: Any) -> FilteringBoundLogger:
        """
        Return a new logger with *new_values* added to the existing ones.

        .. versionadded:: 22.1.0
        """
        pass

    def unbind(self, *keys: str) -> FilteringBoundLogger:
        """
        Return a new logger with *keys* removed from the context.

        .. versionadded:: 22.1.0
        """
        pass

    def try_unbind(self, *keys: str) -> FilteringBoundLogger:
        """
        Like :meth:`unbind`, but best effort: missing keys are ignored.

        .. versionadded:: 22.1.0
        """
        pass

    def new(self, **new_values: Any) -> FilteringBoundLogger:
        """
        Clear context and binds *initial_values* using `bind`.

        .. versionadded:: 22.1.0
        """
        pass

    def is_enabled_for(self, level: int) -> bool:
        """
        Check whether the logger is enabled for *level*.

        .. versionadded:: 25.1.0
        """
        pass

    def get_effective_level(self) -> int:
        """
        Return the effective level of the logger.

        .. versionadded:: 25.1.0
        """
        pass

    def debug(self, event: str, *args: Any, **kw: Any) -> Any:
        """
        Log ``event % args`` with **kw** at **debug** level.
        """
        pass

    async def adebug(self, event: str, *args: Any, **kw: Any) -> Any:
        """
        Log ``event % args`` with **kw** at **debug** level.

        ..versionadded:: 22.2.0
        """
        pass

    def info(self, event: str, *args: Any, **kw: Any) -> Any:
        """
        Log ``event % args`` with **kw** at **info** level.
        """
        pass

    async def ainfo(self, event: str, *args: Any, **kw: Any) -> Any:
        """
        Log ``event % args`` with **kw** at **info** level.

        ..versionadded:: 22.2.0
        """
        pass

    def warning(self, event: str, *args: Any, **kw: Any) -> Any:
        """
        Log ``event % args`` with **kw** at **warn** level.
        """
        pass

    async def awarning(self, event: str, *args: Any, **kw: Any) -> Any:
        """
        Log ``event % args`` with **kw** at **warn** level.

        ..versionadded:: 22.2.0
        """
        pass

    def warn(self, event: str, *args: Any, **kw: Any) -> Any:
        """
        Log ``event % args`` with **kw** at **warn** level.
        """
        pass

    async def awarn(self, event: str, *args: Any, **kw: Any) -> Any:
        """
        Log ``event % args`` with **kw** at **warn** level.

        ..versionadded:: 22.2.0
        """
        pass

    def error(self, event: str, *args: Any, **kw: Any) -> Any:
        """
        Log ``event % args`` with **kw** at **error** level.
        """
        pass

    async def aerror(self, event: str, *args: Any, **kw: Any) -> Any:
        """
        Log ``event % args`` with **kw** at **error** level.

        ..versionadded:: 22.2.0
        """
        pass

    def err(self, event: str, *args: Any, **kw: Any) -> Any:
        """
        Log ``event % args`` with **kw** at **error** level.
        """
        pass

    def fatal(self, event: str, *args: Any, **kw: Any) -> Any:
        """
        Log ``event % args`` with **kw** at **critical** level.
        """
        pass

    async def afatal(self, event: str, *args: Any, **kw: Any) -> Any:
        """
        Log ``event % args`` with **kw** at **critical** level.

        ..versionadded:: 22.2.0
        """
        pass

    def exception(self, event: str, *args: Any, **kw: Any) -> Any:
        """
        Log ``event % args`` with **kw** at **error** level and ensure that
        ``exc_info`` is set in the event dictionary.
        """
        pass

    async def aexception(self, event: str, *args: Any, **kw: Any) -> Any:
        """
        Log ``event % args`` with **kw** at **error** level and ensure that
        ``exc_info`` is set in the event dictionary.

        ..versionadded:: 22.2.0
        """
        pass

    def critical(self, event: str, *args: Any, **kw: Any) -> Any:
        """
        Log ``event % args`` with **kw** at **critical** level.
        """
        pass

    async def acritical(self, event: str, *args: Any, **kw: Any) -> Any:
        """
        Log ``event % args`` with **kw** at **critical** level.

        ..versionadded:: 22.2.0
        """
        pass

    def msg(self, event: str, *args: Any, **kw: Any) -> Any:
        """
        Log ``event % args`` with **kw** at **info** level.
        """
        pass

    async def amsg(self, event: str, *args: Any, **kw: Any) -> Any:
        """
        Log ``event % args`` with **kw** at **info** level.
        """
        pass

    def log(self, level: int, event: str, *args: Any, **kw: Any) -> Any:
        """
        Log ``event % args`` with **kw** at *level*.
        """
        pass

    async def alog(self, level: int, event: str, *args: Any, **kw: Any) -> Any:
        """
        Log ``event % args`` with **kw** at *level*.
        """
        pass