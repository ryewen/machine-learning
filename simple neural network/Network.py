from Node import Node

class Network:

    layers = []

    learning_rate = 0

    def __init__(self, lens, learning_rate, w, threshold):
        self.layers = []
        self.learning_rate = learning_rate
        for length in lens:
            nodes = []
            for i in range(0, length):
                nodes.append(Node(threshold))
            self.layers.append(nodes)
        for i in range(0, len(self.layers) - 1):
            before_nodes = self.layers[i]
            next_nodes = self.layers[i + 1]
            for before_node in before_nodes:
                for next_node in next_nodes:
                    before_node.nexts.append(next_node)
                    before_node.next_ws.append(w)
                    next_node.befores.append(before_node)
                    next_node.before_ws.append(w)

    def set_input_layer(self, values):
        if len(values) != len(self.layers[0]):
            return 0
        for i in range(0, len(values)):
            self.layers[0][i].forward_value = values[i]
        return 1

    def compute_error(self, label):
        outputs = self.layers[len(self.layers) - 1]
        if len(label) != len(outputs):
            return 0
        for i in range(0, len(label)):
            outputs[i].back_value = outputs[i].forward_value - label[i]
            print(outputs[i].back_value)

    def forward(self):
        for i in range(1, len(self.layers)):
            nodes = self.layers[i]
            for node in nodes:
                node.forward()

    def back(self, label):
        for i in range(0, len(self.layers) - 1):
            nodes = self.layers[len(self.layers) - 1 - i]
            if i == 0:
                if self.compute_error(label) == 0:
                    return 0
            else:
                for node in nodes:
                    node.back()
            for node in nodes:
                node.compute_delta_w()
                #print(node.before_delta_ws)
                node.compute_delta_threshold()
                #print(node.delta_threshold)
        for i in range(0, len(self.layers) - 1):
            nodes = self.layers[len(self.layers) - 1 - i]
            index = 0
            for node in nodes:
                befores = node.befores
                for j in range(0, len(befores)):
                    node.before_ws[j] -= self.learning_rate * node.before_delta_ws[j]
                    befores[j].next_ws[index] = node.before_ws[j]
                node.threshold -= self.learning_rate * node.delta_threshold
        return 1

    def train(self, data, label):
        if self.set_input_layer(data) == 0:
            print('length match error')

        self.forward()

        if self.back(label) == 0:
            print('length match error')
