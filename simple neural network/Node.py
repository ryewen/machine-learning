import math

class Node:

    nexts = []

    next_ws = []

    befores = []

    before_ws = []

    before_delta_ws = []

    threshold = 0

    delta_threshold = 0

    forward_value = 0

    back_value = 0

    def __init__(self, threshold):
        self.nexts = []
        self.next_ws = []
        self.befores = []
        self.before_ws = []
        self.before_delta_ws = []
        self.threshold = threshold
        self.delta_threshold = 0
        self.forward_value = 0
        self.back_value = 0

    def forward(self):
        s = 0
        for i in range(0, len(self.befores)):
            s += self.before_ws[i] * self.befores[i].forward_value
        self.forward_value = sigmoid(s - self.threshold)

    def back(self):
        s = 0
        for i in range(0, len(self.nexts)):
            s += self.nexts[i].back_value * de_sigmoid(self.nexts[i].forward_value) * self.next_ws[i]
        self.back_value = s

    def compute_delta_w(self):
        self.before_delta_ws = []
        delta_input = self.back_value * de_sigmoid(self.forward_value)
        for before in self.befores:
            self.before_delta_ws.append(delta_input * before.forward_value)

    def compute_delta_threshold(self):
        self.delta_threshold = self.back_value * (-1) * de_sigmoid(self.forward_value)


def sigmoid(x):
    return 1 / (1 + math.exp((-1) * x))
    
def de_sigmoid(y):
    return y * (1 - y)
