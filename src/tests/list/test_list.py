from unittest import TestCase, main

from src.list.list_implemented_without_list import MyList


class TestMyList(TestCase):
    def test_append_and_indexing(self):
        lst = MyList()

        lst.append(10)
        lst.append(20)
        lst.append(30)

        self.assertEqual(lst[0], 10)
        self.assertEqual(lst[1], 20)
        self.assertEqual(lst[2], 30)

        self.assertEqual(len(lst), 3)

    def test_len_updates_correctly(self):
        lst = MyList()

        self.assertEqual(len(lst), 0)

        for i in range(5):
            lst.append(i)

        self.assertEqual(len(lst), 5)

        lst.pop()

        self.assertEqual(len(lst), 4)

    def test_negative_indexing_basic(self):
        lst = MyList()

        lst.append("a")
        lst.append("b")
        lst.append("c")

        self.assertEqual(lst[-1], "c")
        self.assertEqual(lst[-2], "b")
        self.assertEqual(lst[-3], "a")

    def test_negative_indexing_equivalence_with_python_list(self):
        py = []
        lst = MyList()

        for i in range(10):
            py.append(i)
            lst.append(i)

        for k in range(1, 10):
            self.assertEqual(lst[-k], py[-k])

    def test_pop_returns_and_removes_last(self):
        lst = MyList()

        lst.append(42)
        lst.append(99)

        val = lst.pop()

        self.assertEqual(val, 99)

        self.assertEqual(len(lst), 1)

        self.assertEqual(lst[0], 42)
        self.assertEqual(lst[-1], 42)

    def test_pop_until_empty_and_raise_on_extra(self):
        lst = MyList()

        for i in range(3):
            lst.append(i)

        self.assertEqual(lst.pop(), 2)
        self.assertEqual(lst.pop(), 1)
        self.assertEqual(lst.pop(), 0)

        self.assertEqual(len(lst), 0)

        with self.assertRaises(IndexError):
            lst.pop()

    def test_index_out_of_range_positive(self):
        lst = MyList()

        lst.append(1)

        with self.assertRaises(IndexError):
            _ = lst[1]

    def test_index_out_of_range_negative(self):
        lst = MyList()

        lst.append(1)

        with self.assertRaises(IndexError):
            _ = lst[-2]

    def test_many_appends_then_pops_matches_python_list(self):
        py = []
        lst = MyList()

        for i in range(100):
            py.append(i)
            lst.append(i)

        # positives
        for i in range(100):
            self.assertEqual(lst[i], py[i])

        # negatives 
        for k in range(1, 100):
            self.assertEqual(lst[-k], py[-k])

        # compare pop()
        for _ in range(50):
            self.assertEqual(lst.pop(), py.pop())

        self.assertEqual(len(lst), len(py))
        self.assertEqual(len(lst), 50)

        # after pop()
        for i in [0, 10, 25, 49]:
            self.assertEqual(lst[i], py[i])

        self.assertEqual(lst[-1], py[-1])

    def test_types_and_mixed_values(self):
        lst = MyList()

        lst.append(1)
        lst.append("x")
        lst.append({"k": "v"})

        self.assertEqual(lst[0], 1)
        self.assertEqual(lst[1], "x")
        self.assertEqual(lst[2], {"k": "v"})
        self.assertEqual(lst[-1], {"k": "v"})

    def test_resize_behavior_optional_if_exposed(self):
        """
        This test only checks growth/shrinking if the class exposes _capacity.
        Otherwise, the test is skipped.
        """
        lst = MyList()
        if not hasattr(lst, "_capacity"):
            self.skipTest("Class does not expose '_capacity'; skipping capacity test.")

        cap0 = lst._capacity
        n = max(8, cap0 * 3)

        for i in range(n):
            lst.append(i)

        cap_grown = lst._capacity
        self.assertGreaterEqual(cap_grown, n)

        # shrink
        for _ in range(n // 2):
            lst.pop()
        cap_after = lst._capacity

        # _capacity > __size
        self.assertGreaterEqual(cap_after, len(lst))


if __name__ == "__main__":
    main()
