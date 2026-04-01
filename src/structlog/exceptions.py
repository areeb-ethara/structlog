"""
Exceptions factored out to avoid import loops.
"""
from __future__ import annotations

class DropEvent(BaseException):
    """
    If raised by an processor, the event gets silently dropped.

    Derives from BaseException because it's technically not an error.
    """

class NoConsoleRendererConfiguredError(Exception):
    """
    A user asked for the current `structlog.dev.ConsoleRenderer` but none is
    configured.

    .. versionadded:: 25.5.0
    """

class MultipleConsoleRenderersConfiguredError(Exception):
    """
    A user asked for the current `structlog.dev.ConsoleRenderer` and more than one is configured.

    .. versionadded:: 25.5.0
    """