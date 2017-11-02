def display(fuck, **kwargs):
    for key,value in kwargs.items():
        print(key, value)
    ret = func()
    print(ret)


def t(a,b,c):
    print(a, b, c)

display(t, a='1', b='2', c='3')