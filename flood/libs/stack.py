class Stack:
    def __init__(self):
        """Initializes a new, empty stack."""
        self.top = None

    def push(self, data):
        """Adds a new element to the stack."""
        node = _Node(data, self.top)
        self.top = node

    def pop(self):
        """Pops the top element from the stack and returns it.
        Pre: the stack is NOT empty.
        Post: the new top is the node that was below the previous top."""
        if self.is_empty():
            raise ValueError("Empty stack")
        data = self.top.data
        self.top = self.top.next
        return data

    def peek(self):
        """Returns the element at the top of the stack.
        Pre: the stack is NOT empty."""
        if self.is_empty():
            raise ValueError("Empty stack")
        return self.top.data

    def is_empty(self):
        """Returns True if the stack is empty, otherwise False."""
        return self.top is None

class _Node:
    def __init__(self, data, next=None):
        self.data = data
        self.next = next
