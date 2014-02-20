blvresearch
===========

research tools to be used with Bluevalor database


#########
PORTFOLIO
#########

General description:
provides basic objects for data backtesting:
* StockReturns
* PortfolioDates
* PortfolioStrategy
* Portfolio
* PortfolioCharacteristics

Portfolio formation procedure:
STEP 1. write a "strategy" class, that inherits from PortfolioStrategy
        by overwriting _get_starting_points method with an algorithm of your
        choice

        one can use any type of data available in Bluevalor Model data output

STEP 2. Initiate the object from STEP 1 providing Bluevalor Model data output

STEP 3. Initiate Portfolio class providing result of STEP 2 (i.e. your
        strategy) on init.
        Now you can operate with your portfolio by e.g. checking portfolio
        members over time, or calculating portfolio performance.

STEP 4. Initiate PortfolioCharacteristics class by providing the result of
        STEP 3 on init. This will allow you to check different statistics of
        your portfolio (check description of PortfolioCharacteristics class)


PortfolioStrategy after initiating gives access to the following:
.output = Bluevalor Model data output
.positions = time series with lists of entities for each rebalancing day
any global attributes defined in the class that inherits from PortfolioStrategy
.HOLDING_PERIODS   = how many periods should entities be held in portfolio
.PAUSE_PERIODS     = how many periods should pass between determining portfolio
                     positions and starting to actually hold them
.REBALANCING_FREQUENCY = frequency of rebalancing periods
.PORTFOLIO_SIZE = number of entities held in a portfolios



Explanation of RankingPeriod/RebalancingDay/PausePeriods/HoldingPeriods
relationship:

Rebalancing day vs holding period:
rebalancing day is the day when we decide about the construction of our
portfolio for the next holding period,
we should hold this portfolio starting at the earliest on the next day
this is obtained by shifting portfolio.members by 1 position


################
PortfolioDates:
################
* determines days when security selection is performed
* determines days when portfolio construction is changed
* takes a number of variables on init:
    0. date_index = set of dates that are only taken into account when
                    when determining rebalancing days and ranking days
    1. ranking_periods = number of periods used to calculate certain
                         characteristics, to determine which securities to
                         include in portfolio in the nearest future
    2. pause_periods = number of periods we should wait after determining
                       the next portfolio structure, before actually holding it
    3. holding_periods = number of periods we will be holding a given set of
                         stocks in our portfolio
    4. date_resampling_frequency = frequency with which initial date index
                                   should be resampled

* if pause_periods = 0 => ranking_days will overlap with rebalancing_days,
  since ranking_days are BACKWARD looking (at the end of a given day X we look
  back at certain characteristics of that day and any earlier days), while
  rebalancing_days are FORWARD looking (at the same end of a given day X,
  after deciding about portfolio structure, we rebalance our portfolio with
  action being taken before the start of the next trading day, so that already
  the next trading day return is based on that portfolio we constructed one
  day before; to be more realistic, we should specify a certain number of
  pause_periods)
* what is the last ranking day? it should be such a date close to the end of
  full date index, so that there is still place (a necessary number of days) to
  calculate/accrue interest on this last portfolio; last ranking day cannot be
  the last day of the total date index, and it shouldn't also be the day after
  which there's only place for pause periods; therefore last day is the day
  which is

* setting RANKING_PERIODS = 0:
  i) should it be possible?
     temporarly impossible

* resampling the date index adds days (with NaN values) for equal periods,
  this shouldn't have substantial impact on portfolio performance if any, since
  we will only extend the last period if it doesn't end at the end of last
  resampled period; this will extend last resampled period and leave empty
  cells

CASES: (used in testing as well)
1) daily rankings of securities, daily rebalancings of portfolios, no pause
   periods, bottom line case;
   on day 02.01.2013 after exchange close rank securities, based on a certain
   characteristic (e.g. return) over that day;
   after determining this ranking, construct portfolio and aquire it for the
   next trading day, i.e. hold this portfolio over 03.01.2013;
   at the end of 03.01.2013 repeat ranking, and construct new portfolio to be
   aquired immediately and held over 04.01.2013, and so on and so forth;
   last ranking perform on the day before last day (17.01.2013) and aquire this
   portfolio to hold it over 18.01.2013

   To summarize: we rank stocks on each trading day's evening (from 02.01.2013
   to 17.01.2013) and immediately afterwards we order this portfolio; so that we hold it over the next trading day (assumptions!!); ranking days are
   exactly the same as rebalancing days

2) daily security ranking, daily rebalancing, one day pause between ranking
   and rebalancing; slightly different case compared to (1)
   use first day data to rank securities, without pause we would construct
   portfolio with such securities immediately after determining the ranks
   and buy/sell it to hold over the next day; in this case we apply a 1 day
   pause period, hence rebalancing will occur at the end of next day (X + 1)
   with day X + 2 in mind for this first portfolio; using X + 1 day data (the
   one when we had pause, and our portfolio was empty) we perform the 2nd
   ranking, which will be used for day X + 3 (since day X + 2 will be a pause
   for this second portfolio mixture)

   To summarize: we rank stocks on each trading day's evening (from 02.01.2013
   until 16.01.2013); the differences compared to (1), we apply pause period
   after each ranking evening, hence we rebalance our portfolio on the next
   day's evening after ranking day, to hold it over the next day:
   02.01.2013 - rank stocks after market close, decide on your portfolio
                construction
   03.01.2013 - pause period, we do not hold this portfolio here yet, after
                market closes on that day we order the portfolio on which we
                decided one evening earlier;
   04.01.2013 - we hold over this day the portfolio on which we decided about
                on 02.01.2013 (evening)

   The last ranking day is 16.01.2013 (evening), when we decide about the
   portfolio we will order next evening (17.01.2013) to hold over 18.01.2013
   The lasst rebalancing day is 17.01.2013; this portfolio's return is
   measured over 18.01.2013

3) ranking based on 5 periods (last 5 trading days), one trading day pause and
   a given portfolio is held over the next 3 days before the next rebalancing;
   in this example we use 02.01.2013, 03.01.2013, 04.01.2013, 07.01.2013 and
   08.01.2013 to perform comparison of securities and rank them (pay attention:
   05.01.2013 and 06.01.2013 are omitted since no trading happened on these days); after exchange close on 08.01.2013 we know which stocks to hold in
   our portfolio but before constructing it we wait one trading day
   (09.01.2013) and we order this portfolio on 09.01.2013 (evening) to hold it
   over next, three trading days (10.01.2013, 11.01.2013, 14.01.2013); here
   again, weekend days are omitted; in the meantime second ranking took place,
   namely, on 11.01.2013 evening we considered last 5 trading days and created
   the ranking, the next trading day (14.01.2013) is used as a pause for this portfolio, and therefore we rebalance our portfolio after market close on
   14.01.2013 and hold it over 15.01.2013, 16.01.2013, 17.01.2013; for this
   short period last ranking is performed after market close on 16.01.2013,
   taking into consideration last 5 trading days (10.01.2013, 11.01.2013,
   14.01.2013, 15.01.2013, 16.01.2013); the next trading day (17.01.2013) is
   used as a pause for this portfolio, we order this portfolio on 17.01.2013
   evening and hold it over the next day (one day only), 18.01.2013; because
   in this toy example we don't have more data

   To summarize: rankings were performed on 08.01.2013, 11.01.2013 and
   16.01.2013; for each of those portfolio plans we used one-day breaks:
   09.01.2013, 14.01.2013, 17.01.2013, and we rebalanced our portfolio in the
   evenings of those PAUSE days, to hold it on the next trading day (+ 2 more
   days, since in this example we use 3 holding periods for each portfolio
   we construct)

4) this case includes weekly (weeks ending Fridays) rebalancing, which means
   the last period is extended if it ends on any other day, but Friday, in this
   case (02.01.2013 to 31.01.2013 period) it means we will have 5 periods:
   Period 1: ending 04.01.2013
   Period 2: ending 11.01.2013
   Period 3: ending 18.01.2013
   Period 4: ending 25.01.2013
   Period 5: ending 01.02.2013
   We use 1 period for ranking, 1 period for pause and 1 period for holding;
   therefore first ranking day is 04.01.2013 (evening, after market close);
   we rank securities based on this one period data, over the next period
   (whole week ending next Friday, 11.01.2013) we do nothing, and only then,
   after market closes on 11.01.2013 (first rebalancing day) we order portfolio to hold over the next (3rd period);
   At the end of Period 2 we perform the 2nd ranking, we wait with this
   selection over Period 3, and only at the end of Period 3 we order this
   selection to hold it over Period 4;
   The last ranking is performed at the end of Period 3, using Period 3 data;
   We wait with this selection over Period 4 and only at the end of Period 4
   we order this portfolio and hold it over Period 5;
   We need to pay attention to the fact, that Period 5, although ends on
   01.02.2013, doesn't contain ful data, namely no data fo 01.02.2013
   To summarize: we have three ranking days. 04.01.2013, 11.01.2013, 18.01.2013
   we have three pause periods in the background; having pause periods does not
   mean we have some discontinuities in return generation; not at all, starting
   with the first portfolio, we hold some stocks all the time until the last
   period

5) case 5 uses the same periods as case 4, the difference here is that we use
   two periods to rank securities and we do not have pause period, i.e. we
   order (rebalance) the portfolio immediately after we decide what to order
   and we hold this portfolio over the very next period;
   first ranking day is 11.01.2013, since we use Period 1 and Period 2 to
   decide about our portfolio selection; first rebalancing day is 11.01.2013,
   when we order portfolio to hold over entire Period 3; at the end of Period 3
   (18.01.2013) we use Periods 2 and 3 data to perform another ranking (second
   ranking day) and we rebalance our portfolio immediately (second rebalancing
   day), and hold this portfolio over Period 4; at the end of Period 4 we
   perform our last ranking (using Periods 3 and 4 data) and we rebalance our
   portfolio for the last time and hold it over last Period 5;
   To summarize: we have 3 ranking days (11.01.2013, 18.01.2013, 25.01.2013)
   and 3 rebalancing days (11.01.2013, 18.01.2013, 25.01.2013)

6) in this case we use monthly resampled data, we take our daily data from
   02.01.2013 until 03.07.2013 and we resample it monthly to get 7 periods,
   this example illustrates the issue with expanding last period to its full
   length, even if there's only 1 data point available for that period (here
   we only have 3 data points for July 2013, but we construct full monthly
   period anyway; this won't have any substantial impact on results and is
   convenient, therefore we use this approach);
   another characteristic in this case is we use month-ends, no matter if this
   last day of a month is a trading day, or not
   Period 1: 31.01.2013
   Period 2: 28.02.2013
   Period 3: 31.03.2013
   Period 4: 30.04.2013
   Period 5: 31.05.2013
   Period 6: 30.06.2013
   Period 7: 31.07.2013
   first ranking day is 31.01.2013, we use January data to select stocks; the
   next period (February) is a break, and on 28.02.2013 we order the first
   portfolio which we will hold over the next two periods; therefore first
   rebalancing day is 28.02.2013 and we hold this selection over Periods 3 and
   4 (betweend 01.03.2013 and 30.04.2013);
   the next ranking is performed on 31.03.2013 using March data, this second selection of stocks will be ordered only one period later (second rebalancing day: 30.04.2013) and held over Periods 5 and 6 (between
   01.05.2013 and 30.06.2013);
   the last ranking is performed on 31.05.2013 using May data, this selection
   waits over the whole Period 6 and is ordered on the last rebalancing day
   (30.06.2013) and held over Period 7 (only 3 days of July though)
   To Summarize: in this setting we had three ranking days (31.01.2013,
   31.03.2013 and 31.05.2013) which were based on previous month data
   we had 3 rebalancing days which were one period (one month) later after each
   ranking day (28.02.2013, 30.04.2013, 30.06.2013)

7) this case is a special one, since it uses zero ranking periods; if we use
   zero ranking periods we also need to use zero pause periods, because it
   makes no sense otherwise; such a case is a toy case, where we use a certain
   security selection immediately and hold it over the very first period
   available; then we can rebalance this portfolio based on the length/amount
   of holding periods;
   if we use as input ranking_periods = 0, we won't be able to see ranking_days
   of our PortfolioStrategy, because there are none; we are only able to see
   rebalancing_days, for which the same logic applies as in cases 1 to 6;
   in example case 7 we have 7 periods after resampling our date index:
   Period 1: 02.01.2013
   Period 2: 03.01.2013
   Period 3: 04.01.2013
   Period 4: 07.01.2013
   Period 5: 08.01.2013
   Period 6: 09.01.2013
   Period 7: 10.01.2013
   first rebalancing should happen before trading on 02.01.2013 starts, so that
   we hold first security selection over Periods 1 and 2; this means we need
   to add one data point at the very beginning, i.e. first rebalancing day
   will be 01.01.2013, since we have holding_periods = 1, we will rebalance
   our portfolio daily, so:
   1st rebalancing: 01.01.2013 (hold over 02.01.2013); date point added
   2nd rebalancing: 02.01.2013 (hold over 03.01.2013)
   3rd rebalancing: 03.01.2013 (hold over 04.01.2013)
   4th rebalancing: 04.01.2013 (hold over 07.01.2013)
   5th rebalancing: 07.01.2013 (hold over 08.01.2013)
   6th rebalancing: 08.01.2013 (hold over 09.01.2013)
   7th rebalancing: 09.01.2013 (hold over 10.01.2013)

   * why having ranking_periods = 0 and pause_periods != 0 makes no sense?
     if we have e.g. six periods:
     Period 1: 31.01.2013
     Period 2: 28.02.2013
     Period 3: 31.03.2013
     Period 4: 30.04.2013
     Period 5: 31.05.2013
     Period 6: 30.06.2013
     having ranking_periods = 0 means we do not rank securities based on the
     data over a certaing period, this means we can immediately decide on our
     selection on the very first day and hold this selection over the very
     first period, e.g. by choosing 10 securities randomly;
     if we applied pause periods into this setting this would mean we wouldn't
     order this portfolio for the very first period, but wait over Period 1 and
     order this selection for Period 2; then either applying pause will
     disappear after Period 1, since usually after first pause period it was
     hidden, and we had continuity in holding securities, or we will apply
     pause after each holding period ends and before we rebalance, which would
     mean we would have discontinuities in holding securities

8) last case uses similar setting to (7), but holding_periods = 2;
   therefore again first rebalancing occurs before the first returns happen,
   on 01.01.2013, this selection will be held over 02.01.2013 and 03.01.2013;
   on 03.01.2013 we rebalance and hold this selection over 04.01 and 07.01;
   on 07.01.2013 we rebalance and hold this selection over 08.01 and 09.01;
   on 09.01.2013 we rebalance and hold this selection over 10.01.2013 only
   Thus we have 4 rebalancing days: 01.01.2013, 03.01.2013, 07.01.2013 and
   09.01.2013


################
STATIC STRATEGY
################
StaticStrategy is a PortfolioStrategy where Portfolio changes
only at specific points in time determined by the following strategy
attributes:
* ranking periods = number of periods used to compare certaing
                    characteristics of stocks
* pause periods = number of periods to wait after determining the portfolio
                  for the next holding period before actually holding it
* holding periods = number of periods to hold a given portfolio before next
                    rebalancing
* rebalancing frequency = frequency of periods used, influences the meaning
                          of all the above three attributes

StaticStrategy based on the above attributes determines:
* ranking days: days when we perform analysis of stock attributes to check
                which stocks will form our portfolio at the next
                rebalancing day
* rebalancing days: days when portfolio is changed (by assumption we change
                    portfolio structure on the evening of the day before
                    the first trading day when this portfolio is going to
                    be active)
* positions: most important, as for PortfolioStrategy

Portfolio size can also bounded by default.


##############
STOCK RETURNS
##############

Stock returns are contained in a class StockReturns, which takes total output
and optional return type (by default absolute return is used).
Initialized StockReturns give access to .monthly, .weekly, and .daily returns.


#########
BACKTEST
#########

Any kind of backtest class should perform only "overview" type of operations
using Portfolio/PortfolioStrategy objects


#################
DYNAMIC STRATEGY
#################
DynamicStrategy is a PortfolioStrategy where Portfolio can be adjusted
at every point in time (depending on specified frequency) according to a
specified methodology.

DynamicStrategy checks at every periods end for every stock if it matches
specified requirements, and if so, it adds this stock to a portfolio
(possible pause period before actually adding the stock can also be
specified) and holds it for a specified amount of holding periods


##########
PLOTTING:
##########

provides infrastructure to create plots of data coming from testing Bluevalor's
data
