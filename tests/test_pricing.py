import unittest

from pricing import apply_discount


class TestApplyDiscount(unittest.TestCase):
    def test_whole_number_discount(self):
        self.assertEqual(apply_discount(1000, 10), 900)

    def test_zero_discount(self):
        self.assertEqual(apply_discount(999, 0), 999)

    def test_fractional_discount_rounds_half_up(self):
        # 999 * 15% = 149.85 -> 折扣四舍五入为 150 -> 应付 849
        self.assertEqual(apply_discount(999, 15), 849)

    def test_exactly_half_rounds_up(self):
        # 50 * 5% = 2.5 -> 折扣进位为 3 -> 应付 47
        self.assertEqual(apply_discount(50, 5), 47)


if __name__ == "__main__":
    unittest.main()
