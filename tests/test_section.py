from unittest import TestCase
import punctilious as p
import random_data


class TestSection(TestCase):
    def test_section(self):
        echo_note = p.configuration.echo_note
        p.configuration.echo_note = True
        u = p.UniverseOfDiscourse('white-sheet-of-paper')
        t = u.t('testing-theory')
        s_1 = t.open_section('something interesting', echo=True)
        self.assertEqual('# 𝟏 𝐒𝐨𝐦𝐞𝐭𝐡𝐢𝐧𝐠 𝐢𝐧𝐭𝐞𝐫𝐞𝐬𝐭𝐢𝐧𝐠', s_1.repr_report())
        s_2 = t.open_section('something else', echo=True)
        self.assertEqual('# 𝟐 𝐒𝐨𝐦𝐞𝐭𝐡𝐢𝐧𝐠 𝐞𝐥𝐬𝐞', s_2.repr_report())
        s_2_1 = t.open_section('some details on this topic', section_parent=s_2, echo=True)
        self.assertEqual('## 𝟐.𝟏 𝐒𝐨𝐦𝐞 𝐝𝐞𝐭𝐚𝐢𝐥𝐬 𝐨𝐧 𝐭𝐡𝐢𝐬 𝐭𝐨𝐩𝐢𝐜', s_2_1.repr_report())
        s_2_2 = t.open_section('some more details on this topic', section_parent=s_2, echo=True)
        self.assertEqual('## 𝟐.𝟐 𝐒𝐨𝐦𝐞 𝐦𝐨𝐫𝐞 𝐝𝐞𝐭𝐚𝐢𝐥𝐬 𝐨𝐧 𝐭𝐡𝐢𝐬 𝐭𝐨𝐩𝐢𝐜', s_2_2.repr_report())
        s_2_2_1 = t.open_section('zooming in', section_parent=s_2_2, echo=True)
        self.assertEqual('### 𝟐.𝟐.𝟏 𝐙𝐨𝐨𝐦𝐢𝐧𝐠 𝐢𝐧', s_2_2_1.repr_report())
        s_2_2_7 = t.open_section('jumping sections', section_number=7, section_parent=s_2_2, echo=True)
        self.assertEqual('### 𝟐.𝟐.𝟕 𝐉𝐮𝐦𝐩𝐢𝐧𝐠 𝐬𝐞𝐜𝐭𝐢𝐨𝐧𝐬', s_2_2_7.repr_report())
        s_2_3 = t.open_section('yet more details on this topic', section_parent=s_2, echo=True)
        self.assertEqual('## 𝟐.𝟑 𝐘𝐞𝐭 𝐦𝐨𝐫𝐞 𝐝𝐞𝐭𝐚𝐢𝐥𝐬 𝐨𝐧 𝐭𝐡𝐢𝐬 𝐭𝐨𝐩𝐢𝐜', s_2_3.repr_report())
