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

All four are in your assessment folder and are produced by `NQ1_Poster_Analysis.ipynb`:

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

## Step 5. Build the six charts

Create one worksheet per chart. Right-click the sheet tab → **Rename** (V1, V2, …). After each chart, compare it with the matching reference image in `poster_visuals/`.

### V1. Price trend with 252-day moving average (data: `NQ_clean_for_tableau`)

1. Drag **Date** to **Columns** → right-click it → **Exact Date** → make sure it is **Continuous** (green).
2. Drag **Close** to **Rows**.
3. Drag **MA 252** onto the **left axis** of the chart (drop it when you see a double ruler icon). Both lines now share one axis, and Tableau adds *Measure Names* to Color.
4. Marks card → choose **Line**.
5. Right-click the y-axis → **Edit Axis** → tick **Logarithmic**. Set the title to *Futures price, index points (log scale)*.
6. Click **Color** → **Edit Colors**: Close = blue, MA 252 = orange. Make the MA line thicker with **Size**.
7. **Annotate** (Desktop: right-click a point → Annotate → Point): Mar 2000 peak, Oct 2002 trough (−83%), Nov 2008 low, Oct 2026 all-time high.
8. Title: **E-mini Nasdaq-100: a 27-year climb from the dot-com peak, through two deep bear markets**

### V2. Drawdown from previous high (data: `NQ_clean_for_tableau`)

1. **Date** → Columns (Exact Date, Continuous). **Drawdown** → Rows.
2. Marks → **Area**. Color → red.
3. Right-click the y-axis → **Edit Axis** → Fixed: start −1, end 0. Right-click the axis → **Format** → Numbers → **Percentage**, 0 decimals.
4. Annotate: Dot-com bust −83% (regained Aug 2016), GFC −54%, COVID −28%, 2022 −35%, 2025 −23%.
5. Title: **Drawdown from previous high: the March 2000 peak took 16 years to regain**

### V3. Calendar-year returns (data: `NQ_annual_returns`)

1. **Year** → Columns (it must be a discrete, blue pill). **Annual Return** → Rows.
2. Marks → **Bar**. Drag **Result** to **Color**: Gain = blue, Loss = red.
3. Drag **Year Type** to **Opacity**, or to Color as a second step, so the partial years (1999 and 2026) look lighter. Alternatively, add "partial" and "YTD" as annotations.
4. **Analytics** pane (tab next to Data) → drag **Reference Line** onto the chart → Scope: Entire Table → Value: **Full Year Return**, **Median** → Label: *median 17%*. Using `Full Year Return` excludes the partial years.
5. Format the y-axis as a Percentage. Show labels only on 2003, 2008, 2022 and 2023: right-click a bar → Mark Label → Always Show.
6. Title: **Calendar-year return: 20 of 26 full years positive, but losses cluster in runs**

### V4. Rolling volatility (data: `NQ_clean_for_tableau`)

1. **Date** → Columns (Exact Date, Continuous). **Rolling Vol 21d Ann** → Rows. Marks → **Line**.
2. Create a calculated field (Analysis → **Create Calculated Field**; browser: the dropdown next to Data → Create Calculated Field):
   - Name: `Stress`
   - Formula: `IF [Rolling Vol 21d Ann] > 0.40 THEN "Stress (above 90th pct)" ELSE "Normal" END`
   - Drag **Stress** to **Color**: Normal = blue, Stress = orange.
3. **Analytics** pane → **Reference Line** → Entire Table → Median → label *median 18%*.
4. **Analytics** pane → **Distribution Band** or **Reference Line** → Percentile **90** → label *stress line (90th pct) 40%*.
5. Format the y-axis as a Percentage. Annotate the peaks: 2000–02 99%, 2008 95%, 2020 90%, 2025 58%.
6. Title: **Volatility clusters: calm regimes punctuated by short, violent storms**

### V5. Return distribution with normal curve (data: `NQ_return_histogram`)

1. **Return Bin Pct** → Columns. Right-click → make sure it is **Continuous** and a **Dimension**.
2. **Observed Days** → Rows. Marks → **Bar**, blue, size small.
3. Drag **Normal Expected Days** to Rows as well, to the right of Observed Days.
4. Right-click the second pill → **Dual Axis**. Then right-click the right axis → **Synchronize Axis** → right-click again → untick **Show Header**. The two series now share one scale.
5. On the Marks card for *Normal Expected Days*, choose **Line** and colour it orange.
6. Right-click the y-axis → **Edit Axis** → **Logarithmic**, Fixed start 0.8. Title: *Number of days (log scale)*. X-axis title: *Daily log return (%)*.
7. Add a text box or caption: *117 days beyond ±3 s.d. vs 19 expected; 47 beyond ±4 s.d. vs 0.4 expected; excess kurtosis 7.1.*
8. Title: **Daily returns have fat tails: extreme days are far more common than a bell curve predicts**

### V6. Trend-regime scorecard (data: `NQ_regime_summary`)

1. **Metric** → Columns, then **Regime** → Columns, to the right of Metric.
2. **Value** → Rows. Marks → **Bar**. **Regime** → **Color**: Above = blue, Below = orange.
3. **Value** → **Label**. Format the label and axis as a Percentage, 0 decimals. Then hide the y-axis: right-click → untick Show Header.
4. The metric names start with 1–4, so they already sort in the right order.
5. Caption under the chart, which you must keep: *Volatility gap statistically significant (p < 0.001); return gap not significant (p = 0.22) and reverses after 2013, so the 252-day line is a risk signal, not a return forecast.*
6. Title: **Trend regimes: below its 252-day average, risk more than doubles and most crash days occur**

---

## Step 6. Build the interactive dashboard (Week 7 interactivity)

1. Click the **New Dashboard** icon at the bottom.
2. In the Size panel, choose **Fixed size → Custom**, 1400 × 1000.
3. Drag **V1** to the top and **V4** below it.
4. Click V1 → the small dropdown arrow → **Filters → Date** → choose a **Range of Dates**. On the filter card, click the dropdown → **Apply to Worksheets → All Using This Data Source**. Moving the slider now updates both charts.
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
| Tableau Desktop will not install on Linux | Expected: use Option A (browser), or a Windows/Mac computer |
