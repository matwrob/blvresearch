import pandas as pd
import datetime
import unittest

from blvresearch.concat.analysts.reuters.main import (
    get_analysts_recommendations_from_news_items,
    _get_research_lines, _determine_proper_date

)
from blvresearch.concat.analysts.reuters.researchline import (
    Price, ResearchLine
)


MOCK_NEWS1 = {'story_time': datetime.datetime(2014, 3, 7, 14, 34, 8),
              'language': 'en',
              'rics': ['PLCE.O'],
              'body': ("March 7 (Reuters) - Children's Place Retail " +
                       "Stores Inc <PLCE.O>:\n * Oppenheimer cuts target " +
                       "price to $60 from $65\nFor a summary of rating and " +
                       "price target changes on U.S. companies:\n  Reuters " +
                       "Eikon users, click on [RCH/US]\n  Reuters 3000Xtra " +
                       "users, double-click [RCH/US]\n  Thomson ONE users, " +
                       "type in RT/RCH/US \n  \t\t\n  For a summary of " +
                       "rating and price target changes on Canadian " +
                       "companies:\n  Reuters Eikon users, click on " +
                       "[RCH/CA]\n  Reuters 3000Xtra users, double-click " +
                       "[RCH/CA]\n  Thomson ONE users, type in " +
                       "RT/RCH/CA\n\n((nyc.equities.newsroom@reuters.com); " +
                       "(Reuters Messaging:\nsaqib.ahmed.thomsonreuters.com" +
                       "@reuters.net) ((Bangalore Newsroom +91 80 6749\n1130" +
                       "; within U.S. +1 646 223 8780))")}

MOCK_NEWS2 = {'body': 'LONDON, May 9 (Reuters) - British interdealer...',
              'rics': ['PLCE.O'],
              'story_time': datetime.datetime(2014, 5, 9, 6, 16, 18),
              'language': 'en'}

MOCK_NEWS3 = {'story_time': datetime.datetime(2014, 3, 7, 15, 40, 34, 5000),
              'language': 'en',
              'rics': ['A.N', 'AEO.N', 'AET.N', 'AGN.N', 'ANR.N', 'ARTC.O',
                       'BBNK.O', 'BKE.N', 'BWS.N', 'CCRN.O', 'CHTR.O', 'CI.N',
                       'CIEN.N', 'CNAT.O', 'COG.N', 'COO.N', 'COST.O',
                       'CPA.N', 'CPHD.O', 'CSOD.O', 'CST.N', 'CTCM.O',
                       'CTRX.O', 'CTSH.O', 'CVD.N', 'CYS.N', 'DEI.N', 'DRC.N',
                       'DSGX.O', 'EBS.N', 'EMC.N', 'EXR.N', 'FCH.N', 'FNSR.O',
                       'FSS.N', 'KCNQ.N', 'MTGE.O', 'PLCE.O', 'RDEN.O',
                       'VNET.O'],
              'body': ("March 7 (Reuters) - Wall Street securities analysts " +
                       "revised their ratings and price targets\non several " +
                       "U.S.-listed companies, including Cepheid, Humana " +
                       "Inc, Safeway and Thomson Reuters\nCorp, on Friday. " +
                       "\n    \n    HIGHLIGHTS\n    * Alpha Natural " +
                       "Resources <ANR.N>: Goldman Sachs cuts to sell from " +
                       "neutral\n    * Cross Country Healthcare <CCRN.O>: " +
                       "Citigroup raises to buy from neutral\n    * Humana " +
                       "Inc <HUM.N>: Jefferies cuts to hold [ID:nWNAB04D49]" +
                       "\n    * Houghton Mifflin Harcourt <HMHC.O>: Goldman " +
                       "Sachs cuts to neutral; Stifel cuts to hold \n    " +
                       "* Teva Pharmaceutical <TEVA.N>: Barclays raises to " +
                       "overweight from equal weight\n            " +
                       "\nFollowing is a summary of research actions on U.S." +
                       " companies reported by Reuters on Friday.\nStock" +
                       " entries are in alphabetical order. See bottom of" +
                       " the table for sector changes. \n    \n    * " +
                       "21Vianet Group Inc <VNET.O>: Canaccord Genuity " +
                       "raises target to $31 from $23; rating buy\n    * " +
                       "ACADIA Pharmaceuticals <ACAD.O>: Piper Jaffray " +
                       "raises target to $42 from $28; overweight \n    * " +
                       "Aetna Inc <AET.N>: Jefferies raises price target " +
                       "to $87; rating buy\n    * Agilent Technologies " +
                       "<A.N>: JP Morgan raises target to $65 from $60; " +
                       "rating overweight\n    * Agilent Technologies " +
                       "<A.N>: Jefferies raises price target to $67 from " +
                       "$66; rating buy\n    * Agios Pharmaceuticals " +
                       "<AGIO.O>: Leerink raises target price to $51 from " +
                       "$38; outperform\n    * Allergan Inc <AGN.N>: " +
                       "Barclays raises target price to $130 from $95; " +
                       "rating equal weight \n    * Alpha Natural Resources " +
                       "<ANR.N>: Goldman Sachs cuts to sell from neutral\n" +
                       "    * Sirius XM Holdings <SIRI.O>:Macquarie ups to" +
                       " outperform from neutral- Theflyonthewall.com\n    " +
                       "* Skullcandy <SKUL.O>:Northland ups to outperform " +
                       "from market perform - Theflyonthewall.com\n    " +
                       "* Skullcandy <SKUL.O>: D. A. Davidson raises to " +
                       "neutral from underperform rating\n    * Skullcandy " +
                       "<SKUL.O>: Roth captial raises target price to $10 " +
                       "from $9; rating buy\n    * SNC-Lavalin Group " +
                       "<SNC.TO>:RBC cuts target price to C$49 from C$50; " +
                       "rating sector perform")}

MOCK_NEWS_LIST = [MOCK_NEWS1, MOCK_NEWS2, MOCK_NEWS3]


class TestGetResearchLines(unittest.TestCase):

    def test_get_mock_news1(self):
        res = _get_research_lines(MOCK_NEWS1)

        self.assertEqual(len(res), 1)
        self.assertIsInstance(res, list)

        self.assertIsInstance(res[0], ResearchLine)
        self.assertIsInstance(res[0].new_price_target, Price)
        self.assertIsInstance(res[0].old_price_target, Price)
        self.assertEqual(res[0].analyzed_entity, "001QX0-E")
        self.assertEqual(res[0].analysts_house, "Oppenheimer")
        self.assertEqual(res[0].new_price_target.currency, "USD")
        self.assertEqual(res[0].new_price_target.nominal, 60.0)
        self.assertEqual(res[0].old_price_target.currency, "USD")
        self.assertEqual(res[0].old_price_target.nominal, 65.0)

    def test_get_mock_news3(self):
        res = _get_research_lines(MOCK_NEWS3)
        self.assertEqual(len(res), 17)
        self.assertIsInstance(res, list)

        # * Alpha Natural Resources <ANR.N>: Goldman Sachs cuts to sell from
        # neutral
        i = 0
        self.assertIsInstance(res[i], ResearchLine)
        self.assertIsInstance(res[i].new_price_target, Price)
        self.assertIsInstance(res[i].old_price_target, Price)
        self.assertEqual(res[i].analyzed_entity, "081904-E")
        self.assertEqual(res[i].analysts_house, "Goldman Sachs")
        self.assertEqual(res[i].new_price_target.currency, None)
        self.assertEqual(res[i].new_price_target.nominal, None)
        self.assertEqual(res[i].old_price_target.currency, None)
        self.assertEqual(res[i].old_price_target.nominal, None)

        # * Cross Country Healthcare <CCRN.O>: Citigroup raises to buy from
        # neutral
        i = 1
        self.assertIsInstance(res[i], ResearchLine)
        self.assertIsInstance(res[i].new_price_target, Price)
        self.assertIsInstance(res[i].old_price_target, Price)
        self.assertEqual(res[i].analyzed_entity, "003B0S-E")
        self.assertEqual(res[i].analysts_house, "Citigroup")
        self.assertEqual(res[i].new_price_target.currency, None)
        self.assertEqual(res[i].new_price_target.nominal, None)
        self.assertEqual(res[i].old_price_target.currency, None)
        self.assertEqual(res[i].old_price_target.nominal, None)

        # * Humana Inc <HUM.N>: Jefferies cuts to hold [ID:nWNAB04D49]
        i = 2
        self.assertIsInstance(res[i], ResearchLine)
        self.assertIsInstance(res[i].new_price_target, Price)
        self.assertIsInstance(res[i].old_price_target, Price)
        self.assertEqual(res[i].analyzed_entity, "000LV7-E")
        self.assertEqual(res[i].analysts_house, "Jefferies")
        self.assertEqual(res[i].new_price_target.currency, None)
        self.assertEqual(res[i].new_price_target.nominal, None)
        self.assertEqual(res[i].old_price_target.currency, None)
        self.assertEqual(res[i].old_price_target.nominal, None)

        # * Houghton Mifflin Harcourt <HMHC.O>: Goldman Sachs cuts to neutral;
        # Stifel cuts to hold
        i = 3
        self.assertIsInstance(res[i], ResearchLine)
        self.assertIsInstance(res[i].new_price_target, Price)
        self.assertIsInstance(res[i].old_price_target, Price)
        self.assertEqual(res[i].analyzed_entity, None)
        self.assertEqual(res[i].analysts_house, "Goldman Sachs")
        self.assertEqual(res[i].new_price_target.currency, None)
        self.assertEqual(res[i].new_price_target.nominal, None)
        self.assertEqual(res[i].old_price_target.currency, None)
        self.assertEqual(res[i].old_price_target.nominal, None)

        # * Teva Pharmaceutical <TEVA.N>: Barclays raises to overweight from
        # equal weight
        i = 4
        self.assertIsInstance(res[i], ResearchLine)
        self.assertIsInstance(res[i].new_price_target, Price)
        self.assertIsInstance(res[i].old_price_target, Price)
        self.assertEqual(res[i].analyzed_entity, "00115K-E")
        self.assertEqual(res[i].analysts_house, "Barclays")
        self.assertEqual(res[i].new_price_target.currency, None)
        self.assertEqual(res[i].new_price_target.nominal, None)
        self.assertEqual(res[i].old_price_target.currency, None)
        self.assertEqual(res[i].old_price_target.nominal, None)

        # * 21Vianet Group Inc <VNET.O>: Canaccord Genuity raises target to $31
        # from $23; rating buy
        i = 5
        self.assertIsInstance(res[i], ResearchLine)
        self.assertIsInstance(res[i].new_price_target, Price)
        self.assertIsInstance(res[i].old_price_target, Price)
        self.assertEqual(res[i].analyzed_entity, "00D48N-E")
        self.assertEqual(res[i].analysts_house, "Canaccord Genuity")
        self.assertEqual(res[i].new_price_target.currency, "USD")
        self.assertEqual(res[i].new_price_target.nominal, 31.0)
        self.assertEqual(res[i].old_price_target.currency, "USD")
        self.assertEqual(res[i].old_price_target.nominal, 23.0)

        # * ACADIA Pharmaceuticals <ACAD.O>: Piper Jaffray raises target to $42
        # from $28; overweight
        i = 6
        self.assertIsInstance(res[i], ResearchLine)
        self.assertIsInstance(res[i].new_price_target, Price)
        self.assertIsInstance(res[i].old_price_target, Price)
        self.assertEqual(res[i].analyzed_entity, "0033SF-E")
        self.assertEqual(res[i].analysts_house, "Piper Jaffray")
        self.assertEqual(res[i].new_price_target.currency, "USD")
        self.assertEqual(res[i].new_price_target.nominal, 42.0)
        self.assertEqual(res[i].old_price_target.currency, "USD")
        self.assertEqual(res[i].old_price_target.nominal, 28.0)

        # * Aetna Inc <AET.N>: Jefferies raises price target to $87; rating buy
        i = 7
        self.assertIsInstance(res[i], ResearchLine)
        self.assertIsInstance(res[i].new_price_target, Price)
        self.assertIsInstance(res[i].old_price_target, Price)
        self.assertEqual(res[i].analyzed_entity, "0017BR-E")
        self.assertEqual(res[i].analysts_house, "Jefferies")
        self.assertEqual(res[i].new_price_target.currency, "USD")
        self.assertEqual(res[i].new_price_target.nominal, 87.0)
        self.assertEqual(res[i].old_price_target.currency, None)
        self.assertEqual(res[i].old_price_target.nominal, None)

        # * Agilent Technologies <A.N>: JP Morgan raises target to $65 from
        # $60; rating overweight
        i = 8
        self.assertIsInstance(res[i], ResearchLine)
        self.assertIsInstance(res[i].new_price_target, Price)
        self.assertIsInstance(res[i].old_price_target, Price)
        self.assertEqual(res[i].analyzed_entity, "002LV5-E")
        self.assertEqual(res[i].analysts_house, "JP Morgan")
        self.assertEqual(res[i].new_price_target.currency, "USD")
        self.assertEqual(res[i].new_price_target.nominal, 65.0)
        self.assertEqual(res[i].old_price_target.currency, "USD")
        self.assertEqual(res[i].old_price_target.nominal, 60.0)

        # * Agilent Technologies <A.N>: Jefferies raises price target to $67
        # from $66; rating buy
        i = 9
        self.assertIsInstance(res[i], ResearchLine)
        self.assertIsInstance(res[i].new_price_target, Price)
        self.assertIsInstance(res[i].old_price_target, Price)
        self.assertEqual(res[i].analyzed_entity, "002LV5-E")
        self.assertEqual(res[i].analysts_house, "Jefferies")
        self.assertEqual(res[i].new_price_target.currency, "USD")
        self.assertEqual(res[i].new_price_target.nominal, 67.0)
        self.assertEqual(res[i].old_price_target.currency, "USD")
        self.assertEqual(res[i].old_price_target.nominal, 66.0)

        # * Agios Pharmaceuticals <AGIO.O>: Leerink raises target price to $51
        # from $38; outperform
        i = 10
        self.assertIsInstance(res[i], ResearchLine)
        self.assertIsInstance(res[i].new_price_target, Price)
        self.assertIsInstance(res[i].old_price_target, Price)
        self.assertEqual(res[i].analyzed_entity, None)
        self.assertEqual(res[i].analysts_house, "Leerink")
        self.assertEqual(res[i].new_price_target.currency, "USD")
        self.assertEqual(res[i].new_price_target.nominal, 51.0)
        self.assertEqual(res[i].old_price_target.currency, "USD")
        self.assertEqual(res[i].old_price_target.nominal, 38.0)

        # * Allergan Inc <AGN.N>: Barclays raises target price to $130 from
        # $95; rating equal weight
        i = 11
        self.assertIsInstance(res[i], ResearchLine)
        self.assertIsInstance(res[i].new_price_target, Price)
        self.assertIsInstance(res[i].old_price_target, Price)
        self.assertEqual(res[i].analyzed_entity, "000BQR-E")
        self.assertEqual(res[i].analysts_house, "Barclays")
        self.assertEqual(res[i].new_price_target.currency, "USD")
        self.assertEqual(res[i].new_price_target.nominal, 130.0)
        self.assertEqual(res[i].old_price_target.currency, "USD")
        self.assertEqual(res[i].old_price_target.nominal, 95.0)

        # * Sirius XM Holdings <SIRI.O>:Macquarie ups to outperform from
        # neutral- Theflyonthewall.com
        i = 12
        self.assertIsInstance(res[i], ResearchLine)
        self.assertIsInstance(res[i].new_price_target, Price)
        self.assertIsInstance(res[i].old_price_target, Price)
        self.assertEqual(res[i].analyzed_entity, "07BHVC-E")
        self.assertEqual(res[i].analysts_house, "Macquarie")
        self.assertEqual(res[i].new_price_target.currency, None)
        self.assertEqual(res[i].new_price_target.nominal, None)
        self.assertEqual(res[i].old_price_target.currency, None)
        self.assertEqual(res[i].old_price_target.nominal, None)

        # * Skullcandy <SKUL.O>:Northland ups to outperform from market
        # perform - Theflyonthewall.com
        i = 13
        self.assertIsInstance(res[i], ResearchLine)
        self.assertIsInstance(res[i].new_price_target, Price)
        self.assertIsInstance(res[i].old_price_target, Price)
        self.assertEqual(res[i].analyzed_entity, "009X9J-E")
        self.assertEqual(res[i].analysts_house, "Northland")
        self.assertEqual(res[i].new_price_target.currency, None)
        self.assertEqual(res[i].new_price_target.nominal, None)
        self.assertEqual(res[i].old_price_target.currency, None)
        self.assertEqual(res[i].old_price_target.nominal, None)

        # * Skullcandy <SKUL.O>: D. A. Davidson raises to neutral from
        # underperform rating
        i = 14
        self.assertIsInstance(res[i], ResearchLine)
        self.assertIsInstance(res[i].new_price_target, Price)
        self.assertIsInstance(res[i].old_price_target, Price)
        self.assertEqual(res[i].analyzed_entity, "009X9J-E")
        self.assertEqual(res[i].analysts_house, "D. A. Davidson")
        self.assertEqual(res[i].new_price_target.currency, None)
        self.assertEqual(res[i].new_price_target.nominal, None)
        self.assertEqual(res[i].old_price_target.currency, None)
        self.assertEqual(res[i].old_price_target.nominal, None)

        # * Skullcandy <SKUL.O>: Roth captial raises target price to $10 from
        # $9; rating buy
        i = 15
        self.assertIsInstance(res[i], ResearchLine)
        self.assertIsInstance(res[i].new_price_target, Price)
        self.assertIsInstance(res[i].old_price_target, Price)
        self.assertEqual(res[i].analyzed_entity, "009X9J-E")
        self.assertEqual(res[i].analysts_house, "Roth captial")
        self.assertEqual(res[i].new_price_target.currency, "USD")
        self.assertEqual(res[i].new_price_target.nominal, 10.0)
        self.assertEqual(res[i].old_price_target.currency, "USD")
        self.assertEqual(res[i].old_price_target.nominal, 9.0)

        # * SNC-Lavalin Group <SNC.TO>:RBC cuts target price to C$49 from C$50;
        # rating sector perform
        i = 16
        self.assertIsInstance(res[i], ResearchLine)
        self.assertIsInstance(res[i].new_price_target, Price)
        self.assertIsInstance(res[i].old_price_target, Price)
        self.assertEqual(res[i].analyzed_entity, "003QDH-E")
        self.assertEqual(res[i].analysts_house, "RBC")
        self.assertEqual(res[i].new_price_target.currency, "CAD")
        self.assertEqual(res[i].new_price_target.nominal, 49.0)
        self.assertEqual(res[i].old_price_target.currency, "CAD")
        self.assertEqual(res[i].old_price_target.nominal, 50.0)


class TestDetermineProperDate(unittest.TestCase):

    def test_proper_dates(self):
        MOCK_INDEX = [
            pd.Timestamp(datetime.datetime(2014, 3, 3, 21, 0, 0)),
            pd.Timestamp(datetime.datetime(2014, 3, 4, 21, 0, 0)),
            pd.Timestamp(datetime.datetime(2014, 3, 5, 21, 0, 0)),
            pd.Timestamp(datetime.datetime(2014, 3, 6, 21, 0, 0)),
            pd.Timestamp(datetime.datetime(2014, 3, 7, 21, 0, 0)),
            pd.Timestamp(datetime.datetime(2014, 3, 10, 20, 0, 0))
        ]
        MOCK_INDEX = [d.tz_localize('UTC') for d in MOCK_INDEX]

        EXP = [pd.Timestamp(datetime.datetime(2014, 3, 7, 21, 0, 0)),
               pd.Timestamp(datetime.datetime(2014, 3, 10, 20, 0, 0))]
        EXP = [d.tz_localize('UTC') for d in EXP]

        res = _determine_proper_date(datetime.datetime(2014, 3, 7, 21, 0, 0),
                                     MOCK_INDEX)
        self.assertEqual(res, EXP[1])

        res = _determine_proper_date(datetime.datetime(2014, 3, 7, 6, 16, 18),
                                     MOCK_INDEX)
        self.assertEqual(res, EXP[0])

        res = _determine_proper_date(datetime.datetime(2014, 3, 7, 20, 59, 59),
                                     MOCK_INDEX)
        self.assertEqual(res, EXP[0])
