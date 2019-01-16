import sys

from k_armed_bandit import k_armed_bandit

if __name__ == '__main__':
    k = 5
    ps = [0.7, 0.4, 0.9, 0.1, 0.5]
    coins = [4, 8, 2, 14, 6]
    bandit = k_armed_bandit(k, ps, coins)
    if bandit.k != k:
        print('error')
        sys.exit(0)

    print(bandit.c_hungry(0.4, 1000000) / 1000000)
    print(bandit.softmax(0.2, 1000000) / 1000000)
