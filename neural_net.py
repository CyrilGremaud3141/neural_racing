class Neuron:
    def __init__(self, input_weights, bias):
        self.input_weights = [0.5] * input_weights
        self.bias = bias

    def fire(self, ins):
        summe = 0
        for i in range(len(self.input_weights)):
            summe += self.input_weights[i] * ins[i]
        summe += self.bias
        return summe

class NeuralNet:
    def __init__(self, input_size, hidden_sizes, output_size):
        self.net = []
        self.weights = []

        self.shape = hidden_sizes + [output_size]
        self.layer_sizes = [input_size] + hidden_sizes + [output_size]

        for i in range(len(self.shape)):
            self.net.append([Neuron(self.layer_sizes[i], 0)] * self.shape[i])




    def forward(self, input_activations):
        previous_layer = input_activations
        for layer in range(len(self.shape)):
            this_layer = []
            for neur in range(self.shape[layer]):
                this_layer.append(self.net[layer][neur].fire(previous_layer))
            previous_layer = this_layer
        return this_layer



nn = NeuralNet(6, [4, 5], 2)

print(nn.forward([0.5, 0.5, 0.5, 0.5, 0.5, 0.5]))