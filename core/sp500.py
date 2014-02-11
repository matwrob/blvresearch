from itertools import chain
import pandas as pd
import datetime

from blvworker.news.news_data import (
    _create_entity_lookup_dict, _invert_entity_transl
)


PATH_TO_CSV = 'ticker_rics_sp500_2012.csv'
sp500 = pd.read_csv(PATH_TO_CSV)

entity_lookup = _create_entity_lookup_dict()
ric_to_entity = _invert_entity_transl(entity_lookup)

# sp500.ric contains 892 unique rics

result = dict()
for ric in sp500.ric.dropna():
    result[ric] = ric_to_entity.get(ric)
result = pd.Series(result)
SP500_entities = list(result.dropna())

# factset_entity_id is found for 682 rics

missing = [k for k, v in result.items() if v is None]

all_codes = list(set(chain.from_iterable(entity_lookup.values())))


def int2datetime(proper_int):
    return datetime.datetime.strptime(str(proper_int), "%Y%m%d")


def get_frame_of_start_and_end_dates(ric_codes):
    start, end = dict(), dict()
    for k, v in sp500.iterrows():
        if v['ric'] in ric_codes:
            start[v['ric']] = int2datetime(v['start'])
            end[v['ric']] = int2datetime(v['ending'])
    start = pd.Series(start, name='start')
    end = pd.Series(end, name='end')
    return pd.concat([start, end], axis=1)


INITIAL_DATE = pd.datetime(2003, 1, 1)

result = get_frame_of_start_and_end_dates(missing)

too_old = list()
for k, v in result[result['end'] < INITIAL_DATE].iterrows():
    too_old.append(k)

len(too_old)  # number of entities who ceased to be a member of
              # S&P500 before 2003-01-01
              # it's 65 entities out of 210 missing


# the rest of 210 missing guys
# google rics to find entity names
"""
ABI.N:    1974-10-17 to 2008-11-21
ABS.N:    1984-11-23 to 2006-06-01
ADP.N:    1981-02-26 to 2012-12-31
AMB.N:    2011-06-03 to 2012-12-31
ANDW.O:   1984-11-23 to 2006-09-29
AOC.N:    1996-04-23 to 2012-12-31
APCC.O:   2000-06-01 to 2007-02-14
ASD.N:    2002-05-13 to 2008-06-05
ASN.N:    2004-12-20 to 2007-10-05
ASO.N:    1999-03-10 to 2006-11-03
ATG.N:    2011-12-13 to 2012-12-31
ATH.N:    2002-07-25 to 2012-12-31
AVZ.N:    2008-08-21 to 2012-12-31
AW.N:     1999-08-02 to 2008-12-04
AWE.N:    2001-07-09 to 2004-10-26
BF.N:     1982-10-14 to 2012-12-31
BGEN.O:   2000-01-31 to 2003-11-12
BLI.N:    1998-01-20 to 2012-12-31
BLS.N:    1983-12-01 to 2007-01-03
BMC.N:    1998-10-01 to 2012-12-31
BMET.O:   1990-08-23 to 2007-07-11
BOL.N:    1986-05-08 to 2007-10-26
BRK.N:    2010-02-16 to 2012-12-31
BRL.N:    2006-02-27 to 2008-12-22
BSC.N:    1998-07-01 to 2008-05-30
CA.N:     1987-07-09 to 2012-12-31
CBH.N:    2006-06-06 to 2008-03-28
CBSS.O:   2004-12-20 to 2007-09-06
CC.N:     1989-05-11 to 2008-03-28
CD.N:     1995-05-01 to 2006-07-31
CEY.N:    2006-11-10 to 2012-12-31
CFC.N:    1997-06-18 to 2008-06-30
CHIR.O:   2000-11-24 to 2006-04-19
CIN.N:    1994-10-25 to 2006-03-31
CMX.N:    2004-03-25 to 2007-03-22
CUM.N:    1965-01-07 to 2012-12-31
CZN.N:    2001-02-27 to 2012-12-31
DCN.N:    1957-03-01 to 2006-03-02
DJ.N:     1978-05-04 to 2007-12-13
DPH.N:    1999-05-28 to 2005-10-10
DTV.N:    2006-12-04 to 2012-12-31
DVN.A:    2000-08-30 to 2012-12-31
EDS.N:    1998-08-11 to 2008-08-26
EOP.N:    2001-10-10 to 2007-02-09
EQ.N:     2006-05-18 to 2009-06-30
EXPEV.O:  2007-10-02 to 2012-12-31
FBF.N:    1988-11-10 to 2004-03-31
FD.N:     1995-12-01 to 2012-12-31
FDC.N:    1994-09-27 to 2007-09-24
FO.N:     1925-12-31 to 2012-12-31
FON.N:    1989-07-27 to 2012-12-31
FSH.N:    2004-08-03 to 2006-11-09
FTN.N:    2002-05-06 to 2012-12-31
GDT.N:    1996-12-19 to 2006-04-21
GDW.N:    1988-06-09 to 2006-09-29
GLK.N:    1991-11-25 to 2005-07-01
GP.N:     1964-02-20 to 2005-12-19
GTW.N:    1998-04-27 to 2006-07-31
HANS.O:   2012-06-29 to 2012-12-31
HCR.N:    1998-09-28 to 2007-11-08
HDI.N:    2000-01-31 to 2012-12-31
HET.N:    1990-02-08 to 2008-01-28
HLT.N:    1970-04-23 to 2007-10-24
HMT.N:    2007-03-20 to 2012-12-31
HPC.N:    1957-03-01 to 2008-11-13
IDPH.O:   2003-11-13 to 2012-12-31
IVGN.O:   2008-11-24 to 2012-12-31
JHF.N:    2001-06-28 to 2004-04-28
JNPR.O:   2006-06-02 to 2012-12-31
JP.N:     1976-07-01 to 2006-03-31
KFT.N:    2007-04-02 to 2012-12-31
KFT.O:    2007-04-02 to 2012-12-31
KMG.N:    1984-10-04 to 2006-08-10
KMRT.O:   2005-03-28 to 2012-12-31
KRB.N:    1992-04-23 to 2005-12-30
KRI.N:    1975-12-11 to 2006-06-27
KSE.N:    2000-08-21 to 2007-08-24
LEH.N:    1998-01-12 to 2008-09-16
LIZ.N:    1984-10-25 to 2008-12-01
LTR.N:    1995-05-10 to 2012-12-31
LU.N:     1996-10-01 to 2006-11-30
MEDI.O:   2000-06-16 to 2007-05-31
MEL.N:    1976-07-01 to 2007-06-29
MERQ.O:   2000-06-29 to 2006-01-03
MOT.N:    1957-03-01 to 2012-12-31
MU.N:     1994-09-27 to 2012-12-31
MWD.N:    1995-09-22 to 2012-12-31
MYG.N:    1960-12-14 to 2006-03-31
MYL.N:    2004-04-23 to 2012-12-31
NBR.A:    2000-10-18 to 2012-12-31
NCC.N:    1994-09-27 to 2008-12-31
NET.N:    2008-12-23 to 2011-02-28
NFB.N:    2002-07-17 to 2006-11-30
NOI.N:    2005-03-14 to 2012-12-31
NXTL.O:   1998-04-01 to 2005-08-12
PCCW.O:   1993-10-22 to 2012-12-31
PD.N:     1957-03-01 to 2007-03-19
PGL.N:    1940-04-15 to 2007-02-21
PSFT.O:   1998-10-02 to 2004-12-28
PVN.N:    1997-06-11 to 2005-09-30
QTRN.O:   1999-11-16 to 2003-09-25
RATL.O:   2002-02-01 to 2003-02-21
RBK.N:    1987-01-08 to 2006-01-31
RHAT.O:   2009-07-27 to 2012-12-31
RJR.N:    2002-09-04 to 2012-12-31
RKY.N:    1976-07-01 to 2012-12-31
ROH.N:    1982-09-16 to 2009-04-01
RRD.N:    1984-07-19 to 2012-12-11
RX.N:     1996-11-01 to 2010-02-26
SAF.N:    1976-07-01 to 2008-09-22
SAFC.O:   1976-07-01 to 2008-09-22
SBC.N:    1983-12-01 to 2012-12-31
SBL.N:    2000-12-11 to 2007-01-09
SCH.N:    1997-06-02 to 2012-12-31
SDS.N:    2002-07-22 to 2005-08-11
SEBL.O:   2000-05-05 to 2006-01-31
SFA.N:    1981-02-26 to 2006-02-24
SGP.N:    1957-03-01 to 2009-11-03
SLE.N:    1981-09-10 to 2012-06-28
SLR.N:    1998-12-31 to 2007-10-01
SOTR.O:   1999-03-01 to 2004-10-29
SOV.N:    2004-07-01 to 2009-01-29
SPC.N:    1976-07-01 to 2012-12-31
STA.N:    1976-07-01 to 2012-12-31
STX.N:    2012-07-02 to 2012-12-31
SUNW.O:   1992-08-20 to 2010-01-28
SV.N:     2000-07-13 to 2011-11-22
TEK.N:    1967-02-23 to 2007-11-15
TMPW.O:   2001-06-04 to 2011-12-16
TOY.N:    1983-09-08 to 2005-07-21
TRB.N:    1986-01-30 to 2007-12-20
TSG.N:    2000-03-16 to 2007-03-30
TT.N:     2002-05-13 to 2008-06-05
TXU.N:    1957-03-01 to 2007-10-09
UCL.N:    1957-03-01 to 2005-08-10
UPC.N:    1998-10-01 to 2004-06-30
USAI.O:   2006-12-01 to 2008-08-20
UST.N:    1987-04-09 to 2009-01-05
UVN.N:    2001-02-07 to 2007-03-28
WB.N:     1989-02-09 to 2008-12-31
WIN.N:    2006-07-18 to 2012-12-31
WMI.N:    1998-07-17 to 2012-12-31
WPS.N:    2007-02-22 to 2012-12-31
WWY.N:    1957-03-01 to 2008-10-06
WYE.N:    1957-03-01 to 2009-10-15
"""

"""
ABI.N: APPLIED BIOSYSTEMS INC
ABS.N: ALBERTSONS INC
ADP.N: AUTOMATIC DATA PROCESSING INC
AMB.N:
ANDW.O:
AOC.N:
APCC.O:
ASD.N:
ASN.N:
ASO.N:
ATG.N:
ATH.N:
AVZ.N:
AW.N:
AWE.N:
BF.N:
BGEN.O:
BLI.N:
BLS.N:
BMC.N:
BMET.O:
BOL.N:
BRK.N:
BRL.N:
BSC.N:
CA.N:
CBH.N:
CBSS.O:
CC.N:
CD.N:
CEY.N:
CFC.N:
CHIR.O:
CIN.N:
CMX.N:
CUM.N:
CZN.N:
DCN.N:
DJ.N:
DPH.N:
DTV.N:
DVN.A:
EDS.N:
EOP.N:
EQ.N:
EXPEV.O:
FBF.N:
FD.N:
FDC.N:
FO.N:
FON.N:
FSH.N:
FTN.N:
GDT.N:
GDW.N:
GLK.N:
GP.N:
GTW.N:
HANS.O:
HCR.N:
HDI.N:
HET.N:
HLT.N:
HMT.N:
HPC.N:
IDPH.O:
IVGN.O:
JHF.N:
JNPR.O:
JP.N:
KFT.N:
KFT.O:
KMG.N:
KMRT.O:
KRB.N:
KRI.N:
KSE.N:
LEH.N:
LIZ.N:
LTR.N:
LU.N:
MEDI.O:
MEL.N:
MERQ.O:
MOT.N:
MU.N:
MWD.N:
MYG.N:
MYL.N:
NBR.A:
NCC.N:
NET.N:
NFB.N:
NOI.N:
NXTL.O:
PCCW.O:
PD.N:
PGL.N:
PSFT.O:
PVN.N:
QTRN.O:
RATL.O:
RBK.N:
RHAT.O:
RJR.N:
RKY.N:
ROH.N:
RRD.N:
RX.N:
SAF.N:
SAFC.O:
SBC.N:
SBL.N:
SCH.N:
SDS.N:
SEBL.O:
SFA.N:
SGP.N:
SLE.N:
SLR.N:
SOTR.O:
SOV.N:
SPC.N:
STA.N:
STX.N:
SUNW.O:
SV.N:
TEK.N:
TMPW.O:
TOY.N:
TRB.N:
TSG.N:
TT.N:
TXU.N:
UCL.N:
UPC.N:
USAI.O:
UST.N:
UVN.N:
WB.N:
WIN.N:
WMI.N:
WPS.N:
WWY.N:
WYE.N:
"""
