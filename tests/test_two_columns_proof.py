from unittest import TestCase
import punctilious as pu
import random_data


class TestTwoColumnsProof(TestCase):
    def test_rep_two_columns_proof_item(self):
        left = random_data.random_sentence(min_words=50)
        right = random_data.random_sentence(min_words=20)
        report = pu.rep_two_columns_proof_item(left, right)
        print(report)
