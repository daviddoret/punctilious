def foo(i):
    if i == 1:
        return 1
    if i == 2:
        return 1, 2
    if i == 3:
        return 1, 2, 3


bar = foo(1)
print(bar)

bar = foo(2)
print(bar)

bar = foo(3)
print(bar)

bar, tog = foo(2)
print(bar)
print(tog)
