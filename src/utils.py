from uuid import uuid4
from typing import Callable
import random


class DirectedGraph:
    '''

    '''
    class Node:
        '''

        '''

        def __init__(self, id: str, data: dict[str, any]) -> None:
            '''

            '''
            self.id = id
            self.data = data

    def __init__(self) -> None:
        ''''''
        self._nodes = {}
        self._edges: dict[str, list[str]] = {}

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

    def add_node(self, node_id: str, data: dict[str, any]) -> None:
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
        if node_id not in self._nodes:
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

    # FIXME
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


class ArtificialIntelligence():
    def __init__(self) -> None:
        pass


def select_from_options(options: tuple) -> Callable:
    '''
    Returns selection value from the options tuple or a random value from it
    '''
    return lambda x = -1: random.choice(options) if x == -1 else options[x]
