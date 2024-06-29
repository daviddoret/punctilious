for c, d, u in zip(['zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine'],
                   '𝟶𝟷𝟸𝟹𝟺𝟻𝟼𝟽𝟾𝟿',
                   '0123456789'):
    print(f"""        self._{c}_monospace = self._register(
            Symbol(key='{c}_monospace', latex_math='\\texttt{{{d}}}', unicode_extended='{u}',
                   unicode_limited='{d}'))

    """)
