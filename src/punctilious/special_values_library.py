from __future__ import annotations

import enum


class SpecialValues(enum.Enum):
    """A special value returned when a property or method is not available.

    """
    NOT_AVAILABLE = "not available"


na = SpecialValues.NOT_AVAILABLE
