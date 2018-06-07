import numpy as np
import math
import game

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

    def __init__(self, layers=[42, 14, 12, 10, 8], eta=0.5):
        """layers should be a list of neuron count. The first and last
        are the input and output layers, respectively. The others are
        hidden layers
        """
        self.inputs = np.zeros(layers[0])
        self.outputs = np.zeros(layers[-1])
        self.weights = []
        self.biases = []
        self.num_layers = len(layers)-1

        self.z = [] # store the z values for backprop
        self.a = [] # store the a values for backprop
        self.eta = eta # η (eta) for the learning rate
        
        for i, layer in enumerate(layers[1:]):
            self.weights.append(np.random.rand(layers[i], layer))
            self.biases.append(np.random.rand(layer))

    def train(self, state, z, pi, verbose=False):
        """Train this neural network with the current state
        and the actual values for the position value and 
        probablity array
        """
        self.predict(state)
        if verbose:
            print(f"Loss value: {self.cost_function(z, pi)}")

        self.backpropagate(z, pi)


    def predict(self, state):
        """given a board state, predict the V(s) ∈ [-1,1] and P(s,•)
        """
        self.unpack_inputs(state)
        self.feedforward()
        return self.get_results()


    def get_results(self):
        P = self.softmax(self.outputs[:-1]) # creates a probability dist
        v = np.minimum(self.outputs[-1], 1)
        return P, v

    
    def unpack_inputs(self, state):
        self.inputs = state.board.flatten()


    def feedforward(self):
        self.a = self.z = []
        a = self.inputs
        for w, b in zip(self.weights, self.biases):
            z = w.T.dot(a) + b
            a = self.ReLU(z)
            self.z.append(z)
            self.a.append(a)

        self.outputs[:-1] = a[:-1]
        self.outputs[-1] = z[-1] # we don't want the ReLU version of this


    def backpropagate(self, z, pi):
        d = self.create_gradients(z, pi)
        self.update_weights(d)
        self.update_biases(d)

    def cost_function(self, z, pi):
        """Calculate the cost for actual value z ∈ {-1,0,1} and
        π = visited probabilities from the MCTS
        """
        P, v = self.get_results()
        l = (z - v)**2 - pi.dot(np.log(P))
        return l


    def create_gradients(self, z, pi):
        """Returns a list of gradient arrays δ = ∂C/∂a for each layer
        ∂C/∂p = 1/p
        ∂C/∂v = 2(v-z)
        """
        import pdb; pdb.set_trace()
        d = [[] for _ in range(self.num_layers)]
        L = self.num_layers - 1

        # fill in the gradients for the output neurons
        P, v = self.get_results()
        for pi_i, P_i in zip(pi, P):
            d[L].append(pi_i/P_i)
        d[L].append(2*(v-z))

        # now iterate backwards through the rest of the layers
        for l in reversed(range(L)):
            d[l] = (self.weights[l+1].dot(d[l+1])) * self.ReLU_prime(self.z[l])
        return d


    def update_weights(self, d):
        for l in reversed(range(self.num_layers)):
            if l == 0:
                a = self.inputs
            else:
                a = self.a[l-1]
            gradient = a.reshape(len(a), 1) * d[l].reshape(1, len(d[l]))
            self.weights -= self.eta * gradient


    def update_biases(self, d):
        for b_l, d_l in zip(self.biases, d):
            b_l -= self.eta * d_l


    def ReLU(self, x):
        return np.maximum(x, 0, x)


    def ReLU_prime(self, x):
        return (x > 0) * 1


    def softmax(self, p):
        e_p = np.exp(p - np.max(p))
        return e_p / e_p.sum(axis=0)


def test():
    g = game.Game()
    g.make_random_moves(10)
    nn = NeuralNet([42, 14, 12, 10, 8])
    pi = nn.softmax(np.random.randn(7))
    nn.train(g.board, 1, pi)