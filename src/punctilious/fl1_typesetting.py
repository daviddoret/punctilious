import log
import typesetting as ts


# Treatments

class Treatments:
    _singleton = None

    def __new__(cls):
        if cls._singleton is None:
            cls._singleton = super(Treatments, cls).__new__(cls)
        return cls._singleton

    def __init__(self):
        super().__init__()
        self._symbolic_representation = ts.Treatment(name="symbolic-representation")
        self._common_language = ts.Treatment(name="common-language")

    @property
    def common_language(self) -> ts.Treatment:
        return self._common_language

    @property
    def symbolic_representation(self) -> ts.Treatment:
        return self._symbolic_representation


treatments = Treatments()


# TAGS

class Tags:
    _singleton = None

    def __new__(cls):
        if cls._singleton is None:
            cls._singleton = super(Tags, cls).__new__(cls)
        return cls._singleton

    def __init__(self):
        super().__init__()
        self._connective = ts.tags.register(name="fl1.connective")

    @property
    def connective(self) -> ts.Tag:
        return self._connective


tags = Tags()

log.debug(f"Module {__name__}: loaded.")
