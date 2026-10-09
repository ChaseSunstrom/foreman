import logging
import unittest

import price

log = logging.getLogger("shop")


class PriceTest(unittest.TestCase):
    def test_reduced(self):
        self.assertEqual(price.with_vat(100, "reduced"), 105)

    def test_vat_on_standard(self):
        log.warning("pricing the standard basket")
        self.assertEqual(price.with_vat(100), 120)

    def test_refund_of_a_refund(self):
        with self.assertRaises(ValueError):
            price.refund(5)


for i in range(80):
    def case(self, i=i):
        log.warning("catalogue item %d priced", i)
        self.assertGreater(price.with_vat(i + 1, "reduced"), i)
    setattr(PriceTest, f"test_catalogue_{i:02}", case)


if __name__ == "__main__":
    unittest.main()
