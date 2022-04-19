import random

class Node:
    def __init__(self, position_type):
        self.position_type = position_type #int 0=input, 1=output 2=hidden
        self.dependencies = []
        self.connected_nodes = []
        self.value = None

        #position prevents loops and connections to itself
        
            

    def fire(self):
        if self.value is not None:
            return self.value
        else:
            self.value = sum([no.fire() for no in self.dependencies])
            return self.value

    def update_position(self):
        if self.position_type == 0:
            self.pos = 0
        elif self.position_type == 1:
            self.pos = 1
        else:
            positions = []
            for no in self.connected_nodes:
                positions.append(no.pos)
            self.pos = sum(positions) / len(positions)
        

class Connection:
    def __init__(self, input_node, output_node, weight):
        self.input_node = input_node
        self.output_node = output_node
        self.weight = weight
    def fire(self):
        return self.input_node.fire() * self.weight

class NeuralNet:
    def __init__(self, input_size, output_size):
        self.nodes = []
        self.connections = []
        self.input_size = input_size
        self.output_size = output_size

        for n in range(input_size):
            self.nodes.append(Node(0))
        for n in range(output_size):
            self.nodes.append(Node(1))

        for inp in range(input_size):
            for out in range(input_size, input_size + output_size):
                connection = Connection(self.nodes[inp], self.nodes[out], (random.random() * 2) - 1)
                self.connections.append(connection)
        self.update_dependencies()
        self.update_positions()

    
    def forward(self, x):
        out = []
        for i in range(self.input_size):
            self.nodes[i].value = x[i]
        for i in range(self.input_size, self.input_size + self.output_size):
            no = self.nodes[i]
            if no.position_type == 1:
                out.append(no.fire())
        
        for no in self.nodes:
            no.value = None
        
        return out


    def update_dependencies(self):
        for no in self.nodes:
            no.dependencies = []
        for con in self.connections:
            begin = con.input_node
            end = con.output_node
            end.dependencies.append(con)

            begin.connected_nodes.append(end)
            end.connected_nodes.append(begin)
        


    
    def update_positions(self):
        for no in self.nodes:
            no.update_position()


    def mutate_add_node(self):
        connection = random.choice(self.connections)
        new_node = Node(2)
        self.nodes.append(new_node)

        input_node = connection.input_node
        output_node = connection.output_node
        weight = connection.weight

        self.connections.remove(connection)
        self.connections.append(Connection(input_node, new_node, 1))
        self.connections.append(Connection(new_node, output_node, weight))
        self.update_dependencies()
        new_node.update_position()



    def mutate_add_connections(self):
        dis = 0
        while dis < 1e-2:
            node1 = random.choice(self.nodes)
            node2 = random.choice(self.nodes)
            dis = node2.pos - node1.pos
        weight = random.random()
        self.connections.append(Connection(node1, node2, weight))
        self.update_dependencies()

    def mutate_connections(self):
        connection = random.choice(self.connections)

        alpha = 0.5

        change = ((random.random() * 2) - 1) * alpha

        connection.weight += change


    def mutate(self):
        ran = random.random()

        if ran < 0.1:
            self.mutate_add_node()
        elif ran < 0.3:
            self.mutate_add_connections()
        else:
            self.mutate_connections()


        



if __name__ == '__main__':
    nn = NeuralNet(6, 2)

    print(nn.forward([0.5, 0.5, 0.5, 0.5, 0.5, 0.5]))