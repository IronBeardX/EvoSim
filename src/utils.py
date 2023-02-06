from uuid import uuid4
from typing import Callable
import random
import numpy as np
import math
from collections import defaultdict, deque, Counter
import heapq


class DirectedGraph:
    '''

    '''
    class Node:
        '''

        '''

        def __init__(self, id, data) -> None:
            '''

            '''
            self.id = id
            self.data = data

        def __str__(self):
            return self.id

    def __init__(self) -> None:
        ''''''
        self._nodes = {}
        self._edges = {}

    def get_neighbors(self, node_id: str) -> list[str]:
        '''
        Returns a list of the with the ids of the neighbors of the node with the given id.
        '''
        # Checking if the node exists
        if node_id not in self._nodes:
            raise ValueError("Node with id {} does not exist".format(node_id))

        return self._edges[node_id]

    def get_node(self, node_id: str) -> Node:
        '''
        Returns the node with the given id. If the node does not exist, it returns None.
        '''
        return self._nodes[node_id] if node_id in self._nodes else None

    def add_node(self, node_id, data) -> None:
        '''
        Adds a node to the graph.
        '''

        # Checking if the node already is in the graph
        if node_id in self._nodes:
            raise ValueError("Node already exists in the graph")

        # Adding the node to the graph
        self._nodes[node_id] = DirectedGraph.Node(node_id, data)

        # Adding the node to the edges
        self._edges[node_id] = []

    def add_edge(self, node_id: str, neighbor_id: str) -> None:
        '''
        Adds an edge between the node with the given id and the node with the given neighbor id.
        '''
        # Checking if the nodes exist
        if node_id not in self._nodes:
            raise ValueError("Node with id {} does not exist".format(node_id))
        if neighbor_id not in self._nodes:
            raise ValueError(
                "Node with id {} does not exist".format(neighbor_id))

        # Adding the edge
        self._edges[node_id].append(neighbor_id)

    def remove_node(self, node_id: str) -> None:
        '''
        Removes the node with the given id from the graph.
        '''
        # Checking if the node exists
        if node_id not in self._nodes:
            raise ValueError("Node with id {} does not exist".format(node_id))

        # Removing every edge that points to the node
        for node in self._edges:
            if node_id in self._edges[node]:
                self._edges[node].remove(node_id)

        # Removing the nodes edges
        del self._edges[node_id]

        # Removing the node
        del self._nodes[node_id]

    def remove_edge(self, node_id: str, neighbor_id: str) -> None:
        '''
        Removes the edge between the node with the given id and the node with the given neighbor id.
        '''
        # Checking if the nodes exist
        if node_id not in self._nodes:
            raise ValueError("Node with id {} does not exist".format(node_id))
        if neighbor_id not in self._nodes:
            raise ValueError(
                "Node with id {} does not exist".format(neighbor_id))

        # Removing the edge
        self._edges[node_id].remove(neighbor_id)

    def get_node_data(self, node_id: str) -> dict[str, any]:
        '''
        Returns the data of the node with the given id.
        '''
        # Checking if the node exists
        if node_id not in self._nodes.keys():
            raise ValueError("Node with id {} does not exist".format(node_id))

        return self._nodes[node_id].data

    def set_node_data(self, node_id: str, data: dict[str, any]) -> None:
        '''
        Updates the data of the node with the given id.
        '''
        # Checking if the node exists
        if node_id not in self._nodes:
            raise ValueError("Node with id {} does not exist".format(node_id))

        self._nodes[node_id].data = data

    def get_available_nodes(self, already_selected: list) -> list:
        '''
        Returns nodes that are targeted by the nodes in the given list or aren't
        targeted by any node 
        '''
        available_nodes = list(self._nodes.keys())
        for node_id in self._nodes:
            for neighbor_id in self._edges[node_id]:
                if neighbor_id in available_nodes:
                    available_nodes.remove(neighbor_id)

        for node_id in already_selected:
            if node_id in available_nodes:
                available_nodes.remove(node_id)

        for node_id in already_selected:
            available_nodes.extend(
                [node for node in self._edges[node_id] if node not in already_selected])

        return available_nodes

    def __str__(self):
        '''
        Returns a string representation of the graph.
        it should be printed as a matrix with the nodes as rows and columns
        and the edges as 1s
        and if an edge exists from the node x to the node y then the matrix[x][y] = 1
        it should be formated in a way that it looks aligned
        also th 1's should be aligned with the columnns and rows
        '''
        # Getting the longest node id
        longest_id = 0
        for node_id in self._nodes:
            if len(node_id) > longest_id:
                longest_id = len(node_id)

        # Creating the string
        string = " " * (longest_id + 1)
        for node_id in self._nodes:
            string += node_id + " "
        string += "\n\n\n"
        for node_id in self._nodes:
            string += node_id + " " * (longest_id - len(node_id) + 1)
            for neighbor_id in self._nodes:
                if neighbor_id in self._edges[node_id]:
                    string += "1 "
                else:
                    string += "0 "
            string += "\n\n\n"
        return string


def select_from_options(options: tuple) -> Callable:
    '''
    Returns selection value from the options tuple or a random value from it
    '''
    return lambda x = -1: random.choice(options) if x == -1 else options[x]


class Layer:
    def __init__(self):
        self.input = None
        self.output = None

    # computes the output Y of a layer for a given input X
    def forward_propagation(self, input):
        raise NotImplementedError

    # computes dE/dX for a given dE/dY (and update parameters if any)
    def backward_propagation(self, output_error, learning_rate):
        raise NotImplementedError

class FCLayer(Layer):
    # input_size = number of input neurons
    # output_size = number of output neurons
    def __init__(self, input_size, output_size):
        self.weights = np.random.rand(input_size, output_size) - 0.5
        self.bias = np.random.rand(1, output_size) - 0.5

    # returns output for a given input
    def forward_propagation(self, input_data):
        self.input = input_data
        self.output = np.dot(self.input, self.weights) + self.bias
        return self.output

    # computes dE/dW, dE/dB for a given output_error=dE/dY. Returns input_error=dE/dX.
    def backward_propagation(self, output_error, learning_rate):
        input_error = np.dot(output_error, self.weights.T)
        weights_error = np.dot(self.input.T, output_error)
        # dBias = output_error

        # update parameters
        self.weights -= learning_rate * weights_error
        self.bias -= learning_rate * output_error
        return input_error

class ActivationLayer(Layer):
    def __init__(self, activation, activation_prime):
        self.activation = activation
        self.activation_prime = activation_prime

    # returns the activated input
    def forward_propagation(self, input_data):
        self.input = input_data
        self.output = self.activation(self.input)
        return self.output

    # Returns input_error=dE/dX for a given output_error=dE/dY.
    # learning_rate is not used because there is no "learnable" parameters.
    def backward_propagation(self, output_error, learning_rate):
        return self.activation_prime(self.input) * output_error

class Network:
    def __init__(self):
        self.layers = []
        self.loss = None
        self.loss_prime = None

    # add layer to network
    def add(self, layer):
        self.layers.append(layer)

    # set loss to use
    def use(self, loss, loss_prime):
        self.loss = loss
        self.loss_prime = loss_prime

    # predict output for given input
    def predict(self, input_data):
        # sample dimension first
        samples = len(input_data)
        result = []

        # run network over all samples
        for i in range(samples):
            # forward propagation
            output = input_data[i]
            for layer in self.layers:
                output = layer.forward_propagation(output)
            result.append(output)

        return result

    # train the network
    def fit(self, x_train, y_train, epochs, learning_rate):
        # sample dimension first
        samples = len(x_train)

        # training loop
        for i in range(epochs):
            err = 0
            for j in range(samples):
                # forward propagation
                output = x_train[j]
                for layer in self.layers:
                    output = layer.forward_propagation(output)

                # compute loss (for display purpose only)
                err += self.loss(y_train[j], output)

                # backward propagation
                error = self.loss_prime(y_train[j], output)
                for layer in reversed(self.layers):
                    error = layer.backward_propagation(error, learning_rate)

            # calculate average error on all samples
            err /= samples
            print('epoch %d/%d   error=%f' % (i+1, epochs, err))

def tanh(x):
    return np.tanh(x)

def tanh_prime(x):
    return 1-np.tanh(x)**2

def mse(y_true, y_pred):
    return np.mean(np.power(y_true-y_pred, 2))

def mse_prime(y_true, y_pred):
    return 2*(y_pred-y_true)/y_true.size

