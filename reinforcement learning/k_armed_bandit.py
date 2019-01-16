import numpy as np
import random

class k_armed_bandit:

    k = 0

    ps = [] #每个臂的概率

    coins = [] #每个臂的硬币数


    def __init__(self, k, ps, coins):
        if len(ps) != k or len(coins) != k:
            print('length catch error!')
            return
        self.k = k
        self.ps = ps
        self.coins = coins

        print(self.ps)
        print(self.coins)


    def c_hungry(self, c, T):
        if c < 0 or c > 1:
            return 'error'

        rewards = np.zeros(self.k) #每个臂的平均奖励
        times = np.zeros(self.k) #每个臂的尝试次数

        s = 0 #总奖励
        
        for i in range(T):
            arm = 0
            if random.random() < c: #探索模式
                arm = random.randint(0, self.k - 1)
            else: #利用模式
                indexs = max_indexs(rewards)
                ran = random.randint(0, len(indexs) - 1)
                arm = indexs[ran]
            reward = 0
            if random.random() <= self.ps[arm]:
                reward = self.coins[arm]
            rewards[arm] = (rewards[arm] * times[arm] + reward) / (times[arm] + 1)
            times[arm] += 1
            s += reward

        return s


    def softmax(self, t, T):
        if t <= 0:
            return 'error'

        rewards = np.zeros(self.k) #每个臂的平均奖励
        times = np.zeros(self.k) #每个臂的尝试次数

        s = 0 #总奖励

        for i in range(T):
            arm = 0
            boltz_ps = np.zeros(self.k) #Boltzmann概率分布
            exps = np.exp(rewards / t)
            boltz_ps = exps / np.sum(exps)
            ran = random.random()
            count = 0
            for j in range(0, len(boltz_ps)):
                count += boltz_ps[j]
                if count >= ran:
                    arm = j
                    break
            reward = 0
            if random.random() <= self.ps[arm]:
                reward = self.coins[arm]
            rewards[arm] = (rewards[arm] * times[arm] + reward) / (times[arm] + 1)
            times[arm] += 1
            s += reward

        return s
        
                
def max_indexs(nums):
    max_num = max(nums)
    indexs = []
    for i in range(0, len(nums)):
        if nums[i] == max_num:
            indexs.append(i)
    return indexs
