class Test(tuple):
    def __new__(cls, s: str = ''):
        print(f'__new__: s={s}')
        s = f'{s}+'
        print(f'__new__: updated s={s}')
        o: tuple = super().__new__(cls, (s,))
        return o

    def __init__(self):  # s: str = ''):
        print(f'__init__: s={s}')
        super().__init__()


x = Test(s='a')
print(x)
