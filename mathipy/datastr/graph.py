from typing import TypeVar, Generic
from abc import ABC, abstractmethod, abstractproperty

T = TypeVar('T')

class Graph(ABC):
    """Graph abstract base class"""

    @abstractmethod
    def add(self, *iterable) -> None:
        """Add elements to the graph"""
        pass

    @abstractproperty
    def connections(self):
        """Get connections of the data node"""
        pass

    @abstractmethod
    def __str__(self) -> str:
        """String representation of the graph"""
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

        return new_nodes

    def get_connection(self, value):
        for connection in self.connections:
            if connection.node_value == value:
                return connection

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
