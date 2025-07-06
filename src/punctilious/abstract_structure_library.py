from __future__ import annotations

# Native python modules
import abc
import typing
import inspect

# Punctilious modules
import abstract_formula_library as afl

import types

import types
import inspect


def enrich_object_with_type(o, t):
    if not isinstance(o, object) or not isinstance(t, type):
        raise TypeError("o must be an object and t must be a type")

    current_cls = o.__class__

    # Step 1: Add `t` to the MRO (only if not already in it)
    if not issubclass(current_cls, t):
        NewClass = type(
            f"Enriched{current_cls.__name__}With{t.__name__}",
            (t, current_cls), {}
        )
        o.__class__ = NewClass

    return o


class AbstractMap(abc.ABC):
    """An abstract-formula of the form i(j(...),k(...)).

    """
