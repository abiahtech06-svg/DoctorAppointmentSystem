"""
Stack implementation using Linked List.

A Stack is a Linear Data Structure that follows LIFO principle:
LIFO = Last In, First Out

Think of it like a stack of plates:
- You add (push) a plate on top
- You remove (pop) a plate from the top
- The last plate you added is the first one you remove

The Stack MUST use the custom LinkedList internally.
It does NOT use Python's built-in list.

Operations:
- push(data): Add element to the top
- pop(): Remove and return element from top
- peek(): View top element without removing
- is_empty(): Check if stack is empty
- display(): Show all elements

Real-world application in this project:
- Track appointment operations (Register, Book, Cancel)
- Most recent operation is at the top
- Expression/Parentheses validation
"""
  
from .linked_list import LinkedList


class Stack:
    """
    Implements a Stack data structure using a custom Linked List.
    
    This Stack follows the LIFO (Last In, First Out) principle.
    The most recently added element is removed first.
    """
    
    def __init__(self):
        """Initialize an empty Stack using a Linked List."""
        self.items = LinkedList()
    
    def push(self, data):
        """
        Push (add) an element to the top of the Stack.
        
        LIFO means new elements go to the top (head of linked list).
        
        Args:
            data: The element to push onto the stack
        """
        # Insert at position 0 (head) to maintain LIFO property
        self.items.insert(data, position=0)
    
    def pop(self):
        """
        Pop (remove and return) the top element from the Stack.
        
        The most recently added element is removed.
        
        Returns:
            The top element if stack is not empty, None otherwise
        """
        if self.is_empty():
            return None
        
        # Get the top element (head)
        top_data = self.items.head.data
        
        # Remove it by moving head to next node
        self.items.head = self.items.head.next
        
        return top_data
    
    def peek(self):
        """
        Peek at the top element without removing it.
        
        Returns:
            The top element if stack is not empty, None otherwise
        """
        if self.is_empty():
            return None
        
        return self.items.head.data
    
    def is_empty(self):
        """
        Check if the Stack is empty.
        
        Returns:
            True if stack is empty, False otherwise
        """
        return self.items.is_empty()
    
    def get_size(self):
        """
        Get the number of elements in the Stack.
        
        Returns:
            The count of elements in the stack
        """
        return self.items.get_size()
    
    def display(self):
        """
        Get all elements in the Stack in order (top to bottom).
        
        Returns:
            A list of elements from top (first) to bottom (last)
        """
        return self.items.traverse()
    
    def display_visual(self):
        """
        Get a visual representation of the Stack.
        
        Shows elements from TOP to BOTTOM:
        
        TOP
         ↓
        [Element 1]
        [Element 2]
        [Element 3]
        
        Returns:
            A string showing the stack structure
        """
        elements = self.display()
        
        if not elements:
            return "Empty Stack"
        
        visual = "TOP\n ↓\n"
        for elem in elements:
            visual += f"[{str(elem)}]\n"
        
        return visual
