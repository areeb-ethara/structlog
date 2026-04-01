"""
Deprecated name for :mod:`structlog.typing`.

.. versionadded:: 20.2.0
.. deprecated:: 22.2.0
"""
from __future__ import annotations
from .typing import BindableLogger, Context, EventDict, ExceptionRenderer, ExceptionTransformer, ExcInfo, FilteringBoundLogger, Processor, WrappedLogger
__all__ = ('BindableLogger', 'Context', 'EventDict', 'ExcInfo', 'ExceptionRenderer', 'ExceptionTransformer', 'FilteringBoundLogger', 'Processor', 'WrappedLogger')