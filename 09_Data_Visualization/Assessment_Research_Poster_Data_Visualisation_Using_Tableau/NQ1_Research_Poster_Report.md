# Trend, Volatility and Market States in E-mini Nasdaq-100 Futures, 1999–2026

**Module:** 7CS079 Data Visualisation — Research Poster: Data Visualisation Using Tableau
**Author:** Santiago Cruz | **Student ID:** 2584023 | University of Wolverhampton
**Dataset:** `CME_MINI_DL_NQ1!_1D.csv`, E-mini Nasdaq-100 continuous front-month futures (CME Globex), daily OHLC, 30 Jun 1999 – 30 Oct 2026. Source: TradingView. Cleaned to `NQ_clean_for_tableau.csv`.
**Supporting files:** `NQ1_Poster_Analysis.ipynb` (audit, metrics, robustness tests, reference charts), `ndx_poster_analysis.py` (the same pipeline as a script), `poster_visuals/V1–V6*.png`, `poster_visuals/poster_layout_A1_reference.png`

> **How to use this document.** This is the full working report. The brief caps the poster at
> 1,000 words (±10%) on A1, so the poster itself should use the condensed text in
> **Appendix C** and the layout in `poster_layout_A1_reference.png`. The longer sections below
> are your working evidence and speaker notes. Every figure quoted here comes from the executed
> outputs of `NQ1_Poster_Analysis.ipynb`. Appendix D maps each rubric criterion to where it is
> addressed.

---

## 1. Title

**Trend, Volatility and Market States in E-mini Nasdaq-100 Futures, 1999–2026**

The title names the three analytical themes (trend, volatility, market states), the instrument and the period in twelve words, without a decorative hook. It matches the three research objectives one-to-one, which makes the poster's structure predictable for the reader.

---

## 2. Introduction

### 2.1 Topic and significance

The NASDAQ-100 index tracks the hundred largest non-financial companies listed on the Nasdaq Stock Market and is the main benchmark for listed technology and growth equities (Nasdaq, 2024). Its most actively traded derivative is the CME E-mini Nasdaq-100 future (ticker NQ), which is worth $20 per index point and trades almost around the clock on CME Globex (CME Group, n.d.). Much of the index's price discovery outside stock-exchange hours happens in this contract, and it is where hedgers and leveraged traders take their exposure. The NQ contract therefore records what the market believed about the technology sector, day by day, from its launch in June 1999 to the present.

That record covers some of the most extreme episodes in modern market history. The contract began trading months before the dot-com peak. It then lost 83% of its value by October 2002 and took until August 2016 to regain the March 2000 high. It went on to absorb the 2008 financial crisis, the 2020 pandemic crash, the 2022 interest-rate shock and the April 2025 tariff shock, before reaching an all-time high of 31,483 on 6 October 2026.

### 2.2 Justification

Investment information is usually communicated through a single long-run average, such as "about 10% a year". For this market, that number is accurate yet misleading. It hides the depth and length of losses, the way risk arrives in bursts, and the frequency of extreme days. Millions of non-specialists now hold Nasdaq-100 exposure through tracker funds and pensions, often without seeing that risk profile. Data visualisation is well suited to closing this gap, because it can show distributions and sequences that a single statistic cannot (Tufte, 2001; Munzner, 2014). This poster applies the module's lifecycle of **data → story → audience → tools** to that communication problem.

### 2.3 Objectives, research questions and audience

| Objective | Research question | Visuals |
|---|---|---|
| **O1 Trend** | **RQ1** How deep and how long were the interruptions to the long-run trend? | V1, V2, V3 |
| **O2 Volatility** | **RQ2** Is risk spread evenly over time and across days, as a bell-curve model assumes? | V4, V5 |
| **O3 Market states** | **RQ3** Does a simple 252-day moving average separate calm from turbulent markets? | V6 |

**Audience:** non-specialists with exposure to the Nasdaq-100 (retail investors, pension savers and business students) and early-career traders. The poster therefore uses plain-language titles that state each finding, annotations instead of jargon, and headline-number tiles for the main results.

---

## 3. Data Source and Methodology

### 3.1 Data source and provenance

The dataset is a daily open-high-low-close (OHLC) history of the continuous front-month E-mini Nasdaq-100 futures contract (`CME_MINI:NQ1!`). It was exported from TradingView on 31 October 2026 (TradingView, 2026). TradingView redistributes CME Globex market data, so the original source is the exchange itself (CME Group, n.d.), which makes it a credible primary source for traded prices. The file contains public market prices only, so it raises no personal-data or ethics issues, and TradingView's terms permit personal, non-commercial use such as academic analysis.

| Column | Meaning | Unit |
|---|---|---|
| `time` | Trading date (session close) | M/D/YYYY |
| `open`, `high`, `low`, `close` | First, highest, lowest and settlement price of the front-month contract that day | Index points (×$20 per contract) |
| `MA_n_Close` | Simple moving average of `close` over n = 21, 63, 125, 252, 504, 756 sessions | Index points |
| `TSI_21_13`, `TSI_Signal_13` | True Strength Index and its signal line | Oscillator, −100 to +100 |
| `W%R_21_(OHLC)/4` | Williams %R on the OHLC average | Oscillator, −100 to 0 |

The file has 6,914 rows and no volume column.

### 3.2 Why this dataset

| Candidate | Strength | Weakness for this research | Decision |
|---|---|---|---|
| **NQ futures (chosen)** | Exchange-sourced; 27 years of daily OHLC; the instrument professionals trade | Contract rolls; excludes dividends | **Selected**: matches RQ1–RQ3 and is the market where tail risk is actually borne |
| NDX cash index | No rolls; longer history | Not directly tradable; the earlier file had joined exports and a 10-month gap | Used only as a cross-check of the futures data |
| QQQ ETF | Tradable by retail investors | Includes fund fees and dividends; also starts in 1999 | Not needed for these questions |
| Generic Kaggle extracts | Convenient | Provenance often unclear | Rejected |

### 3.3 Data audit and cleaning

The file was profiled in Python (`NQ1_Poster_Analysis.ipynb`, section 2) before being loaded into Tableau. Its structure is clean: one header row, no duplicate or unparseable dates, no missing prices, and no bar that breaks the Low ≤ Open, Close ≤ High rule. Four issues specific to futures data shaped the method:

| Issue found | Evidence | Treatment |
|---|---|---|
| Futures-only sessions | 38 rows fall on days the NYSE was closed: holidays, Good Fridays, and the closures for 9/11, Hurricane Sandy and the 2004, 2018 and 2025 state funerals. Median move 0.12% against 0.74% normally | Dropped, so every row is a full regular session |
| Bad print | 10 Apr 2000: open of 4031.66 is off the 0.25 tick grid and equals the high; close equals the low; −15.8% then +6.5%, while the cash index fell 7.1% that day | Dropped |
| Missing session | 2 Jul 1999 is absent | The return spanning it is set to missing |
| Off-tick or flat bars | 8 bars with off-grid prices and one flat bar (20 Dec 1999), all in 1999–2001 apart from one in 2008 | Kept and flagged; excluded from the daily-range measure |

The trading calendar comes from the open-source `exchange_calendars` library's NYSE schedule. After cleaning, 6,875 sessions remain, and only two returns are set to missing. Three checks support the result. The recomputed 252-day moving average differs from the file's own by a median of 0.013%. The largest daily moves fall on well-documented events: 3 January 2001 (+15.4%, an unscheduled Federal Reserve rate cut), October 2008 (bank rescues), 16 March 2020 (−11.5%) and 9 April 2025 (+11.2%, the tariff pause). And a comparison with the NASDAQ-100 cash index shows the futures price staying within about ±1% of the index for 27 years, with daily returns correlated at 0.975. This confirms that the series is an *unadjusted* continuous contract: small quarterly roll jumps remain, but there is no back-adjustment drift.

### 3.4 Derived measures

Seven fields were added for Tableau, both as columns in `NQ_clean_for_tableau.csv` and as equivalent Tableau calculated fields (Appendix A):

1. **Daily log return**, ln(Close_t / Close_t−1). Log returns are additive over time and are the standard input for volatility estimation (Cont, 2001).
2. **Moving averages** (21, 63, 252 and 756 sessions), recomputed on the cleaned closes.
3. **Drawdown**, the percentage decline from the highest close so far.
4. **21-day realised volatility**, the rolling standard deviation of log returns × √252, giving an annualised percentage.
5. **Daily range %**, (High − Low) / Close, an intraday risk measure related to Wilder's (1978) Average True Range.
6. **Trend regime**, "Above" or "Below" the 252-day moving average. The regime known at today's close is paired with *tomorrow's* return, so the comparison has no look-ahead bias.
7. **Data flag**, a text note on bars kept despite an anomaly, so they can be filtered in Tableau.

### 3.5 Visualisation method in Tableau

The workflow follows the module's lifecycle. **Data:** Python audit and export. **Story:** three research questions. **Audience:** non-specialists. **Tools:** Tableau for every poster chart, with PowerPoint for the A1 layout.

Tableau Desktop is the primary tool for both exploratory and explanatory work. The exploratory phase used Tableau's date hierarchy (year → quarter → month → day) to drill into crises, quick filters on date ranges to isolate episodes, and table calculations (`WINDOW_AVG`, `WINDOW_STDEV`, `RUNNING_MAX`, `LOOKUP`) and LOD expressions to rebuild the derived measures. Each chart type was then chosen for the job the data had to do (Week 5):

| Visual | Data's job | Chart type | Why this form |
|---|---|---|---|
| V1 | Change over time across a ×12 range | Line on a log axis | Equal heights mean equal percentage moves, so 2000 and 2020 can be compared fairly |
| V2 | Depth and duration of losses | Area ("underwater") | The filled area makes both depth and length visible at once |
| V3 | Comparing years with gains and losses | Diverging bar | Bars read as magnitudes; a blue/red pair encodes sign |
| V4 | Risk changing over time | Line with reference lines | The median and 90th-percentile lines turn a noisy series into calm and storm states |
| V5 | Shape of a distribution | Histogram with a normal curve on a log axis | Puts the tails, where the story is, in view |
| V6 | Comparing two states on four measures | Small multiples of paired bars | Each measure keeps its own scale without a dual axis |

Design decisions apply the five elements of informative visualisation (Week 2) and the palette guidance from Week 3. Each title states its conclusion, so the intended message comes first. The context of use is a poster read from about a metre away, so there are few labels, all direct. Every chart has a single y-axis and a recessive grey grid (Tufte, 2001; Kirk, 2016). What matters is emphasised with one saturated colour: blue for the market, orange for the reference measure. A **qualitative** pair (blue/orange) marks the regime, and a **diverging** blue/red pair marks gains and losses. It is never red/green, so it stays readable for viewers with colour-vision deficiency. A dashboard combining V1 and V4 with a shared date filter provides the interactive component covered in Week 7.

### 3.6 Statistical checks

To avoid over-claiming from in-sample charts, each headline finding was tested (notebook §5.8–5.9):

- the return difference between regimes, using a Welch t-test (Welch, 1947) and a bootstrap confidence interval (Efron, 1979);
- the volatility difference, using Levene's test (Levene, 1960);
- the regime split, repeated for 50-, 100-, 200- and 252-day averages and for 2000–2012 and 2013–2026 separately;
- fat tails, re-measured after excluding the noisier 1999–2002 data, and the tail weight estimated with a fitted Student-t distribution.

The Python notebook is used only to audit the data, test the findings and produce reference images. **All charts on the poster must be built in Tableau**, as the brief requires.

---

## 4. Key Visualisations and Results

The six visualisations follow the poster's narrative. V1–V3 answer RQ1, V4–V5 answer RQ2, and V6 answers RQ3. Reference renders are in `poster_visuals/`.

### V1. Long-run trend: *E-mini Nasdaq-100: a 27-year climb from the dot-com peak, through two deep bear markets*

- **Objective:** O1 / RQ1.
- **Chart type and layout:** a line chart; top-left in the chart grid. Continuous `Date` (day) on Columns; `Close` and `MA_252` on a single shared axis using Measure Names/Values, not a dual axis.
- **Axes:** x = "Date (daily)", 1999–2026. y = "Futures price, index points (log scale)", formatted 1,000 / 10,000.
- **Encoding:** daily settlement in blue (thin), 252-day moving average in orange (thicker). Annotations mark the March 2000 peak, the October 2002 trough (−83%), the November 2008 low and the October 2026 all-time high.
- **Caption:** *On a log scale, equal vertical distances mean equal percentage changes. From 2,325.50 at the end of June 1999, the contract rose to 28,534, about 12 times its starting level, or 9.6% a year in price terms. That average conceals a lost decade and a half: the March 2000 peak of 4,804 was not regained until 2016. Since 2009 the path has been steeper and steadier, with 2022 the only sustained break below the one-year average.*

### V2. Drawdown: *Drawdown from previous high: the March 2000 peak took 16 years to regain*

- **Objective:** O1 / RQ1.
- **Chart type and layout:** an area chart; top-right, with the same date axis as V1 so the two read as a pair.
- **Axes:** x = "Date (daily)". y = "Decline from running peak (%)", 0% to −100%, with zero at the top.
- **Encoding:** a single red fill. Each label quotes the episode's own peak-to-trough fall: dot-com bust −83% (24 Mar 2000 – 9 Oct 2002, regained 12 Aug 2016); GFC −54% (31 Oct 2007 – 20 Nov 2008); COVID-19 −28%; 2022 rate shock −35%; 2025 tariff shock −23%.
- **Caption:** *This chart shows how far the market sits below its previous high on each day. Buyers at the March 2000 peak waited 5,985 calendar days, more than 16 years, to break even. Later declines were sharp but recovered far faster: COVID in 107 days, the April 2025 tariff shock in 125 days, and the 2022 rate shock in about two years (753 days). Depth and duration are separate dimensions of risk, and average returns show neither.*

### V3. Annual returns: *Calendar-year return: 20 of 26 full years positive, but losses cluster in runs*

- **Objective:** O1 / RQ1.
- **Chart type and layout:** a vertical bar chart, one bar per year; middle-left.
- **Axes:** x = "Year". y = "Annual price return (%)", with a zero baseline and a dashed reference line at the full-year median (+17.4%).
- **Encoding:** a diverging blue (gain) / red (loss) scheme. The partial years (1999 from 30 June, +61.4%; 2026 year-to-date, +12.1%) are drawn lighter. Direct labels only on the extremes: 2003 +49%, 2008 −42%, 2022 −32%, 2023 +54%.
- **Caption:** *Twenty of the 26 full calendar years ended higher, with a median gain of 17%. The six losing years were not spread out: 2000, 2001 and 2002 fell one after another (−37%, −33%, −38%). Each later large loss was followed by a strong rebound: 2008's −42% by +53% in 2009, and 2022's −32% by +54% in 2023, the best year in the sample.*

### V4. Volatility regimes: *Volatility clusters: calm regimes punctuated by short, violent storms*

- **Objective:** O2 / RQ2.
- **Chart type and layout:** a line chart with reference lines; middle-right.
- **Axes:** x = "Date (daily)". y = "21-day realised volatility (annualised, %)", 0–118%.
- **Encoding:** a blue line. Reference lines at the median (18%) and the 90th percentile (40%, labelled "stress line"). An orange fill shows readings above the stress line, and the peaks are labelled: 2000–02 99%, 2008 95%, 2020 90%, 2025 58%.
- **Caption:** *Risk does not arrive evenly. Most of the time annualised volatility sits near its 18% median, but it periodically jumps three to five times higher, peaking at 99% on 4 January 2001. Storms persist: when volatility is above the stress line, there is a 65% chance it is still above it a month later, against a 10% base rate. Volatility also rises when prices fall: trailing one-month return and volatility are negatively correlated (−0.35).*

### V5. Return distribution: *Daily returns have fat tails: extreme days are far more common than a bell curve predicts*

- **Objective:** O2 / RQ2.
- **Chart type and layout:** a histogram with an overlaid reference curve; bottom-left.
- **Axes:** x = "Daily log return (%)", in bins of 0.25 percentage points. y = "Number of days (log scale)". The log scale makes the tails visible.
- **Encoding:** blue bars. An orange curve shows a normal distribution with the same mean and standard deviation. A text box gives the tail counts, and the two most extreme days are labelled (16 Mar 2020 −11.5%; 3 Jan 2001 +15.4%).
- **Caption:** *If daily returns followed a normal distribution, about 19 of the 6,872 trading days would move more than three standard deviations; the contract produced 117. Beyond four standard deviations the bell curve expects fewer than one such day; the data contain 47. Excess kurtosis is 7.1 and the Jarque-Bera test rejects normality decisively. Risk models that assume a bell curve will repeatedly underestimate how often crash days occur.*

### V6. Trend-regime scorecard: *Trend regimes: below its 252-day average, risk more than doubles and most crash days occur*

- **Objective:** O3 / RQ3.
- **Chart type and layout:** small multiples of four paired bar charts; bottom-right. A Tableau sheet with `Measure Names` on Columns and `Trend_Regime` on Colour, or four sheets on a dashboard strip.
- **Axes:** each panel has its own value scale, with values labelled directly on the bars and the y-axis hidden. Panel titles: "Share of trading days", "Annualised next-day return", "Annualised volatility", "Share of worst 1% of days".
- **Encoding:** blue = above the 252-day moving average, orange = below. The footnote states the no-look-ahead rule and the test results.
- **Caption:** *The contract settled above its one-year average on 74% of days, when volatility averaged 18%. Below it, volatility was 40%, and those days contained 87% of the worst 1% of sessions. This separation holds for every average length tested. The apparent return gap (+12.8% vs −7.0% a year) is not statistically significant and reverses after 2013, so the line works as a risk thermometer, not a return forecast.*

### Poster layout (A1 portrait)

`poster_visuals/poster_layout_A1_reference.png` shows the proposed layout at true A1 proportions (594 × 841 mm), built from the six reference charts:

- **Header band:** title, author, student ID, module and university, with a blue rule underneath.
- **Top row:** Introduction (with RQ1–RQ3), Data and Method, and four headline-number tiles (×12.3 growth; −83% worst fall; 117 vs 19 three-sigma days; 2.3× volatility below the trend line). The tiles let a passer-by take in the story in seconds.
- **Chart grid:** two columns by three rows, read left to right and top to bottom in objective order (O1, O1, O1, O2, O2, O3). Each chart has a one-sentence caption tagged with its objective.
- **Bottom row:** Discussion, Conclusion and References.

One font family, the same three colours as the charts and about 35% white space keep the poster balanced. In the final PowerPoint poster, replace each image with its Tableau export. Use a title of about 60 pt or more, body text of 20–24 pt, captions of at least 16 pt and chart labels of at least 14 pt at A1 size.

---

## 5. Discussion and Interpretation

### 5.1 Trend (RQ1)

V1 and V2 together show both the strength and the fragility of long-horizon equity exposure. A twelvefold rise in 27 years is a strong result, yet V2 shows that an investor's experience depended almost entirely on when they started. A buyer in March 2000 spent sixteen years under water; a buyer in October 2002 multiplied their stake about 35 times. The dot-com cycle fits Shiller's (2000) account of feedback-driven speculative bubbles: the contract rose 61% in its first six months of trading (V3), then collapsed by an amount proportionate to the earlier excess. Ofek and Richardson (2003) link the reversal to the expiry of share lock-ups and a wave of new supply in internet stocks, a mechanism visible here only as its price consequence. The post-2009 period looks different. Its drawdowns (2018, 2020, 2022, 2025) were sharp but shallower and recovered within months or a couple of years. That is consistent with an index now dominated by highly profitable, cash-generative firms, although this dataset alone cannot test that hypothesis. High volatility also coincides with poor years (correlation −0.65 between annual volatility and annual return), which links RQ1 to RQ2.

### 5.2 Volatility (RQ2)

V4 and V5 show two of the best-documented stylised facts of financial returns (Cont, 2001). The first is **volatility clustering**. Calm and turbulent periods each persist: absolute returns remain autocorrelated at 0.30 after one day and 0.18 after six months, while returns themselves are uncorrelated (−0.05). In plain terms, being in a storm today raises the chance of being in a storm a month from now from 10% to 65%. This is the empirical observation behind Engle's (1982) ARCH model and the GARCH family it inspired. Volatility also has a long-cycle component: the median 21-day reading was 36% in 2000–04 but only 14% in 2010–19.

The second fact is **heavy tails**, first described by Mandelbrot (1963) for commodity prices and clearly present here: 47 four-sigma days where a normal model expects fewer than one. This is not an artefact of the noisier early data: after 2003 the tails are even heavier (excess kurtosis 8.1; 83 three-sigma days against 16 expected), and a Student-t distribution fits with only about 2.5 degrees of freedom. Together the two charts explain why the 2001, 2008 and 2020 shocks felt "impossible" to practitioners using Gaussian risk measures. They were rare, but not nearly as rare as those models implied. The negative relationship between returns and later volatility (−0.35) is consistent with the leverage and volatility-feedback effects identified in the literature (Christie, 1982). For a leveraged futures position, where losses are marked to market daily, this asymmetry matters more than it does for a cash investor.

### 5.3 Market states (RQ3): what survives scrutiny

V6 suggests that the market does not behave as one stationary process. A critical reading, however, has to separate what the chart shows from what the data can support. The robustness tests (notebook §5.8) give a clear answer:

| Specification | Share of days below | Vol above | Vol below | Worst-1% days below | Return above | Return below | p (return) | p (volatility) |
|---|---|---|---|---|---|---|---|---|
| 50-day MA | 35% | 19.8% | 36.2% | 81% | +12.8% | +2.7% | 0.42 | 5e−117 |
| 100-day MA | 31% | 19.0% | 38.8% | 84% | +10.1% | +5.5% | 0.75 | 1e−163 |
| 200-day MA | 27% | 18.5% | 40.1% | 84% | +11.4% | −0.2% | 0.46 | 8e−192 |
| **252-day MA** | **26%** | **17.9%** | **40.5%** | **87%** | **+12.8%** | **−7.0%** | **0.22** | **2e−212** |
| 252-day, 2000–2012 | 38% | 18.4% | 42.7% | 97% | +8.4% | −20.1% | 0.17 | 1e−106 |
| 252-day, 2013–2026 | 14% | 17.5% | 34.6% | 51% | +15.8% | +24.2% | 0.74 | 6e−66 |

- **The risk separation is robust.** Volatility below the average is roughly double the volatility above it in every specification. Below-average days also hold a disproportionate share of the worst 1% of days, even in 2013–2026, when they made up only 14% of days but 51% of the worst days.
- **The return separation is not.** No specification gives a significant return difference. The bootstrap 95% interval for the 252-day gap runs from −11.4% to +51.1% a year. After 2013 the sign reverses, because sell-offs below the average were followed by sharp rebounds, the same pattern V3 shows for 2009 and 2023.
- **Whipsaw is real.** The price crossed the 252-day line 140 times, with a median spell of only 5 days, so trading each crossing would be costly.

The evidence therefore supports a narrower but stronger claim than an earlier draft of this poster made. The 252-day line identifies **risk states**, not reliably profitable or unprofitable ones. This is consistent with volatility clustering (Engle, 1982), with the conditional nature of momentum effects (Brock, Lakonishok and LeBaron, 1992; Moskowitz, Ooi and Pedersen, 2012; Faber, 2007), and with discrete state-switching models (Hamilton, 1989). It also fits the Adaptive Markets Hypothesis better than either extreme (Lo, 2004). Risk is predictable from public information, which the strong form of the Efficient Market Hypothesis would not lead one to expect (Fama, 1970). Return predictability, however, comes and goes.

### 5.4 The futures lens

Using futures rather than the cash index adds a dimension of its own. The NQ price tracked the index to within about ±1% throughout, but its premium moved with interest rates as cost-of-carry pricing predicts (Cornell and French, 1983; Hull, 2022). It was slightly negative in the near-zero-rate years after 2008 and about +0.5% to +0.7% in 2023–26. Futures returns therefore approximate the index's return minus the risk-free rate plus dividends, rather than the price return itself.

### 5.5 Implications for the audience

- **Investors and pension savers:** expect long, deep drawdowns as a normal feature of this market, not an anomaly. Time horizon and entry point matter as much as the average return.
- **Traders and risk managers:** size positions and margin buffers for fat tails and volatility persistence. A position that is safe at 18% volatility carries more than twice the risk when the market is below its 252-day average.
- **Dashboard designers:** show drawdown and rolling volatility beside price. A price chart alone tells the wrong story.

### 5.6 Limitations

- The series begins in June 1999, near the top of the bubble, which depresses the long-run growth rate and excludes earlier crises such as 1987.
- The unadjusted continuous contract includes small quarterly roll jumps, and futures returns exclude dividends net of financing.
- Early pit-era settlement times do not align exactly with the cash close, which adds noise to 1999–2002 returns (MacKinlay and Ramaswamy, 1988).
- The regime statistics are in-sample and ignore transaction costs and roll slippage. The significance tests assume independent days, which volatility clustering partly violates, so the p-values are approximate.
- The index's composition has changed substantially, so earlier and later periods are not strictly comparable.
- Because the data are a single time series, the charts describe *what happened*, not *why*. The links to the dot-com bubble, the financial crisis and the pandemic depend on external historical sources (Baker et al., 2020).

---

## 6. Conclusion

### 6.1 Answers to the research questions

- **RQ1 (trend):** the interruptions were deep and very uneven in length. The dot-com bust took 83% off the price and lasted 16.4 years from peak to recovery; the GFC took 54% and 3.2 years. Post-2009 shocks of 23–35% recovered within 3.5 months to 2 years. Long-run growth (×12.3, 9.6% a year) therefore depended heavily on the entry date.
- **RQ2 (volatility):** risk is neither steady nor bell-shaped. It clusters (a 65% chance of continued stress, against a 10% base rate), rises when prices fall, and has fat tails (117 three-sigma days against 19 expected; 47 four-sigma days against 0.4).
- **RQ3 (market states):** yes for risk, no for returns. Below the 252-day average, volatility more than doubles (40% vs 18%) and 87% of the worst days occur, robustly across every specification. The return difference is not statistically significant and reverses after 2013.

### 6.2 Recommendations

Dashboards that track this market should show drawdown and rolling volatility alongside price, because a price chart alone hides the investor's experience. Risk summaries and margin planning for futures positions should use fat-tailed or empirical measures rather than assuming a bell curve. A visible regime indicator, such as distance from the 252-day average, is a useful context layer for a non-specialist audience, provided it is presented as a risk thermometer rather than a trading signal. As of 30 October 2026 the contract sits 9.4% below its 6 October all-time high, 3.6% above its 252-day average, with volatility at 23%. By this framework it is in a correction within a calm-to-normal risk state, not a regime change.

### 6.3 Future work

A back-adjusted or individual-contract series would remove roll effects, and comparing it with the total-return index would separate dividends from financing. GARCH volatility forecasts and Markov regime-switching models (Hamilton, 1989) could formalise the states shown here, and could be added through Tableau's R/Python integration. And an interactive Tableau Public dashboard with linked date filters would let viewers explore each crisis themselves, in line with the module's emphasis on interactive storytelling.

---

## References (Harvard)

> Verify each entry yourself before submission. All are real publications; DOIs are given where
> they exist. Add access dates where shown.

- Baker, S.R., Bloom, N., Davis, S.J., Kost, K., Sammon, M. and Viratyosin, T. (2020) 'The unprecedented stock market reaction to COVID-19', *Review of Asset Pricing Studies*, 10(4), pp. 742–758. doi:10.1093/rapstu/raaa008.
- Brock, W., Lakonishok, J. and LeBaron, B. (1992) 'Simple technical trading rules and the stochastic properties of stock returns', *Journal of Finance*, 47(5), pp. 1731–1764. doi:10.1111/j.1540-6261.1992.tb04681.x.
- Christie, A.A. (1982) 'The stochastic behavior of common stock variances: value, leverage and interest rate effects', *Journal of Financial Economics*, 10(4), pp. 407–432. doi:10.1016/0304-405X(82)90018-6.
- CME Group (n.d.) *E-mini Nasdaq-100 Futures Contract Specs*. Available at: https://www.cmegroup.com/markets/equities/nasdaq/e-mini-nasdaq-100.contractSpecs.html (Accessed: [date]).
- Cont, R. (2001) 'Empirical properties of asset returns: stylized facts and statistical issues', *Quantitative Finance*, 1(2), pp. 223–236. doi:10.1080/713665670.
- Cornell, B. and French, K.R. (1983) 'The pricing of stock index futures', *Journal of Futures Markets*, 3(1), pp. 1–14. doi:10.1002/fut.3990030102.
- Efron, B. (1979) 'Bootstrap methods: another look at the jackknife', *Annals of Statistics*, 7(1), pp. 1–26. doi:10.1214/aos/1176344552.
- Engle, R.F. (1982) 'Autoregressive conditional heteroscedasticity with estimates of the variance of United Kingdom inflation', *Econometrica*, 50(4), pp. 987–1007. doi:10.2307/1912773.
- Faber, M.T. (2007) 'A quantitative approach to tactical asset allocation', *Journal of Wealth Management*, 9(4), pp. 69–79. doi:10.3905/jwm.2007.674809.
- Fama, E.F. (1970) 'Efficient capital markets: a review of theory and empirical work', *Journal of Finance*, 25(2), pp. 383–417. doi:10.2307/2325486.
- Hamilton, J.D. (1989) 'A new approach to the economic analysis of nonstationary time series and the business cycle', *Econometrica*, 57(2), pp. 357–384. doi:10.2307/1912559.
- Hull, J.C. (2022) *Options, Futures, and Other Derivatives*. 11th edn. Harlow: Pearson.
- Kirk, A. (2016) *Data Visualisation: A Handbook for Data Driven Design*. London: SAGE.
- Levene, H. (1960) 'Robust tests for equality of variances', in Olkin, I. (ed.) *Contributions to Probability and Statistics: Essays in Honor of Harold Hotelling*. Stanford, CA: Stanford University Press, pp. 278–292.
- Lo, A.W. (2004) 'The adaptive markets hypothesis', *Journal of Portfolio Management*, 30(5), pp. 15–29. doi:10.3905/jpm.2004.442611.
- MacKinlay, A.C. and Ramaswamy, K. (1988) 'Index-futures arbitrage and the behavior of stock index futures prices', *Review of Financial Studies*, 1(2), pp. 137–158. doi:10.1093/rfs/1.2.137.
- Mandelbrot, B. (1963) 'The variation of certain speculative prices', *Journal of Business*, 36(4), pp. 394–419. doi:10.1086/294632.
- Moskowitz, T.J., Ooi, Y.H. and Pedersen, L.H. (2012) 'Time series momentum', *Journal of Financial Economics*, 104(2), pp. 228–250. doi:10.1016/j.jfineco.2011.11.003.
- Munzner, T. (2014) *Visualization Analysis and Design*. Boca Raton: CRC Press. doi:10.1201/b17511.
- Nasdaq (2024) *Nasdaq-100 Index Methodology*. Available at: https://indexes.nasdaqomx.com/docs/Methodology_NDX.pdf (Accessed: [date]).
- Ofek, E. and Richardson, M. (2003) 'DotCom mania: the rise and fall of internet stock prices', *Journal of Finance*, 58(3), pp. 1113–1137. doi:10.1111/1540-6261.00560.
- Shiller, R.J. (2000) *Irrational Exuberance*. Princeton: Princeton University Press.
- Tableau (n.d.) *Transform Values with Table Calculations*. Available at: https://help.tableau.com/current/pro/desktop/en-us/calculations_tablecalculations.htm (Accessed: [date]).
- TradingView (2026) *E-mini Nasdaq-100 Futures continuous contract (CME_MINI:NQ1!), daily OHLC data*. Available at: https://www.tradingview.com/symbols/CME_MINI-NQ1!/ (Accessed: 31 October 2026).
- Tufte, E.R. (2001) *The Visual Display of Quantitative Information*. 2nd edn. Cheshire, CT: Graphics Press.
- Welch, B.L. (1947) 'The generalization of "Student's" problem when several different population variances are involved', *Biometrika*, 34(1–2), pp. 28–35. doi:10.1093/biomet/34.1-2.28.
- Wilder, J.W. (1978) *New Concepts in Technical Trading Systems*. Greensboro, NC: Trend Research.

---

## Appendix A. Tableau build notes

Connect to `NQ_clean_for_tableau.csv` (Text file). Set `Date` to Date, and `Trend_Regime` and `Data_Flag` to string dimensions. The pre-computed columns let every chart be built with drag-and-drop. The calculated fields below reproduce them inside Tableau as evidence of method; compute table calculations *along Table (across)* with `Date` at day level.

| Field | Tableau formula |
|---|---|
| Log Return (TC) | `LN(SUM([Close]) / LOOKUP(SUM([Close]), -1))` |
| MA 252 (TC) | `WINDOW_AVG(SUM([Close]), -251, 0)` |
| Drawdown (TC) | `SUM([Close]) / RUNNING_MAX(SUM([Close])) - 1` |
| Rolling Vol 21d (TC) | `WINDOW_STDEV([Log Return (TC)], -20, 0) * SQRT(252)` |
| Daily Range % | `([High] - [Low]) / [Close]` (filter `[Data_Flag] = ""`) |
| Regime | `IF [Close] > [MA_252] THEN "Above 252-day MA" ELSE "Below 252-day MA" END` |
| Year-End Close (LOD) | `{FIXED YEAR([Date]) : MAX(IF [Date] = {FIXED YEAR([Date]) : MAX([Date])} THEN [Close] END)}` |
| Annual Return | `MIN([Year-End Close (LOD)])` with Quick Table Calculation → Percent Difference |
| Partial-year flag | `IF YEAR([Date]) = 1999 OR YEAR([Date]) = 2026 THEN "Partial" ELSE "Full" END` (use on Opacity) |
| Return bins | Right-click `Log_Return` → Create → Bins, size 0.0025 |
| Above-stress flag | `[Rolling_Vol_21d_Ann] > 0.40` (colour the area) |

Sheet recipes:

- **V1:** Columns `DAY(Date)` (continuous). Rows `Measure Values` filtered to `Close`, `MA_252`. Axis → Logarithmic. Annotate → Point.
- **V2:** Rows `Drawdown`, mark Area. Axis fixed −1 to 0, number format percentage.
- **V3:** Columns `YEAR(Date)` (discrete), Rows `Annual Return`, colour by sign, `Partial-year flag` on opacity. Analytics → Reference Line → Median (exclude partial years).
- **V4:** Rows `Rolling_Vol_21d_Ann`. Analytics → two Reference Lines, at the Median and at the 90th percentile (Distribution).
- **V5:** Columns `Log_Return (bin)`, Rows `CNT(Log_Return)`, y-axis log. Add the normal curve via a calculated field `[N] * 0.0025 * EXP(-0.5*(([bin]-[mean])/[sd])^2) / ([sd]*SQRT(2*PI()))` on a combined (not dual) axis, or describe it in the text box if time is short.
- **V6:** Columns `Measure Names` (the four metrics, built as aggregate fields), Rows `Measure Values`, Colour `Trend_Regime`, labels on. Put the significance note in the caption.
- **Dashboard:** V1 + V4 with a shared `Date` range filter applied to both sheets (Week 7 interactivity). Publish to Tableau Public and add the link or a QR code on the poster.
- **Formatting for A1:** Format → Workbook → one font (e.g. Tableau Book); worksheet titles about 20 pt, axis labels about 14 pt; export each sheet as an image at 300 dpi (Worksheet → Export → Image).

## Appendix B. Key numbers (from `NQ1_Poster_Analysis.ipynb`)

| Measure | Value |
|---|---|
| Sessions after cleaning | 6,875 (30 Jun 1999 – 30 Oct 2026); 39 rows dropped, 2 returns set to missing |
| Start / end settlement | 2,325.50 → 28,534.00 (×12.3) |
| Price CAGR / annualised volatility | 9.6% / 26.7% |
| Skew / excess kurtosis | −0.02 / 7.10 (Jarque-Bera 14,441, p ≈ 0); 8.1 for 2003–2026 |
| Days beyond ±3σ / ±4σ | 117 (normal 19) / 47 (normal 0.4) |
| Student-t degrees of freedom (fitted) | 2.5 |
| Largest daily moves | +15.4% (3 Jan 2001); −11.5% (16 Mar 2020) |
| Max drawdown | −83.1% (24 Mar 2000 → 9 Oct 2002; regained 12 Aug 2016, 5,985 days) |
| Other drawdowns | GFC −53.9%; 2022 −35.3%; COVID −28.4%; Q4 2018 −23.2%; 2025 −22.5% |
| All-time high | 31,483.25 on 6 Oct 2026; −9.4% and +3.6% vs 252-day MA on 30 Oct 2026 |
| Positive full years / median | 20 of 26 (2000–2025) / +17.4% |
| Best / worst full year | 2023 +54.4% / 2008 −42.4% |
| 21-day vol median / 90th pct / max | 18.1% / 40.0% / 98.9% (4 Jan 2001) |
| Autocorrelation of returns / absolute returns (lag 1) | −0.05 / 0.30 |
| P(stress in 21 days given stress today) | 65% (base rate 10%) |
| Annual volatility vs annual return correlation | −0.65 |
| Above vs below 252-day MA | 74% vs 26% of days; 17.9% vs 40.5% vol (Levene p ≈ 2e−212); 13% vs 87% of worst-1% days |
| Return gap above vs below | +12.8% vs −7.0% a year; Welch p = 0.22; bootstrap 95% interval −11.4% to +51.1% |
| Regime crossings / median spell | 140 / 5 days |

---

## Appendix C. Condensed poster text

> About 560 words of body text. The brief's range is 900–1,100 words, so roughly 340–540 words
> are left for chart titles, axis labels, the headline-number tiles and references. The A1
> reference layout uses a still shorter version of this text.

**Trend, Volatility and Market States in E-mini Nasdaq-100 Futures, 1999–2026**
Santiago Cruz · 2584023 · University of Wolverhampton

**Introduction.** The E-mini Nasdaq-100 future (NQ) is the most heavily traded derivative on the NASDAQ-100, the benchmark for technology stocks (Nasdaq, 2024; CME Group, n.d.). Since 1999 it has risen twelvefold, yet it also lost 83% in 2000–02. Long-run averages hide this. Using Tableau, this poster asks: **RQ1** How deep and long were the trend's interruptions? **RQ2** Is risk spread evenly over time and days? **RQ3** Does the 252-day moving average separate calm from turbulent markets?

**Data and Method.** Daily OHLC prices of the continuous front-month NQ contract, June 1999 – October 2026, from TradingView (2026), sourced from CME Globex. A Python audit removed 38 futures-only holiday sessions and one bad print, and flagged nine anomalous bars, leaving 6,875 sessions. Returns, drawdown, rolling volatility and a regime flag were built as Tableau calculated fields (LOOKUP, WINDOW_STDEV, RUNNING_MAX, LOD). Each chart states its finding in the title, uses one axis and a colour-blind-safe palette (Tufte, 2001; Munzner, 2014). Findings were tested for statistical significance and robustness.

**Headline numbers.** ×12.3 growth (9.6% a year) · −83% worst fall, regained after 16 years · 117 three-sigma days vs 19 expected · 2.3× volatility below the trend line.

**V1 caption.** On a log scale, equal heights mean equal percentage moves. Twelvefold growth, but the March 2000 peak was not regained until 2016.

**V2 caption.** The dot-com bust (−83%) took 16 years to recover. Later shocks recovered far faster: COVID (−28%) in 107 days, 2025 (−23%) in 125 days, 2022 (−35%) in two years.

**V3 caption.** 20 of 26 full years rose (median +17%), but losses cluster (2000–02), and the worst years were followed by rebounds of more than 50%.

**V4 caption.** Volatility clusters around an 18% median, with storms near 100%. In a storm, there is a 65% chance of still being in one a month later.

**V5 caption.** Fat tails: 47 four-sigma days where a bell curve expects fewer than one. Normal-based risk models understate crash risk.

**V6 caption.** Below its 252-day average, volatility is 40% vs 18%, and 87% of the worst days occur, across every average length tested. The return gap is not significant (p = 0.22): a risk signal, not a forecast.

**Discussion.** Entry date mattered as much as holding period: the same market produced a sixteen-year loss and a 35-fold gain. Volatility clustering and fat tails reproduce the stylised facts of returns (Mandelbrot, 1963; Engle, 1982; Cont, 2001), and they persist after 2003, so they are not an artefact of the early data. The trend line robustly separates risk states, but return differences are not significant and reverse after 2013. This fits the Adaptive Markets Hypothesis (Lo, 2004) better than either strict efficiency (Fama, 1970) or a simple trading rule (Brock, Lakonishok and LeBaron, 1992). Limitations: the series starts at the bubble peak, futures returns include roll jumps and exclude dividends, and the tests are in-sample.

**Conclusion.** The market's long-run growth came with deep, clustered and fat-tailed risk. Investors should expect long drawdowns; risk and margin planning should not assume a bell curve; and dashboards should show drawdown and rolling volatility beside price, with the 252-day line as a risk thermometer. Future work: roll-adjusted data, GARCH and regime-switching models, and a Tableau Public dashboard.

**References:** [selected Harvard entries from the full list].

---

## Appendix D. Rubric alignment checklist

| Criterion (marks) | Distinction descriptor | Where it is met | Still to do before submission |
|---|---|---|---|
| Title, introduction and background (15) | Concise, descriptive title; strong justification; clear objectives | §1 (12-word descriptive title matching the three objectives); §2.2 justification (the averages problem, non-specialist exposure); §2.3 objectives, research questions and audience | Keep the title identical on the poster, report and Tableau workbook |
| Data source and methodology (15) | Credible, cited sources; logical explanation of data selection and visualisation methods, including Tableau | §3.1 exchange-sourced data via TradingView with a data dictionary; §3.2 dataset comparison; §3.3 audit; §3.5 chart-choice table and design rationale; §3.6 statistical checks; Appendix A Tableau recipes | Add access dates to the CME, Nasdaq and Tableau references |
| Quality of visualisations and integration (30) | Clear, accurate, professional; strongly support objectives; well-integrated, labelled, balanced | Six charts, each mapped to an RQ; conclusion-stating titles; one axis; direct labels; colour-blind-safe; V6 claim corrected to what the tests support; A1 layout reference | Build all six in Tableau; export at 300 dpi; check fonts are legible at A1 |
| Analysis, discussion and critical thinking (25) | Thorough interpretation; well-justified findings tied to objectives; critical thinking, meaningful conclusions and implications | §5.1–5.3 interpretation linked to theory; robustness table with significance tests; §5.5 audience implications; §5.6 limitations; §6.1 explicit answers to RQ1–RQ3 | Be ready to explain why the return gap is not significant if asked |
| Layout, text–visual balance and aesthetics (15) | Well organised, clear headings; minimal concise text; consistent fonts and colours | A1 layout: header band, three top panels, 2 × 3 chart grid, bottom panels; headline tiles; about 35% white space; one font family; consistent palette | Proofread; keep total poster text within 900–1,100 words |
