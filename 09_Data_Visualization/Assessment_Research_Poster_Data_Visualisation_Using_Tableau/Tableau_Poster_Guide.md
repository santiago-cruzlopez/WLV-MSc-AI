# Step-by-Step Guide: Building the A1 Poster with Tableau

**What you will produce:**
1. Six Tableau charts (V1–V6) and one interactive dashboard.
2. A saved Tableau workbook as evidence.
3. An A1 poster PDF to upload to Canvas.

**Time needed:** about 6–8 hours. **Deadline:** 2 Nov 2026, 14:00 UK time.

**The workflow:** build the charts in Tableau, export them as images, then assemble the A1 poster in PowerPoint or LibreOffice. This is the method taught in Week 4 ("Poster Designing in MS PowerPoint … Importing Tableau charts and graphs"), and it is the reliable way to get an exact A1 page with your text, headings and references.

---

## Step 1. Choose how you will run Tableau

**Important:** Tableau Desktop installs only on **Windows or macOS**. It will not install on your Ubuntu computer. Pick one option:

| Option | Works on | Cost | Speed to start | Saves a workbook locally? | Recommended when |
|---|---|---|---|---|---|
| **A. Tableau Public in the browser ("web authoring")** | Any computer, including Linux | Free | Minutes | No; saved to your Tableau Public profile (public) | **You only have the Linux machine.** Fastest route |
| B. Tableau Desktop Public Edition | Windows / macOS | Free | About 20 minutes | Saves to Tableau Public | You have a Windows/Mac laptop and want the full interface |
| C. Tableau Desktop 14-day free trial | Windows / macOS | Free for 14 days | About 20 minutes | Yes (`.twbx`) and PDF export | You have Windows/Mac and want a local `.twbx` as evidence |
| D. Tableau for Students licence | Windows / macOS | Free for a year | **Verification can take days** | Yes | Long-term use; probably too slow for this deadline |

Links:
- Tableau Public (sign up, and the browser editor): https://public.tableau.com
- Tableau Desktop Public Edition download: https://www.tableau.com/products/public/download
- Tableau Desktop free trial: https://www.tableau.com/products/trial (the module page uses https://www.tableau.com/en-gb/trial/tableau-software)
- Tableau for Students: https://www.tableau.com/academic/students
- Tableau releases and versions: https://www.tableau.com/support/releases

> **Privacy note for Option A/B:** anything saved to Tableau Public is visible to anyone. That is
> fine here, because the data are public market prices, but do not upload anything private.

### 1.1 Create your account (all options)

1. Go to https://public.tableau.com and click **Sign Up**. For Options C/D, use the trial or student link instead.
2. Use your university email if possible, choose a password and verify the email Tableau sends you.
3. Sign in.

### 1.2 Open Tableau

- **Option A (browser):** on public.tableau.com, click **Create** (top menu) → **Web Authoring**. A blank workbook opens and asks you to connect to data.
- **Options B/C:** download and run the installer from the link above, open Tableau and sign in when asked.

Menu names can differ slightly between the browser and Desktop versions. The steps below give the Desktop wording, with browser differences noted.

---

## Step 2. Gather the four data files

All four are in the `spreadsheets_assessment/` folder and are produced by `NQ1_Poster_Analysis.ipynb`:

| File | Used for | Rows |
|---|---|---|
| `NQ_clean_for_tableau.csv` | V1, V2, V4 and the dashboard (daily data) | 6,875 |
| `NQ_annual_returns.csv` | V3 (annual returns) | 28 |
| `NQ_return_histogram.csv` | V5 (histogram and normal curve) | 116 |
| `NQ_regime_summary.csv` | V6 (regime scorecard) | 8 |

If you work on another computer, copy these four files to it (USB stick, email or cloud drive).

---

## Step 3. Connect the data

1. **Connect:** in the connect screen choose **Text file** (Desktop) or **Upload from computer / Files** (browser), and select `NQ_clean_for_tableau.csv`.
2. **Check the field types** on the Data Source tab. Click the small type icon above a column to change it.
   - `Date` must be a **Date** (calendar icon). If it shows "Abc", change it to Date.
   - `Trend_Regime` and `Data_Flag` must be strings (Abc).
   - All other columns must be numbers (#).
3. **Add the other three files:** for each one, go to **Data → New Data Source** (browser: the "+" next to Data) and connect it.
   - `NQ_annual_returns.csv`: make `Year` a **string** (Abc) so it behaves as a category, not a number.
   - `NQ_return_histogram.csv` and `NQ_regime_summary.csv`: keep the default types.
4. Click **Sheet 1** to start building.

> **The single most important setting:** when you drag `Date` onto a shelf, Tableau groups it by
> YEAR by default. For daily charts, right-click the `Date` pill → choose **Exact Date**, then
> make sure it is **Continuous** (a green pill). Otherwise Tableau will add up thousands of days
> into one point per year.

---

## Step 4. Set the look once (consistency matters for the "Aesthetics" marks)

- **Font:** use one font family everywhere. In Desktop, go to **Format → Workbook** and choose *Tableau Book* or *Arial*. Use the same family in the poster.
- **Colours:** use the same meaning in every chart.
  - **Blue** = the market or "above the trend". **Orange** = the reference line, or "below the trend". **Red** = losses or drawdown.
  - Easiest: Tableau's built-in **Color Blind** palette (in Edit Colors), which is blue and orange.
  - Exact hex values used in the reference charts: blue `#2a78d6`, orange `#eb6834`, red `#d03b3b`, grey `#898781`.
  - Never use a red/green pair; it is unreadable for colour-blind viewers.
- **Titles:** double-click each sheet title and type the finding, not just a label. The exact titles are listed below.
- **Gridlines:** go to Format → Lines and make the grid light grey, or remove it.

---

## Step 5. Build the six charts (explained simply)

This step explains every click, in plain words. Go slowly, one chart at a time. After each chart, compare it with the matching picture in `poster_visuals/`. Yours does not have to be identical, just close.

> **Ready-made workbook or build it yourself?** `Tableau_Workbook/NQ1_Poster.twbx` already has the six
> charts started. Building them yourself with this step is better: your poster says the measures were
> built as **Tableau calculated fields**, and Step 5.2 is where you actually do that. You can open the
> ready-made workbook beside yours to compare.

### 5.1 The Tableau words you need

When you open a sheet, the screen looks roughly like this:

```
┌──────────────┬────────────────────────────────────────────────────┐
│  DATA PANE   │  Columns  [ things here go LEFT → RIGHT ]          │
│ (a list of   │  Rows     [ things here go BOTTOM → TOP ]          │
│ your columns)├──────────────┬─────────────────────────────────────┤
│              │  MARKS CARD  │                                     │
│  Date        │  [Line    ▼] │                                     │
│  Close       │  Color  Size │      YOUR CHART APPEARS HERE        │
│  MA 252      │  Label Detail│                                     │
│  ...         │  Tooltip     │                                     │
└──────────────┴──────────────┴─────────────────────────────────────┘
   [Data Source]  [V1 Price trend]  [V2 ...]   ← sheet tabs at the bottom
```

| Word | What it means |
|---|---|
| **Data pane** | The list on the left. Every column of your CSV file is there. At the top it says **Data** and, next to it, **Analytics**. |
| **Drag** | Click a field and **hold the mouse button down**, move it to the right place, then let go. |
| **Shelf** | A strip where you drop fields: **Columns** (the left-to-right direction) and **Rows** (the up-and-down direction). |
| **Pill** | When you drop a field on a shelf, it turns into a rounded box called a pill. Each pill has a small **▼ arrow** on its right; click it to change settings. |
| **Blue pill / green pill** | **Blue = discrete**: separate boxes, like Lego bricks (years, names). **Green = continuous**: a smooth ruler, like a timeline or a number line. |
| **Marks card** | The panel beside the chart. The drop-down at the top chooses the shape (Line, Bar, Area). The buttons (**Color, Size, Label, Detail**) are boxes you drop fields onto to colour or label the chart. |
| **Axis** | The numbers along the side or bottom of a chart. Right-click them for **Edit Axis** and **Format**. |
| **Calculated field** | A new column that Tableau works out from a formula, like a recipe for a calculator. |
| **Sheet tab** | The tabs along the bottom. One sheet holds one chart. |

**Three golden rules:**
1. Made a mistake? Press **Ctrl + Z** (undo). You can undo as many times as you like.
2. Save often: **Ctrl + S**. Choose **Tableau Packaged Workbook (.twbx)** the first time.
3. To make a new sheet, click the small **New Worksheet** icon at the bottom (it looks like a little chart with a +). To rename a sheet, right-click its tab → **Rename**.

**Colours you will use** (in the colour box, type these numbers in the Red, Green and Blue boxes):

| Colour | Means | Red, Green, Blue | Hex |
|---|---|---|---|
| Blue | the market, "above the trend", gains | 42, 120, 214 | `#2a78d6` |
| Orange | the reference line, "below the trend" | 235, 104, 52 | `#eb6834` |
| Red | losses and drawdown | 208, 59, 59 | `#d03b3b` |
| Grey | median lines and notes | 137, 135, 129 | `#898781` |

**Quick way to set a colour:** click **Color** on the Marks card → **Edit Colors…**. On the left, click the item, for example "Close". On the right, click any square. Then **double-click** the item on the left: a colour box opens where you can type the Red, Green and Blue numbers. Click **OK** twice. If there is only one colour (one line), click **Color** and pick the square in the little pop-up, or click **More Colors…** to type the numbers.

### 5.2 Make the calculated fields (do this once)

**What and why:** the CSV already contains the answers, which Python calculated. Here you make Tableau calculate them itself, so the sentence on your poster ("built as Tableau calculated fields") is true. You will use these fields in V1, V2 and V4.

**How to make one:**
1. Make sure the data source at the top of the Data pane is **NQ_clean_for_tableau**.
2. Top menu: **Analysis → Create Calculated Field…**
3. A small window opens. In the **top box**, type the name. In the **big box**, type (or paste) the formula exactly as shown.
4. Look at the bottom-left: it must say **"The calculation is valid."** If it shows red text, check the spelling and the brackets.
5. Click **OK**. The new field appears in the Data pane with an **=** sign next to its icon.

Make these six:

| # | Name (top box) | Formula (big box) | In plain words |
|---|---|---|---|
| 1 | `Log Return (TC)` | `LN(SUM([Close]) / LOOKUP(SUM([Close]), -1))` | Today's price divided by yesterday's price. `LOOKUP(…, -1)` means "the row before me". |
| 2 | `MA 252 (TC)` | `IF INDEX() >= 252 THEN WINDOW_AVG(SUM([Close]), -251, 0) END` | The average price of the last 252 trading days (about one year). It stays blank until there are 252 days to average. |
| 3 | `Drawdown (TC)` | `SUM([Close]) / RUNNING_MAX(SUM([Close])) - 1` | How far today's price is below the highest price so far. `RUNNING_MAX` is "the record high up to today". |
| 4 | `Rolling Vol 21d (TC)` | `WINDOW_STDEV([Log Return (TC)], -20, 0) * SQRT(252)` | How bumpy the last 21 days were, scaled to a year. Make field 1 first, because this one uses it. |
| 5 | `Regime` | `IF ISNULL([MA 252]) THEN "n/a" ELSEIF [Close] > [MA 252] THEN "Above 252-day MA" ELSE "Below 252-day MA" END` | Is the price above or below its one-year average today? |
| 6 | `Year-End Close (LOD)` | `{FIXED YEAR([Date]) : MAX(IF [Date] = {FIXED YEAR([Date]) : MAX([Date])} THEN [Close] END)}` | The last price of each year. The `{FIXED …}` part is an LOD expression: "for each year, find…". You will use it to check V3. |

> **Why fields 1–4 need Date at day level:** they are *table calculations* (TC). They work along the
> chart from left to right, one day at a time. They give the right answer only when **Date** is on
> Columns as **Exact Date** and **Continuous** (a green pill that just says `Date`). Every recipe below
> sets this up.

### 5.3 The one setting you will use in V1, V2 and V4: "Date as a timeline"

When you drop **Date** on Columns, Tableau groups it into years (`YEAR(Date)`, blue pill) and you get only 28 points. Change it like this:
1. Click the **▼ arrow** on the `YEAR(Date)` pill.
2. In the menu, click **Exact Date**.
3. Click the **▼ arrow** again and click **Continuous**. The pill turns **green** and says just `Date`.

---

### V1. Price trend with 252-day moving average

**What it shows:** the price over 27 years (blue), with its one-year average (orange) on top.
**Data:** `NQ_clean_for_tableau`. **Picture to copy:** `poster_visuals/V1_price_trend_log_ma252.png`.

1. Make a new sheet and rename it **V1 Price trend**.
2. Drag **Date** to **Columns**, then make it a timeline (Step 5.3).
3. Drag **Close** to **Rows**. A blue line appears. That's the price.
4. Now add the average **on the same axis**. Drag **MA 252 (TC)** onto the **numbers on the left side** of the chart (the axis). Move it slowly until you see a little **double ruler** icon, then let go.
   - It worked if the Rows shelf now says **Measure Values** and you see two lines.
   - If you got two separate charts stacked on top of each other instead, press **Ctrl + Z** and try again, dropping exactly on the axis numbers.
5. On the Marks card, set the drop-down to **Line**.
6. **Colours:** **Color → Edit Colors…** → set **Close** to blue and **MA 252 (TC)** to orange (Step 5.1).
7. **Make the average line thicker:** click **Size** and move the slider a little to the right.
8. **Log scale** (each step up the axis is "×10", so early and late years are equally easy to read): right-click the left axis numbers → **Edit Axis…** → under *Scale* tick **Logarithmic**. In *Axis Titles* → Title, type `Futures price, index points (log scale)`. Close the window.
9. **Bottom axis:** right-click the date axis → **Edit Axis…** → Title: delete the text (dates need no title).
10. **Title:** double-click the title at the top of the sheet → select all the text → type: **E-mini Nasdaq-100: a 27-year climb from the dot-com peak, through two deep bear markets** → **OK**.
11. **Notes on the chart (annotations):** hover over the line until the little tooltip shows the right date. Right-click that point → **Annotate → Point…** → type the note → **OK**. Then drag the note box to an empty spot. Add four notes:
    - 24 Mar 2000 → `Mar 2000 peak`
    - 9 Oct 2002 → `Oct 2002 trough (−83%)`
    - Nov 2008 (the lowest point that year) → `Nov 2008 low`
    - the last point → `Oct 2026 all-time high`
12. **Check:** hover over the last point. Close should be **28,534** and MA 252 (TC) about **27,536**. The orange line starts about a year after the blue one; that's correct.

### V2. Drawdown from previous high

**What it shows:** how far below its record high the market was on each day. 0% = at a record; −83% = lost 83%.
**Data:** `NQ_clean_for_tableau`. **Picture:** `poster_visuals/V2_drawdown_underwater.png`.

1. New sheet → rename **V2 Drawdown**.
2. **Date** → **Columns** → make it a timeline (Step 5.3).
3. **Drawdown (TC)** → **Rows**.
4. Marks drop-down → **Area**. The chart now looks like water filling down from the top.
5. **Colour:** click **Color** → **More Colors…** → red (208, 59, 59).
6. **Show it as %:** right-click the left axis → **Format…**. A Format panel opens on the left. On the **Axis** tab, under *Scale* → **Numbers**, choose **Percentage** and set **Decimal places = 0**.
7. **Fix the range:** right-click the left axis → **Edit Axis…** → *Range*: choose **Fixed**, Start `-1`, End `0`. (−1 is −100%.) Title: `Drawdown (%)`.
8. **Annotations** (as in V1): `Dot-com bust −83% (regained Aug 2016)` at 9 Oct 2002, `GFC −54%` (late 2008/early 2009), `COVID −28%` (Mar 2020), `2022 −35%` (Dec 2022), `2025 −23%` (Apr 2025).
9. **Title:** **Drawdown from previous high: the March 2000 peak took 16 years to regain**
10. **Check:** the lowest point is about **−83%** on **9 Oct 2002**, and the last point is about **−9%**.

### V3. Calendar-year returns

**What it shows:** one bar per year: up (blue) or down (red).
**Data:** `NQ_annual_returns`. **Picture:** `poster_visuals/V3_annual_returns.png`.

1. New sheet → rename **V3 Annual returns**.
2. **Switch data source:** at the top of the Data pane, click **NQ_annual_returns**. The field list changes.
3. Drag **Year** to **Columns**. It must be a **blue** pill that says `Year`.
   - If it says `SUM(Year)` or is green: click its **▼** → **Dimension**, then **▼** → **Discrete**.
4. Drag **Annual Return** to **Rows**. Bars appear. If not, set the Marks drop-down to **Bar**.
5. Drag **Result** onto **Color**. **Edit Colors…** → **Gain** = blue, **Loss** = red.
6. **Show as %:** right-click the left axis → **Format…** → Axis tab → Numbers → **Percentage**, 0 decimals. Do the same on the **Pane** tab, so the bar labels are % too. Axis title: `Calendar-year return (%)`.
7. **Median line** (the "typical" year):
   1. Drag **Full Year Return** onto **Detail** on the Marks card. This makes it available for the line. It is blank for the two part-years, so they are left out of the median.
   2. Click the **Analytics** tab (top-left, next to Data).
   3. Drag **Reference Line** onto the chart and drop it on the box that says **Table**.
   4. In the window: *Value* → choose **SUM(Full Year Return)** and **Median**. *Label* → **Custom** → type `median 17%`. *Line* → grey, dashed. Click **OK**.
8. **Labels on four bars:** right-click the 2003 bar → **Mark Label → Always Show**. Repeat for 2008, 2022 and 2023.
9. **Mark the part-years:** annotate the 1999 bar `partial year (from Jun)` and the 2026 bar `year to date`.
10. **Title:** **Calendar-year return: 20 of 26 full years positive, but losses cluster in runs**
11. **Check:** 28 bars in total. Of the 26 full years (2000–2025), 20 are blue. The median line sits at about **17%**.

> **Optional LOD check (good evidence of method, about 5 minutes):** make a new sheet using
> `NQ_clean_for_tableau`. Drag **Date** to Columns (leave it as `YEAR(Date)`, blue). Drag **Year-End
> Close (LOD)** to Rows, click its ▼ → **Measure → Minimum**. Then ▼ → **Quick Table Calculation →
> Percent Difference**. Switch the view to a table (Show Me → text table). The numbers for 2000–2025
> match `Annual Return` in `NQ_annual_returns.csv`. Rename the sheet **Check: annual returns (LOD)**
> and keep it in your workbook.

### V4. Rolling volatility

**What it shows:** how bumpy (risky) the market was over each 21-day window. Most of the time it's calm, with sudden storms.
**Data:** `NQ_clean_for_tableau`. **Picture:** `poster_visuals/V4_rolling_volatility_regimes.png`.

1. New sheet → rename **V4 Volatility**.
2. Click **NQ_clean_for_tableau** at the top of the Data pane.
3. **Date** → **Columns** → timeline (Step 5.3).
4. **Rolling Vol 21d (TC)** → **Rows**. Marks drop-down → **Line**. **Color** → blue.
5. **Show as %:** right-click the left axis → **Format…** → Numbers → **Percentage**, 0 decimals. Title: `21-day realised volatility, annualised (%)`.
6. **Median line:** **Analytics** tab → drag **Reference Line** → drop on **Table**. *Value* → **AGG(Rolling Vol 21d (TC))** and **Median**. *Label* → Custom → `median 18%`. *Line* → grey, dashed. **OK**.
7. **Stress line:** drag another **Reference Line** → **Table**. *Value* → **AGG(Rolling Vol 21d (TC))**. In the second drop-down choose **Percentile → 90**. *Label* → Custom → `stress line (90th percentile) 40%`. *Line* → orange. **OK**.
8. **Annotations** on the tallest spikes: `2000–02: 99%`, `2008: 95%`, `2020: 90%`, `2025: 58%`.
9. **Title:** **Volatility clusters: calm regimes punctuated by short, violent storms**
10. **Check:** the median line is at about **18%** and the stress line at about **40%**. Your line may look slightly different from the picture for a few weeks around April 2000. That's expected: Python skipped the bad price removed on 10 Apr 2000, while Tableau simply joins the day before to the day after.

### V5. Fat tails: daily returns vs the bell curve

**What it shows:** blue bars count how many days had each size of move. The orange line is how many there *would* be if markets followed a perfect bell curve. Far from the middle, the bars are much taller than the line: big crash and jump days happen far more often than the bell curve says.
**Data:** `NQ_return_histogram`. **Picture:** `poster_visuals/V5_return_distribution_fat_tails.png`.

1. New sheet → rename **V5 Fat tails**. Click **NQ_return_histogram** at the top of the Data pane.
2. Drag **Return Bin Pct** to **Columns**. Click its **▼** → **Dimension**, then **▼** → **Continuous** (green).
3. Drag **Observed Days** to **Rows**.
4. Drag **Normal Expected Days** to **Rows** too, dropping it to the **right** of the first pill. You now see two charts, one above the other.
5. Click the **▼** on the second pill (`SUM(Normal Expected Days)`) → **Dual Axis**. The two charts merge into one.
6. Right-click the **right-hand** axis → **Synchronize Axis**. This is important: now both use the **same** scale. Right-click it again → untick **Show Header** to hide the duplicate numbers.
7. The Marks card now has tabs: **All**, **SUM(Observed Days)** and **SUM(Normal Expected Days)**.
   - Click the **Observed Days** tab → drop-down **Bar** → **Color** blue → **Size** slider a little to the left (thin bars).
   - Click the **Normal Expected Days** tab → drop-down **Line** → **Color** orange.
   - If Tableau coloured both with Measure Names, remove **Measure Names** from Color by dragging it off the card.
8. **Log scale** (so you can see the tiny counts far from the middle): right-click the left axis → **Edit Axis…** → tick **Logarithmic**. *Range* → **Fixed**, Start `0.8`, and leave End at the number Tableau suggests. Title: `Number of days (log scale)`. Then repeat step 6 (**Synchronize Axis**) in case it switched off.
9. Bottom axis: **Edit Axis…** → Title: `Daily log return (%)`.
10. **Caption:** top menu **Worksheet → Show Caption**. Double-click the caption box under the chart → replace the text with: `117 days beyond ±3 s.d. vs 19 expected; 47 beyond ±4 s.d. vs 0.4 expected; excess kurtosis 7.1.`
11. **Title:** **Daily returns have fat tails: extreme days are far more common than a bell curve predicts**
12. **Check:** the line sits **below** the bars at both far ends. Some bins have no days at all, so there are gaps on the log scale. That's normal.

### V6. Trend-regime scorecard

**What it shows:** four little contests between "price above its one-year average" (blue) and "below it" (orange). Below the average, the market is more than twice as bumpy, and most of the worst days happen there.
**Data:** `NQ_regime_summary`. **Picture:** `poster_visuals/V6_trend_regime_scorecard.png`.

1. New sheet → rename **V6 Regime scorecard**. Click **NQ_regime_summary** at the top of the Data pane.
2. Drag **Metric** to **Columns**. Then drag **Regime** to **Columns**, dropping it to the **right** of Metric.
3. Drag **Value** to **Rows**. Marks drop-down → **Bar**.
4. Drag **Regime** onto **Color**. **Edit Colors…** → **Above 252-day MA** = blue, **Below 252-day MA** = orange.
5. Drag **Value** onto **Label**. Each bar now shows its number.
6. **Show as %:** right-click the **SUM(Value)** pill on Rows → **Format…** → **Pane** tab → Numbers → **Percentage**, 0 decimals.
7. **Hide the side numbers** (the labels already show them): right-click the left axis → untick **Show Header**.
8. **Hide the repeated regime names under each bar** (the colours and legend already say it): right-click one of the "Above 252-day MA" labels under the bars → untick **Show Header**.
9. If the metric names are squashed, drag the edge of the chart to make it wider, or right-click a metric name → **Format…** → Header → set the alignment to **wrap**.
10. **Caption** (keep this; it stops the chart from claiming too much): **Worksheet → Show Caption** → `Volatility gap statistically significant (p < 0.001); return gap not significant (p = 0.22) and reverses after 2013, so the 252-day line is a risk signal, not a return forecast.`
11. **Title:** **Trend regimes: below its 252-day average, risk more than doubles and most crash days occur**
12. **Check** the labels (Above vs Below): share of days **74% vs 26%**; next-day return **13% vs −7%**; volatility **18% vs 40%**; share of worst days **13% vs 87%**.

### 5.4 Done? Tidy up

- **Same font everywhere:** **Format → Workbook…** → set every font to **Arial**.
- **Light gridlines:** **Format → Lines…** → set the *Grid Lines* to light grey, or *None*.
- **Legends:** keep the colour legend on V1, V3, V5 and V6 so colour is never the only clue.
- **Save** (**Ctrl + S**) as `NQ1_Poster_SantiagoCruz.twbx`.

---

## Step 6. Build the interactive dashboard (Week 7 interactivity)

1. Click the **New Dashboard** icon at the bottom.
2. In the Size panel, choose **Fixed size → Custom**, 1400 × 1000.
3. Drag **V1** to the top and **V4** below it.
4. Click V1 → the small dropdown arrow → **Filters → Date** → choose a **Range of Dates**. On the filter card, click the dropdown → **Apply to Worksheets → All Using This Data Source**. Moving the slider now updates both charts. (The first three weeks of the volatility line go blank after you move the slider. That's expected, because each point needs 21 days of data before it.)
5. Add a title: *Explore the crises: drag the date range*.
6. Name the dashboard **Interactive: price and volatility**.

---

## Step 7. Export high-resolution chart images

Poster charts must stay sharp at A1, so export them large.

**Easiest (all options):** make one dashboard per chart.
1. New Dashboard → Size **Fixed → Custom 2000 × 1000** (use 2000 × 1300 for V1).
2. Drag in one worksheet and set it to fill the dashboard (Fit: **Entire View**).
3. Before exporting, increase the fonts so they are readable on the poster: chart title about 20 pt, axis labels about 14 pt, annotations about 12 pt.
4. Export:
   - **Desktop (B/C):** **Dashboard → Export Image** → PNG.
   - **Browser (A):** publish first (Step 8), open the viz on your profile, then click **Download** (toolbar under the viz) → **Image**.
5. Name the files V1.png … V6.png.

---

## Step 8. Save and publish (this is your evidence)

- **Option A/B (Tableau Public):** **File → Save to Tableau Public As…** (browser: **Publish As**). Name it *NQ1 Research Poster – Santiago Cruz*. Then, on your profile, open the viz settings and allow others to **download** the workbook. Download the `.twbx` yourself and keep it with your drafts. Copy the viz URL; you can add it, or a QR code, to the poster.
- **Option C (trial):** **File → Save As** → `NQ1_Poster_SantiagoCruz.twbx`. The `.twbx` format packages the data with the workbook.

---

## Step 9. Assemble the A1 poster

### 9.1 Pick the tool

| Tool | Works on | How to get it |
|---|---|---|
| PowerPoint Online | Any browser, including Linux | https://www.office.com, using your university Microsoft 365 account |
| PowerPoint desktop | Windows / macOS | University software |
| LibreOffice Impress | Linux (often preinstalled; else `sudo apt install libreoffice-impress`) | https://www.libreoffice.org |

### 9.2 Set the page to A1 portrait

- **PowerPoint:** Design → Slide Size → Custom Slide Size → Width **59.4 cm**, Height **84.1 cm**, Portrait → *Ensure Fit*.
- **LibreOffice Impress:** Slide → Slide Properties → Paper format **A1**, Orientation **Portrait**, then set all margins to 0.

### 9.3 Copy the layout from `poster_visuals/poster_layout_A1_reference.png`

Measurements are in cm from the top-left corner of the page:

| Block | Left (x) | Top (y) | Width | Height |
|---|---|---|---|---|
| Title and author line | 1.8 | 1.5 | 55.8 | 3.5 |
| Blue rule under header | 1.8 | 5.2 | 55.8 | 0.15 |
| Introduction panel | 1.8 | 5.9 | 17.8 | 13.9 |
| Data and Method panel | 20.8 | 5.9 | 17.8 | 13.9 |
| 4 headline tiles (2 × 2) | 39.8 | 5.9 | 17.8 total | 13.9 total |
| Charts row 1: V1, V2 | 1.8 and 30.3 | 20.8 | 27.3 each | 15.4 (incl. caption) |
| Charts row 2: V3, V4 | 1.8 and 30.3 | 36.2 | 27.3 each | 15.4 |
| Charts row 3: V5, V6 | 1.8 and 30.3 | 51.6 | 27.3 each | 15.4 |
| Discussion, Conclusion, References | 1.8 / 20.8 / 39.8 | 69.4 | 17.8 each | 12.6 |

Steps:
1. **Text panels:** draw rectangles with a light grey fill (`#f0efec`) and no outline, then add text boxes on top.
2. **Charts:** Insert → Pictures → choose V1.png … V6.png. Resize them by the corners only, so they don't stretch, and place them in the grid.
3. **Captions:** add a one-sentence caption under each chart, starting with the objective tag (e.g. "O1 ·"). Copy the captions from Appendix C of `NQ1_Research_Poster_Report.md`.
4. **Headline tiles:** four small grey boxes, each with a big blue number and a short label: ×12.3 *price growth (9.6% a year)*; −83% *worst fall; regained after 16 years*; 117 vs 19 *3-sigma days: actual vs bell curve*; 2.3× *volatility below the 252-day average*.
5. **Text:** copy the Introduction, Data and Method, Discussion, Conclusion and References from Appendix C of the report.
6. **Align:** select a row of objects → Arrange → **Align Top** and **Distribute Horizontally**. Keep equal gaps (about 1 cm).

### 9.4 Font sizes for A1 (readable from about 1–2 m)

| Element | Size |
|---|---|
| Title | 60–72 pt, bold (two lines is fine) |
| Author line | 32–36 pt |
| Section headings | 36–40 pt, bold, blue |
| Body text | 22–24 pt |
| Captions | 18–20 pt |
| References | 14–16 pt |
| Headline numbers | 72–96 pt, bold, blue |

If the text does not fit at these sizes, cut words rather than shrinking the font. The rubric rewards "minimal text with clear, concise language".

### 9.5 Word count

The brief requires 1,000 words ±10%, so aim for **900–1,100 words in total**, including titles, captions, tiles and references. Appendix C has about 560 words of body text, and the chart titles, captions, tiles and references bring it into range. To check, copy all the text into a word processor and use its word count.

---

## Step 10. Export and check the poster

1. **Export to PDF:**
   - PowerPoint: **File → Export → PDF** (or Save As → PDF). Choose standard/high quality, not "minimum size".
   - LibreOffice: **File → Export as PDF** → quality 100%, JPEG compression off.
2. **Check the PDF:** open it and confirm the page size is 594 × 841 mm (Document Properties).
3. **Zoom to 100%:** every chart label must be readable and nothing should be blurry.
4. **Print test (optional):** print one corner on A4 at 100% scale (not "fit to page") to see real text sizes.
5. **Proofread:** spelling, consistent number formats (e.g. "−83%" everywhere), and the same title as the report.
6. **Name the file:** `NQ1_Research_Poster_SantiagoCruz_2584023.pdf`.

---

## Step 11. Submit

1. Upload the PDF to the assignment on **Canvas** before **2 Nov 2026, 14:00 UK**. First check the Canvas page for the accepted file format and size limit.
2. Keep these files, in case you are asked to show your working:
   - your Tableau workbook (`.twbx`) and Tableau Public link;
   - the poster source (`.pptx` or `.odp`);
   - `NQ1_Poster_Analysis.ipynb`, `ndx_poster_analysis.py`, the four CSVs and the raw data;
   - `NQ1_Research_Poster_Report.md`.
3. If the University requires a declaration of AI assistance, include it.

---

## Troubleshooting

| Problem | Fix |
|---|---|
| The line chart shows only ~28 points | `Date` is set to YEAR. Right-click → **Exact Date**, Continuous |
| Values look far too big | Tableau is summing several rows. Use Exact Date on Columns, or change the measure to **Attribute/Average** |
| `Date` shows as text (Abc) | On the Data Source tab, click the Abc icon → **Date** |
| Log axis errors or a blank chart | The histogram has blank bins for zero days; this is expected. Fix the axis start at 0.8 |
| V3 bars sort strangely | Make `Year` a string or discrete dimension, then sort ascending |
| A second line gets its own scale | You created a dual axis. Right-click the right axis → **Synchronize Axis** (V5 only); for V1, drop onto the existing axis instead |
| No upload option for CSV in the browser | Open the CSV in LibreOffice Calc or Excel, save it as `.xlsx`, and upload that |
| Annotations are missing in the browser editor | Add the labels as text boxes in the poster instead |
| Exported images look blurry | Export from a dashboard sized 2000 × 1000 or larger, and increase the font sizes before exporting |
| Opening `NQ1_Poster.twbx` shows a list of errors such as `missing required attribute 'dim-percentage'` or `no declaration found for element 'simple-id'` | The workbook was written for a newer Tableau than yours. Use the updated `Tableau_Workbook/NQ1_Poster.twbx` (rebuilt for older versions), or build the charts yourself with Step 5 |
| A calculated field shows red text: "The calculation contains errors" | Check that every `(` has a matching `)`, every `[` a matching `]`, and that field names are spelt as in the Data pane (`[MA 252]` with a space, not `[MA_252]`) |
| A (TC) line looks wrong, flat or like a staircase | `Date` is not at day level. Make it **Exact Date** and **Continuous** (Step 5.3). Then click the field's ▼ → **Compute Using → Table (across)** |
| The Reference Line window doesn't list the field I need | The field must be in the view first. Drag it onto **Detail** on the Marks card, then add the line again |
| Tableau Desktop will not install on Linux | Expected: use Option A (browser), or a Windows/Mac computer |
