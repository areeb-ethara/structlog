"""
Processors and helpers specific to the :mod:`logging` module from the `Python
standard library <https://docs.python.org/>`_.

See also :doc:`structlog's standard library support <standard-library>`.
"""
from __future__ import annotations
import asyncio
import contextvars
import functools
import logging
import sys
import warnings
from collections.abc import Collection, Iterable, Sequence
from functools import partial
from typing import Any, Callable, cast
if sys.version_info >= (3, 11):
    from typing import Self
else:
    from typing_extensions import Self
from . import _config
from ._base import BoundLoggerBase
from ._frames import _find_first_app_frame_and_name, _format_stack
from ._log_levels import LEVEL_TO_NAME, NAME_TO_LEVEL, add_log_level
from .contextvars import _ASYNC_CALLING_STACK, merge_contextvars
from .exceptions import DropEvent
from .processors import StackInfoRenderer
from .typing import Context, EventDict, ExcInfo, Processor, ProcessorReturnValue, WrappedLogger
__all__ = ['BoundLogger', 'ExtraAdder', 'LoggerFactory', 'PositionalArgumentsFormatter', 'ProcessorFormatter', 'add_log_level', 'add_log_level_number', 'add_logger_name', 'filter_by_level', 'get_logger', 'recreate_defaults', 'render_to_log_args_and_kwargs', 'render_to_log_kwargs']

def recreate_defaults(*, log_level: int | None=logging.NOTSET) -> None:
    """
    Recreate defaults on top of standard library's logging.

    The output looks the same, but goes through `logging`.

    As with vanilla defaults, the backwards-compatibility guarantees don't
    apply to the settings applied here.

    Args:
        log_level:
            If `None`, don't configure standard library logging **at all**.

            Otherwise configure it to log to `sys.stdout` at *log_level*
            (``logging.NOTSET`` being the default).

            If you need more control over `logging`, pass `None` here and
            configure it yourself.

    .. versionadded:: 22.1.0
    .. versionchanged:: 23.3.0 Added `add_logger_name`.
    .. versionchanged:: 25.1.0 Added `PositionalArgumentsFormatter`.
    """
    pass
_SENTINEL = object()

class _FixedFindCallerLogger(logging.Logger):
    """
    Change the behavior of `logging.Logger.findCaller` to cope with
    *structlog*'s extra frames.
    """

    def findCaller(self, stack_info: bool=False, stacklevel: int=1) -> tuple[str, int, str, str | None]:
        """
        Finds the first caller frame outside of structlog so that the caller
        info is populated for wrapping stdlib.

        This logger gets set as the default one when using LoggerFactory.
        """
        pass

class BoundLogger(BoundLoggerBase):
    """
    Python Standard Library version of `structlog.BoundLogger`.

    Works exactly like the generic one except that it takes advantage of
    knowing the logging methods in advance.

    Use it like::

        structlog.configure(
            wrapper_class=structlog.stdlib.BoundLogger,
        )

    It also contains a bunch of properties that pass-through to the wrapped
    `logging.Logger` which should make it work as a drop-in replacement.

    .. versionadded:: 23.1.0
       Async variants `alog()`, `adebug()`, `ainfo()`, and so forth.

    .. versionchanged:: 24.2.0
        Callsite parameters are now also collected by
        `structlog.processors.CallsiteParameterAdder` for async log methods.
    """
    _logger: logging.Logger

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
        Clear context and binds *initial_values* using `bind`.

        Only necessary with dict implementations that keep global state like
        those wrapped by `structlog.threadlocal.wrap_dict` when threads
        are reused.
        """
        pass

    def debug(self, event: str | None=None, *args: Any, **kw: Any) -> Any:
        """
        Process event and call `logging.Logger.debug` with the result.
        """
        pass

    def info(self, event: str | None=None, *args: Any, **kw: Any) -> Any:
        """
        Process event and call `logging.Logger.info` with the result.
        """
        pass

    def warning(self, event: str | None=None, *args: Any, **kw: Any) -> Any:
        """
        Process event and call `logging.Logger.warning` with the result.
        """
        pass
    warn = warning

    def error(self, event: str | None=None, *args: Any, **kw: Any) -> Any:
        """
        Process event and call `logging.Logger.error` with the result.
        """
        pass

    def critical(self, event: str | None=None, *args: Any, **kw: Any) -> Any:
        """
        Process event and call `logging.Logger.critical` with the result.
        """
        pass

    def fatal(self, event: str | None=None, *args: Any, **kw: Any) -> Any:
        """
        Process event and call `logging.Logger.critical` with the result.
        """
        pass

    def exception(self, event: str | None=None, *args: Any, **kw: Any) -> Any:
        """
        Process event and call `logging.Logger.exception` with the result,
        after setting ``exc_info`` to `True` if it's not already set.
        """
        pass

    def log(self, level: int, event: str | None=None, *args: Any, **kw: Any) -> Any:
        """
        Process *event* and call the appropriate logging method depending on
        *level*.
        """
        pass

    def _proxy_to_logger(self, method_name: str, event: str | None=None, *event_args: str, **event_kw: Any) -> Any:
        """
        Propagate a method call to the wrapped logger.

        This is the same as the superclass implementation, except that
        it also preserves positional arguments in the ``event_dict`` so
        that the stdlib's support for format strings can be used.
        """
        pass

    @property
    def name(self) -> str:
        """
        Returns :attr:`logging.Logger.name`
        """
        pass

    @property
    def level(self) -> int:
        """
        Returns :attr:`logging.Logger.level`
        """
        pass

    @property
    def parent(self) -> Any:
        """
        Returns :attr:`logging.Logger.parent`
        """
        pass

    @property
    def propagate(self) -> bool:
        """
        Returns :attr:`logging.Logger.propagate`
        """
        pass

    @property
    def handlers(self) -> Any:
        """
        Returns :attr:`logging.Logger.handlers`
        """
        pass

    @property
    def disabled(self) -> int:
        """
        Returns :attr:`logging.Logger.disabled`
        """
        pass

    def setLevel(self, level: int) -> None:
        """
        Calls :meth:`logging.Logger.setLevel` with unmodified arguments.
        """
        pass

    def findCaller(self, stack_info: bool=False, stacklevel: int=1) -> tuple[str, int, str, str | None]:
        """
        Calls :meth:`logging.Logger.findCaller` with unmodified arguments.
        """
        pass

    def makeRecord(self, name: str, level: int, fn: str, lno: int, msg: str, args: tuple[Any, ...], exc_info: ExcInfo, func: str | None=None, extra: Any=None) -> logging.LogRecord:
        """
        Calls :meth:`logging.Logger.makeRecord` with unmodified arguments.
        """
        pass

    def handle(self, record: logging.LogRecord) -> None:
        """
        Calls :meth:`logging.Logger.handle` with unmodified arguments.
        """
        pass

    def addHandler(self, hdlr: logging.Handler) -> None:
        """
        Calls :meth:`logging.Logger.addHandler` with unmodified arguments.
        """
        pass

    def removeHandler(self, hdlr: logging.Handler) -> None:
        """
        Calls :meth:`logging.Logger.removeHandler` with unmodified arguments.
        """
        pass

    def hasHandlers(self) -> bool:
        """
        Calls :meth:`logging.Logger.hasHandlers` with unmodified arguments.

        Exists only in Python 3.
        """
        pass

    def callHandlers(self, record: logging.LogRecord) -> None:
        """
        Calls :meth:`logging.Logger.callHandlers` with unmodified arguments.
        """
        pass

    def getEffectiveLevel(self) -> int:
        """
        Calls :meth:`logging.Logger.getEffectiveLevel` with unmodified
        arguments.
        """
        pass

    def isEnabledFor(self, level: int) -> bool:
        """
        Calls :meth:`logging.Logger.isEnabledFor` with unmodified arguments.
        """
        pass

    def getChild(self, suffix: str) -> logging.Logger:
        """
        Calls :meth:`logging.Logger.getChild` with unmodified arguments.
        """
        pass

    async def _dispatch_to_sync(self, meth: Callable[..., Any], event: str, args: tuple[Any, ...], kw: dict[str, Any]) -> None:
        """
        Merge contextvars and log using the sync logger in a thread pool.
        """
        pass

    async def adebug(self, event: str, *args: Any, **kw: Any) -> None:
        """
        Log using `debug()`, but asynchronously in a separate thread.

        .. versionadded:: 23.1.0
        """
        pass

    async def ainfo(self, event: str, *args: Any, **kw: Any) -> None:
        """
        Log using `info()`, but asynchronously in a separate thread.

        .. versionadded:: 23.1.0
        """
        pass

    async def awarning(self, event: str, *args: Any, **kw: Any) -> None:
        """
        Log using `warning()`, but asynchronously in a separate thread.

        .. versionadded:: 23.1.0
        """
        pass

    async def aerror(self, event: str, *args: Any, **kw: Any) -> None:
        """
        Log using `error()`, but asynchronously in a separate thread.

        .. versionadded:: 23.1.0
        """
        pass

    async def acritical(self, event: str, *args: Any, **kw: Any) -> None:
        """
        Log using `critical()`, but asynchronously in a separate thread.

        .. versionadded:: 23.1.0
        """
        pass

    async def afatal(self, event: str, *args: Any, **kw: Any) -> None:
        """
        Log using `critical()`, but asynchronously in a separate thread.

        .. versionadded:: 23.1.0
        """
        pass

    async def aexception(self, event: str, *args: Any, **kw: Any) -> None:
        """
        Log using `exception()`, but asynchronously in a separate thread.

        .. versionadded:: 23.1.0
        """
        pass

    async def alog(self, level: Any, event: str, *args: Any, **kw: Any) -> None:
        """
        Log using `log()`, but asynchronously in a separate thread.

        .. versionadded:: 23.1.0
        """
        pass

def get_logger(*args: Any, **initial_values: Any) -> BoundLogger:
    """
    Only calls `structlog.get_logger`, but has the correct type hints.

    .. warning::

       Does **not** check whether -- or ensure that -- you've configured
       *structlog* for standard library :mod:`logging`!

       See :doc:`standard-library` for details.

    .. versionadded:: 20.2.0
    """
    pass

class AsyncBoundLogger:
    """
    Wraps a `BoundLogger` & exposes its logging methods as ``async`` versions.

    Instead of blocking the program, they are run asynchronously in a thread
    pool executor.

    This means more computational overhead per log call. But it also means that
    the processor chain (e.g. JSON serialization) and I/O won't block your
    whole application.

    Only available for Python 3.7 and later.

    .. versionadded:: 20.2.0
    .. versionchanged:: 20.2.0 fix _dispatch_to_sync contextvars usage
    .. deprecated:: 23.1.0
       Use the regular `BoundLogger` with its a-prefixed methods instead.
    .. versionchanged:: 23.3.0
        Callsite parameters are now also collected for async log methods.
    """
    __slots__ = ('_loop', 'sync_bl')
    sync_bl: BoundLogger
    _executor = None
    _bound_logger_factory = BoundLogger

    def __init__(self, logger: logging.Logger, processors: Iterable[Processor], context: Context, *, _sync_bl: Any=None, _loop: Any=None):
        if _sync_bl:
            self.sync_bl = _sync_bl
            self._loop = _loop
            return
        self.sync_bl = self._bound_logger_factory(logger=logger, processors=processors, context=context)
        self._loop = asyncio.get_running_loop()

    @property
    def _context(self) -> Context:
        pass

    def bind(self, **new_values: Any) -> Self:
        pass

    def new(self, **new_values: Any) -> Self:
        pass

    def unbind(self, *keys: str) -> Self:
        pass

    def try_unbind(self, *keys: str) -> Self:
        pass

    async def _dispatch_to_sync(self, meth: Callable[..., Any], event: str, args: tuple[Any, ...], kw: dict[str, Any]) -> None:
        """
        Merge contextvars and log using the sync logger in a thread pool.
        """
        pass

    async def debug(self, event: str, *args: Any, **kw: Any) -> None:
        pass

    async def info(self, event: str, *args: Any, **kw: Any) -> None:
        pass

    async def warning(self, event: str, *args: Any, **kw: Any) -> None:
        pass

    async def warn(self, event: str, *args: Any, **kw: Any) -> None:
        pass

    async def error(self, event: str, *args: Any, **kw: Any) -> None:
        pass

    async def critical(self, event: str, *args: Any, **kw: Any) -> None:
        pass

    async def fatal(self, event: str, *args: Any, **kw: Any) -> None:
        pass

    async def exception(self, event: str, *args: Any, **kw: Any) -> None:
        pass

    async def log(self, level: Any, event: str, *args: Any, **kw: Any) -> None:
        pass

class LoggerFactory:
    """
    Build a standard library logger when an *instance* is called.

    Sets a custom logger using :func:`logging.setLoggerClass` so variables in
    log format are expanded properly.

    >>> from structlog import configure
    >>> from structlog.stdlib import LoggerFactory
    >>> configure(logger_factory=LoggerFactory())

    Args:
        ignore_frame_names:
            When guessing the name of a logger, skip frames whose names *start*
            with one of these.  For example, in pyramid applications you'll
            want to set it to ``["venusian", "pyramid.config"]``. This argument
            is called *additional_ignores* in other APIs throughout
            *structlog*.
    """

    def __init__(self, ignore_frame_names: list[str] | None=None):
        self._ignore = ignore_frame_names
        logging.setLoggerClass(_FixedFindCallerLogger)

    def __call__(self, *args: Any) -> logging.Logger:
        """
        Deduce the caller's module name and create a stdlib logger.

        If an optional argument is passed, it will be used as the logger name
        instead of guesswork.  This optional argument would be passed from the
        :func:`structlog.get_logger` call.  For example
        ``structlog.get_logger("foo")`` would cause this method to be called
        with ``"foo"`` as its first positional argument.

        .. versionchanged:: 0.4.0
            Added support for optional positional arguments.  Using the first
            one for naming the constructed logger.
        """
        if args:
            return logging.getLogger(args[0])
        _, name = _find_first_app_frame_and_name(self._ignore)
        return logging.getLogger(name)

class PositionalArgumentsFormatter:
    """
    Apply stdlib-like string formatting to the ``event`` key.

    If the ``positional_args`` key in the event dict is set, it must
    contain a tuple that is used for formatting (using the ``%s`` string
    formatting operator) of the value from the ``event`` key.  This works
    in the same way as the stdlib handles arguments to the various log
    methods: if the tuple contains only a single `dict` argument it is
    used for keyword placeholders in the ``event`` string, otherwise it
    will be used for positional placeholders.

    ``positional_args`` is populated by `structlog.stdlib.BoundLogger` or
    can be set manually.

    The *remove_positional_args* flag can be set to `False` to keep the
    ``positional_args`` key in the event dict; by default it will be
    removed from the event dict after formatting a message.
    """

    def __init__(self, remove_positional_args: bool=True) -> None:
        self.remove_positional_args = remove_positional_args

    def __call__(self, _: WrappedLogger, __: str, event_dict: EventDict) -> EventDict:
        args = event_dict.get('positional_args')
        if args:
            if len(args) == 1 and isinstance(args[0], dict) and args[0]:
                args = args[0]
            event_dict['event'] %= args
        if self.remove_positional_args and args is not None:
            del event_dict['positional_args']
        return event_dict

def filter_by_level(logger: logging.Logger, method_name: str, event_dict: EventDict) -> EventDict:
    """
    Check whether logging is configured to accept messages from this log level.

    Should be the first processor if stdlib's filtering by level is used so
    possibly expensive processors like exception formatters are avoided in the
    first place.

    >>> import logging
    >>> from structlog.stdlib import filter_by_level
    >>> logging.basicConfig(level=logging.WARN)
    >>> logger = logging.getLogger()
    >>> filter_by_level(logger, 'warn', {})
    {}
    >>> filter_by_level(logger, 'debug', {})
    Traceback (most recent call last):
    ...
    DropEvent
    """
    pass

def add_log_level_number(logger: logging.Logger, method_name: str, event_dict: EventDict) -> EventDict:
    """
    Add the log level number to the event dict.

    Log level numbers map to the log level names. The Python stdlib uses them
    for filtering logic. This adds the same numbers so users can leverage
    similar filtering. Compare::

       level in ("warning", "error", "critical")
       level_number >= 30

    The mapping of names to numbers is in
    ``structlog.stdlib._log_levels._NAME_TO_LEVEL``.

    .. versionadded:: 18.2.0
    """
    pass

def add_logger_name(logger: logging.Logger, method_name: str, event_dict: EventDict) -> EventDict:
    """
    Add the logger name to the event dict.
    """
    pass
_LOG_RECORD_KEYS = logging.LogRecord('name', 0, 'pathname', 0, 'msg', (), None).__dict__.keys()

class ExtraAdder:
    """
    Add extra attributes of `logging.LogRecord` objects to the event
    dictionary.

    This processor can be used for adding data passed in the ``extra``
    parameter of the `logging` module's log methods to the event dictionary.

    Args:
        allow:
            An optional collection of attributes that, if present in
            `logging.LogRecord` objects, will be copied to event dictionaries.

            If ``allow`` is None all attributes of `logging.LogRecord` objects
            that do not exist on a standard `logging.LogRecord` object will be
            copied to event dictionaries.

    .. versionadded:: 21.5.0
    """
    __slots__ = ('_copier',)

    def __init__(self, allow: Collection[str] | None=None) -> None:
        self._copier: Callable[[EventDict, logging.LogRecord], None]
        if allow is not None:
            self._copier = functools.partial(self._copy_allowed, [*allow])
        else:
            self._copier = self._copy_all

    def __call__(self, logger: logging.Logger, name: str, event_dict: EventDict) -> EventDict:
        record: logging.LogRecord | None = event_dict.get('_record')
        if record is not None:
            self._copier(event_dict, record)
        return event_dict

    @classmethod
    def _copy_all(cls, event_dict: EventDict, record: logging.LogRecord) -> None:
        pass

    @classmethod
    def _copy_allowed(cls, allow: Collection[str], event_dict: EventDict, record: logging.LogRecord) -> None:
        pass
LOG_KWARG_NAMES = ('exc_info', 'stack_info', 'stacklevel')

def render_to_log_args_and_kwargs(_: logging.Logger, __: str, event_dict: EventDict) -> tuple[tuple[Any, ...], dict[str, Any]]:
    """
    Render ``event_dict`` into positional and keyword arguments for
    `logging.Logger` logging methods.
    See `logging.Logger.debug` method for keyword arguments reference.

    The ``event`` field is passed in the first positional argument, positional
    arguments from ``positional_args`` field are passed in subsequent positional
    arguments, keyword arguments are extracted from the *event_dict* and the
    rest of the *event_dict* is added as ``extra``.

    This allows you to defer formatting to `logging`.

    .. versionadded:: 25.1.0
    """
    pass

def render_to_log_kwargs(_: logging.Logger, __: str, event_dict: EventDict) -> EventDict:
    """
    Render ``event_dict`` into keyword arguments for `logging.Logger` logging
    methods.
    See `logging.Logger.debug` method for keyword arguments reference.

    The ``event`` field is translated into ``msg``, keyword arguments are
    extracted from the *event_dict* and the rest of the *event_dict* is added as
    ``extra``.

    This allows you to defer formatting to `logging`.

    .. versionadded:: 17.1.0
    .. versionchanged:: 22.1.0
       ``exc_info``, ``stack_info``, and ``stacklevel`` are passed as proper
       kwargs and not put into ``extra``.
    .. versionchanged:: 24.2.0
       ``stackLevel`` corrected to ``stacklevel``.
    """
    pass

class ProcessorFormatter(logging.Formatter):
    """
    Call *structlog* processors on `logging.LogRecord`\\s.

    This is an implementation of a `logging.Formatter` that can be used to
    format log entries from both *structlog* and `logging`.

    Its static method `wrap_for_formatter` must be the final processor in
    *structlog*'s processor chain.

    Please refer to :ref:`processor-formatter` for examples.

    Args:
        foreign_pre_chain:
            If not `None`, it is used as a processor chain that is applied to
            **non**-*structlog* log entries before the event dictionary is
            passed to *processors*. (default: `None`)

        processors:
            A chain of *structlog* processors that is used to process **all**
            log entries. The last one must render to a `str` which then gets
            passed on to `logging` for output.

            Compared to *structlog*'s regular processor chains, there's a few
            differences:

            - The event dictionary contains two additional keys:

              #. ``_record``: a `logging.LogRecord` that either was created
                  using `logging` APIs, **or** is a wrapped *structlog* log
                  entry created by `wrap_for_formatter`.

              #. ``_from_structlog``: a `bool` that indicates whether or not
                 ``_record`` was created by a *structlog* logger.

              Since you most likely don't want ``_record`` and
              ``_from_structlog`` in your log files,  we've added the static
              method `remove_processors_meta` to ``ProcessorFormatter`` that
              you can add just before your renderer.

            - Since this is a `logging` *formatter*, raising
              `structlog.DropEvent` will crash your application.

        keep_exc_info:
            ``exc_info`` on `logging.LogRecord`\\ s is added to the
            ``event_dict`` and removed afterwards. Set this to ``True`` to keep
            it on the `logging.LogRecord`. (default: False)

        keep_stack_info:
            Same as *keep_exc_info* except for ``stack_info``. (default: False)

        logger:
            Logger which we want to push through the *structlog* processor
            chain. This parameter is necessary for some of the processors like
            `filter_by_level`. (default: None)

        pass_foreign_args:
            If True, pass a foreign log record's ``args`` attribute to the
            ``event_dict`` under ``positional_args`` key. (default: False)

        processor:
            A single *structlog* processor used for rendering the event
            dictionary before passing it off to `logging`. Must return a `str`.
            The event dictionary does **not** contain ``_record`` and
            ``_from_structlog``.

            This parameter exists for historic reasons. Please use *processors*
            instead.

        use_get_message:
            If True, use ``record.getMessage`` to get a fully rendered log
            message, otherwise use ``str(record.msg)``. (default: True)

    Raises:
        TypeError: If both or neither *processor* and *processors* are passed.

    .. versionadded:: 17.1.0
    .. versionadded:: 17.2.0 *keep_exc_info* and *keep_stack_info*
    .. versionadded:: 19.2.0 *logger*
    .. versionadded:: 19.2.0 *pass_foreign_args*
    .. versionadded:: 21.3.0 *processors*
    .. deprecated:: 21.3.0
       *processor* (singular) in favor of *processors* (plural). Removal is not
       planned.
    .. versionadded:: 23.3.0 *use_get_message*
    """

    def __init__(self, processor: Processor | None=None, processors: Sequence[Processor] | None=(), foreign_pre_chain: Sequence[Processor] | None=None, keep_exc_info: bool=False, keep_stack_info: bool=False, logger: logging.Logger | None=None, pass_foreign_args: bool=False, use_get_message: bool=True, *args: Any, **kwargs: Any) -> None:
        fmt = kwargs.pop('fmt', '%(message)s')
        super().__init__(*args, fmt=fmt, **kwargs)
        if processor and processors:
            msg = 'The `processor` and `processors` arguments are mutually exclusive.'
            raise TypeError(msg)
        self.processors: Sequence[Processor]
        if processor is not None:
            self.processors = (self.remove_processors_meta, processor)
        elif processors:
            self.processors = processors
        else:
            msg = 'Either `processor` or `processors` must be passed.'
            raise TypeError(msg)
        self.foreign_pre_chain = foreign_pre_chain
        self.keep_exc_info = keep_exc_info
        self.keep_stack_info = keep_stack_info
        self.logger = logger
        self.pass_foreign_args = pass_foreign_args
        self.use_get_message = use_get_message

    def format(self, record: logging.LogRecord) -> str:
        """
        Extract *structlog*'s `event_dict` from ``record.msg`` and format it.

        *record* has been patched by `wrap_for_formatter` first though, so the
         type isn't quite right.
        """
        pass

    @staticmethod
    def wrap_for_formatter(logger: logging.Logger, name: str, event_dict: EventDict) -> tuple[tuple[EventDict], dict[str, dict[str, Any]]]:
        """
        Wrap *logger*, *name*, and *event_dict*.

        The result is later unpacked by `ProcessorFormatter` when formatting
        log entries.

        Use this static method as the renderer (in other words, final
        processor) if you want to use `ProcessorFormatter` in your `logging`
        configuration.
        """
        pass

    @staticmethod
    def remove_processors_meta(_: WrappedLogger, __: str, event_dict: EventDict) -> EventDict:
        """
        Remove ``_record`` and ``_from_structlog`` from *event_dict*.

        These keys are added to the event dictionary, before
        `ProcessorFormatter`'s *processors* are run.

        .. versionadded:: 21.3.0
        """
        pass