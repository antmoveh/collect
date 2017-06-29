

def move(S, D):
    D.append(S.pop())


def hanoi(n, A, B, C):
    if n == 1:
        C.append(A.pop())
    else:
        hanoi(n-1, A, C, B)
        C.append(A.pop())
        print(n-1)
        hanoi(n-1, B, A, C)


if __name__ == "__main__":
    n = 10
    A, B, C = list(range(n)), [], []
    print(A, B, C)
    hanoi(n, A, B, C)
    print(A, B, C)