import random
import numpy as np

_consonants = (
    'b', 'b', 'b', 'b', 'b', 'bl', 'br', 'd', 'd', 'd', 'd', 'd', 'dr', 'f', 'fl', 'fr', 'g', 'gn',
    'h', 'j', 'k', 'l',
    'm',
    'n', 'p', 'ph', 'r', 's', 'st', 't', 'v', 'z')
_vowels = (
    'a', 'a', 'a', 'a', 'a', 'ae', 'e', 'e', 'e', 'e', 'e', 'ee', 'i', 'i', 'i', 'i', 'i', 'ia',
    'ie', 'io', 'o', 'o',
    'o',
    'o', 'o', 'oa', 'oe', 'oi', 'oo', 'ou', 'u', 'u', 'u', 'u', 'u', 'y', 'ya', 'ye', 'yo', 'yu')

pangram1 = 'the quick brown fox jumps over the lazy dog. 0123456789!'


def random_word(min_syllable=2, n=3, p=.2):
    global _consonants
    global _vowels
    num_syllables = np.random.binomial(n=n, p=p) + min_syllable
    return ''.join(
        (_consonants[random.randint(0, len(_consonants) - 1)] + _vowels[
            random.randint(0, len(_vowels) - 1)] for i in
         range(random.randint(min_syllable, num_syllables))))


def random_sentence(min_words=3, n=12, p=.2):
    num_words = np.random.binomial(n=n, p=p) + min_words
    sentence = ' '.join(
        (random_word() for i in range(random.randint(min_words, num_words))))
    return f'{sentence}.'


def random_dashed_name(min_words=1, n=3, p=.2):
    num_words = np.random.binomial(n=n, p=p) + min_words
    return '-'.join(
        (random_word() for i in range(random.randint(min_words, num_words))))
