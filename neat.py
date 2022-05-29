import random
import math

class Node:
    def __init__(self, position_type, bias):
        self.position_type = position_type #int 0=input, 1=output 2=hidden
        self.dependencies = []
        self.connected_nodes = []
        self.value = None
        self.bias = bias

        #position prevents loops and connections to itself
        self.pos = None
            

    def fire(self):
        if self.value is not None:
            return self.activation(self.value)
        else:
            self.value = sum([no.fire() for no in self.dependencies]) + self.bias
            return self.activation(self.value)

    def activation(self, x):
        # return 1/(1 + math.exp(-x))
        return max(0.2 * x, x)

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
        
    def get_str(self):
        s = str(self.position_type) + ';' + str(self.bias) + ';' + str(self.pos) + '\n'
        return s

    def load_str(self, s):
        p, b, po = s.split(';')
        self.position_type = int(p)
        self.bias = float(b)
        self.pos = float(po)
        

class Connection:
    def __init__(self, input_node, output_node, weight):
        self.input_node = input_node
        self.output_node = output_node
        self.weight = weight

    def fire(self):
        return self.input_node.fire() * self.weight
    
    def get_str(self, nodes):
        s = str(nodes.index(self.input_node)) + ';' + str(nodes.index(self.output_node)) + ';' + str(self.weight) + '\n'
        return s
    
    def load_str(self, nodes, c):
        n1, n2, w = c.split(';')
        self.input_node = nodes[int(n1)]
        self.output_node = nodes[int(n2)]
        self.weight = float(w)

class NeuralNet:
    def __init__(self, input_size, output_size):
        self.nodes = []
        self.connections = []
        self.input_size = input_size
        self.output_size = output_size

        for n in range(input_size):
            self.nodes.append(Node(0, (random.random() * 2) - 1))
        for n in range(output_size):
            self.nodes.append(Node(1, (random.random() * 2) - 1))

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

        for i in range(len(out)):
            # out[0] *= 1
            out[i] = 1/(1 + math.exp(-out[i]))

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
        new_node = Node(2, (random.random() * 2) - 1)
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

        for con in self.connections:
            if con.input_node == node1 and con.output_node == node2:
                self.connections.remove(con)
                break
        else:         
            weight = random.random()
            self.connections.append(Connection(node1, node2, weight))
            self.update_dependencies()

    
    def mutate_node(self):
        node = random.choice(self.nodes)
        
        factor = 2

        change = ((random.random() * 2) - 1) * factor


    def mutate_connections(self):
        connection = random.choice(self.connections)

        factor = 2

        change = ((random.random() * 2) - 1) * factor

        connection.weight += change


    def mutate(self):
        ran = random.random()
        if ran < 0.75:
            self.mutate_add_node()
        ran = random.random()
        if ran < 0.5:
            self.mutate_add_connections()
        ran = random.random()
        if ran < 0.5:
            self.mutate_node()
        ran = random.random()
        if ran < 0.5:
            self.mutate_connections()
    
    def save(self, filename):
        path = filename + '.txt'
        node_str = []
        conn_str = []
        for node in self.nodes:
            node_str.append(node.get_str())
        for conn in self.connections:
            conn_str.append(conn.get_str(self.nodes))

        str_list = node_str + ['-\n'] + conn_str

        with open(path, 'w+') as f:
            f.writelines(str_list)
    
    def load(self, filename):
        path = filename + '.txt'
        with open(path, 'r') as f:
            lines = f.readlines()

        data = list(map(lambda x: x.replace('\n', ''), lines))

        split_point = data.index('-')
        node_str = data[:split_point]
        conn_str = data[split_point+1:]

        self.nodes = []
        self.connections = []

        for n in node_str:
            new_node = Node(0, 0)
            new_node.load_str(n)
            self.nodes.append(new_node)

        for c in conn_str:
            new_conn = Connection(None, None, 0)
            new_conn.load_str(self.nodes, c)
            self.connections.append(new_conn)

        self.update_dependencies()
        new_node.update_position()


        



if __name__ == '__main__':
    nn = NeuralNet(6, 2)
    nn.load('moin')

    # print(nn.forward([0.5, 0.5, 0.5, 0.5, 0.5, 0.5]))