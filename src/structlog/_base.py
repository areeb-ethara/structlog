"""
Logger wrapper and helper class.
"""
from __future__ import annotations
import sys
from collections.abc import Iterable, Mapping, Sequence
from typing import Any
from structlog.exceptions import DropEvent
from .typing import BindableLogger, Context, Processor, WrappedLogger
if sys.version_info >= (3, 11):
    from typing import Self
else:
    from typing_extensions import Self

class BoundLoggerBase:
    """
    Immutable context carrier.

    Doesn't do any actual logging; examples for useful subclasses are:

    - the generic `BoundLogger` that can wrap anything,
    - `structlog.stdlib.BoundLogger`.
    - `structlog.twisted.BoundLogger`,

    See also `custom-wrappers`.
    """
    _logger: WrappedLogger
    '\n    Wrapped logger.\n\n    .. note::\n\n        Despite underscore available **read-only** to custom wrapper classes.\n\n        See also `custom-wrappers`.\n    '

    def __init__(self, logger: WrappedLogger, processors: Iterable[Processor], context: Context):
        self._logger = logger
        self._processors = processors
        self._context = context

    def __repr__(self) -> str:
        return f'<{self.__class__.__name__}(context={self._context!r}, processors={self._processors!r})>'

    def __eq__(self, other: object) -> bool:
        try:
            return self._context == other._context
        except AttributeError:
            return False

    def __ne__(self, other: object) -> bool:
        return not self.__eq__(other)

    def bind(self, **new_values: Any) -> Self:
        """
        Return a new logger with *new_values* added to the existing ones.
        """
        pass

    def unbind(self, *keys: str) -> Self:
        """
        Return a new logger with *keys* removed from the context.

        Raises:
            KeyError: If the key is not part of the context.
        """
        pass

    def try_unbind(self, *keys: str) -> Self:
        """
        Like :meth:`unbind`, but best effort: missing keys are ignored.

        .. versionadded:: 18.2.0
        """
        pass

    def new(self, **new_values: Any) -> Self:
        """
        Clear context and binds *new_values* using `bind`.

        Only necessary with dict implementations that keep global state like
        those wrapped by `structlog.threadlocal.wrap_dict` when threads
        are reused.
        """
        pass

    def _process_event(self, method_name: str, event: str | None, event_kw: dict[str, Any]) -> tuple[Sequence[Any], Mapping[str, Any]]:
        """
        Combines creates an ``event_dict`` and runs the chain.

        Call it to combine your *event* and *context* into an event_dict and
        process using the processor chain.

        Args:
            method_name:
                The name of the logger method.  Is passed into the processors.

            event:
                The event -- usually the first positional argument to a logger.

            event_kw:
                Additional event keywords.  For example if someone calls
                ``log.info("foo", bar=42)``, *event* would to be ``"foo"`` and
                *event_kw* ``{"bar": 42}``.

        Raises:
            structlog.DropEvent: if log entry should be dropped.

            ValueError:
                if the final processor doesn't return a str, bytes, bytearray,
                tuple, or a dict.

        Returns:
             `tuple` of ``(*args, **kw)``

        .. note::
            Despite underscore available to custom wrapper classes.

            See also `custom-wrappers`.

        .. versionchanged:: 14.0.0
            Allow final processor to return a `dict`.
        .. versionchanged:: 20.2.0
            Allow final processor to return `bytes`.
        .. versionchanged:: 21.2.0
            Allow final processor to return a `bytearray`.
        """
        pass

    def _proxy_to_logger(self, method_name: str, event: str | None=None, **event_kw: Any) -> Any:
        """
        Run processor chain on event & call *method_name* on wrapped logger.

        DRY convenience method that runs :func:`_process_event`, takes care of
        handling :exc:`structlog.DropEvent`, and finally calls *method_name* on
        :attr:`_logger` with the result.

        Args:
            method_name:
                The name of the method that's going to get called.  Technically
                it should be identical to the method the user called because it
                also get passed into processors.

            event:
                The event -- usually the first positional argument to a logger.

            event_kw:
                Additional event keywords.  For example if someone calls
                ``log.info("foo", bar=42)``, *event* would to be ``"foo"`` and
                *event_kw* ``{"bar": 42}``.

        .. note::
            Despite underscore available to custom wrapper classes.

            See also `custom-wrappers`.
        """
        pass

def get_context(bound_logger: BindableLogger) -> Context:
    """
    Return *bound_logger*'s context.

    The type of *bound_logger* and the type returned depend on your
    configuration.

    Args:
        bound_logger: The bound logger whose context you want.

    Returns:
        The *actual* context from *bound_logger*. It is *not* copied first.

    .. versionadded:: 20.2.0
    """
    pass