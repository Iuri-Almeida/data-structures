class Node:
    def __init__(self, val, next=None):
        self.val = val
        self.next = next

    def __repr__(self):
        return self.val


class Queue:
    def __init__(self):
        self._head: Node | None = None
        self._tail: Node | None = None

        self._length: int = 0

    def __repr__(self):
        curr_node = self._head
        nodes = []

        while curr_node:
            nodes.append(str(curr_node))
            curr_node = curr_node.next

        nodes.append("None")

        return " -> ".join(nodes)

    def peek(self):
        if not self._head:
            raise ReferenceError(f"You must add some value to the Queue")

        return self._head.val

    def add(self, new_val):
        new_node = Node(new_val)

        if not self._head:
            self._head = new_node
        else:
            self._tail.next = new_node

        self._tail = new_node
        self._length += 1

    def remove(self):
        if not self._head:
            raise ReferenceError(f"You must add some value to the Queue")

        if self._head == self._tail:
            self._tail = None

        removed_node = self._head

        self._head = self._head.next
        self._length -= 1

        return removed_node.val

    def is_empty(self):
        return self._length == 0
