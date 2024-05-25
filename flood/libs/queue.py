class Queue:
    """Represents a queue with enqueue and dequeue operations.
    The first enqueued item is also the first to be dequeued."""

    def __init__(self):
        """Creates an empty queue"""
        self.front = None
        self.back = None

    def enqueue(self, data):
        """Adds the element `data` to the end of the queue."""
        node = _Node(data)
        if self.is_empty():
            self.front = node
        else:
            self.back.next = node
        self.back = node

    def dequeue(self):
        """Dequeues the first element and returns its value.
        Pre: the queue is NOT empty.
        Post: the new front is the node that was next to the previous front."""
        if self.is_empty():
            raise ValueError("Empty queue")
        data = self.front.data
        self.front = self.front.next
        if self.front is None:
            self.back = None
        return data

    def peek(self):
        """Returns the element at the front of the queue.
        Pre: the queue is NOT empty."""
        if self.is_empty():
            raise ValueError("Empty queue")
        return self.front.data

    def is_empty(self):
        """Returns True if the queue is empty, otherwise False."""
        return self.front is None

class _Node:
    def __init__(self, data, next=None):
        self.data = data
        self.next = next
