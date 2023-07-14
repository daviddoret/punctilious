"""Unicode text utilities."""

unicode_serif_normal_index = 0
unicode_serif_bold_index = 1
unicode_serif_italic_index = 2
unicode_serif_bold_italic_index = 3
unicode_sans_serif_normal_index = 4
unicode_sans_serif_bold_index = 5
unicode_sans_serif_italic_index = 6
unicode_sans_serif_bold_italic_index = 7
unicode_script_normal_index = 8
unicode_script_bold_index = 9
unicode_fraktur_normal_index = 10
unicode_fraktur_bold_index = 11
unicode_monospace_index = 12
unicode_double_struck_index = 13

unicode_styled_characters = {
    'a': 'a𝐚𝑎𝒂𝖺𝗮𝘢𝙖𝒶𝓪𝔞𝖆𝚊𝕒',
    'b': 'b𝐛𝑏𝒃𝖻𝗯𝘣𝙗𝒷𝓫𝔟𝖇𝚋𝕓',
    'c': 'c𝐜𝑐𝒄𝖼𝗰𝘤𝙘𝒸𝓬𝔠𝖈𝚌𝕔',
    'd': 'd𝐝𝑑𝒅𝖽𝗱𝘥𝙙𝒹𝓭𝔡𝖉𝚍𝕕',
    'e': 'e𝐞𝑒𝒆𝖾𝗲𝘦𝙚ℯ𝓮𝔢𝖊𝚎𝕖',
    'f': 'f𝐟𝑓𝒇𝖿𝗳𝘧𝙛𝒻𝓯𝔣𝖋𝚏𝕗',
    'g': 'g𝐠𝑔𝒈𝗀𝗴𝘨𝙜ℊ𝓰𝔤𝖌𝚐𝕘',
    'h': 'h𝐡ℎ𝒉𝗁𝗵𝘩𝙝𝒽𝓱𝔥𝖍𝚑𝕙',
    'i': 'i𝐢𝑖𝒊𝗂𝗶𝘪𝙞𝒾𝓲𝔦𝖎𝚒𝕚',
    'j': 'j𝐣𝑗𝒋𝗃𝗷𝘫𝙟𝒿𝓳𝔧𝖏𝚓𝕛',
    'k': 'k𝐤𝑘𝒌𝗄𝗸𝘬𝙠𝓀𝓴𝔨𝖐𝚔𝕜',
    'l': 'l𝐥𝑙𝒍𝗅𝗹𝘭𝙡𝓁𝓵𝔩𝖑𝚕𝕝',
    'm': 'm𝐦𝑚𝒎𝗆𝗺𝘮𝙢𝓂𝓶𝔪𝖒𝚖𝕞',
    'n': 'n𝐧𝑛𝒏𝗇𝗻𝘯𝙣𝓃𝓷𝔫𝖓𝚗𝕟',
    'o': 'o𝐨𝑜𝒐𝗈𝗼𝘰𝙤ℴ𝓸𝔬𝖔𝚘𝕠',
    'p': 'p𝐩𝑝𝒑𝗉𝗽𝘱𝙥𝓅𝓹𝔭𝖕𝚙𝕡',
    'q': 'q𝐪𝑞𝒒𝗊𝗾𝘲𝙦𝓆𝓺𝔮𝖖𝚚𝕢',
    'r': 'r𝐫𝑟𝒓𝗋𝗿𝘳𝙧𝓇𝓻𝔯𝖗𝚛𝕣',
    's': 's𝐬𝑠𝒔𝗌𝘀𝘴𝙨𝓈𝓼𝔰𝖘𝚜𝕤',
    't': 't𝐭𝑡𝒕𝗍𝘁𝘵𝙩𝓉𝓽𝔱𝖙𝚝𝕥',
    'u': 'u𝐮𝑢𝒖𝗎𝘂𝘶𝙪𝓊𝓾𝔲𝖚𝚞𝕦',
    'v': 'v𝐯𝑣𝒗𝗏𝘃𝘷𝙫𝓋𝓿𝔳𝖛𝚟𝕧',
    'w': 'w𝐰𝑤𝒘𝗐𝘄𝘸𝙬𝓌𝔀𝔴𝖜𝚠𝕨',
    'x': 'x𝐱𝑥𝒙𝗑𝘅𝘹𝙭𝓍𝔁𝔵𝖝𝚡𝕩',
    'y': 'y𝐲𝑦𝒚𝗒𝘆𝘺𝙮𝓎𝔂𝔶𝖞𝚢𝕪',
    'z': 'z𝐳𝑧𝒛𝗓𝘇𝘻𝙯𝓏𝔃𝔷𝖟𝚣𝕫',
    'A': 'A𝐀𝐴𝑨𝖠𝗔𝘈𝘼𝒜𝓐𝔄𝕬𝙰𝔸',
    'B': 'B𝐁𝐵𝑩𝖡𝗕𝘉𝘽ℬ𝓑𝔅𝕭𝙱𝔹',
    'C': 'C𝐂𝐶𝑪𝖢𝗖𝘊𝘾𝒞𝓒ℭ𝕮𝙲ℂ',
    'D': 'D𝐃𝐷𝑫𝖣𝗗𝘋𝘿𝒟𝓓𝔇𝕯𝙳𝔻',
    'E': 'E𝐄𝐸𝑬𝖤𝗘𝘌𝙀ℰ𝓔𝔈𝕰𝙴𝔼',
    'F': 'F𝐅𝐹𝑭𝖥𝗙𝘍𝙁ℱ𝓕𝔉𝕱𝙵𝔽',
    'G': 'G𝐆𝐺𝑮𝖦𝗚𝘎𝙂𝒢𝓖𝔊𝕲𝙶𝔾',
    'H': 'H𝐇𝐻𝑯𝖧𝗛𝘏𝙃ℋ𝓗ℌ𝕳𝙷ℍ',
    'I': 'I𝐈𝐼𝑰𝖨𝗜𝘐𝙄ℐ𝓘ℑ𝕴𝙸𝕀',
    'J': 'J𝐉𝐽𝑱𝖩𝗝𝘑𝙅𝒥𝓙𝔍𝕵𝙹𝕁',
    'K': 'K𝐊𝐾𝑲𝖪𝗞𝘒𝙆𝒦𝓚𝔎𝕶𝙺𝕂',
    'L': 'L𝐋𝐿𝑳𝖫𝗟𝘓𝙇ℒ𝓛𝔏𝕷𝙻𝕃',
    'M': 'M𝐌𝑀𝑴𝖬𝗠𝘔𝙈ℳ𝓜𝔐𝕸𝙼𝕄',
    'N': 'N𝐍𝑁𝑵𝖭𝗡𝘕𝙉𝒩𝓝𝔑𝕹𝙽ℕ',
    'O': 'O𝐎𝑂𝑶𝖮𝗢𝘖𝙊𝒪𝓞𝔒𝕺𝙾𝕆',
    'P': 'P𝐏𝑃𝑷𝖯𝗣𝘗𝙋𝒫𝓟𝔓𝕻𝙿ℙ',
    'Q': 'Q𝐐𝑄𝑸𝖰𝗤𝘘𝙌𝒬𝓠𝔔𝕼𝚀ℚ',
    'R': 'R𝐑𝑅𝑹𝖱𝗥𝘙𝙍ℛ𝓡ℜ𝕽𝚁ℝ',
    'S': 'S𝐒𝑆𝑺𝖲𝗦𝘚𝙎𝒮𝓢𝔖𝕾𝚂𝕊',
    'T': 'T𝐓𝑇𝑻𝖳𝗧𝘛𝙏𝒯𝓣𝔗𝕿𝚃𝕋',
    'U': 'U𝐔𝑈𝑼𝖴𝗨𝘜𝙐𝒰𝓤𝔘𝖀𝚄𝕌',
    'V': 'V𝐕𝑉𝑽𝖵𝗩𝘝𝙑𝒱𝓥𝔙𝖁𝚅𝕍',
    'W': 'W𝐖𝑊𝑾𝖶𝗪𝘞𝙒𝒲𝓦𝔚𝖂𝚆𝕎',
    'X': 'X𝐗𝑋𝑿𝖷𝗫𝘟𝙓𝒳𝓧𝔛𝖃𝚇𝕏',
    'Y': 'Y𝐘𝑌𝒀𝖸𝗬𝘠𝙔𝒴𝓨𝔜𝖄𝚈𝕐',
    'Z': 'Z𝐙𝑍𝒁𝖹𝗭𝘡𝙕𝒵𝓩ℨ𝖅𝚉ℤ',
    '0': '0𝟎0𝟎𝟢𝟬𝟢𝟬𝟢𝟬𝟢𝟬𝟶𝟘',
    '1': '1𝟏1𝟏𝟣𝟭𝟣𝟭𝟣𝟭𝟣𝟭𝟷𝟙',
    '2': '2𝟐2𝟐𝟤𝟮𝟤𝟮𝟤𝟮𝟤𝟮𝟸𝟚',
    '3': '3𝟑3𝟑𝟥𝟯𝟥𝟯𝟥𝟯𝟥𝟯𝟹𝟛',
    '4': '4𝟒4𝟒𝟦𝟰𝟦𝟰𝟦𝟰𝟦𝟰𝟺𝟜',
    '5': '5𝟓5𝟓𝟧𝟱𝟧𝟱𝟧𝟱𝟧𝟱𝟻𝟝',
    '6': '6𝟔6𝟔𝟨𝟲𝟨𝟲𝟨𝟲𝟨𝟲𝟼𝟞',
    '7': '7𝟕7𝟕𝟩𝟳𝟩𝟳𝟩𝟳𝟩𝟳𝟽𝟟',
    '8': '8𝟖8𝟖𝟪𝟴𝟪𝟴𝟪𝟴𝟪𝟴𝟾𝟠',
    '9': '9𝟗9𝟗𝟫𝟵𝟫𝟵𝟫𝟵𝟫𝟵𝟿𝟡'
}


def unicode_format(s: str = '', index: int = 0) -> str:
    """Formats a string with Unicode formatting.
    
    :param s: A string of basic plaintext (visible ASCII characters).
    :param index: The style index from the unicode_styles_dictionary.
    :return: The string formatted with the desired style.
    """
    global unicode_styled_characters
    return ''.join([unicode_styled_characters.get(c, c * 14)[index] for c in s])


def unicode_sans_serif_normal(s: str):
    return unicode_format(s=s, index=unicode_sans_serif_normal_index)


def unicode_sans_serif_bold(s: str):
    return unicode_format(s=s, index=unicode_sans_serif_bold_index)


def unicode_sans_serif_italic(s: str):
    return unicode_format(s=s, index=unicode_sans_serif_italic_index)


def unicode_sans_serif_bold_italic(s: str):
    return unicode_format(s=s, index=unicode_sans_serif_bold_italic_index)


def unicode_serif_normal(s: str):
    return unicode_format(s=s, index=unicode_serif_normal_index)


def unicode_serif_bold(s: str):
    return unicode_format(s=s, index=unicode_serif_bold_index)


def unicode_serif_italic(s: str):
    return unicode_format(s=s, index=unicode_serif_italic_index)


def unicode_serif_bold_italic(s: str):
    return unicode_format(s=s, index=unicode_serif_italic_bold_index)


def unicode_script_normal(s: str):
    return unicode_format(s=s, index=unicode_script_normal_index)


def unicode_script_bold(s: str):
    return unicode_format(s=s, index=unicode_script_bold_index)


def unicode_fraktur_normal(s: str):
    return unicode_format(s=s, index=unicode_fraktur_normal_index)


def unicode_fraktur_bold(s: str):
    return unicode_format(s=s, index=unicode_fraktur_bold_index)


def unicode_monospace(s: str):
    return unicode_format(s=s, index=unicode_monospace_index)


def unicode_double_struck(s: str):
    return unicode_format(s=s, index=unicode_double_struck_index)


unicode_subscript_dictionary = {
    '0': u'₀',
    '1': u'₁',
    '2': u'₂',
    '3': u'₃',
    '4': u'₄',
    '5': u'₅',
    '6': u'₆',
    '7': u'₇',
    '8': u'₈',
    '9': u'₉',
    'a': u'ₐ',
    'e': u'ₑ',
    'o': u'ₒ',
    'x': u'ₓ',
    # '???': u'ₔ',
    'h': u'ₕ',
    'k': u'ₖ',
    'l': u'ₗ',
    'm': u'ₘ',
    'n': u'ₙ',
    'p': u'ₚ',
    's': u'ₛ',
    't': u'ₜ',
    '+': u'₊',
    '-': u'₋',
    '=': u'₌',
    '(': u'₍',
    ')': u'₎',
    'j': u'ⱼ',
    'i': u'ᵢ',  # Alternative from the Unicode Phonetic Extensions block: ᵢ
    'r': u'ᵣ',  # Source: Unicode Phonetic Extensions block.
    'u': u'ᵤ',  # Source: Unicode Phonetic Extensions block.
    'v': u'ᵥ',  # Source: Unicode Phonetic Extensions block.
    'β': u'ᵦ',  # Source: Unicode Phonetic Extensions block.
    'γ': u'ᵧ',  # Source: Unicode Phonetic Extensions block.
    # '???': u'ᵨ', # Source: Unicode Phonetic Extensions block.
    'φ': u'ᵩ',  # Source: Unicode Phonetic Extensions block.
    'χ': u'ᵪ'  # Source: Unicode Phonetic Extensions block.
}


def unicode_subscriptify(s: str = ''):
    """Converts to unicode-subscript the string s.

    This is done in best effort, knowing that Unicode only contains a small subset of subscript characters.

    References:
        * https://stackoverflow.com/questions/13875507/convert-numeric-strings-to-superscript
        * https://en.wikipedia.org/wiki/Unicode_subscripts_and_superscripts
    """
    global unicode_subscript_dictionary
    if isinstance(s, int):
        s = str(s)
    if s is None or s == '':
        return ''
    return ''.join([unicode_subscript_dictionary.get(c, c) for c in s])
