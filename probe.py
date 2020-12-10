
from datetime import datetime
from random import choice
import itertools, random
import numpy as np


uniq = True

# def select(size, pair_size):
#     g =itertools.combinations(range(size),pair_size)
#     alist = list(g)
#     random.shuffle(alist)
#     return alist
numbers = {'4': ['5'], '5': ['4'], '3': ['9'], '9': ['3'], '1': ['2'], '2': ['1'], '8': ['10'], '10': ['8'], '6': ['7'], '7': ['6']}

l = [i for i in range(1, 11)]

while True:
    pairs = np.random.choice(a=l, size=(len(l) // 2, 2), replace=False)
    print(pairs)
    pre_numbers = numbers.copy()
    for user_id, partner_id in pairs:
        user_id, partner_id = str(user_id), str(partner_id)
        print('User_id ', user_id, 'Partner_id ', partner_id)
        # if partner_id in numbers[user_id] or user_id in numbers[partner_id]:
        print(numbers[user_id], 'uniq', np.unique(numbers[user_id]))
        print(numbers[partner_id], 'uniq', np.unique(numbers[partner_id]))
        if len(numbers[user_id]) > len(np.unique(numbers[user_id])) or \
            len(numbers[partner_id]) > len(np.unique(numbers[partner_id])):
            print(partner_id, numbers[user_id])
            print(user_id, numbers[partner_id])
            print('numbers', numbers)
            print('pre_numbers', pre_numbers)
            print('Повторение')
            numbers = pre_numbers.copy()
            break
        else:
            numbers[user_id].append(partner_id)
            numbers[partner_id].append(user_id)

        # else:
        #     numbers[user_id] = [partner_id]
        #     numbers[partner_id] = [user_id]
    print(numbers)
    input()
f = ['1', '5', '1', '2']

print(np.unique(f))

print(numbers)
# a= select(3, 2)
# print(a)
# l = [1, 2, 3, 4, 5, 6]
# while l:
#     chosen = choice(l)
#     l.remove(chosen)
#     print(chosen)
#     print(l)
#     input()


