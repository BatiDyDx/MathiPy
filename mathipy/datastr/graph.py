class Graph(object):
    pass

class Node(Graph):
    def __init__(self, node_value):
        self.node_value = node_value
        self.connections = []

    def add(self, *iterable):
        nodes = []
        new_node_values = []
        for n in iterable:
            if isinstance(n, Node):
                nodes.append(n)
            else:
                new_node_values.append(n)
    
        for node in nodes:
            self.connections.append(node)
            node.connections.append(self)
    
        new_nodes = []
        for value in new_node_values:
            new_node = Node(value)
            self.connections.append(new_node)
            new_node.connections.append(self)
            new_nodes.append(new_node)

        return new_nodes if True else None

    def get_connection(self, value):
        for connection in self.connections:
            if connection.node_value == value:
                return connection

    def get_connections(self):
        return self.connections

    def is_connected_with(self, node):
        for connection in self.connections:
            if connection.node_value == node.node_value:
                return True
        return False

    def __str__(self):
        connections = [c.node_value for c in self.connections]
        return f'Graph(Value: {self.node_value}, Connections: {connections})'

    def __repr__(self):
        return str(self)
