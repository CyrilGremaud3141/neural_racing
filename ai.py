import random
import math
class Neuron:
    def __init__(self, input_weights):
        self.input_weights = [random.random() for _ in range(input_weights)]
        self.in_size = input_weights
        self.bias = random.random()

    def fire(self, ins):
        summe = 0
        for i in range(len(self.input_weights)):
            summe += self.input_weights[i] * ins[i]
        summe += self.bias
        return self.activation(summe)

    def activation(self, number):
        return 1/ (1 + math.exp(number))
    
    def randomize(self):
        self.input_weights = [random.random() for _ in range(self.in_size)]


class NeuralNet:
    def __init__(self, input_size, hidden_sizes, output_size):
        self.net = []

        self.shape = hidden_sizes + [output_size]
        self.layer_sizes = [input_size] + hidden_sizes + [output_size]

        for i in range(len(self.shape)):
            layer = []
            for neur in range(self.shape[i]):
                layer.append(Neuron(self.layer_sizes[i]))
            self.net.append(layer)


    def forward(self, input_activations):
        previous_layer = input_activations
        for layer in range(len(self.shape)):
            this_layer = []
            for neur in range(self.shape[layer]):
                this_layer.append(self.net[layer][neur].fire(previous_layer))
            previous_layer = this_layer
        return this_layer


if __name__ == '__main__':
    nn = NeuralNet(6, [4, 5], 2)
    print(nn.net)

    print(nn.forward([0.5, 0.5, 0.5, 0.5, 0.5, 0.5]))