import time

from unittest import TestCase, main

from src.queue.queue_implemented_with_linked_list import Queue


class TestQueueLinkedList(TestCase):
    def test_add_and_peek_returns_first_element(self):
        q = Queue()

        q.add("a")
        q.add("b")
        q.add("c")

        self.assertEqual(q.peek(), "a")

        self.assertFalse(q.is_empty())

    def test_remove_returns_in_fifo_order(self):
        q = Queue()

        elements = [1, 2, 3, 4]

        for e in elements:
            q.add(e)

        removed = [q.remove() for _ in elements]

        self.assertEqual(removed, elements)

        self.assertTrue(q.is_empty())

    def test_peek_does_not_remove(self):
        q = Queue()

        q.add("x")

        self.assertEqual(q.peek(), "x")
        self.assertEqual(q.peek(), "x")

        self.assertEqual(q.remove(), "x")

        self.assertTrue(q.is_empty())

    def test_remove_on_empty_raises(self):
        q = Queue()

        with self.assertRaises(ReferenceError):
            q.remove()

    def test_peek_on_empty_raises(self):
        q = Queue()

        with self.assertRaises(ReferenceError):
            q.peek()

    def test_is_empty_transitions(self):
        q = Queue()

        self.assertTrue(q.is_empty())

        q.add(10)
        self.assertFalse(q.is_empty())

        q.remove()
        self.assertTrue(q.is_empty())

    def test_mixed_operations_pointer_safety(self):
        q = Queue()

        q.add("a")           # [a]

        self.assertEqual(q.remove(), "a")  # []

        q.add("b")           # [b]
        q.add("c")           # [b, c]

        self.assertEqual(q.peek(), "b")
        self.assertEqual(q.remove(), "b")  # [c]

        q.add("d")           # [c, d]
        q.add("e")           # [c, d, e]

        self.assertEqual(q.remove(), "c")  # [d, e]
        self.assertEqual(q.remove(), "d")  # [e]
        self.assertEqual(q.remove(), "e")  # []

        self.assertTrue(q.is_empty())

    def test_large_sequence_fifo(self):
        q = Queue()
        n = 10_000

        for i in range(n):
            q.add(i)

        for i in range(n):
            self.assertEqual(q.remove(), i)

        self.assertTrue(q.is_empty())

    def test_head_tail_consistency_optional(self):
        """
        Runs only if the implementation exposes _head/_tail/_length.
            - When the queue is empty: _head and _tail should be None (if they exist).
            - With one element: _head and _tail should point to the same node.
            - _length (if it exists) should correctly reflect the number of operations.
        """
        q = Queue()

        has_head = hasattr(q, "_head")
        has_tail = hasattr(q, "_tail")
        has_length = hasattr(q, "_length")

        if not (has_head or has_tail or has_length):
            self.skipTest("Queue does not expose internals; skipping optional internal checks.")

        if has_head:
            self.assertIsNone(q._head)
        if has_tail:
            self.assertIsNone(q._tail)
        if has_length:
            self.assertEqual(q._length, 0)

        q.add("only")

        if has_head and has_tail:
            self.assertIs(q._head, q._tail, "With one element, head and tail should be the same node.")
        if has_length:
            self.assertEqual(q._length, 1)

        self.assertEqual(q.remove(), "only")

        if has_head:
            self.assertIsNone(q._head)
        if has_tail:
            self.assertIsNone(q._tail)
        if has_length:
            self.assertEqual(q._length, 0)

    def test_tail_updates_after_removing_last_then_adding_again(self):
        """
        Classic scenario: removing the last element should set tail to None; adding a new element afterward
        should correctly update tail to point to the new final node.
        This does not depend on internals to validate the functional behavior.
        """
        q = Queue()

        q.add(1)

        self.assertEqual(q.remove(), 1)
        self.assertTrue(q.is_empty())

        q.add(2)
        q.add(3)

        self.assertEqual(q.peek(), 2)

        self.assertEqual(q.remove(), 2)
        self.assertEqual(q.remove(), 3)

        self.assertTrue(q.is_empty())

    def test_supports_various_types(self):
        q = Queue()

        q.add(1)
        q.add("x")
        q.add({"k": "v"})

        self.assertEqual(q.remove(), 1)
        self.assertEqual(q.remove(), "x")
        self.assertEqual(q.remove(), {"k": "v"})

        self.assertTrue(q.is_empty())

    def test_no_aliasing_of_nodes_functionally(self):
        """
        Checks, functionally, that each add creates an independent logical node.
        If pointers get mixed up (a common bug), the FIFO order tends to break.
        """
        q = Queue()

        for i in range(50):
            q.add(i)
        for i in range(25):
            self.assertEqual(q.remove(), i)
        for i in range(50, 75):
            q.add(i)

        expected = list(range(25, 75))
        got = []

        while not q.is_empty():
            got.append(q.remove())

        self.assertEqual(got, expected)

    def test_empty_after_many_interleaved_ops(self):
        q = Queue()

        for i in range(1000):
            q.add(i)

            if i % 2 == 0:
                self.assertEqual(q.remove(), i - (i // 2))

        while not q.is_empty():
            _ = q.remove()

        self.assertTrue(q.is_empty())

    def test_time_reasonableness_linked_list(self):
        """
        Optional: operations should be amortized O(1) in a linked list.
        This isn't a rigorous timing benchmark, just a check to catch anything egregious.
        """
        q = Queue()
        n = 50_000
        t0 = time.time()

        for i in range(n):
            q.add(i)
        for _ in range(n):
            q.remove()

        elapsed = time.time() - t0

        self.assertLess(elapsed, 2.5, f"Queue operations took too long: {elapsed:.2f}s")


if __name__ == "__main__":
    main()
