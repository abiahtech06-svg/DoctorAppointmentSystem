"""
LinkedList implementation - A fundamental data structure.

A Linked List is a linear data structure where:
- Elements are stored in nodes
- Each node contains data and a reference to the next node
- Nodes are connected sequentially
- The last node points to None (NULL)

Advantages:
- Dynamic size (grows/shrinks at runtime)
- Efficient insertion/deletion at known positions
- No need to pre-allocate memory

Applications in this project:
- Store Doctor records
- Store Patient records
- Store Appointment records
- Foundation for Stack and Queue implementations
"""

from .node import Node


class LinkedList:
    """
    Implements a singly Linked List data structure.
    
    A Linked List stores a collection of nodes, where each node
    contains data and a reference to the next node.
    """
    
    def __init__(self):
        """Initialize an empty Linked List."""
        self.head = None
    
    def insert(self, data, position=None):
        """
        Insert a new node into the Linked List.
        
        If position is None, insert at the end (tail).
        If position is 0, insert at the beginning (head).
        If position is a specific index, insert at that position.
        
        Args:
            data: The record/value to insert
            position: Position to insert (None=end, 0=beginning, or specific index)
        
        Returns:
            True if insertion was successful
        """
        new_node = Node(data)
        
        # Case 1: Insert at the beginning (position 0)
        if position == 0:
            new_node.next = self.head
            self.head = new_node
            return True
        
        # Case 2: Insert at end or specific position
        current = self.head
        previous = None
        index = 0
        
        # If list is empty and we're trying to insert anywhere other than 0
        if self.head is None:
            self.head = new_node
            return True
        
        # Traverse to find the insertion point
        while current is not None and (position is None or index < position):
            previous = current
            current = current.next
            index += 1
        
        # Connect the new node
        new_node.next = current
        if previous is not None:
            previous.next = new_node
        
        return True
    
    def delete(self, key):
        """
        Delete the first node with matching key from the Linked List.
        
        This method searches for a node where node.data == key
        and removes it from the list.
        
        Args:
            key: The value/record to delete (usually a doctor/patient/appointment ID)
        
        Returns:
            True if deletion was successful, False if key not found
        """
        # Case 1: Delete the head node
        if self.head is not None and self.head.data == key:
            self.head = self.head.next
            return True
        
        # Case 2: Search for the node to delete
        current = self.head
        previous = None
        
        while current is not None:
            if current.data == key:
                # Found the node - remove it by connecting previous to next
                previous.next = current.next
                return True
            
            previous = current
            current = current.next
        
        # Node not found
        return False
    
    def traverse(self):
        """
        Traverse the entire Linked List and return all elements.
        
        Returns:
            A list containing all elements in the Linked List in order
        """
        elements = []
        current = self.head
        
        while current is not None:
            elements.append(current.data)
            current = current.next
        
        return elements
    
    def search(self, key):
        """
        Search for a node with matching key in the Linked List.
        
        Args:
            key: The value/record to search for
        
        Returns:
            The node if found, None otherwise
        """
        current = self.head
        
        while current is not None:
            if current.data == key:
                return current
            current = current.next
        
        return None
    
    def is_empty(self):
        """
        Check if the Linked List is empty.
        
        Returns:
            True if the list is empty, False otherwise
        """
        return self.head is None
    
    def get_size(self):
        """
        Get the number of nodes in the Linked List.
        
        Returns:
            The count of nodes in the list
        """
        count = 0
        current = self.head
        
        while current is not None:
            count += 1
            current = current.next
        
        return count
    
    def display_as_list(self):
        """
        Get a string representation of the Linked List.
        
        Returns:
            A string showing the structure: [elem1] → [elem2] → [elem3] → NULL
        """
        elements = self.traverse()
        
        if not elements:
            return "Empty List (NULL)"
        
        # Create visual representation
        visual = " → ".join(f"[{str(elem)}]" for elem in elements)
        visual += " → NULL"
        
        return visual
