_reserved_words = (
    'axiom',
    'corollary',
    'lemma',
    'proposition',
    'proof',
    'punctilious',
    'relation',
    'statement',
    'theorem',
    'theory',
    'universe-of-discourse')


def is_reserved(w):
    return w in _reserved_words
