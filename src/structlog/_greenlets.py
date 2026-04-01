"""
greenlet-specific code that pretends to be a `threading.local`.

Fails to import if not running under greenlet.
"""
from __future__ import annotations
from typing import Any
from weakref import WeakKeyDictionary
from greenlet import getcurrent

class GreenThreadLocal:
    """
    threading.local() replacement for greenlets.
    """

    def __init__(self) -> None:
        self.__dict__['_weakdict'] = WeakKeyDictionary()

    def __getattr__(self, name: str) -> Any:
        key = getcurrent()
        try:
            return self._weakdict[key][name]
        except KeyError:
            raise AttributeError(name) from None

    def __setattr__(self, name: str, val: Any) -> None:
        key = getcurrent()
        self._weakdict.setdefault(key, {})[name] = val

    def __delattr__(self, name: str) -> None:
        key = getcurrent()
        try:
            del self._weakdict[key][name]
        except KeyError:
            raise AttributeError(name) from None