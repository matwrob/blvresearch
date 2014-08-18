import unittest


from blvresearch.concat.analysts.reuters.researchline import (
    ResearchLine, is_research_line, Price
)


class TestIsResearchLine(unittest.TestCase):

    def test1(self):
        l = "* American Electric Power <AEP.N>: BMO raises to outperform "
        self.assertTrue(is_research_line(l))

    def test2(self):
        l = ("For a summary of rating and price target changes on U.S. " +
             "companies:")
        self.assertFalse(is_research_line(l))

    def test3(self):
        l = "* KBW raises to outperform from market perform"
        self.assertTrue(is_research_line(l))

    def test4(self):
        l = ("HIKMA PHARMACEUTICALS PLC <HIK.L>: UBS RAISES TO BUY FROM " +
             "NEUTRAL; RAISES PRICE TARGET TO GBP 1350 FROM GBP 1050")
        self.assertFalse(is_research_line(l))

    def test5(self):
        l = ("    * Hikma Pharmaceuticals Plc <HIK.L>: UBS raises to buy " +
             "from neutral; raises price target to GBP 1350 from GBP 1050")
        self.assertTrue(is_research_line(l))

    def test6(self):
        l = ("CASINO <CASP.PA>: RAYMOND JAMES CUTS TO MARKET PERFORM " +
             "FROM OUTPERFORM")
        self.assertFalse(is_research_line(l))

    def test7(self):
        l = ("    * Casino <CASP.PA>: Raymond James cuts to market perform " +
             "from outperform")
        self.assertTrue(is_research_line(l))

    def test8(self):
        l = "INTERSIL CORP <ISIL.O>: EVERCORE PARTNERS CUTS TO UNDERWEIGHT"
        self.assertFalse(is_research_line(l))

    def test9(self):
        l = ("    * Intersil Corp <ISIL.O>: Evercore Partners cuts " +
             "to underweight")
        self.assertTrue(is_research_line(l))


class TestPrice(unittest.TestCase):

    def test_price_equality(self):
        p1 = Price("a", 1.0)
        p2 = Price("a", 1.0)
        self.assertEqual(p1, p2)

        p1 = Price("a", 1.0)
        p2 = Price("a", 2.0)
        self.assertNotEqual(p1, p2)

        p1 = Price("a", 1.0)
        p2 = Price("b", 1.0)
        self.assertNotEqual(p1, p2)

        p1 = Price("a", 1.0)
        p2 = Price("b", 2.0)
        self.assertNotEqual(p1, p2)


class TestResearchLine(unittest.TestCase):

    def test_lines_equality(self):
        l1, l2 = ResearchLine(''), ResearchLine('')
        l1.analyzed_entity = 'a'
        l2.analyzed_entity = 'a'
        l1.analysts_house = 'b'
        l2.analysts_house = 'b'
        l1.new_price_target = Price('c', 1.0)
        l2.new_price_target = Price('c', 1.0)
        l1.old_price_target = Price('c', 2.0)
        l2.old_price_target = Price('c', 2.0)
        self.assertEqual(l1, l2)

        list_of_lines = [l1]
        self.assertTrue(l2 in list_of_lines)

    def test_lines_inequality(self):
        l1, l2 = ResearchLine(''), ResearchLine('')
        l1.analyzed_entity = 'a1'
        l2.analyzed_entity = 'a2'
        l1.analysts_house = 'b'
        l2.analysts_house = 'b'
        l1.new_price_target = Price('c', 1.0)
        l2.new_price_target = Price('c', 1.0)
        l1.old_price_target = Price('c', 2.0)
        l2.old_price_target = Price('c', 2.0)
        self.assertNotEqual(l1, l2)

        list_of_lines = [l1]
        self.assertFalse(l2 in list_of_lines)

    def test_string1(self):
        string = ("* Sterne Agee cuts price target to $60 from $62.50; " +
                  "rating buy  ")
        res = ResearchLine(string)
        res.find_info()
        self.assertEqual(res.analyzed_entity, None)
        self.assertEqual(res.analysts_house, "Sterne Agee")
        self.assertEqual(res.new_price_target.currency, "USD")
        self.assertEqual(res.new_price_target.nominal, 60.0)
        self.assertEqual(res.old_price_target.currency, "USD")
        self.assertEqual(res.old_price_target.nominal, 62.50)

    def test_string2(self):
        string = ("* Natixis cuts to reduce from neutral; " +
                  "target price of 4.7 euros  ")
        res = ResearchLine(string)
        res.find_info()
        self.assertEqual(res.analyzed_entity, None)
        self.assertEqual(res.analysts_house, "Natixis")
        self.assertEqual(res.new_price_target.currency, "EUR")
        self.assertEqual(res.new_price_target.nominal, 4.7)
        self.assertEqual(res.old_price_target.currency, None)
        self.assertEqual(res.old_price_target.nominal, None)

    def test_string3(self):
        string = "* SocGen cuts to hold from buy  "
        res = ResearchLine(string)
        res.find_info()
        self.assertEqual(res.analyzed_entity, None)
        self.assertEqual(res.analysts_house, "SocGen")
        self.assertEqual(res.new_price_target.currency, None)
        self.assertEqual(res.new_price_target.nominal, None)
        self.assertEqual(res.old_price_target.currency, None)
        self.assertEqual(res.old_price_target.nominal, None)

    def test_string4(self):
        string = ("* FirstEnergy Capital raises target price to C$15.75 " +
                  "from C$15; rating market perform  ")
        res = ResearchLine(string)
        res.find_info()
        self.assertEqual(res.analyzed_entity, None)
        self.assertEqual(res.analysts_house, "FirstEnergy Capital")
        self.assertEqual(res.new_price_target.currency, "CAD")
        self.assertEqual(res.new_price_target.nominal, 15.75)
        self.assertEqual(res.old_price_target.currency, "CAD")
        self.assertEqual(res.old_price_target.nominal, 15.0)

    def test_string5(self):
        string = "* First Analysis raises to overweight rating  "
        res = ResearchLine(string)
        res.find_info()
        self.assertEqual(res.analyzed_entity, None)
        self.assertEqual(res.analysts_house, "First Analysis")
        self.assertEqual(res.new_price_target.currency, None)
        self.assertEqual(res.new_price_target.nominal, None)
        self.assertEqual(res.old_price_target.currency, None)
        self.assertEqual(res.old_price_target.nominal, None)

    def test_string6(self):
        string = "* Credit Suisse raises price target to $92 from $83  "
        res = ResearchLine(string)
        res.find_info()
        self.assertEqual(res.analyzed_entity, None)
        self.assertEqual(res.analysts_house, "Credit Suisse")
        self.assertEqual(res.new_price_target.currency, "USD")
        self.assertEqual(res.new_price_target.nominal, 92.0)
        self.assertEqual(res.old_price_target.currency, "USD")
        self.assertEqual(res.old_price_target.nominal, 83.0)

    def test_string7(self):
        string = "* Baird raises to outperform  "
        res = ResearchLine(string)
        res.find_info()
        self.assertEqual(res.analyzed_entity, None)
        self.assertEqual(res.analysts_house, "Baird")
        self.assertEqual(res.new_price_target.currency, None)
        self.assertEqual(res.new_price_target.nominal, None)
        self.assertEqual(res.old_price_target.currency, None)
        self.assertEqual(res.old_price_target.nominal, None)

    def test_string8(self):
        string = ("* S&P Capital IQ cuts to hold from strong buy; " +
                  "cuts target price by $5 to $30  ")
        res = ResearchLine(string)
        res.find_info()
        self.assertEqual(res.analyzed_entity, None)
        self.assertEqual(res.analysts_house, "S&P Capital IQ")
        self.assertEqual(res.new_price_target.currency, "USD")
        self.assertEqual(res.new_price_target.nominal, 30.0)
        self.assertEqual(res.old_price_target.currency, None)
        self.assertEqual(res.old_price_target.nominal, None)

    def test_string9(self):
        string = "* JMP securities starts with market perform rating  "
        res = ResearchLine(string)
        res.find_info()
        self.assertEqual(res.analyzed_entity, None)
        self.assertEqual(res.analysts_house, "JMP securities")
        self.assertEqual(res.new_price_target.currency, None)
        self.assertEqual(res.new_price_target.nominal, None)
        self.assertEqual(res.old_price_target.currency, None)
        self.assertEqual(res.old_price_target.nominal, None)

    def test_string10(self):
        string = ("* Goldman Sachs raises to buy from neutral; " +
                  "raises target price to 5600p from 5400p  ")
        res = ResearchLine(string)
        res.find_info()
        self.assertEqual(res.analyzed_entity, None)
        self.assertEqual(res.analysts_house, "Goldman Sachs")
        self.assertEqual(res.new_price_target.currency, "GBP")
        self.assertEqual(res.new_price_target.nominal, 5600.0)
        self.assertEqual(res.old_price_target.currency, "GBP")
        self.assertEqual(res.old_price_target.nominal, 5400.0)

    def test_string11(self):
        string = ("* Transneft <TRNF_p.RTS>: Credit Suisse raises target " +
                  "price to 46,961 roubles from 31,632.91 roubles; " +
                  "rating underperform  ")
        res = ResearchLine(string)
        res.find_info()
        self.assertEqual(res.analyzed_entity, '05HZ97-E')
        self.assertEqual(res.analysts_house, "Credit Suisse")
        self.assertEqual(res.new_price_target.currency, "RUB")
        self.assertEqual(res.new_price_target.nominal, 46961.0)
        self.assertEqual(res.old_price_target.currency, "RUB")
        self.assertEqual(res.old_price_target.nominal, 31632.91)

    def test_string12(self):
        string = ("* Octagon raises Maple Leaf Foods Inc target price " +
                  "to C$14.50 from C$13.75; rating buy  ")
        res = ResearchLine(string)
        res.find_info()
        self.assertEqual(res.analyzed_entity, None)
        self.assertEqual(res.analysts_house, "Octagon")
        self.assertEqual(res.new_price_target.currency, "CAD")
        self.assertEqual(res.new_price_target.nominal, 14.50)
        self.assertEqual(res.old_price_target.currency, "CAD")
        self.assertEqual(res.old_price_target.nominal, 13.75)

    def test_string13(self):
        string = ("* Nordea Markets downgrades to sell from hold, " +
                  "target price 24 euros versus previous 23.5 euros  ")
        res = ResearchLine(string)
        res.find_info()
        self.assertEqual(res.analyzed_entity, None)
        self.assertEqual(res.analysts_house, "Nordea Markets")
        self.assertEqual(res.new_price_target.currency, "EUR")
        self.assertEqual(res.new_price_target.nominal, 24.0)
        self.assertEqual(res.old_price_target.currency, "EUR")
        self.assertEqual(res.old_price_target.nominal, 23.5)

    def test_string14(self):
        string = ("* Barclays reinstates with overweight rating; " +
                  "target EUR 72  ")
        res = ResearchLine(string)
        res.find_info()
        self.assertEqual(res.analyzed_entity, None)
        self.assertEqual(res.analysts_house, "Barclays")
        self.assertEqual(res.new_price_target.currency, "EUR")
        self.assertEqual(res.new_price_target.nominal, 72.0)
        self.assertEqual(res.old_price_target.currency, None)
        self.assertEqual(res.old_price_target.nominal, None)

    def test_string15(self):
        string = ("* TD Securities cuts target price to CAD 73 from CAD 76: " +
                  "rating action list buy  ")
        res = ResearchLine(string)
        res.find_info()
        self.assertEqual(res.analyzed_entity, None)
        self.assertEqual(res.analysts_house, "TD Securities")
        self.assertEqual(res.new_price_target.currency, "CAD")
        self.assertEqual(res.new_price_target.nominal, 73.0)
        self.assertEqual(res.old_price_target.currency, "CAD")
        self.assertEqual(res.old_price_target.nominal, 76.0)

    def test_string16(self):
        string = ("* Apple <AAPL.O>: Wells Fargo cuts to market perform " +
                  "from outperform ")
        res = ResearchLine(string)
        res.find_info()
        self.assertEqual(res.analyzed_entity, '000C7F-E')
        self.assertEqual(res.analysts_house, "Wells Fargo")
        self.assertEqual(res.new_price_target.currency, None)
        self.assertEqual(res.new_price_target.nominal, None)
        self.assertEqual(res.old_price_target.currency, None)
        self.assertEqual(res.old_price_target.nominal, None)

    def test_string17(self):
        string = "* American Electric Power <AEP.N>: BMO raises to outperform "
        res = ResearchLine(string)
        res.find_info()
        self.assertEqual(res.analyzed_entity, '000BY1-E')
        self.assertEqual(res.analysts_house, "BMO")
        self.assertEqual(res.new_price_target.currency, None)
        self.assertEqual(res.new_price_target.nominal, None)
        self.assertEqual(res.old_price_target.currency, None)
        self.assertEqual(res.old_price_target.nominal, None)

    def test_string18(self):
        string = ("* Astoria Financial <AF.N>: KBW raises to outperform " +
                  "from market perform")
        res = ResearchLine(string)
        res.find_info()
        self.assertEqual(res.analyzed_entity, '000CCH-E')
        self.assertEqual(res.analysts_house, "KBW")
        self.assertEqual(res.new_price_target.currency, None)
        self.assertEqual(res.new_price_target.nominal, None)
        self.assertEqual(res.old_price_target.currency, None)
        self.assertEqual(res.old_price_target.nominal, None)

    def test_string19(self):
        string = ("* Bank of America <BAC.N>: Raymond James raises target " +
                  "to USD 17 from USD 16; rating outperform")
        res = ResearchLine(string)
        res.find_info()
        self.assertEqual(res.analyzed_entity, '000R3K-E')
        self.assertEqual(res.analysts_house, "Raymond James")
        self.assertEqual(res.new_price_target.currency, 'USD')
        self.assertEqual(res.new_price_target.nominal, 17)
        self.assertEqual(res.old_price_target.currency, 'USD')
        self.assertEqual(res.old_price_target.nominal, 16)

    def test_string20(self):
        string = ("* Rockwell Collins <COL.N>: Jefferies raises price " +
                  "target to USD 77 from USD 68; rating buy")
        res = ResearchLine(string)
        res.find_info()
        self.assertEqual(res.analyzed_entity, '00375R-E')
        self.assertEqual(res.analysts_house, "Jefferies")
        self.assertEqual(res.new_price_target.currency, 'USD')
        self.assertEqual(res.new_price_target.nominal, 77)
        self.assertEqual(res.old_price_target.currency, 'USD')
        self.assertEqual(res.old_price_target.nominal, 68)

    def test_string21(self):
        string = ("    * T. Rowe Price <TROW.O>: Citigroup cuts to neutral " +
                  "from buy - Theflyonthewall.com* Tableau Software <DATA.N>" +
                  ": JMP Securities raises target to USD 80; market "+
                  "outperform ")
        res = ResearchLine(string)
        res.find_info()
        self.assertEqual(res.analyzed_entity, '002XXL-E')
        self.assertEqual(res.analysts_house, "Citigroup")
        self.assertEqual(res.new_price_target.currency, None)
        self.assertEqual(res.new_price_target.nominal, None)
        self.assertEqual(res.old_price_target.currency, None)
        self.assertEqual(res.old_price_target.nominal, None)
