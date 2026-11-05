"""
Node class for Linked List implementation.

Each Node contains:
- data: The actual record (doctor, patient, appointment, etc.)
- next: Reference to the next node in the linked list
"""


class Node:
    """
    Represents a single node in a Linked List.
    
    Each node holds a data element and a reference to the next node.
    This is a fundamental building block for Linked Lists, Stacks, and Queues.
    """
    
    def __init__(self, data):
        """
        Initialize a Node.
        
        Args:
            data: The value/record to be stored in this node
        """
        self.data = data
        self.next = None
    
    def __repr__(self):
        """String representation of the node."""
        return f"Node({self.data})"
