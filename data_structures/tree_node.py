"""
TreeNode class for Binary Tree and Binary Search Tree implementations.

Each TreeNode contains:
- key: The searchable identifier (e.g. Doctor ID, Department Name)
- data: The detailed record or description associated with the key
- left: Reference to the left child TreeNode
- right: Reference to the right child TreeNode
"""


class TreeNode:
    """
    Represents a single node in a hierarchical Tree structure.
    
    Used in both general Binary Trees and Binary Search Trees (BST).
    """
    
    def __init__(self, key, data=None):
        """
        Initialize a TreeNode.
        
        Args:
            key: Unique key/label used for ordering or identification
            data: Optional payload/dictionary record attached to this node
        """
        self.key = key
        self.data = data if data is not None else {}
        self.left = None
        self.right = None
    
    def to_dict(self):
        """
        Convert node and its subtree to a dictionary for visual rendering.
        """
        return {
            'key': self.key,
            'data': self.data,
            'left': self.left.to_dict() if self.left else None,
            'right': self.right.to_dict() if self.right else None
        }
    
    def __repr__(self):
        return f"TreeNode({self.key})"
