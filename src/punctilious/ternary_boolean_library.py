from __future__ import annotations

import enum

import punctilious.util as util
import punctilious.special_values_library as spl


class TernaryBoolean(enum.Enum):
    """A ternary Boolean where the 3rd value means "not available".

    """
    TRUE = True
    FALSE = False
    NOT_AVAILABLE = spl.SpecialValues.NOT_AVAILABLE

    def __and__(self, x):
        return self.land(x)

    def __or__(self, x):
        return self.lor(x)

    def __not__(self):
        return self.lnot()

    def __bool__(self):
        if self is TernaryBoolean.NOT_AVAILABLE:
            raise util.PunctiliousException("Cannot convert NOT_AVAILABLE to bool.")
        return self.value

    def land(self, x: TernaryBoolean) -> TernaryBoolean:
        if self is TernaryBoolean.FALSE or x is TernaryBoolean.FALSE:
            # if one operand is false, the conjunction is necessarily false.
            return TernaryBoolean.FALSE
        elif self is TernaryBoolean.NOT_AVAILABLE or x is TernaryBoolean.NOT_AVAILABLE:
            return TernaryBoolean.NOT_AVAILABLE
        else:
            return TernaryBoolean(self.value and x.value)

    def lor(self, x: TernaryBoolean) -> TernaryBoolean:
        if self is TernaryBoolean.TRUE or x is TernaryBoolean.TRUE:
            # if one operand is true, the disjunction is necessarily true.
            return TernaryBoolean.TRUE
        elif self is TernaryBoolean.NOT_AVAILABLE or x is TernaryBoolean.NOT_AVAILABLE:
            return TernaryBoolean.NOT_AVAILABLE
        else:
            return TernaryBoolean(self.value or x.value)

    def lnot(self) -> TernaryBoolean:
        if self is TernaryBoolean.NOT_AVAILABLE:
            return TernaryBoolean.NOT_AVAILABLE
        return TernaryBoolean(not self.value)


f = TernaryBoolean.FALSE
t = TernaryBoolean.TRUE
na = TernaryBoolean.NOT_AVAILABLE
