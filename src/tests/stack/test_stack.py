from unittest import TestCase, main

from src.stack.stack_implemented_with_list import Stack


class TestStack(TestCase):
    def test_add_and_remove_lifo_order(self):
        s = Stack()

        s.add(1)
        s.add(2)
        s.add(3)

        self.assertEqual(s.remove(), 3)
        self.assertEqual(s.remove(), 2)
        self.assertEqual(s.remove(), 1)

    def test_repr_returns_list_string(self):
        s = Stack()

        s.add("a")
        s.add("b")

        self.assertEqual(repr(s), "['a', 'b']")

    def test_remove_on_empty_stack_raises(self):
        s = Stack()

        with self.assertRaises(IndexError):
            s.remove()

    def test_mixed_operations(self):
        s = Stack()

        s.add("x")
        s.add("y")

        self.assertEqual(s.remove(), "y")

        s.add("z")

        self.assertEqual(s.remove(), "z")
        self.assertEqual(s.remove(), "x")

    def test_supports_various_types(self):
        s = Stack()

        s.add(1)
        s.add("hello")
        s.add({"k": "v"})

        self.assertEqual(s.remove(), {"k": "v"})
        self.assertEqual(s.remove(), "hello")
        self.assertEqual(s.remove(), 1)

    def test_large_number_of_elements(self):
        s = Stack()
        n = 5000

        for i in range(n):
            s.add(i)
        for i in reversed(range(n)):
            self.assertEqual(s.remove(), i)

        with self.assertRaises(IndexError):
            s.remove()


if __name__ == "__main__":
    main()
