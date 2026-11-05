"""
Queue implementation using Linked List.

A Queue is a Linear Data Structure that follows FIFO principle:
FIFO = First In, First Out

Think of it like a queue at a bank or ticket counter:
- New people join at the REAR (end)
- People are served from the FRONT (beginning)
- The first person who joined is the first one served

The Queue MUST use the custom LinkedList internally.
It does NOT use Python's built-in list.

Operations:
- enqueue(data): Add element to the rear
- dequeue(): Remove and return element from front
- peek(): View front element without removing
- is_empty(): Check if queue is empty
- display(): Show all elements

Real-world application in this project:
- Manage patients waiting for appointments
- First patient to join is first to be served2
- Patients are added at the rear, served from the front
"""

from .linked_list import LinkedList


class Queue:
    """
    Implements a Queue data structure using a custom Linked List.
    
    This Queue follows the FIFO (First In, First Out) principle.
    The first added element is removed first.
    """
    
    def __init__(self):
        """Initialize an empty Queue using a Linked List."""
        self.items = LinkedList()
    
    def enqueue(self, data):
        """
        Enqueue (add) an element to the rear of the Queue.
        
        FIFO means new elements go to the rear (tail of linked list).
        
        Args:
            data: The element to enqueue
        """
        # Insert at the end (None position) to add at rear
        self.items.insert(data, position=None)
    
    def dequeue(self):
        """
        Dequeue (remove and return) the front element from the Queue.
        
        The first added element is removed first (FIFO).
        
        Returns:
            The front element if queue is not empty, None otherwise
        """
        if self.is_empty():
            return None
        
        # Get the front element (head)
        front_data = self.items.head.data
        
        # Remove it by moving head to next node
        self.items.head = self.items.head.next
        
        return front_data
    
    def peek(self):
        """
        Peek at the front element without removing it.
        
        Returns:
            The front element if queue is not empty, None otherwise
        """
        if self.is_empty():
            return None
        
        return self.items.head.data
    
    def is_empty(self):
        """
        Check if the Queue is empty.
        
        Returns:
            True if queue is empty, False otherwise
        """
        return self.items.is_empty()
    
    def get_size(self):
        """
        Get the number of elements in the Queue.
        
        Returns:
            The count of elements in the queue
        """
        return self.items.get_size()
    
    def display(self):
        """
        Get all elements in the Queue in order (front to rear).
        
        Returns:
            A list of elements from front (first) to rear (last)
        """
        return self.items.traverse()
    
    def display_visual(self):
        """
        Get a visual representation of the Queue.
        
        Shows elements from FRONT to REAR:
        
        FRONT                                REAR
         ↓                                      ↓
        [Element 1] → [Element 2] → [Element 3]
        
        Returns:
            A string showing the queue structure
        """
        elements = self.display()
        
        if not elements:
            return "Empty Queue"
        
        visual = "FRONT"
        for elem in elements:
            visual += f" → [{str(elem)}]"
        visual += " → REAR"
        
        return visual
