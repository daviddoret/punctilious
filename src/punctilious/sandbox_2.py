import collections
import collections.abc


class Renderer:
    def __init__(self, tags):
        self._tags = tags


class Tag(tuple):

    def __init__(self, label: str, value: str):
        super().__init__()

    def __new__(cls, label: str, value: str):
        return super().__new__(cls, [label, value])

    @property
    def label(self):
        return self[0]

    @property
    def value(self):
        return self[1]


class TagsAssignment(tuple):
    """A canonically sorted tuple of tags whose labels are unique."""

    def __init__(self, *tags: tuple[Tag, ...]):
        super().__init__()

    def __new__(cls, *tags: tuple[Tag, ...]):
        # validate that every label is unique
        labels = tuple(sub[0] for sub in tags)
        unique_labels = tuple(set(labels))
        if not len(labels) == len(unique_labels):
            raise ValueError('some labels are not unique')
        # sort the tuple
        tags_sorted = tuple(sorted(tags, key=lambda tag: tag.label))
        return super().__new__(cls, tags_sorted)

    def labels(self) -> collections.abc.Iterable:
        return (tag.label for tag in self)

    def values(self) -> collections.abc.Iterable:
        return (tag.value for tag in self)


class TagsPreferences(dict):
    def __init__(self):
        super().__init__()

    def __setitem__(self, key, value):
        self._validate_key_value(key, value)
        super().__setitem__(key, value)

    def update(self, *args, **kwargs):
        for key, value in dict(*args, **kwargs).items():
            self._validate_key_value(key, value)
        super().update(*args, **kwargs)

    def _validate_key_value(self, key, value):
        if not isinstance(key, Tag):
            raise TypeError(f"Key must be of type Tag, got {type(key).__name__} instead.")
        if not isinstance(value, int):
            raise TypeError(f"Value must be of type int, got {type(value).__name__} instead.")

    def score_tags_assignment(self, tags: TagsAssignment):
        return sum(self.get(tag, 0) for tag in tags)


en = Tag('language', 'en')
fr = Tag('language', 'fr')
symbol = Tag('connector_representation', 'symbol')
word = Tag('connector_representation', 'word')
print(en)

a1 = TagsAssignment(en, symbol)
print(a1)

prefs = TagsPreferences()
prefs[en] = 6
prefs[fr] = 9

print(prefs.score_tags_assignment(a1))
