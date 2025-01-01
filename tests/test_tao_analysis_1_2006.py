import pytest
import punctilious as pu


class TestTaoAnalysis12006:
    def test_tao_analysis_1_2006(self):
        """Test of representation with multiple string-constant renderers.
        """
        zero = pu.tao_analysis_1_2006.zero
        zero_constant = pu.formal_language.Formula(zero)
        zero_constant.represent()
        pass
