from unittest import TestCase
import repm
import random_data


class TestMultiFormatString(TestCase):
    def test_multi_format_string(self):
        raw = '𝛽a⋁b₁1'
        mms = repm.StyledText(raw, raw)
        self.assertEqual(raw, dashed_name.repr())
        self.assertEqual(raw, dashed_name.repr_dashed_name())
