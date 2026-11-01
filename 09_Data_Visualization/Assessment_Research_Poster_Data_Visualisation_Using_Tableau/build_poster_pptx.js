/*
 * Build the A1 research poster (NQ1_Research_Poster.pptx) from the Tableau-style
 * chart exports in poster_visuals_v2/.
 *
 * Layout follows the assessment brief's required sections (Title, Introduction,
 * Data Source and Methodology, Key Visualisations and Results, Discussion,
 * Conclusion) on a portrait A1 page (594 x 841 mm). Colours are the charts'
 * Tableau "Color Blind" palette, so poster and charts read as one system.
 *
 * Run from the assessment folder (needs pptxgenjs: `npm install pptxgenjs`):
 *     node build_poster_pptx.js
 */
const path = require("path");
const pptxgen = require("pptxgenjs");

const HERE = __dirname;
const FIG = (name) => path.join(HERE, "poster_visuals_v2", name);

// Page and grid (inches)
const W = 23.39, H = 33.11, M = 0.55, GAP = 0.4;
const CW = W - 2 * M;

// Palette: Tableau "Color Blind" plus poster neutrals
const NAVY = "0B3D60", BLUE = "1170AA", ORANGE = "C85200", SLATE = "57606C";
const INK = "1F2933", INK_2 = "4A5560", PAGE = "F3F5F7", CARD = "FFFFFF", RULE = "D5DBE1";
const LIGHT_ORANGE = "FFBC79", HEADER_TEXT = "C9DAE8";
const OBJ = { O1: { name: "Trend", color: BLUE }, O2: { name: "Volatility", color: ORANGE },
              O3: { name: "Regimes", color: SLATE } };

const FONT = "Arial";
const BODY = 15, CAPTION = 15, HEAD = 26;

const pres = new pptxgen();
pres.defineLayout({ name: "A1_PORTRAIT", width: W, height: H });
pres.layout = "A1_PORTRAIT";
pres.author = "Santiago Cruz";
pres.title = "Trend, Volatility and Market States in E-mini Nasdaq-100 Futures, 1999–2026";

const slide = pres.addSlide();
slide.background = { color: PAGE };

// ---------------------------------------------------------------------------------
// Helpers
// ---------------------------------------------------------------------------------
function card(x, y, w, h, name) {
  slide.addShape(pres.shapes.ROUNDED_RECTANGLE, {
    x, y, w, h, rectRadius: 0.08, fill: { color: CARD }, line: { color: RULE, width: 0.75 },
    objectName: name,
  });
}

function heading(num, text, x, y, w) {
  slide.addShape(pres.shapes.OVAL, { x, y: y + 0.04, w: 0.52, h: 0.52, fill: { color: BLUE },
                                     line: { color: BLUE }, objectName: `Badge ${num}` });
  slide.addText(String(num), { x, y: y + 0.04, w: 0.52, h: 0.52, margin: 0, align: "center",
                               valign: "middle", fontFace: FONT, fontSize: 20, bold: true,
                               color: "FFFFFF", isTextBox: true });
  slide.addText(text, { x: x + 0.7, y, w: w - 0.7, h: 0.6, margin: 0, valign: "middle",
                        fontFace: FONT, fontSize: HEAD, bold: true, color: NAVY, isTextBox: true,
                        objectName: `Heading ${num}` });
}

// Paragraphs: array of arrays of runs [{text, b, color}]; each inner array is one paragraph
function paragraphs(paras, opts) {
  const runs = [];
  paras.forEach((para, i) => {
    para.forEach((r, j) => {
      const o = { fontFace: FONT, fontSize: opts.fontSize || BODY, color: r.color || INK,
                  bold: !!r.b, italic: !!r.i };
      if (j === para.length - 1 && i < paras.length - 1) {
        o.breakLine = true;
        o.paraSpaceAfter = opts.paraSpaceAfter ?? 7;
      }
      runs.push({ text: r.text || r, options: o });
    });
  });
  slide.addText(runs, { x: opts.x, y: opts.y, w: opts.w, h: opts.h, margin: 0, valign: "top",
                        lineSpacingMultiple: opts.lineSpacing || 1.12, isTextBox: true,
                        objectName: opts.name });
}

const t = (text, extra = {}) => ({ text, ...extra });
const tag = (key) => t(`${key} ${OBJ[key].name}  `, { b: true, color: OBJ[key].color });

// ---------------------------------------------------------------------------------
// Title section
// ---------------------------------------------------------------------------------
const HEADER_H = 2.6;
slide.addShape(pres.shapes.RECTANGLE, { x: 0, y: 0, w: W, h: HEADER_H, fill: { color: NAVY },
                                        line: { color: NAVY }, objectName: "Title band" });
slide.addText("Trend, Volatility and Market States\nin E-mini Nasdaq-100 Futures, 1999–2026", {
  x: M, y: 0.28, w: 15.6, h: 1.6, margin: 0, valign: "top", fontFace: FONT, fontSize: 48, bold: true,
  color: "FFFFFF", lineSpacingMultiple: 0.95, isTextBox: true, objectName: "Title",
});
slide.addText("Santiago Cruz  ·  Student ID 2584023  ·  7CS079 Data Visualisation  ·  University of Wolverhampton", {
  x: M, y: 1.95, w: 15.6, h: 0.45, margin: 0, fontFace: FONT, fontSize: 18, color: HEADER_TEXT,
  isTextBox: true, objectName: "Author line",
});
slide.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: 16.35, y: 0.32, w: W - M - 16.35, h: 1.96,
  rectRadius: 0.08, fill: { color: "134E78" }, line: { color: "134E78" }, objectName: "Key message card" });
paragraphs([
  [t("KEY MESSAGE", { b: true, color: LIGHT_ORANGE })],
  [t("Twelvefold growth hid a 16-year loss, clustered storms and fat tails. A 252-day average flags "
     + "changing risk, not future returns.", { color: "FFFFFF" })],
], { x: 16.65, y: 0.5, w: W - M - 16.95, h: 1.7, fontSize: 18.5, paraSpaceAfter: 4,
     name: "Key message" });

// ---------------------------------------------------------------------------------
// Row 1: Introduction | Data source and methodology | headline numbers
// ---------------------------------------------------------------------------------
const R1Y = HEADER_H + 0.25, R1H = 5.85;
const INTRO_W = 7.0, METHOD_W = 9.3;
const METHOD_X = M + INTRO_W + GAP, TILES_X = METHOD_X + METHOD_W + GAP, TILES_W = W - M - TILES_X;

card(M, R1Y, INTRO_W, R1H, "Introduction card");
heading(1, "Introduction", M + 0.3, R1Y + 0.22, INTRO_W - 0.6);
paragraphs([
  [t("The E-mini Nasdaq-100 future (NQ) is the most heavily traded derivative on the Nasdaq-100, the "
     + "index behind the technology trackers many retail investors and pension savers hold (CME Group, "
     + "n.d.; Nasdaq, 2024). Since 1999 its price has grown twelvefold, but long-run averages hide how "
     + "unevenly that growth arrived. For a saver, what matters is not only how much the market grew, but "
     + "how far, how long and how often it fell on the way.")],
  [t("Objective: ", { b: true }), t("use Tableau to show non-specialist investors and early-career "
     + "traders what the averages hide.")],
  [tag("O1"), t("RQ1 How deep and how long were the interruptions to the trend?")],
  [tag("O2"), t("RQ2 Is risk spread evenly over time and across days, as a bell curve assumes?")],
  [tag("O3"), t("RQ3 Does the 252-day average separate calm from turbulent markets?")],
], { x: M + 0.3, y: R1Y + 0.98, w: INTRO_W - 0.6, h: R1H - 1.15, name: "Introduction text" });

card(METHOD_X, R1Y, METHOD_W, R1H, "Method card");
heading(2, "Data source and methodology", METHOD_X + 0.3, R1Y + 0.22, METHOD_W - 0.6);
paragraphs([
  [t("Source: ", { b: true }), t("daily open, high, low and settlement prices of the continuous "
     + "front-month contract CME_MINI:NQ1!, 30 Jun 1999 – 30 Oct 2026 (6,914 bars), exported from "
     + "TradingView (2026), which redistributes CME Globex exchange data.")],
  [t("Why this dataset: ", { b: true }), t("27 years of daily, exchange-sourced prices spanning four "
     + "crises, on the instrument professionals use to trade Nasdaq-100 risk. ETF prices embed fees "
     + "and dividends; generic Kaggle extracts lack clear provenance. Public prices only, so no "
     + "personal-data issues. Chart choices follow Munzner (2014) and Tufte (2001): one axis per "
     + "chart, direct labels and Tableau's colour-blind palette.")],
], { x: METHOD_X + 0.3, y: R1Y + 0.98, w: METHOD_W - 0.6, h: R1H - 1.15 - 1.95, name: "Method text" });

// Four-step pipeline
const steps = [
  ["1  Audit", "Python", "OHLC logic, 0.25-point tick grid and NYSE calendar checked"],
  ["2  Clean", "Python", "38 holiday sessions and 1 bad print removed: 6,875 sessions"],
  ["3  Visualise", "Tableau", "LOOKUP, RUNNING_MAX and WINDOW_STDEV fields; bins; reference lines"],
  ["4  Test", "Statistics", "Welch t, Levene, bootstrap; four averages, two sub-periods"],
];
const PH = 1.75, PY = R1Y + R1H - PH - 0.25, ARROW = 0.26;
const PW = (METHOD_W - 0.6 - 3 * ARROW) / 4;
steps.forEach(([title, tool, body], i) => {
  const x = METHOD_X + 0.3 + i * (PW + ARROW);
  slide.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y: PY, w: PW, h: PH, rectRadius: 0.06,
    fill: { color: i === 2 ? "E3EEF6" : "F0F3F6" }, line: { color: i === 2 ? BLUE : RULE, width: 0.75 },
    objectName: `Step ${i + 1}` });
  slide.addText([
    { text: title, options: { bold: true, color: NAVY, fontSize: 14, breakLine: true } },
    { text: tool, options: { color: i === 2 ? BLUE : INK_2, bold: i === 2, fontSize: 12.5, breakLine: true,
                             paraSpaceAfter: 3 } },
    { text: body, options: { color: INK, fontSize: 12.5 } },
  ], { x: x + 0.1, y: PY + 0.08, w: PW - 0.2, h: PH - 0.14, margin: 0, valign: "top", fontFace: FONT,
       lineSpacingMultiple: 1.0, isTextBox: true });
  if (i < 3) {
    slide.addShape(pres.shapes.CHEVRON, { x: x + PW + 0.06, y: PY + PH / 2 - 0.15, w: 0.14, h: 0.3,
      fill: { color: BLUE }, line: { color: BLUE }, objectName: `Arrow ${i + 1}` });
  }
});

// Headline numbers
const tiles = [
  ["×12.3", "price growth since 1999\n(9.6% a year)", BLUE],
  ["−83%", "worst fall (2000–02);\n16 years to regain", ORANGE],
  ["117 vs 19", "3-sigma days in 27 years:\nactual vs bell curve", ORANGE],
  ["2.3×", "volatility below vs above\nthe 252-day average", ORANGE],
];
const TG = 0.3, TW = (TILES_W - TG) / 2, TH = (R1H - TG) / 2;
tiles.forEach(([big, small, color], i) => {
  const x = TILES_X + (i % 2) * (TW + TG), y = R1Y + Math.floor(i / 2) * (TH + TG);
  card(x, y, TW, TH, `Headline ${i + 1}`);
  slide.addText(big, { x, y: y + TH / 2 - 0.9, w: TW, h: 0.95, margin: 0, align: "center", valign: "middle",
                       fontFace: FONT, fontSize: big.length > 6 ? 36 : 44, bold: true, color, isTextBox: true });
  slide.addText(small, { x: x + 0.1, y: y + TH / 2 + 0.1, w: TW - 0.2, h: 0.75, margin: 0, align: "center",
                         valign: "top", fontFace: FONT, fontSize: 14, color: INK_2, isTextBox: true });
});

// ---------------------------------------------------------------------------------
// Key visualisations and results: 2 x 3 grid of chart cards with captions
// ---------------------------------------------------------------------------------
const S3Y = R1Y + R1H + 0.25;
heading(3, "Key visualisations and results", M, S3Y, 12);
// Objective key, right-aligned on the heading row
const keyRuns = [];
["O1", "O2", "O3"].forEach((k, i) => {
  keyRuns.push({ text: "■ ", options: { color: OBJ[k].color, fontSize: 18 } });
  keyRuns.push({ text: `${k} ${OBJ[k].name}${i < 2 ? "     " : ""}`,
                 options: { color: INK, bold: true, fontSize: 16 } });
});
slide.addText([{ text: "Six Tableau worksheets, tagged by objective:   ", options: { color: INK_2, fontSize: 15 } },
               ...keyRuns], { x: 10.2, y: S3Y, w: W - M - 10.2, h: 0.6, margin: 0, align: "right",
               valign: "middle", fontFace: FONT, isTextBox: true, objectName: "Objective key" });

const charts = [
  { file: "V1_price_trend_log_ma252.png", px: [3245, 1537], obj: "O1",
    alt: "Line chart of the NQ futures price on a log scale with its 252-day moving average, 1999 to 2026, annotated at the dot-com peak and trough, the 2008 low and the 2026 all-time high",
    text: "Log scale, so equal heights are equal percentage moves. The March 2000 peak of 4,804 fell 83% "
          + "and was not regained until August 2016. Since 2009 the climb has been steeper, with 2022 the "
          + "only sustained break below the 252-day average." },
  { file: "V2_drawdown_underwater.png", px: [3267, 1537], obj: "O1",
    alt: "Area chart of the percentage decline from the previous high, with the dot-com, GFC, COVID-19, 2022 and 2025 declines labelled",
    text: "Drawdown shows what a holder lived through: the distance below the last peak. The dot-com and "
          + "GFC losses ran together for 16 years, while COVID (−28%) and the 2025 tariff shock (−23%) "
          + "recovered within 4 months and 2022 (−35%) in about two years." },
  { file: "V3_annual_returns.png", px: [3126, 1503], obj: "O1",
    alt: "Bar chart of calendar-year returns from 1999 to 2026, gains in blue and losses in orange, with a median reference line at 17 percent",
    text: "20 of 26 full years rose, with a median gain of 17%, but losses cluster: 2000–02 fell three "
          + "years running. The two other large losses, 2008 (−42%) and 2022 (−32%), were each followed "
          + "by a rebound above 50%." },
  { file: "V4_rolling_volatility_regimes.png", px: [3240, 1471], obj: "O2",
    alt: "Line chart of 21-day realised volatility with median and 90th-percentile stress reference lines and peaks labelled in 2001, 2008, 2020 and 2025",
    text: "Volatility sits near its 18% median for years, then storms of 58–99% erupt. Storms persist: in "
          + "one, there is a 65% chance of still being in one a month later (base rate 10%). Volatility "
          + "also rises as prices fall (correlation −0.35)." },
  { file: "V5_return_distribution_fat_tails.png", px: [3210, 1471], obj: "O2",
    alt: "Histogram of daily returns on a log count scale with a normal curve overlay, showing many more extreme days than the curve predicts",
    text: "A bell curve with the same mean and spread predicts 19 three-sigma days in 27 years; the market "
          + "produced 117, plus 47 four-sigma days where fewer than one is expected. Excess kurtosis is 7.1 "
          + "and normality is rejected (Jarque-Bera p < 0.001)." },
  { file: "V6_trend_regime_scorecard.png", px: [3161, 1597], obj: "O3",
    alt: "Four paired bar charts comparing days above and below the 252-day moving average on share of days, next-day return, volatility and share of the worst 1 percent of days",
    text: "Below its 252-day average the contract spent only 26% of days, yet volatility more than doubled "
          + "(40% vs 18%) and 87% of the worst 1% of days occurred. The return gap is not significant "
          + "(Welch p = 0.22) and reverses after 2013." },
];

const CARD_W = (CW - GAP) / 2, IMG_W = 9.5, PAD = 0.15, CAP_H = 0.86, ROW_GAP = 0.2;
let y = S3Y + 0.7;
for (let row = 0; row < 3; row++) {
  const pair = charts.slice(row * 2, row * 2 + 2);
  const imgH = Math.max(...pair.map((c) => IMG_W * c.px[1] / c.px[0]));
  const cardH = PAD + imgH + 0.1 + CAP_H + 0.12;
  pair.forEach((c, col) => {
    const x = M + col * (CARD_W + GAP), n = row * 2 + col + 1;
    const h = IMG_W * c.px[1] / c.px[0];
    card(x, y, CARD_W, cardH, `V${n} card`);
    slide.addImage({ path: FIG(c.file), x: x + (CARD_W - IMG_W) / 2, y: y + PAD + (imgH - h) / 2,
                     w: IMG_W, h, altText: c.alt, objectName: `V${n} chart` });
    paragraphs([[t(`V${n} · `, { b: true, color: OBJ[c.obj].color }), tag(c.obj), t(c.text)]],
               { x: x + 0.3, y: y + PAD + imgH + 0.1, w: CARD_W - 0.6, h: CAP_H, fontSize: CAPTION,
                 lineSpacing: 1.08, name: `V${n} caption` });
  });
  y += cardH + ROW_GAP;
}

// ---------------------------------------------------------------------------------
// Bottom row: Discussion | Conclusion | References
// ---------------------------------------------------------------------------------
const BY = y + 0.05, BH = H - 0.35 - BY;
const DISC_W = 9.3, CONC_W = 7.55, REF_W = CW - DISC_W - CONC_W - 2 * GAP;
const CONC_X = M + DISC_W + GAP, REF_X = CONC_X + CONC_W + GAP;

card(M, BY, DISC_W, BH, "Discussion card");
heading(4, "Discussion and interpretation", M + 0.3, BY + 0.22, DISC_W - 0.6);
paragraphs([
  [tag("O1"), t("Entry date mattered as much as holding period: a March 2000 buyer waited 16 years to "
     + "break even, while a 2009 buyer gained more than tenfold. A long-run growth rate is a poor guide "
     + "to any one investor's experience.")],
  [tag("O2"), t("Clustering and fat tails reproduce the stylised facts of returns (Mandelbrot, 1963; "
     + "Cont, 2001). They are not an artefact of noisy early data: excess kurtosis is higher after "
     + "2003 (8.1).")],
  [tag("O3"), t("The 252-day line separates risk states for every average length (50–252 days) and in "
     + "both sub-periods, but not returns, and the price crossed it 140 times with a median spell of "
     + "five days. This fits the Adaptive Markets view (Lo, 2004) better than a trading rule.")],
  [t("So what? ", { b: true }), t("For non-specialists, an investment should be judged by its drawdowns and "
     + "storms as well as its average return. Because these are in-sample results for one contract, they "
     + "describe past risk rather than forecast it.")],
], { x: M + 0.3, y: BY + 0.98, w: DISC_W - 0.6, h: BH - 1.15, name: "Discussion text" });

card(CONC_X, BY, CONC_W, BH, "Conclusion card");
heading(5, "Conclusion", CONC_X + 0.3, BY + 0.22, CONC_W - 0.6);
paragraphs([
  [t("NQ's long-run growth was real but unrepresentative: it came with deep, clustered and fat-tailed "
     + "risk.", { b: true })],
  [t("RQ1: ", { b: true, color: BLUE }), t("deep and uneven: −83% over 16 years, then 23–35% shocks that "
     + "recovered within months to two years.")],
  [t("RQ2: ", { b: true, color: ORANGE }), t("no. Risk clusters in storms and has fat tails.")],
  [t("RQ3: ", { b: true, color: SLATE }), t("yes for risk, no for returns.")],
  [t("Recommendations: ", { b: true }), t("show drawdown and volatility beside price on investor "
     + "dashboards; never size positions or margin with a bell curve; read the 252-day line as a risk "
     + "thermometer, not a signal.")],
  [t("Limitations and future work: ", { b: true }), t("bubble-peak start, unadjusted contract rolls, "
     + "in-sample tests; next, GARCH and regime-switching models and a public Tableau dashboard.")],
], { x: CONC_X + 0.3, y: BY + 0.98, w: CONC_W - 0.6, h: BH - 1.15, paraSpaceAfter: 4,
     name: "Conclusion text" });

card(REF_X, BY, REF_W, BH, "References card");
slide.addText("References", { x: REF_X + 0.3, y: BY + 0.22, w: REF_W - 0.6, h: 0.6, margin: 0,
  valign: "middle", fontFace: FONT, fontSize: 22, bold: true, color: NAVY, isTextBox: true });
const refs = [
  "CME Group (n.d.) E-mini Nasdaq-100 futures contract specs. cmegroup.com (Accessed: 31 Oct 2026).",
  "Cont, R. (2001) Quantitative Finance, 1(2), pp. 223–236.",
  "Lo, A.W. (2004) Journal of Portfolio Management, 30(5), pp. 15–29.",
  "Mandelbrot, B. (1963) Journal of Business, 36(4), pp. 394–419.",
  "Munzner, T. (2014) Visualization Analysis and Design. CRC Press.",
  "Nasdaq (2024) Nasdaq-100 Index Methodology. Nasdaq, Inc.",
  "TradingView (2026) CME_MINI:NQ1! daily data. tradingview.com (Accessed: 31 Oct 2026).",
  "Tufte, E.R. (2001) The Visual Display of Quantitative Information. Graphics Press.",
];
slide.addText(refs.map((r, i) => ({ text: r, options: { breakLine: i < refs.length - 1, paraSpaceAfter: 4 } })), {
  x: REF_X + 0.3, y: BY + 0.95, w: REF_W - 0.6, h: BH - 1.1, margin: 0, valign: "top", fontFace: FONT,
  fontSize: 11.5, color: INK_2, lineSpacingMultiple: 1.05, isTextBox: true, objectName: "References text",
});

slide.addNotes(
  "A1 portrait poster (594 x 841 mm). Charts are the Tableau-style exports in poster_visuals_v2/; to swap "
  + "in a direct Tableau export, right-click a chart > Change Picture > From a File (export at a similar "
  + "aspect ratio, about 2.1:1). Before submitting: File > Export > PDF and confirm the page is 594 x 841 mm."
);

pres.writeFile({ fileName: path.join(HERE, "NQ1_Research_Poster.pptx") })
  .then((f) => console.log(`wrote ${path.basename(f)}`));
