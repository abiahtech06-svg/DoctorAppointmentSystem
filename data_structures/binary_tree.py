"""
Binary Tree implementation for structured hierarchical data storage.

A Binary Tree is a hierarchical data structure where:
- Each node has at most two children (left child and right child)
- The topmost node is called the ROOT
- Nodes with no children are called LEAF nodes

Applications in this project:
- Structured hierarchical hospital organization storage:
    Chief Medical Officer (Root)
    ├── Clinical Services (Left Subtree)
    │   ├── General Medicine
    │   └── Cardiology
    └── Surgical Services (Right Subtree)
        ├── Orthopedics
        └── Neurology

Traversals implemented:
- Inorder: Left -> Root -> Right
- Preorder: Root -> Left -> Right
- Postorder: Left -> Right -> Root
"""

from .tree_node import TreeNode
from .queue import Queue


class BinaryTree:
    """
    Implements a general Binary Tree for structured hierarchical data storage.
    """
    
    def __init__(self, root_key=None, root_data=None):
        """
        Initialize a Binary Tree.
        
        Args:
            root_key: Optional key for the root node
            root_data: Optional data payload for the root node
        """
        self.root = TreeNode(root_key, root_data) if root_key is not None else None
    
    def insert(self, key, data=None):
        """
        Insert a node using level-order (breadth-first) insertion.
        Fills the tree from top to bottom, left to right.
        
        Args:
            key: Key identifier of the new node
            data: Payload information of the new node
        """
        new_node = TreeNode(key, data)
        if self.root is None:
            self.root = new_node
            return True
        
        # Use queue for level-order traversal to find the first open spot
        q = Queue()
        q.enqueue(self.root)
        
        while not q.is_empty():
            current = q.dequeue()
            
            if current.left is None:
                current.left = new_node
                return True
            else:
                q.enqueue(current.left)
            
            if current.right is None:
                current.right = new_node
                return True
            else:
                q.enqueue(current.right)
        
        return False
    
    def find_node(self, key, current=None):
        """
        Find a node by its key.
        """
        if current is None:
            current = self.root
        if current is None:
            return None
        
        if current.key == key:
            return current
        
        left_search = self.find_node(key, current.left) if current.left else None
        if left_search:
            return left_search
            
        right_search = self.find_node(key, current.right) if current.right else None
        return right_search
    
    def insert_child(self, parent_key, child_key, child_data=None, side='left'):
        """
        Explicitly insert a child under a specific parent node.
        
        Args:
            parent_key: Key of the existing parent node
            child_key: Key of the new child node
            child_data: Payload for the child node
            side: 'left' or 'right'
        
        Returns:
            bool: True if inserted successfully, False otherwise
        """
        parent = self.find_node(parent_key)
        if not parent:
            return False
        
        new_node = TreeNode(child_key, child_data)
        if side == 'left':
            if parent.left is None:
                parent.left = new_node
                return True
            else:
                new_node.left = parent.left
                parent.left = new_node
                return True
        elif side == 'right':
            if parent.right is None:
                parent.right = new_node
                return True
            else:
                new_node.right = parent.right
                parent.right = new_node
                return True
        return False
    
    # ================== TRAVERSALS ==================
    
    def inorder_traversal(self, node=None, result=None):
        """
        Inorder Traversal: Left -> Root -> Right
        
        Returns:
            list: List of visited node keys in Inorder sequence
        """
        if result is None:
            result = []
        if node is None and self.root and len(result) == 0:
            node = self.root
        
        if node is not None:
            if node.left:
                self.inorder_traversal(node.left, result)
            result.append(node.key)
            if node.right:
                self.inorder_traversal(node.right, result)
        
        return result
    
    def preorder_traversal(self, node=None, result=None):
        """
        Preorder Traversal: Root -> Left -> Right
        
        Returns:
            list: List of visited node keys in Preorder sequence
        """
        if result is None:
            result = []
        if node is None and self.root and len(result) == 0:
            node = self.root
        
        if node is not None:
            result.append(node.key)
            if node.left:
                self.preorder_traversal(node.left, result)
            if node.right:
                self.preorder_traversal(node.right, result)
        
        return result
    
    def postorder_traversal(self, node=None, result=None):
        """
        Postorder Traversal: Left -> Right -> Root
        
        Returns:
            list: List of visited node keys in Postorder sequence
        """
        if result is None:
            result = []
        if node is None and self.root and len(result) == 0:
            node = self.root
        
        if node is not None:
            if node.left:
                self.postorder_traversal(node.left, result)
            if node.right:
                self.postorder_traversal(node.right, result)
            result.append(node.key)
        
        return result
    
    def get_detailed_traversal_trace(self, traversal_type='inorder'):
        """
        Get an educational step-by-step trace of the traversal.
        
        Args:
            traversal_type: 'inorder', 'preorder', or 'postorder'
            
        Returns:
            dict with 'sequence', 'steps', and 'description'
        """
        steps = []
        
        if traversal_type == 'inorder':
            def _trace_inorder(curr):
                if not curr:
                    return
                if curr.left:
                    steps.append(f"Proceed to division branch '{curr.key}' → '{curr.left.key}'")
                    _trace_inorder(curr.left)
                    steps.append(f"Return from branch back to '{curr.key}'")
                steps.append(f"Review Department / Unit: '{curr.key}'")
                if curr.right:
                    steps.append(f"Proceed to division branch '{curr.key}' → '{curr.right.key}'")
                    _trace_inorder(curr.right)
                    steps.append(f"Return from branch back to '{curr.key}'")
            
            _trace_inorder(self.root)
            seq = self.inorder_traversal()
            desc = "Standard Clinical Walkthrough: Inspects department units systematically in operational sequence across clinical and surgical wings."
            
        elif traversal_type == 'preorder':
            def _trace_preorder(curr):
                if not curr:
                    return
                steps.append(f"Review Leadership & Unit: '{curr.key}' (Executive level first)")
                if curr.left:
                    steps.append(f"Cascade directives down to '{curr.key}' → '{curr.left.key}'")
                    _trace_preorder(curr.left)
                if curr.right:
                    steps.append(f"Cascade directives down to '{curr.key}' → '{curr.right.key}'")
                    _trace_preorder(curr.right)
            
            _trace_preorder(self.root)
            seq = self.preorder_traversal()
            desc = "Top-Down Executive Briefing: Starts at Executive Medical Leadership and cascades downwards through Division Heads to Department Units."
            
        elif traversal_type == 'postorder':
            def _trace_postorder(curr):
                if not curr:
                    return
                if curr.left:
                    steps.append(f"Collect operational reports from '{curr.key}' → '{curr.left.key}'")
                    _trace_postorder(curr.left)
                if curr.right:
                    steps.append(f"Collect operational reports from '{curr.key}' → '{curr.right.key}'")
                    _trace_postorder(curr.right)
                steps.append(f"Compile Division Summary: '{curr.key}' (All sub-units verified)")
            
            _trace_postorder(self.root)
            seq = self.postorder_traversal()
            desc = "Bottom-Up Operational Rollup: Aggregates patient load and staffing audits from Department Units upwards to Division Heads and Executive Leadership."
        else:
            return {'error': 'Unknown traversal type'}
            
        return {
            'type': traversal_type,
            'description': desc,
            'sequence': seq,
            'steps': steps
        }
    
    def get_height(self, node=None):
        """
        Calculate height of the binary tree.
        """
        if node is None:
            if self.root is None:
                return 0
            node = self.root
        
        left_h = self.get_height(node.left) if node.left else 0
        right_h = self.get_height(node.right) if node.right else 0
        return 1 + max(left_h, right_h)
    
    def to_dict(self):
        """Convert tree to dictionary representation for UI rendering."""
        return self.root.to_dict() if self.root else None

    def get_department_division(self, dept_name):
        """
        Determine which hospital division (Clinical Services vs Surgical Services) a department belongs to.
        """
        if not self.root:
            return {
                'division': 'General Clinical Services',
                'wing': 'Central Medical Pavilion',
                'reporting_to': 'Hospital Board'
            }
            
        target = dept_name.lower()
        
        # Check left subtree (Clinical Services)
        if self.root.left:
            inorder_left = [k.lower() for k in self.inorder_traversal(self.root.left, [])]
            if any(target in k or k in target for k in inorder_left):
                return {
                    'division': self.root.left.key,
                    'wing': 'Clinical Wing - West Block (Floors 1-2)',
                    'reporting_to': self.root.key
                }
                
        # Check right subtree (Surgical Services)
        if self.root.right:
            inorder_right = [k.lower() for k in self.inorder_traversal(self.root.right, [])]
            if any(target in k or k in target for k in inorder_right):
                return {
                    'division': self.root.right.key,
                    'wing': 'Surgical Wing - East Block (Floors 2-4)',
                    'reporting_to': self.root.key
                }
                
        return {
            'division': 'Specialist Consultation Division',
            'wing': 'Outpatient Clinic Tower - Wing B',
            'reporting_to': self.root.key
        }

