import unittest

from blvresearch.concat.analysts.reuters.normalizer import (
    normalize_line
)


class TestNormalizeReutersResearchString(unittest.TestCase):

    def test_string1(self):
        s = ("    * Sterne Agee cuts price target to $60 from $62.50; " +
             "rating buy  ")
        e = ("* Sterne Agee cuts price target to USD 60 from USD 62.50; " +
             "rating buy")
        self.assertEqual(normalize_line(s), e)

    def test_string2(self):
        s = ("    * Natixis cuts to reduce from neutral; " +
             "target price of 4.7 euros  ")
        e = ("* Natixis cuts to reduce from neutral; " +
             "target price of EUR 4.7")
        self.assertEqual(normalize_line(s), e)

    def test_string3(self):
        s = "    * SocGen cuts to hold from buy  "
        e = "* SocGen cuts to hold from buy"
        self.assertEqual(normalize_line(s), e)

    def test_string4(self):
        s = ("    * FirstEnergy Capital raises target price to C$15.75 " +
             "from C$15; rating market perform  ")
        e = ("* FirstEnergy Capital raises target price to CAD 15.75 " +
             "from CAD 15; rating market perform")
        self.assertEqual(normalize_line(s), e)

    def test_string5(self):
        s = "    * First Analysis raises to overweight rating  "
        e = "* First Analysis raises to overweight rating"
        self.assertEqual(normalize_line(s), e)

    def test_string6(self):
        s = "    * Credit Suisse raises price target to $92 from $83  "
        e = "* Credit Suisse raises price target to USD 92 from USD 83"
        self.assertEqual(normalize_line(s), e)

    def test_string7(self):
        s = "    * Baird raises to outperform  "
        e = "* Baird raises to outperform"
        self.assertEqual(normalize_line(s), e)

    def test_string8(self):
        s = ("    * S&P Capital IQ cuts to hold from strong buy; " +
             "cuts target price by $5 to $30  ")
        e = ("* S&P Capital IQ cuts to hold from strong buy; " +
             "cuts target price by USD 5 to USD 30")
        self.assertEqual(normalize_line(s), e)

    def test_string9(self):
        s = "    * JMP securities starts with market perform rating  "
        e = "* JMP securities starts with market perform rating"
        self.assertEqual(normalize_line(s), e)

    def test_string10(self):
        s = ("    * Goldman Sachs raises to buy from neutral; " +
             "raises target price to 5600p from 5400p  ")
        e = ("* Goldman Sachs raises to buy from neutral; " +
             "raises target price to GBP 5600 from GBP 5400")
        self.assertEqual(normalize_line(s), e)

    def test_string11(self):
        s = ("    * Transneft: Credit Suisse raises target price " +
             "to 46,961 roubles from 31,632.91 roubles; rating underperform  ")
        e = ("* Transneft: Credit Suisse raises target price to " +
             "RUB 46,961 from RUB 31,632.91; rating underperform")
        self.assertEqual(normalize_line(s), e)

    def test_string12(self):
        s = ("    * Octagon raises Maple Leaf Foods Inc target price " +
             "to C$14.50 from C$13.75; rating buy  ")
        e = ("* Octagon raises Maple Leaf Foods Inc target price " +
             "to CAD 14.50 from CAD 13.75; rating buy")
        self.assertEqual(normalize_line(s), e)

    def test_string13(self):
        s = ("    * Nordea Markets downgrades to sell from hold, target " +
             "price 24 euros versus previous 23.5 euros  ")
        e = ("* Nordea Markets downgrades to sell from hold, target price " +
             "EUR 24 versus previous EUR 23.5")
        self.assertEqual(normalize_line(s), e)
