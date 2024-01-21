import log
import typesetting as ts


# Treatments

class Treatments(ts.Treatments):
    _singleton = None

    def __new__(cls):
        if cls._singleton is None:
            cls._singleton = super(Treatments, cls).__new__(cls)
        return cls._singleton

    def __init__(self):
        super().__init__()
        self._symbolic_representation = ts.Treatment(name="Symbolic Representation")
        self._common_language = ts.Treatment(name="Common Language")

    @property
    def common_language(self) -> ts.Treatment:
        return self._common_language

    @property
    def symbolic_representation(self) -> ts.Treatment:
        return self._symbolic_representation


treatments = Treatments()


# TAGS
def load():
    ts.tags.set(key="fl1.connective")


load()

log.debug(f"Module {__name__}: loaded.")
