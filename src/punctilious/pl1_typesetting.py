import log
import typesetting as ts
import fl1_typesetting as fl1_ts


# TODO: See Lawler, John. “Notation, Logical (See: Notation, Mathematical),” n.d. https://websites.umich.edu/~jlawler/IELL-LogicalNotation.pdf.
#   For a good synthesis on notation conventions for propositional logic.


class Flavors:
    _singleton = None

    def __new__(cls):
        if cls._singleton is None:
            cls._singleton = super(Flavors, cls).__new__(cls)
        return cls._singleton

    def __init__(self):
        super().__init__()
        self._negation_tilde = ts.flavors.register(name="pl1.connective.negation.tilde", predecessor=ts.flavors.default)
        self._negation_not = ts.flavors.register(name="pl1.connective.negation.not",
            predecessor=self._negation_tilde)  # define default preference.

    @property
    def negation_not(self) -> ts.Flavor:
        return self._negation_not

    @property
    def negation_tilde(self) -> ts.Flavor:
        return self._negation_tilde


flavors = Flavors()


class Tags:
    _singleton = None

    def __new__(cls):
        if cls._singleton is None:
            cls._singleton = super(Tags, cls).__new__(cls)
        return cls._singleton

    def __init__(self):
        super().__init__()
        self._conditional = ts.tags.register(name="pl1.connective.conditional", predecessor=fl1_ts.tags.connective)
        self._negation = ts.tags.register(name="pl1.connective.negation", predecessor=fl1_ts.tags.connective)

    @property
    def conditional(self) -> ts.Tag:
        return self._conditional

    @property
    def negation(self) -> ts.Tag:
        return self._negation


tags = Tags()

log.debug(f"Module {__name__}: loaded.")
