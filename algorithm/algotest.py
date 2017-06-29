


def binary_serach(list_, item):
    low = 0
    high = len(list_) - 1

    while low <= high:
        mid = int((low + high) / 2)
        print(mid)
        guess = list_[mid]
        if guess == item:
            return mid
        if guess > item:
            high = mid
        else:
            low = mid
    return None

my_list = range(0, 10)

#print(binary_serach(my_list, 3))

def search(low, high, list_, item):
    mid = int((low + high)/2)
    guess = list_[mid]
    if guess == item:
        return mid
    elif guess > item:
        high = mid
    else:
        low = mid
    return search(low, high, list_, item)

print(search(0, len(my_list), my_list, 3))
