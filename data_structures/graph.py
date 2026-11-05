"""
Graph representation and traversal module.

A Graph G = (V, E) consists of:
- V: A set of vertices (departments/wards in a hospital)
- E: A set of edges (hallways/connections between departments)

Two standard representations implemented:
1. Adjacency List:
   - Space efficient: O(V + E)
   - A dictionary where each vertex maps to its list of adjacent neighbors
2. Adjacency Matrix:
   - A 2D array matrix[V][V] where matrix[i][j] = 1 if an edge exists, 0 otherwise
   - Fast edge lookup: O(1)

Traversals implemented:
1. Breadth-First Search (BFS):
   - Uses Phase 1 custom Queue (FIFO)
   - Explores neighbors level-by-level (e.g. finding closest emergency route)
2. Depth-First Search (DFS):
   - Uses Phase 1 custom Stack (LIFO) or recursive backtracking
   - Explores as deep as possible along each branch before backtracking
"""

from .queue import Queue
from .stack import Stack


class Graph:
    """
    Implements an undirected/directed Graph with Adjacency List and Adjacency Matrix,
    and supports both BFS and DFS traversals.
    """
    
    def __init__(self, directed=False):
        """
        Initialize the Graph.
        
        Args:
            directed (bool): True for directed graph, False for undirected graph (default)
        """
        self.directed = directed
        self.adj_list = {}     # vertex -> list of neighbor vertices
        self.vertices = []     # ordered list of vertex names
    
    def add_vertex(self, vertex):
        """
        Add a vertex to the graph.
        
        Args:
            vertex (str): Name/Identifier of the vertex
        """
        if vertex not in self.adj_list:
            self.adj_list[vertex] = []
            self.vertices.append(vertex)
            return True
        return False
    
    def add_edge(self, u, v):
        """
        Add an edge between vertex u and vertex v.
        
        Args:
            u (str): First vertex
            v (str): Second vertex
        """
        if u not in self.adj_list:
            self.add_vertex(u)
        if v not in self.adj_list:
            self.add_vertex(v)
            
        if v not in self.adj_list[u]:
            self.adj_list[u].append(v)
            
        if not self.directed and u not in self.adj_list[v]:
            self.adj_list[v].append(u)
            
        return True
    
    def get_adjacency_list(self):
        """
        Get the Adjacency List representation.
        
        Returns:
            dict: {vertex: [neighbors]}
        """
        return self.adj_list
    
    def get_adjacency_matrix(self):
        """
        Generate the 2D Adjacency Matrix representation.
        
        Returns:
            dict: Contains 'headers' (list of vertices) and 'matrix' (2D list of 0s and 1s)
        """
        n = len(self.vertices)
        matrix = [[0] * n for _ in range(n)]
        vertex_to_index = {v: i for i, v in enumerate(self.vertices)}
        
        for u in self.vertices:
            u_idx = vertex_to_index[u]
            for v in self.adj_list.get(u, []):
                v_idx = vertex_to_index[v]
                matrix[u_idx][v_idx] = 1
                
        return {
            'headers': self.vertices,
            'matrix': matrix
        }
    
    # ================== TRAVERSALS ==================
    
    def bfs(self, start_vertex):
        """
        Breadth-First Search (BFS) using Phase 1 custom Queue.
        
        Explores vertices level-by-level starting from start_vertex.
        
        Args:
            start_vertex: Starting vertex label
            
        Returns:
            dict: Contains 'traversal_order', 'steps', and 'summary'
        """
        if start_vertex not in self.adj_list:
            return {'error': f"Vertex '{start_vertex}' not found in graph."}
        
        visited = set()
        traversal_order = []
        steps = []
        
        queue = Queue()
        queue.enqueue(start_vertex)
        visited.add(start_vertex)
        steps.append(f"Start BFS at '{start_vertex}': Enqueue '{start_vertex}' and mark as visited.")
        
        while not queue.is_empty():
            current = queue.dequeue()
            traversal_order.append(current)
            steps.append(f"Dequeue and VISIT '{current}'. Current traversal: {traversal_order}")
            
            # Inspect all unvisited neighbors
            for neighbor in self.adj_list.get(current, []):
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.enqueue(neighbor)
                    steps.append(f"  → Found unvisited neighbor '{neighbor}'. Enqueue '{neighbor}'.")
        
        return {
            'algorithm': 'BFS (Breadth-First Search)',
            'data_structure_used': 'Queue (FIFO from Phase 1)',
            'start_vertex': start_vertex,
            'traversal_order': traversal_order,
            'steps': steps,
            'summary': f"BFS traversed {len(traversal_order)} vertices level-by-level."
        }
    
    def dfs(self, start_vertex):
        """
        Depth-First Search (DFS) using Phase 1 custom Stack.
        
        Explores as deep as possible along each branch before backtracking.
        
        Args:
            start_vertex: Starting vertex label
            
        Returns:
            dict: Contains 'traversal_order', 'steps', and 'summary'
        """
        if start_vertex not in self.adj_list:
            return {'error': f"Vertex '{start_vertex}' not found in graph."}
        
        visited = set()
        traversal_order = []
        steps = []
        
        stack = Stack()
        stack.push(start_vertex)
        steps.append(f"Start DFS at '{start_vertex}': Push '{start_vertex}' onto Stack.")
        
        while not stack.is_empty():
            current = stack.pop()
            
            if current not in visited:
                visited.add(current)
                traversal_order.append(current)
                steps.append(f"Pop and VISIT '{current}'. Current traversal: {traversal_order}")
                
                # Push unvisited neighbors in reverse order so first neighbor is popped first
                neighbors = self.adj_list.get(current, [])
                for neighbor in reversed(neighbors):
                    if neighbor not in visited:
                        stack.push(neighbor)
                        steps.append(f"  → Push unvisited neighbor '{neighbor}' onto Stack.")
        
        return {
            'algorithm': 'DFS (Depth-First Search)',
            'data_structure_used': 'Stack (LIFO from Phase 1)',
            'start_vertex': start_vertex,
            'traversal_order': traversal_order,
            'steps': steps,
            'summary': f"DFS explored {len(traversal_order)} vertices by moving deep into each branch."
        }
    
    def get_graph_summary(self):
        """
        Get overview metrics of the graph.
        """
        total_edges = sum(len(neighbors) for neighbors in self.adj_list.values())
        if not self.directed:
            total_edges //= 2
            
        return {
            'num_vertices': len(self.vertices),
            'num_edges': total_edges,
            'vertices': self.vertices,
            'directed': self.directed
        }
    
    def find_shortest_path(self, start_vertex, end_vertex):
        """
        Find the shortest corridor navigation path between two departments using BFS (Queue).
        
        Args:
            start_vertex (str): Starting department (e.g. 'Reception')
            end_vertex (str): Destination department (e.g. 'Cardiology')
            
        Returns:
            dict: Contains 'path' (list of departments), 'steps_count', and 'directions'
        """
        if start_vertex not in self.adj_list:
            return {'error': f"Start vertex '{start_vertex}' not found."}
        if end_vertex not in self.adj_list:
            return {'error': f"Destination vertex '{end_vertex}' not found."}
            
        if start_vertex == end_vertex:
            return {
                'start': start_vertex,
                'destination': end_vertex,
                'path': [start_vertex],
                'steps_count': 0,
                'distance': 0,
                'directions': [f"You are already at {start_vertex}."]
            }
            
        visited = set([start_vertex])
        parent = {}
        queue = Queue()
        queue.enqueue(start_vertex)
        found = False
        
        while not queue.is_empty():
            curr = queue.dequeue()
            if curr == end_vertex:
                found = True
                break
                
            for neighbor in self.adj_list.get(curr, []):
                if neighbor not in visited:
                    visited.add(neighbor)
                    parent[neighbor] = curr
                    queue.enqueue(neighbor)
                    
        if not found:
            return {'error': f"No navigation path exists between '{start_vertex}' and '{end_vertex}'."}
            
        # Reconstruct path from destination backwards to start
        path = []
        curr = end_vertex
        while curr != start_vertex:
            path.append(curr)
            curr = parent[curr]
        path.append(start_vertex)
        path.reverse()
        
        # Build turn-by-turn patient instructions
        directions = []
        for i in range(len(path) - 1):
            directions.append(f"Step {i + 1}: From '{path[i]}', follow corridor directly to '{path[i + 1]}'")
            
        return {
            'start': start_vertex,
            'destination': end_vertex,
            'path': path,
            'steps_count': len(path) - 1,
            'distance': len(path) - 1,
            'directions': directions
        }

