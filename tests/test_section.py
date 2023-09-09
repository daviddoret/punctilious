from unittest import TestCase
import punctilious as p


class TestSection(TestCase):
    def test_section(self):
        echo_note = p.configuration.echo_note
        p.configuration.echo_note = True
        u = p.UniverseOfDiscourse()
        t = u.t(subtitle='A test theory')
        s_1 = t.open_section('something interesting', echo=True)
        self.assertEqual('# 𝟭: 𝗦𝗼𝗺𝗲𝘁𝗵𝗶𝗻𝗴 𝗶𝗻𝘁𝗲𝗿𝗲𝘀𝘁𝗶𝗻𝗴', s_1.rep_report())
        s_2 = t.open_section('something else', echo=True)
        self.assertEqual('# 𝟮: 𝗦𝗼𝗺𝗲𝘁𝗵𝗶𝗻𝗴 𝗲𝗹𝘀𝗲', s_2.rep_report())
        s_2_1 = t.open_section('some details on this topic', section_parent=s_2, echo=True)
        self.assertEqual('## 𝟮.𝟭: 𝗦𝗼𝗺𝗲 𝗱𝗲𝘁𝗮𝗶𝗹𝘀 𝗼𝗻 𝘁𝗵𝗶𝘀 𝘁𝗼𝗽𝗶𝗰', s_2_1.rep_report())
        s_2_2 = t.open_section('some more details on this topic', section_parent=s_2, echo=True)
        self.assertEqual('## 𝟮.𝟮: 𝗦𝗼𝗺𝗲 𝗺𝗼𝗿𝗲 𝗱𝗲𝘁𝗮𝗶𝗹𝘀 𝗼𝗻 𝘁𝗵𝗶𝘀 𝘁𝗼𝗽𝗶𝗰', s_2_2.rep_report())
        s_2_2_1 = t.open_section('zooming in', section_parent=s_2_2, echo=True)
        self.assertEqual('### 𝟮.𝟮.𝟭: 𝗭𝗼𝗼𝗺𝗶𝗻𝗴 𝗶𝗻', s_2_2_1.rep_report())
        s_2_2_7 = t.open_section('jumping sections', section_number=7, section_parent=s_2_2,
                                 echo=True)
        self.assertEqual('### 𝟮.𝟮.𝟳: 𝗝𝘂𝗺𝗽𝗶𝗻𝗴 𝘀𝗲𝗰𝘁𝗶𝗼𝗻𝘀', s_2_2_7.rep_report())
        s_2_3 = t.open_section('yet more details on this topic', section_parent=s_2, echo=True)
        self.assertEqual('## 𝟮.𝟯: 𝗬𝗲𝘁 𝗺𝗼𝗿𝗲 𝗱𝗲𝘁𝗮𝗶𝗹𝘀 𝗼𝗻 𝘁𝗵𝗶𝘀 𝘁𝗼𝗽𝗶𝗰', s_2_3.rep_report())
