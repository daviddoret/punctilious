
class SuperTuple(tuple):
    pass

x = SuperTuple()

print(x)

setattr(x, 'test', 17)
print(getattr(x, 'test'))