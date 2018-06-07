import numpy as np
import math
import IPython

class RandomNeuralNet:

    def predict(self, state):
        pi = np.random.randn(state.cols)
        legal_moves = state.get_legal_moves()
        for i in range(state.cols):
            if i not in legal_moves:
                pi[i] = 0
        pi = self.softmax(pi)

        v = np.random.uniform(-1,1)
        return (pi, v)

    def softmax(self, p):
        e_p = np.exp(p - np.max(p))
        return e_p / e_p.sum(axis=0)

class NeuralNet:

    def __init__(self, layers=[42, 14, 12, 10, 8]):
        """layers should be a list of neuron count. The first and last
        are the input and output layers, respectively. The others are
        hidden layers
        """
        self.inputs = np.zeros(layers[0])
        self.outputs = np.zeros(layers[-1])
        self.weights = []
        self.biases = []

        self.z = [] # store the z values for backprop
        self.a = [] # store the a values for backprop
        
        for i, layer in enumerate(layers[1:]):
            shape = (layer, layers[i])
            self.weights.append(np.random.rand(layer, layers[i]))
            self.biases.append(np.random.rand(layer))

    def train(self, state, outcome):
        value, probs = self.predict(state)
        pass


    def predict(self, state):
        """given a board state, predict the V(s) ∈ [-1,1] and P(s,•)
        """
        self.unpack_inputs(state)
        self.feedforward()
        P = self.softmax(self.outputs[:-1]) # creates a probability dist
        v = np.minimum(self.outputs[-1], 1)
        return (P,v)

    
    def unpack_inputs(self, state):
        self.inputs = state.board.flatten()


    def feedforward(self):
        self.a = self.z = []
        a = self.inputs
        for w, b in zip(self.weights, self.biases):
            #IPython.embed()
            z = w.dot(a) + b
            a = self.ReLU(z)
            self.z.append(z)
            self.a.append(a)

        self.outputs = a[:-1]
        self.outputs[-1] = z[-1] # we don't want the ReLU version of this


    def ReLU(self, x):
        return np.maximum(x, 0, x)


    def ReLU_prime(self, x):
        return (x > 0) * 1


    def softmax(self, p):
        e_p = np.exp(p - np.max(p))
        return e_p / e_p.sum(axis=0)


if __name__ == "__main__":
    nn = NeuralNet(2, 1, 1, 3)