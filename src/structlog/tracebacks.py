"""
Extract a structured traceback from an exception.

Based on work by Will McGugan
<https://github.com/hynek/structlog/pull/407#issuecomment-1150926246>`_ from
`rich.traceback
<https://github.com/Textualize/rich/blob/972dedff/rich/traceback.py>`_.
"""
from __future__ import annotations
import os
import os.path
import sys
from collections.abc import Iterable, Sequence
from dataclasses import asdict, dataclass, field
from traceback import walk_tb
from types import ModuleType, TracebackType
from typing import Any, Union
try:
    import rich
    import rich.pretty
except ImportError:
    rich = None
from .typing import ExcInfo
__all__ = ['ExceptionDictTransformer', 'Frame', 'Stack', 'SyntaxError_', 'Trace', 'extract', 'safe_str', 'to_repr']
SHOW_LOCALS = True
LOCALS_MAX_LENGTH = 10
LOCALS_MAX_STRING = 80
MAX_FRAMES = 50
OptExcInfo = Union[ExcInfo, tuple[None, None, None]]

@dataclass
class Frame:
    """
    Represents a single stack frame.
    """
    filename: str
    lineno: int
    name: str
    locals: dict[str, str] | None = None

@dataclass
class SyntaxError_:
    """
    Contains detailed information about :exc:`SyntaxError` exceptions.
    """
    offset: int
    filename: str
    line: str
    lineno: int
    msg: str

@dataclass
class Stack:
    """
    Represents an exception and a list of stack frames.

    .. versionchanged:: 25.2.0
       Added the *exc_notes* field.

    .. versionchanged:: 25.4.0
       Added the *is_group* and *exceptions* fields.
    """
    exc_type: str
    exc_value: str
    exc_notes: list[str] = field(default_factory=list)
    syntax_error: SyntaxError_ | None = None
    is_cause: bool = False
    frames: list[Frame] = field(default_factory=list)
    is_group: bool = False
    exceptions: list[Trace] = field(default_factory=list)

@dataclass
class Trace:
    """
    Container for a list of stack traces.
    """
    stacks: list[Stack]

def safe_str(_object: Any) -> str:
    """Don't allow exceptions from __str__ to propagate."""
    pass

def to_repr(obj: Any, max_length: int | None=None, max_string: int | None=None, use_rich: bool=True) -> str:
    """
    Get repr string for an object, but catch errors.

    :func:`repr()` is used for strings, too, so that secret wrappers that
    inherit from :func:`str` and overwrite ``__repr__()`` are handled correctly
    (i.e. secrets are not logged in plain text).

    Args:
        obj: Object to get a string representation for.

        max_length: Maximum length of containers before abbreviating, or
            ``None`` for no abbreviation.

        max_string: Maximum length of string before truncating, or ``None`` to
            disable truncating.

        use_rich: If ``True`` (the default), use rich_ to compute the repr.
            If ``False`` or if rich_ is not installed, fall back to a simpler
            algorithm.

    Returns:
        The string representation of *obj*.

    .. versionchanged:: 24.3.0
       Added *max_length* argument.  Use :program:`rich` to render locals if it
       is available.  Call :func:`repr()` on strings in fallback
       implementation.
    """
    pass

def extract(exc_type: type[BaseException], exc_value: BaseException, traceback: TracebackType | None, *, show_locals: bool=False, locals_max_length: int=LOCALS_MAX_LENGTH, locals_max_string: int=LOCALS_MAX_STRING, locals_hide_dunder: bool=True, locals_hide_sunder: bool=False, use_rich: bool=True, _seen: set[int] | None=None) -> Trace:
    """
    Extract traceback information.

    Args:
        exc_type: Exception type.

        exc_value: Exception value.

        traceback: Python Traceback object.

        show_locals: Enable display of local variables. Defaults to False.

        locals_max_length:
            Maximum length of containers before abbreviating, or ``None`` for
            no abbreviation.

        locals_max_string:
            Maximum length of string before truncating, or ``None`` to disable
            truncating.

        locals_hide_dunder:
            Hide locals prefixed with double underscore.
            Defaults to True.

        locals_hide_sunder:
            Hide locals prefixed with single underscore.
            This implies hiding *locals_hide_dunder*.
            Defaults to False.

        use_rich: If ``True`` (the default), use rich_ to compute the repr.
            If ``False`` or if rich_ is not installed, fall back to a simpler
            algorithm.

    Returns:
        A Trace instance with structured information about all exceptions.

    .. versionadded:: 22.1.0

    .. versionchanged:: 24.3.0
       Added *locals_max_length*, *locals_hide_sunder*, *locals_hide_dunder*
       and *use_rich* arguments.

    .. versionchanged:: 25.4.0
       Handle exception groups.

    .. versionchanged:: 25.5.0
       Handle loops in exception cause chain.
    """
    pass

class ExceptionDictTransformer:
    """
    Return a list of exception stack dictionaries for an exception.

    These dictionaries are based on :class:`Stack` instances generated by
    :func:`extract()` and can be dumped to JSON.

    Args:
        show_locals:
            Whether or not to include the values of a stack frame's local
            variables.

        locals_max_length:
            Maximum length of containers before abbreviating, or ``None`` for
            no abbreviation.

        locals_max_string:
            Maximum length of string before truncating, or ``None`` to disable
            truncating.

        locals_hide_dunder:
            Hide locals prefixed with double underscore.
            Defaults to True.

        locals_hide_sunder:
            Hide locals prefixed with single underscore.
            This implies hiding *locals_hide_dunder*.
            Defaults to False.

        suppress:
            Optional sequence of modules or paths for which to suppress the
            display of locals even if *show_locals* is ``True``.

        max_frames:
            Maximum number of frames in each stack.  Frames are removed from
            the inside out.  The idea is, that the first frames represent your
            code responsible for the exception and last frames the code where
            the exception actually happened.  With larger web frameworks, this
            does not always work, so you should stick with the default.

        use_rich: If ``True`` (the default), use rich_ to compute the repr of
            locals.  If ``False`` or if rich_ is not installed, fall back to
            a simpler algorithm.

    .. seealso::
        :doc:`exceptions` for a broader explanation of *structlog*'s exception
        features.

    .. versionchanged:: 24.3.0
       Added *locals_max_length*, *locals_hide_sunder*, *locals_hide_dunder*,
       *suppress* and *use_rich* arguments.

    .. versionchanged:: 25.1.0
       *locals_max_length* and *locals_max_string* may be None to disable
       truncation.

    .. versionchanged:: 25.4.0
       Handle exception groups.
    """

    def __init__(self, *, show_locals: bool=SHOW_LOCALS, locals_max_length: int=LOCALS_MAX_LENGTH, locals_max_string: int=LOCALS_MAX_STRING, locals_hide_dunder: bool=True, locals_hide_sunder: bool=False, suppress: Iterable[str | ModuleType]=(), max_frames: int=MAX_FRAMES, use_rich: bool=True) -> None:
        if locals_max_length is not None and locals_max_length < 0:
            msg = f'"locals_max_length" must be >= 0: {locals_max_length}'
            raise ValueError(msg)
        if locals_max_string is not None and locals_max_string < 0:
            msg = f'"locals_max_string" must be >= 0: {locals_max_string}'
            raise ValueError(msg)
        if max_frames < 2:
            msg = f'"max_frames" must be >= 2: {max_frames}'
            raise ValueError(msg)
        self.show_locals = show_locals
        self.locals_max_length = locals_max_length
        self.locals_max_string = locals_max_string
        self.locals_hide_dunder = locals_hide_dunder
        self.locals_hide_sunder = locals_hide_sunder
        self.suppress: Sequence[str] = []
        for suppress_entity in suppress:
            if not isinstance(suppress_entity, str):
                if suppress_entity.__file__ is None:
                    msg = f""""suppress" item {suppress_entity!r} must be a module with '__file__' attribute"""
                    raise ValueError(msg)
                path = os.path.dirname(suppress_entity.__file__)
            else:
                path = suppress_entity
            path = os.path.normpath(os.path.abspath(path))
            self.suppress.append(path)
        self.max_frames = max_frames
        self.use_rich = use_rich

    def __call__(self, exc_info: ExcInfo) -> list[dict[str, Any]]:
        trace = extract(*exc_info, show_locals=self.show_locals, locals_max_length=self.locals_max_length, locals_max_string=self.locals_max_string, locals_hide_dunder=self.locals_hide_dunder, locals_hide_sunder=self.locals_hide_sunder, use_rich=self.use_rich)
        for stack in trace.stacks:
            if len(stack.frames) <= self.max_frames:
                continue
            half = self.max_frames // 2
            fake_frame = Frame(filename='', lineno=-1, name=f'Skipped frames: {len(stack.frames) - 2 * half}')
            stack.frames[:] = [*stack.frames[:half], fake_frame, *stack.frames[-half:]]
        return self._as_dict(trace)

    def _as_dict(self, trace: Trace) -> list[dict[str, Any]]:
        pass