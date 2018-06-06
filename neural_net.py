import numpy as np
import math

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

    layers = []
    def __init__(self, num_cells, num_actions, num_hidden = 2, size_hidden = 21):
        # represents each cells in the board
        pass

    def train(self, state, outcome):
        value, probs = self.predict(state)
        pass


    def predict(self, state):
        # given a board state, predict the
        # value [-1,1] and P(s,*)
        return np.random.rand()*2-1, [np.random.rand()]*(len(self.layers[-1])-1)

if __name__ == "__main__":
    nn = NeuralNet(2, 1, 1, 3)