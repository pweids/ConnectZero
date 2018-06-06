import numpy as np
import math

class RandomNeuralNet:

    def predict(self, state):
        np.random.seed(state.board.flatten())
        pi = np.random.randn(len(state.board[0]))
        pi = self.softmax(pi)

        v = np.random.uniform(-1,1)
        return (pi, v)

    def softmax(self, p):
        e_p = np.exp(p - np.max(p))
        return e_p / e_p.sum(axis=0)

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