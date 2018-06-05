import numpy as np
import math

class Neuron:

    def __init__(self, inputs = [], outputs = []):
        self.value = 0
        self.input_synapses = inputs
        self.output_synapses = outputs

    def forward(self):
        if self.input_synapses:
            self.sum_inputs()
        if self.output_synapses:
            for synapse in self.output_synapses:
                synapse.fire(self.value)

    def sum_inputs(self):
        self.value = self.sigmoid(sum(self.input_synapses))

    def sigmoid(self, x):
        return 1 / (1 + math.exp(-x))


class Synapse:

    def __init__(self):
        self.weight = np.random.rand()*2 - 1
        self.value = 0

    def fire(self, in_val):
        self.value = self.weight * in_val

    def __add__(self, other):
        return self.value + other.value

class NeuralNet:

    layers = []
    def __init__(self, num_cells, num_actions, num_hidden = 2, size_hidden = 21):
        # represents each cells in the board
        self.layers.append([Neuron() for _ in range(num_cells)])
        self.add_layer(size_hidden, num_hidden)
        self.add_layer(num_actions+1)
    
    def train(self, state, outcome):
        value, probs = self.predict(state)
        pass


    def predict(self, state):
        # given a board state, predict the
        # value [-1,1] and P(s,*)
        return np.random.rand()*2-1, [np.random.rand()]*(len(self.layers[-1])-1)


    def add_layer(self, size, num_layers = 1):
        for _ in range(num_layers):
            new_layer = [Neuron() for i in range(size)]
            for old in self.layers[-1]:
                for new in new_layer:
                    s = Synapse()
                    old.output_synapses.append(s)
                    new.input_synapses.append(s)
            self.layers.append(new_layer)

if __name__ == "__main__":
    nn = NeuralNet(2, 1, 1, 3)