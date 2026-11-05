# Data Structures Package
# Contains custom implementations of fundamental data structures
# used in Phase 1 & Phase 2 of the Doctor Appointment System

from .node import Node
from .linked_list import LinkedList
from .stack import Stack
from .queue import Queue
from .tree_node import TreeNode
from .binary_tree import BinaryTree
from .bst import BinarySearchTree
from .graph import Graph

__all__ = [
    'Node', 'LinkedList', 'Stack', 'Queue',
    'TreeNode', 'BinaryTree', 'BinarySearchTree', 'Graph'
]

