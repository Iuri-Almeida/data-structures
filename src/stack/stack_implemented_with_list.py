class Stack:
    def __init__(self):
        self._stack = []

    def __repr__(self):
        return repr(self._stack)

    def add(self, val):
        self._stack.append(val)

    def remove(self):
        return self._stack.pop()
