"""
Global state department.  Don't reload this module or everything breaks.
"""
from __future__ import annotations
import os
import sys
import warnings
from collections.abc import Iterable, Sequence
from typing import Any, Callable, cast
from ._native import make_filtering_bound_logger
from ._output import PrintLoggerFactory
from .contextvars import merge_contextvars
from .dev import ConsoleRenderer, _has_colors, set_exc_info
from .processors import StackInfoRenderer, TimeStamper, add_log_level
from .typing import BindableLogger, Context, Processor, WrappedLogger
"\nAny changes to these defaults must be reflected in:\n\n- `getting-started`.\n- structlog.stdlib.recreate_defaults()'s docstring.\n"
_no_colors = os.environ.get('NO_COLOR', '') != ''
_force_colors = os.environ.get('FORCE_COLOR', '') != ''
_BUILTIN_DEFAULT_PROCESSORS: Sequence[Processor] = [merge_contextvars, add_log_level, StackInfoRenderer(), set_exc_info, TimeStamper(fmt='%Y-%m-%d %H:%M:%S', utc=False), ConsoleRenderer(colors=not _no_colors and (_force_colors or (_has_colors and sys.stdout is not None and hasattr(sys.stdout, 'isatty') and sys.stdout.isatty())), force_colors=_force_colors)]
_BUILTIN_DEFAULT_CONTEXT_CLASS = cast(type[Context], dict)
_BUILTIN_DEFAULT_WRAPPER_CLASS = make_filtering_bound_logger(0)
_BUILTIN_DEFAULT_LOGGER_FACTORY = PrintLoggerFactory()
_BUILTIN_CACHE_LOGGER_ON_FIRST_USE = False

class _Configuration:
    """
    Global defaults.
    """
    is_configured: bool = False
    default_processors: Iterable[Processor] = _BUILTIN_DEFAULT_PROCESSORS[:]
    default_context_class: type[Context] = _BUILTIN_DEFAULT_CONTEXT_CLASS
    default_wrapper_class: Any = _BUILTIN_DEFAULT_WRAPPER_CLASS
    logger_factory: Callable[..., WrappedLogger] = _BUILTIN_DEFAULT_LOGGER_FACTORY
    cache_logger_on_first_use: bool = _BUILTIN_CACHE_LOGGER_ON_FIRST_USE
_CONFIG = _Configuration()
'\nGlobal defaults used when arguments to `wrap_logger` are omitted.\n'

def is_configured() -> bool:
    """
    Return whether *structlog* has been configured.

    If `False`, *structlog* is running with builtin defaults.

    .. versionadded: 18.1.0
    """
    pass

def get_config() -> dict[str, Any]:
    """
    Get a dictionary with the current configuration.

    .. note::

       Changes to the returned dictionary do *not* affect *structlog*.

    .. versionadded: 18.1.0
    """
    pass

def get_logger(*args: Any, **initial_values: Any) -> Any:
    """
    Convenience function that returns a logger according to configuration.

    >>> from structlog import get_logger
    >>> log = get_logger(y=23)
    >>> log.info("hello", x=42)
    y=23 x=42 event='hello'

    Args:
        args:
            *Optional* positional arguments that are passed unmodified to the
            logger factory.  Therefore it depends on the factory what they
            mean.

        initial_values: Values that are used to pre-populate your contexts.

    Returns:
        A proxy that creates a correctly configured bound logger when
        necessary. The type of that bound logger depends on your configuration
        and is `structlog.BoundLogger` by default.

    See `configuration` for details.

    If you prefer CamelCase, there's an alias for your reading pleasure:
    `structlog.getLogger`.

    .. versionadded:: 0.4.0 *args*
    """
    pass
getLogger = get_logger
"\nCamelCase alias for `structlog.get_logger`.\n\nThis function is supposed to be in every source file -- we don't want it to\nstick out like a sore thumb in frameworks like Twisted or Zope.\n"

def wrap_logger(logger: WrappedLogger | None, processors: Iterable[Processor] | None=None, wrapper_class: type[BindableLogger] | None=None, context_class: type[Context] | None=None, cache_logger_on_first_use: bool | None=None, logger_factory_args: Iterable[Any] | None=None, **initial_values: Any) -> Any:
    """
    Create a new bound logger for an arbitrary *logger*.

    Default values for *processors*, *wrapper_class*, and *context_class* can
    be set using `configure`.

    If you set an attribute here, `configure` calls have *no* effect for the
    *respective* attribute.

    In other words: selective overwriting of the defaults while keeping some
    *is* possible.

    Args:
        initial_values: Values that are used to pre-populate your contexts.

        logger_factory_args:
            Values that are passed unmodified as ``*logger_factory_args`` to
            the logger factory if not `None`.

    Returns:
        A proxy that creates a correctly configured bound logger when
        necessary.

    See `configure` for the meaning of the rest of the arguments.

    .. versionadded:: 0.4.0 *logger_factory_args*
    """
    pass

def configure(processors: Iterable[Processor] | None=None, wrapper_class: type[BindableLogger] | None=None, context_class: type[Context] | None=None, logger_factory: Callable[..., WrappedLogger] | None=None, cache_logger_on_first_use: bool | None=None) -> None:
    """
    Configures the **global** defaults.

    They are used if `wrap_logger` or `get_logger` are called without
    arguments.

    Can be called several times, keeping an argument at `None` leaves it
    unchanged from the current setting.

    After calling for the first time, `is_configured` starts returning `True`.

    Use `reset_defaults` to undo your changes.

    Args:
        processors: The processor chain. See :doc:`processors` for details.

        wrapper_class:
            Class to use for wrapping loggers instead of
            `structlog.BoundLogger`.  See `standard-library`, :doc:`twisted`,
            and `custom-wrappers`.

        context_class:
            Class to be used for internal context keeping. The default is a
            `dict` and since dictionaries are ordered as of Python 3.6, there's
            few reasons to change this option.

        logger_factory:
            Factory to be called to create a new logger that shall be wrapped.

        cache_logger_on_first_use:
            `wrap_logger` doesn't return an actual wrapped logger but a proxy
            that assembles one when it's first used. If this option is set to
            `True`, this assembled logger is cached. See `performance`.

    .. versionadded:: 0.3.0 *cache_logger_on_first_use*
    """
    pass

def configure_once(processors: Iterable[Processor] | None=None, wrapper_class: type[BindableLogger] | None=None, context_class: type[Context] | None=None, logger_factory: Callable[..., WrappedLogger] | None=None, cache_logger_on_first_use: bool | None=None) -> None:
    """
    Configures if structlog isn't configured yet.

    It does *not* matter whether it was configured using `configure` or
    `configure_once` before.

    Raises:
        RuntimeWarning: if repeated configuration is attempted.
    """
    pass

def reset_defaults() -> None:
    """
    Resets global default values to builtin defaults.

    `is_configured` starts returning `False` afterwards.
    """
    pass

class BoundLoggerLazyProxy:
    """
    Instantiates a bound logger on first usage.

    Takes both configuration and instantiation parameters into account.

    The only points where a bound logger changes state are ``bind()``,
    ``unbind()``, and ``new()`` and that return the actual ``BoundLogger``.

    If and only if configuration says so, that actual bound logger is cached on
    first usage.

    .. versionchanged:: 0.4.0 Added support for *logger_factory_args*.
    """

    @property
    def _context(self) -> dict[str, str]:
        pass

    def __init__(self, logger: WrappedLogger | None, wrapper_class: type[BindableLogger] | None=None, processors: Iterable[Processor] | None=None, context_class: type[Context] | None=None, cache_logger_on_first_use: bool | None=None, initial_values: dict[str, Any] | None=None, logger_factory_args: Any=None) -> None:
        self._logger = logger
        self._wrapper_class = wrapper_class
        self._processors = processors
        self._context_class = context_class
        self._cache_logger_on_first_use = cache_logger_on_first_use
        self._initial_values = initial_values or {}
        self._logger_factory_args = logger_factory_args or ()

    def __repr__(self) -> str:
        return f'<BoundLoggerLazyProxy(logger={self._logger!r}, wrapper_class={self._wrapper_class!r}, processors={self._processors!r}, context_class={self._context_class!r}, initial_values={self._initial_values!r}, logger_factory_args={self._logger_factory_args!r})>'

    def bind(self, **new_values: Any) -> BindableLogger:
        """
        Assemble a new BoundLogger from arguments and configuration.
        """
        pass

    def unbind(self, *keys: str) -> BindableLogger:
        """
        Same as bind, except unbind *keys* first.

        In our case that could be only initial values.
        """
        pass

    def try_unbind(self, *keys: str) -> BindableLogger:
        pass

    def new(self, **new_values: Any) -> BindableLogger:
        """
        Clear context, then bind.
        """
        pass

    def __getattr__(self, name: str) -> Any:
        """
        If a logging method if called on a lazy proxy, we have to create an
        ephemeral BoundLogger first.
        """
        if name == '__isabstractmethod__':
            raise AttributeError
        bl = self.bind()
        return getattr(bl, name)

    def __getstate__(self) -> dict[str, Any]:
        """
        Our __getattr__ magic makes this necessary.
        """
        return self.__dict__

    def __setstate__(self, state: dict[str, Any]) -> None:
        """
        Our __getattr__ magic makes this necessary.
        """
        for k, v in state.items():
            setattr(self, k, v)