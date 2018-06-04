import numpy as np

class Neuron:

    def __init__(self):
        self.weight = np.random.rand()*2 -1
        self.output_neurons = []
        self.input_neurons = None

class NeuralNet:

    layers = []
    def __init__(self, num_cells, num_actions, num_hidden = 2, size_hidden = 21):
        # represents each cells in the board
        self.layers.append([Neuron()] * num_cells)
        self.add_hidden_layers(num_hidden, size_hidden)
        self.add_last_layer(num_actions+1)
    
    def train(self, state, outcome):
        value, probs = self.predict(state)
        pass


    def predict(self, state):
        # given a board state, predict the
        # value [-1,1] and P(s,*)
        return np.random.rand()*2-1, [np.random.rand()]*(len(self.layers[-1])-1)


    def add_hidden_layers(self, num, size):
        for _ in range(num):
            new_layer = [Neuron()] * size
            for out in self.layers[-1]:
                out.output_neurons = new_layer
            for new in new_layer:
                new.input_neurons = self.layers[-1]
            self.layers.append(new_layer)

    def add_last_layer(self, num):
        layer = [Neuron()] * num
        last_layer = self.layers[-1]
        for neuron in layer:
            neuron.input_neurons = last_layer
        for neuron in last_layer:
            neuron.output_neurons = layer
        self.layers.append(layer)
