

def xx():
    print('ddd')
    for i in range(3):
        yield i
        print('ssss')

j = xx()
print(next(j))
print(next(j))