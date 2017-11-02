
def login(func):
    def wapper(a, b):
        print(a, b)
        print('111111111')
        func(a, b)
        print('666666666')
    return wapper
