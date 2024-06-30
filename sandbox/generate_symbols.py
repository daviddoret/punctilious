def uppercase_script_register():
    for k, u, n in zip('abcdefghijklmnopqrstuvwxyz',
                       '𝒜ℬ𝒞𝒟ℰℱ𝒢ℋℐ𝒥𝒦ℒℳ𝒩𝒪𝒫𝒬ℛ𝒮𝒯𝒰𝒱𝒲𝒳𝒴𝒵',
                       'ABCDEFGHIJKLMNOPQRSTUVWXYZ'):
        print(f"""        self._{k}_uppercase_script = self._register(
                Symbol(key='{k}_uppercase_script', latex_math='\\\\texttt{{{n}}}', unicode_extended='{u}',
                       unicode_limited='{n}'))
    
        """)


def lowercase_script_register():
    for k, u, n in zip('abcdefghijklmnopqrstuvwxyz',
                       '𝒶𝒷𝒸𝒹ℯ𝒻ℊ𝒽𝒾𝒿𝓀𝓁𝓂𝓃ℴ𝓅𝓆𝓇𝓈𝓉𝓊𝓋𝓌𝓍𝓎𝓏',
                       'abcdefghijklmnopqrstuvwxyz'):
        print(f"""        self._{k}_lowercase_script = self._register(
                Symbol(key='{k}_lowercase_script', latex_math='\\\\texttt{{{n}}}', unicode_extended='{u}',
                       unicode_limited='{n}'))
    
        """)


def uppercase_script_properties():
    for k, n in zip('abcdefghijklmnopqrstuvwxyz', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'):
        print(f"""    @property
    def {k}_uppercase_script(self) -> Symbol:
        return self._{k}_uppercase_script""")


def lowercase_script_properties():
    for k, n in zip('abcdefghijklmnopqrstuvwxyz', 'abcdefghijklmnopqrstuvwxyz'):
        print(f"""    @property
    def {k}_lowercase_script(self) -> Symbol:
        return self._{k}_lowercase_script""")


lowercase_script_properties()
