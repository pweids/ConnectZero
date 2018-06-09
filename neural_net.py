import math
import game

import numpy as np
import logging, pickle, os

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

class Layer:
    def __init__(self, size, W, z=None, b=None, a=None, delta=None):
        """the 5 data points are the z vector, b weights, a output,
        delta "error" and W weights matrix
        """
        self.size = size
        self.z = z or np.zeros(size)
        self.b = b or np.random.randn(size)
        self.a = a or np.zeros(size)
        self.delta = delta or np.zeros(size)
        self.W = W
        self.next = None

        
    def __repr__(self):
        return f"Layer <size:{self.size}, W:{self.W.shape}, z,b,a:({len(self.z)}, 1)>"

class NeuralNet:

    def __init__(self, layers=[42, 14, 12, 10, 8], eta=0.5):
        """layers should be a list of neuron count. The first and last
        are the input and output layers, respectively. The others are
        hidden layers
        """
        self.inputs = np.zeros(layers[0])
        self.num_layers = len(layers)-1 # input doesn't count

        # The Layer is a class to help keep all the indices aligned
        self.layers = []
        self.eta = eta # η (eta) for the learning rate
        
        for i in range(self.num_layers): # i represents Layer-1
            curr_size = layers[i+1]
            prev_size = layers[i]
            # shape of Weights is current layer x prev layer
            W = np.random.randn(curr_size, prev_size)
            layer = Layer(curr_size, W)
            if i > 0:
                self.layers[-1].next = layer
            self.layers.append(layer)

        logging.basicConfig(filename="nn.log", level=logging.DEBUG, filemode='w')


    def train(self, state, pi, z):
        """Train this neural network with the current state
        and the actual values for the position value and 
        probablity array
        """
        self.predict(state)
        cost_start = self.cost_function(z, pi)

        self.backpropagate(z, pi)
        
        self.predict(state)
        cost_end = self.cost_function(z, pi)
        delta_cost = cost_start - cost_end
        out = f"Loss change: {cost_start:.2f} - {cost_end:.2f} = {delta_cost:.2f}"


    def predict(self, state):
        """given a board state, predict the V(s) ∈ [-1,1] and P(s,•)
        """
        self.unpack_inputs(state)
        self.feedforward()
        return self.get_results()


    def get_results(self):
        P = self.layers[-1].a[:-1]
        v = self.layers[-1].a[-1]
        return P, v

    
    def unpack_inputs(self, state):
        self.inputs = state.board.flatten()


    def feedforward(self):
        a = self.inputs
        for layer in self.layers:
            layer.z = layer.W.dot(a) + layer.b
            if layer is not self.layers[-1]: # don't apply relu to last layer
                layer.a = self.ReLU(layer.z)
                a = layer.a
            else: # last layer is a prob distribution + a value in [-1, 1]
                layer.a = np.append(self.softmax(layer.z[:-1]), np.tanh(layer.z[-1]))


    def backpropagate(self, z, pi):
        self.create_gradients(z, pi)
        self.update_weights()
        self.update_biases()


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
        out_layer = self.layers[-1]
        # fill in the gradients for the output neurons
        P, v = self.get_results()
        delta = []
        for pi_i, P_i in zip(pi, P):
            #p_i / P_i
            delta.append(pi_i*(1-P_i))
        delta.append(2*(v-z))
        out_layer.delta = np.array(delta)

        # now iterate backwards through the rest of the layers
        # δ_l = ((W_(l+1)T) • δ_(l+1)) * ReLU'(z_l)
        for l in reversed(self.layers[:-1]):
            l.delta = np.dot(l.next.W.T, l.next.delta) * self.ReLU_prime(l.z)


    def update_weights(self):
        """Gradient matrix is a_(l-1) * δ_l
        """
        a = self.inputs
        for layer in self.layers:
            d = layer.delta
            gradient = np.dot(d.reshape(len(d), 1), a.reshape(1, len(a)))
            layer.W -= self.eta * gradient
            a = layer.a


    def update_biases(self):
        for layer in self.layers:
            layer.b -= self.eta * layer.delta


    def ReLU(self, x):
        return np.maximum(x, 0, x)


    def ReLU_prime(self, x):
        return (x > 0) * 1


    def softmax(self, p):
        p = p / np.sum(p) # i found this helps when the values are really high
        e_p = np.exp(p - np.max(p))
        return e_p / e_p.sum(axis=0)


    def save_checkpoint(self, file="dnn_checkpoint.bin"):
        with open(file, 'wb+') as dnn_f:
            pickle.dump(self, dnn_f)


    @staticmethod
    def load_checkpoint(file="dnn_checkpoint.bin"):
        if (os.path.isfile(file)):
            with open(file, 'rb') as dnn_f:
                return pickle.load(dnn_f)
        return NeuralNet()


def test():
    g = game.Game()
    g.make_random_moves(10)
    nn = NeuralNet([42, 14, 12, 10, 8])
    pi = nn.softmax(np.random.randn(7))
    nn.train(g.board, 1, pi)