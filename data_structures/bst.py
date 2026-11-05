"""
Binary Search Tree (BST) implementation for efficient data access.

A Binary Search Tree is a binary tree with the BST property:
- For any node X:
  - All keys in left subtree of X are LESS than X.key (left < X)
  - All keys in right subtree of X are GREATER than X.key (right > X)

Advantages:
- Efficient Search, Insertion, and Deletion: O(log n) average time complexity
- Inorder traversal automatically produces keys in strictly SORTED order
- Fast key-based lookup for Doctor and Patient records

Applications in this project:
- Indexing and fast lookup of Doctor records by Doctor ID
- Instant validation and retrieval of Doctor profile in O(log n) time
- Dynamic insertion and deletion of staff records
"""

from .tree_node import TreeNode


class BinarySearchTree:
    """
    Implements a Binary Search Tree (BST) for fast structured record retrieval.
    """
    
    def __init__(self):
        """Initialize an empty Binary Search Tree."""
        self.root = None
        self.size = 0
    
    def insert(self, key, data=None):
        """
        Insert a new (key, data) pair into the BST following BST rules.
        
        Args:
            key: Comparable key (e.g. integer Doctor ID)
            data: Payload record (e.g. dict of doctor information)
            
        Returns:
            bool: True if inserted, False if key already exists (updated)
        """
        new_node = TreeNode(key, data)
        if self.root is None:
            self.root = new_node
            self.size += 1
            return True
        
        current = self.root
        while True:
            if key == current.key:
                # Update existing record data
                current.data = data
                return False
            elif key < current.key:
                if current.left is None:
                    current.left = new_node
                    self.size += 1
                    return True
                current = current.left
            else:  # key > current.key
                if current.right is None:
                    current.right = new_node
                    self.size += 1
                    return True
                current = current.right
    
    def search(self, key):
        """
        Search for a record by its key.
        
        Args:
            key: Key to search for
            
        Returns:
            tuple: (found: bool, node: TreeNode or None, search_trace: list)
                   search_trace gives step-by-step comparison narrative for demonstration.
        """
        current = self.root
        trace = []
        step = 1
        
        if current is None:
            trace.append("BST is empty. Search terminated.")
            return False, None, trace
        
        while current is not None:
            trace.append(f"Step {step}: Compare target key {key} with current node {current.key}")
            step += 1
            
            if key == current.key:
                doctor_name = current.data.get('doctor_name', str(current.key)) if isinstance(current.data, dict) else str(current.key)
                trace.append(f"MATCH FOUND: Key {key} matches node ({doctor_name})!")
                return True, current, trace
            elif key < current.key:
                trace.append(f"Decision: {key} < {current.key} → Branch to LEFT child")
                current = current.left
            else:
                trace.append(f"Decision: {key} > {current.key} → Branch to RIGHT child")
                current = current.right
        
        trace.append(f"Target key {key} not found (reached NULL).")
        return False, None, trace
    
    def min_value_node(self, node):
        """Find node with the minimum key in a given subtree."""
        current = node
        while current and current.left is not None:
            current = current.left
        return current
    
    def max_value_node(self, node):
        """Find node with the maximum key in a given subtree."""
        current = node
        while current and current.right is not None:
            current = current.right
        return current
    
    def delete(self, key):
        """
        Delete a key from the BST.
        
        Returns:
            bool: True if key was deleted, False if not found
        """
        deleted_flag = [False]
        
        def _delete_node(root, k):
            if root is None:
                return root
            
            if k < root.key:
                root.left = _delete_node(root.left, k)
            elif k > root.key:
                root.right = _delete_node(root.right, k)
            else:
                # Found node to delete
                deleted_flag[0] = True
                
                # Case 1 & 2: Node with 0 or 1 child
                if root.left is None:
                    temp = root.right
                    root = None
                    return temp
                elif root.right is None:
                    temp = root.left
                    root = None
                    return temp
                
                # Case 3: Node with 2 children
                # Get the inorder successor (smallest in the right subtree)
                temp = self.min_value_node(root.right)
                root.key = temp.key
                root.data = temp.data
                root.right = _delete_node(root.right, temp.key)
            
            return root
        
        self.root = _delete_node(self.root, key)
        if deleted_flag[0]:
            self.size -= 1
        return deleted_flag[0]
    
    def inorder_records(self, node=None, result=None):
        """
        Inorder Traversal: Left -> Root -> Right.
        For a BST, this yields all records in strictly SORTED order by key.
        
        Returns:
            list: List of dicts {'key': key, 'data': data} in ascending order
        """
        if result is None:
            result = []
        if node is None and self.root and len(result) == 0:
            node = self.root
        
        if node is not None:
            if node.left:
                self.inorder_records(node.left, result)
            result.append({'key': node.key, 'data': node.data})
            if node.right:
                self.inorder_records(node.right, result)
        
        return result
    
    def is_empty(self):
        return self.root is None
    
    def get_size(self):
        return self.size
    
    def to_dict(self):
        """Convert BST structure to nested dict for visual rendering."""
        return self.root.to_dict() if self.root else None
