"""
Expression Validator using Stack.

This module demonstrates the application of Stack data structure
for validating balanced parentheses and expressions.

Problem: Check if parentheses/brackets in an expression are balanced.

Examples:
✓ (10 + 5) * 2              → Balanced
✓ [(a + b) * {c - d}]       → Balanced
✗ (10 + 5 * 2                → Not balanced (missing closing)
✗ )10 + 5(                   → Not balanced (wrong order)

Algorithm:
1. Use a Stack to track opening brackets
2. For each character in the expression:
   - If opening bracket ( { [ → PUSH to stack
   - If closing bracket ) } ] → POP from stack and match
   - If POP fails or doesn't match → Expression is unbalanced
3. At the end, stack must be empty

Time Complexity: O(n) where n is length of expression
Space Complexity: O(m) where m is the maximum nesting depth
"""

from data_structures import Stack


class ExpressionValidator:
    """
    Validates if expressions have balanced parentheses and brackets.
    
    Uses a custom Stack data structure (which internally uses LinkedList).
    This demonstrates a real-world application of Stacks.
    """
    
    def __init__(self):
        """Initialize the validator."""
        # Mapping of closing brackets to opening brackets
        self.bracket_pairs = {
            ')': '(',
            '}': '{',
            ']': '['
        }
        
        self.opening_brackets = set('({[')
        self.closing_brackets = set(')}]')
    
    def validate_balanced_parentheses(self, expression):
        """
        Check if an expression has balanced parentheses and brackets.
        
        Supports three types of brackets: (), {}, []
        
        Args:
            expression (str): The expression to validate
        
        Returns:
            tuple: (is_balanced: bool, message: str, stack_trace: list)
                - is_balanced: True if expression is balanced
                - message: Detailed explanation
                - stack_trace: Steps taken by the stack
        """
        if not expression:
            return True, "Expression is empty", []
        
        stack = Stack()
        stack_trace = []
        
        for i, char in enumerate(expression):
            # Skip non-bracket characters
            if char not in self.opening_brackets and char not in self.closing_brackets:
                continue
            
            # If opening bracket, push to stack
            if char in self.opening_brackets:
                stack.push(char)
                stack_trace.append(f"Position {i}: '{char}' → PUSH. Stack: {stack.display()}")
            
            # If closing bracket, pop and check match
            elif char in self.closing_brackets:
                # Check if stack is empty
                if stack.is_empty():
                    stack_trace.append(f"Position {i}: '{char}' → POP FAILED (stack empty)")
                    return False, f"Unbalanced expression: Closing bracket '{char}' at position {i} has no matching opening bracket.", stack_trace
                
                # Pop top element
                top = stack.pop()
                expected_opening = self.bracket_pairs[char]
                
                # Check if it matches
                if top != expected_opening:
                    stack_trace.append(f"Position {i}: '{char}' → POP '{top}' (expected '{expected_opening}') - MISMATCH")
                    return False, f"Unbalanced expression: '{char}' at position {i} doesn't match with '{top}'.", stack_trace
                
                stack_trace.append(f"Position {i}: '{char}' → POP '{top}' (matched). Stack: {stack.display()}")
        
        # Check if stack is empty at the end
        if not stack.is_empty():
            remaining = stack.display()
            stack_trace.append(f"Final check: Stack is NOT empty. Remaining: {remaining}")
            return False, f"Unbalanced expression: {len(remaining)} unclosed bracket(s): {remaining}", stack_trace
        
        stack_trace.append("Final check: Stack is empty. Expression is BALANCED ✓")
        return True, "Expression is balanced. ✓", stack_trace
    
    def validate_simple_parentheses(self, expression):
        """
        Check if an expression has balanced parentheses only (simple version).
        
        Only checks () brackets, ignores other characters.
        
        Args:
            expression (str): The expression to validate
        
        Returns:
            tuple: (is_balanced: bool, message: str)
        """
        stack = Stack()
        
        for char in expression:
            if char == '(':
                stack.push(char)
            elif char == ')':
                if stack.is_empty():
                    return False, "Unbalanced: Closing ')' without matching '('"
                stack.pop()
        
        if not stack.is_empty():
            return False, f"Unbalanced: {stack.get_size()} unclosed '(' bracket(s)"
        
        return True, "Expression is balanced"
    
    def validate_expression_with_operators(self, expression):
        """
        Validate and evaluate a simple mathematical expression.
        
        Checks balance and can handle basic arithmetic.
        
        Args:
            expression (str): The mathematical expression to validate
        
        Returns:
            tuple: (is_valid: bool, result: float/str, message: str)
        """
        # First validate balance
        is_balanced, message, _ = self.validate_balanced_parentheses(expression)
        
        if not is_balanced:
            return False, None, message
        
        # If balanced, try to evaluate
        try:
            # Simple evaluation using Python's eval (only for demonstration)
            # In production, use a proper expression parser
            result = eval(expression)
            return True, result, f"Expression is valid. Result: {result}"
        except Exception as e:
            return False, None, f"Invalid expression: {str(e)}"
    
    def get_detailed_analysis(self, expression):
        """
        Get detailed analysis of an expression with step-by-step execution.
        
        Args:
            expression (str): The expression to analyze
        
        Returns:
            dict: Analysis results with all details
        """
        is_balanced, message, trace = self.validate_balanced_parentheses(expression)
        
        return {
            'expression': expression,
            'is_balanced': is_balanced,
            'message': message,
            'bracket_count': len([c for c in expression if c in self.opening_brackets or c in self.closing_brackets]),
            'stack_trace': trace,
            'validation_status': 'PASS ✓' if is_balanced else 'FAIL ✗'
        }
