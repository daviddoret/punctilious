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
        self._classical_1 = ts.Flavor(name="Classical 1")
        self._classical_2 = ts.Flavor(name="Classical 2")
        self._classical_3 = ts.Flavor(name="Classical 3")
        self._classical_4 = ts.Flavor(name="Classical 4")
        self._polish_1 = ts.Flavor(name="Polish 1")
        self._reverse_polish_1 = ts.Flavor(name="Reverse Polish 1")

    @property
    def classical_1(self) -> ts.Flavor:
        return self._classical_1

    @property
    def classical_2(self) -> ts.Flavor:
        return self._classical_2

    @property
    def classical_3(self) -> ts.Flavor:
        return self._classical_3

    @property
    def classical_4(self) -> ts.Flavor:
        return self._classical_4

    @property
    def polish_1(self) -> ts.Flavor:
        return self._polish_1

    @property
    def reverse_polish_1(self) -> ts.Flavor:
        return self._reverse_polish_1


flavors = Flavors()


class Tags:
    _singleton = None

    def __new__(cls):
        if cls._singleton is None:
            cls._singleton = super(Tags, cls).__new__(cls)
        return cls._singleton

    def __init__(self):
        super().__init__()
        self._conditional = ts.Tag(name="pl1.connective.conditional", specialized_tag=fl1_ts.tags.connective)
        self._negation = ts.Tag(name="pl1.connective.negation", specialized_tag=fl1_ts.tags.connective)

    @property
    def conditional(self) -> ts.Tag:
        return self._conditional

    @property
    def negation(self) -> ts.Tag:
        return self._negation


tags = Tags()

log.debug(f"Module {__name__}: loaded.")
