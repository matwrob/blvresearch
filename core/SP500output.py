import pandas as pd
import datetime

from concat.core.utils import load_object
from concat.core.prices import to_log_returns

from blvresearch.core.sp500 import tick_to_ent_no_dupli
from blvresearch.core.utils import int2datetime


def get_incl_and_excl_dates_for_SP500():
    temp = pd.read_csv('ticker_rics_sp500_2012.csv')
    temp = temp[['start', 'ending', 'TICKER']]
    temp['index'] = temp['TICKER'].map(tick_to_ent_no_dupli)
    temp = temp.dropna()
    temp.index = temp['index']
    temp = temp.drop(['TICKER', 'index'], axis=1)
    temp = temp[['start', 'ending']].applymap(int2datetime)
    return temp


def remove_data_for_time_when_not_in_SP500(dataframe):
    incl_excl = get_incl_and_excl_dates_for_SP500()
    result = dict()
    for k, v in dataframe.items():
        s, e = incl_excl['start'][k], incl_excl['ending'][k]
        if isinstance(s, pd.Series):
            result[k] = solve_for_more_periods(s, e, v)
        else:
            result[k] = v[s:e]
    return pd.DataFrame(result)


def solve_for_more_periods(starts, ends, values):
    def _get_inbetweens(iterable):
        return [(v[-1], iterable[(i + 1) % len(iterable)][0])
                for i, v in enumerate(iterable) if i < len(iterable) - 1]
    result = values[starts.values[0]:ends.values[-1]]
    periods = list(zip(starts, ends))
    for per in _get_inbetweens(periods):
        result[per[0]:per[1]] = None
    return result


ENTITIES_SP560 = ['000BG2-E', '000BH0-E', '000BJB-E', '000BJT-E', '000BK7-E', '000BMB-E', '000BMH-E', '000BN8-E', '000BNF-E', '000BNN-E', '000BQK-E', '000BQR-E', '000BTQ-E', '000BTW-E', '000BWL-E', '000BY1-E', '000BY7-E', '000BZV-E', '000C35-E', '000C3J-E', '000C49-E', '000C4B-E', '000C6S-E', '000C6X-E', '000C77-E', '000C7F-E', '000C7R-E', '000C8L-E', '000CBF-E', '000CFP-E', '000CFX-E', '000CGC-E', '000CGK-E', '000CHM-E', '000CJY-E', '000CLT-E', '000CN7-E', '000CNJ-E', '000CNK-E', '000CPS-E', '000CPT-E', '000CQ8-E', '000CR1-E', '000CSN-E', '000CVZ-E', '000CW6-E', '000CXX-E', '000CYC-E', '000CZ5-E', '000D1R-E', '000D2Z-E', '000D30-E', '000D4L-E', '000D63-E', '000D8R-E', '000DB4-E', '000DCC-E', '000DFY-E', '000DGZ-E', '000DLP-E', '000DLW-E', '000DP2-E', '000DP6-E', '000DQ8-E', '000DR3-E', '000DRH-E', '000DRP-E', '000DS6-E', '000DSS-E', '000DTT-E', '000DV5-E', '000DW6-E', '000DWY-E', '000DXS-E', '000F01-E', '000F2F-E', '000F2P-E', '000F2V-E', '000F34-E', '000F36-E', '000F6B-E', '000F6H-E', '000F7B-E', '000FC8-E', '000FDD-E', '000FFC-E', '000FFW-E', '000FHS-E', '000FMM-E', '000HGZ-E', '000HH9-E', '000HHD-E', '000HJ0-E', '000HJ4-E', '000HKP-E', '000HLG-E', '000HMG-E', '000HMR-E', '000HN5-E', '000HN8-E', '000HSZ-E', '000HT4-E', '000HXM-E', '000HZY-E', '000J0M-E', '000J7C-E', '000J81-E', '000J8F-E', '000JB1-E', '000JF5-E', '000JG9-E', '000JH2-E', '000JHG-E', '000JHP-E', '000JJ3-E', '000JND-E', '000JVP-E', '000KJ3-E', '000KLQ-E', '000KLW-E', '000KN2-E', '000KNF-E', '000KPH-E', '000KRC-E', '000KS2-E', '000KWH-E', '000KWJ-E', '000KYC-E', '000KYG-E', '000KYW-E', '000KZV-E', '000L1R-E', '000L50-E', '000L54-E', '000L76-E', '000LCV-E', '000LD9-E', '000LDD-E', '000LGS-E', '000LGX-E', '000LHC-E', '000LJT-E', '000LKT-E', '000LKV-E', '000LL1-E', '000LM7-E', '000LMP-E', '000LNJ-E', '000LNN-E', '000LPQ-E', '000LR9-E', '000LS4-E', '000LS9-E', '000LV7-E', '000LVH-E', '000M15-E', '000N01-E', '000N1N-E', '000N1Z-E', '000N20-E', '000N29-E', '000N2T-E', '000N7V-E', '000NB6-E', '000NB8-E', '000NGP-E', '000NH1-E', '000NSX-E', '000NVS-E', '000NVT-E', '000NX1-E', '000NXL-E', '000NYF-E', '000NYZ-E', '000P26-E', '000P2H-E', '000P2Z-E', '000P56-E', '000P59-E', '000P5T-E', '000P6R-E', '000P7N-E', '000P7W-E', '000P9F-E', '000P9L-E', '000P9S-E', '000PF5-E', '000PH0-E', '000PH7-E', '000PHP-E', '000PK1-E', '000PKD-E', '000PL0-E', '000PLG-E', '000PLK-E', '000PLS-E', '000PLZ-E', '000PM1-E', '000PP9-E', '000PQC-E', '000PQK-E', '000PR2-E', '000PYN-E', '000PZP-E', '000PZY-E', '000Q07-E', '000Q29-E', '000Q51-E', '000QSM-E', '000R3K-E', '000R4P-E', '000R9L-E', '000R9T-E', '000R9Z-E', '000RBW-E', '000RC9-E', '000RD1-E', '000RD2-E', '000RFJ-E', '000RGR-E', '000RH4-E', '000RH5-E', '000RHT-E', '000SSF-E', '000SSV-E', '000SVP-E', '000SW8-E', '000SY8-E', '000T00-E', '000T0D-E', '000T3J-E', '000T43-E', '000T4W-E', '000T67-E', '000T7G-E', '000T99-E', '000TBR-E', '000TBT-E', '000TCH-E', '000TFT-E', '000TH5-E', '000TJ9-E', '000TLW-E', '000TLX-E', '000TM7-E', '000TMB-E', '000TRY-E', '000TSD-E', '000V1Y-E', '000V67-E', '000V77-E', '000V98-E', '000VJS-E', '000VKM-E', '000VKZ-E', '000VMV-E', '000VNZ-E', '000VQ6-E', '000VRD-E', '000VSF-E', '000VTN-E', '000VWG-E', '000WF5-E', '000WGT-E', '000WMF-E', '000WMS-E', '000WMW-E', '000WQ5-E', '000WQH-E', '000WR8-E', '000WRR-E', '000WTZ-E', '000WV4-E', '000WVZ-E', '000WW4-E', '000WX2-E', '000X16-E', '000X2H-E', '000X3M-E', '000X42-E', '000X58-E', '000X5M-E', '000X5W-E', '000X6Q-E', '000XLF-E', '000XM1-E', '000XM9-E', '000XN9-E', '000XNK-E', '000XNL-E', '000XNQ-E', '000XNY-E', '000XP9-E', '000XPZ-E', '000XR0-E', '000XRR-E', '000XSK-E', '000XSX-E', '000XZN-E', '000XZR-E', '000Y1Z-E', '000Y2H-E', '000Y3J-E', '000Y4G-E', '000Y55-E', '000Y6D-E', '000Y86-E', '000Y8N-E', '000YLB-E', '000YM7-E', '000YMS-E', '000YMW-E', '000YPP-E', '000YTL-E', '000YVQ-E', '000YVZ-E', '000YWV-E', '000YY2-E', '000Z0L-E', '000Z1T-E', '000Z21-E', '000Z3H-E', '000ZPG-E', '000ZW7-E', '00101M-E', '0010CQ-E', '0010HF-E', '0011BL-E', '0011FZ-E', '0011GG-E', '0011HX-E', '0011NQ-E', '0011S2-E', '0011SR-E', '001274-E', '0012KJ-E', '0012PR-E', '0012RM-E', '0013FQ-E', '0013V2-E', '0013WC-E', '0013YQ-E', '00140N-E', '00147D-E', '0014C0-E', '0014DV-E', '001562-E', '001585-E', '0015N4-E', '0015NZ-E', '0015Q5-E', '0015RG-E', '00167Y-E', '0016FD-E', '0016MB-E', '00172J-E', '00172L-E', '00172R-E', '0017BJ-E', '0017F0-E', '0017JW-E', '0018R5-E', '001963-E', '0019JD-E', '0019PR-E', '001B00-E', '001BFQ-E', '001BN4-E', '001CGF-E', '001CHF-E', '001CKB-E', '001CW1-E', '001FBC-E', '001FR9-E', '001H0J-E', '001HHK-E', '001K97-E', '001MCF-E', '001MF1-E', '001MY1-E', '001N7P-E', '001NBX-E', '001NWQ-E', '001P2P-E', '001QFL-E', '001R78-E', '001R8V-E', '001RMM-E', '001RND-E', '001T5S-E', '001TL0-E', '001TPD-E', '001TR0-E', '001VHN-E', '001W7N-E', '001WC9-E', '001WPM-E', '001XPN-E', '001XVL-E', '001YRD-E', '001ZRY-E', '001ZY8-E', '00208X-E', '0020FC-E', '0020GS-E', '0021JW-E', '0021ZC-E', '0022L7-E', '0022QP-E', '002323-E', '0023BK-E', '0023JS-E', '00247H-E', '0024V8-E', '0024XW-E', '00255C-E', '002615-E', '00266T-E', '0026HZ-E', '0027L0-E', '0027RH-E', '0028D2-E', '002983-E', '0029GL-E', '0029VC-E', '002DJM-E', '002DZR-E', '002F93-E', '002FH6-E', '002FQK-E', '002FR0-E', '002HJD-E', '002HW9-E', '002J5D-E', '002JTY-E', '002KXQ-E', '002KXV-E', '002L44-E', '002LV5-E', '002LZ3-E', '002M0S-E', '002M94-E', '002M9F-E', '002MY0-E', '002P6D-E', '002PGB-E', '002PV7-E', '002Q0G-E', '002Q2X-E', '002Q6V-E', '002RNG-E', '002RXT-E', '002W5H-E', '002WNN-E', '002X9M-E', '002XXL-E', '002YTH-E', '002Z19-E', '0030MN-E', '003108-E', '0033W4-E', '00345K-E', '0034R9-E', '0035K2-E', '0035RF-E', '0035XX-E', '0035YR-E', '0036GM-E', '0036P0-E', '00371D-E', '00375R-E', '0037KG-E', '003894-E', '0038M5-E', '0038QK-E', '003BWN-E', '003DJY-E', '003F4V-E', '003GLW-E', '003GNF-E', '003GTW-E', '003JLG-E', '003TXQ-E', '003W46-E', '003ZHQ-E', '003ZLL-E', '003ZXF-E', '0049BR-E', '0053CW-E', '0058W5-E', '0059GK-E', '005CPH-E', '005RBG-E', '006N1R-E', '00797Q-E', '007S7R-E', '008C5Y-E', '008FJT-E', '008LZ1-E', '008RHB-E', '0091M7-E', '009Z0H-E', '00B2RQ-E', '00B36T-E', '00BGRV-E', '00BN44-E', '00BYDR-E', '00C5YS-E', '00C8ZJ-E', '00DGRF-E', '00DS8H-E', '00DXNY-E', '05G2MG-E', '05M40C-E', '05MDRV-E', '05SK38-E', '05VFN0-E', '05X3H7-E', '05Z5MM-E', '05ZN64-E', '060KMN-E', '060W5N-E', '061F6G-E', '064WW9-E', '066ZNL-E', '06773B-E', '068T0P-E', '069J8N-E', '06BZ2R-E', '06CVZ2-E', '06F9DV-E', '06FMKM-E', '06GFD5-E', '06GLFT-E', '06LJVN-E', '06LZX3-E', '06P3KD-E', '06QDKY-E', '06S1MZ-E', '06S9GH-E', '06Y3ZW-E', '072GKL-E', '0758Z9-E', '07F0V6-E', '07H0VZ-E', '07H311-E', '081904-E', '083HBL-E', '088S35-E', '08BFNX-E', '09N01T-E', '09RDF7-E', '09SD1S-E', '09TVPW-E', '0B3BTL-E', '0BC4VB-E', '0BCNPT-E', '0BDGY2-E', '0BT29H-E', '0C4770-E']

DATA = load_object('bmd_sp500_2003_2013.pickle')

NEWS = DATA.matrix('news')
# NEWS = remove_data_for_time_when_not_in_SP500(NEWS)
NEWS = NEWS[ENTITIES_SP560]

ALPHA = DATA.matrix('alpha')
# ALPHA = remove_data_for_time_when_not_in_SP500(ALPHA)
ALPHA = ALPHA[ENTITIES_SP560]

ABSRET = DATA.matrix('abs_ret')
# ABSRET = remove_data_for_time_when_not_in_SP500(ABSRET)
ABSRET = ABSRET[ENTITIES_SP560]


def get_sp500_close_series():
    res = pd.read_csv('blvresearch/projects/momentum/sp500_2003_2012.csv')
    res.index = res['Date'].apply(
        lambda x: datetime.datetime.strptime(x, '%Y-%m-%d')
    )
    res = res.drop(['Date', 'Open', 'High', 'Low', 'Volume', 'Adj Close'],
                   axis=1)
    res = res['Close']
    res.name = 'SP500'
    return res.sort_index()


SP500_RETURNS = to_log_returns(get_sp500_close_series())
