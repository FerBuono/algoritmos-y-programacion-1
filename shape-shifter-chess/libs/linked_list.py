class LinkedList:
    def __init__(self):
        self.first = None
        self.count = 0

    def append(self, data):
        new_node = _Node(data)
        if not self.first:
            self.first = new_node
        else:
            current = self.first
            while current.next:
                current = current.next
            current.next = new_node
        self.count += 1

    def remove_all(self, elem):
        count = 0
        previous = None
        current = self.first
        while current:
            if current.data == elem:
                if previous:
                    previous.next = current.next
                    count += 1
                    self.count -= 1
                else:
                    self.first = current.next
                    count += 1
                    self.count -= 1
            else:
                previous = current
            current = current.next
        return count

    def __len__(self):
        return self.count

    def __str__(self):
        result = '['
        current = self.first
        while current:
            result += f'{current.data}'
            if current.next:
                result += ', '
            current = current.next
        return result + ']'


class _Node:
    def __init__(self, data, next=None):
        self.data = data
        self.next = next
