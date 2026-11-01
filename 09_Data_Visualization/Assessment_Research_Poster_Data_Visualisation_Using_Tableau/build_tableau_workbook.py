"""Build a ready-made Tableau workbook (NQ1_Poster.twbx) for the six poster charts.

Reads the outputs of NQ1_Poster_Analysis.ipynb from spreadsheets_assessment/
(NQ_clean_for_tableau.csv and the three summary tables), writes one tidy CSV per chart into
Tableau_Workbook/Data/, then writes a Tableau workbook that connects to them. Tableau renders
every chart itself.

The sheets follow the notebook's v2 reference charts (poster_visuals_v2/): Tableau's Color Blind
palette, a title with a grey subtitle, log or fixed axes, Analytics-pane reference lines, a
synchronised dual axis for V5 and selective mark labels. Labels come from a `Note` column that
is blank except on the marks worth labelling, shown with ATTR() so they do not split the lines.
Values are stored in percent units (e.g. -83.1) so axes read correctly without number formats.

Run from the assessment folder:
    uv run --no-project --with pandas python build_tableau_workbook.py
"""

import math
import zipfile
from pathlib import Path
from xml.sax.saxutils import escape, quoteattr

import pandas as pd

HERE = Path(__file__).resolve().parent
SRC = HERE / "spreadsheets_assessment"          # where the notebook outputs are kept
OUT_DIR = HERE / "Tableau_Workbook"
DATA_DIR = OUT_DIR / "Data"
TWB = OUT_DIR / "NQ1_Poster.twb"
TWBX = OUT_DIR / "NQ1_Poster.twbx"

# Tableau "Color Blind" palette, as in the notebook's Tableau-style theme
BLUE, ORANGE = "#1170AA", "#C85200"
LIGHT_BLUE, LIGHT_ORANGE = "#A3CCE9", "#FFBC79"
TITLE_INK, SUB_INK, REF = "#333333", "#555555", "#7F7F7F"

# Same episode windows as ndx_poster_analysis.py
EPISODES = {"Dot-com bust": ("2000-01", "2003-12"), "GFC": ("2007-09", "2009-12"),
            "COVID-19": ("2020-02", "2020-04"), "2022 rate shock": ("2021-11", "2022-12"),
            "2025 tariff shock": ("2025-01", "2025-05")}


def episode(close: pd.Series, start: str, end: str) -> dict:
    s = close[start:end]
    trough = (s / s.cummax() - 1).idxmin()
    peak = s[:trough].idxmax()
    after = close[trough:]
    regained = after[after >= close[peak]]
    return {"peak": peak, "trough": trough, "depth": close[trough] / close[peak] - 1,
            "regained": regained.index[0] if len(regained) else None}


def pct(v: float, decimals: int = 0, sign: bool = False) -> str:
    """Percentage with a typographic minus sign (v is a fraction)."""
    return f"{v:{'+' if sign else ''}.{decimals}%}".replace("-", "−")


SUBTITLES: dict[str, list[str]] = {}            # sheet -> subtitle lines, filled from the data


def write_chart_data() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    df = pd.read_csv(SRC / "NQ_clean_for_tableau.csv", parse_dates=["Date"]).set_index("Date")
    c = df["Close"]

    # V1: price and 252-day MA, notes on the settlement series
    dot, gfc = episode(c, *EPISODES["Dot-com bust"]), episode(c, *EPISODES["GFC"])
    ath = c.idxmax()
    brk = c["2022-10-15":].index[0]
    notes = {dot["peak"]: f"Dot-com peak {dot['peak']:%b %Y}: {c[dot['peak']]:,.0f}",
             dot["trough"]: f"Trough {dot['trough']:%b %Y}: {pct(dot['depth'])} from peak",
             gfc["trough"]: f"GFC low {gfc['trough']:%b %Y}: {pct(gfc['depth'])}",
             brk: "2022: the only sustained break below the average since 2009",
             ath: f"All-time high {ath:%b %Y}: {c[ath]:,.0f}"}
    price = pd.concat([
        pd.DataFrame({"Date": c.index, "Series": "Daily settlement", "Price": c.values,
                      "Note": [notes.get(t, "") for t in c.index]}),
        pd.DataFrame({"Date": c.index, "Series": "252-day moving average", "Price": df["MA_252"].values,
                      "Note": ""}).dropna(subset=["Price"]),
    ])
    price.to_csv(DATA_DIR / "V1_price.csv", index=False, date_format="%Y-%m-%d")
    years = (c.index[-1] - c.index[0]).days / 365.25
    growth = c.iloc[-1] / c.iloc[0]
    SUBTITLES["V1 Price trend"] = [
        f"Daily settlement of the front-month NQ contract and its 252-day moving average, "
        f"{c.index[0]:%b %Y} – {c.index[-1]:%b %Y}  |  ×{growth:.1f} (≈{growth ** (1 / years) - 1:.1%} a year)",
        "Log scale: equal vertical distances are equal percentage moves. "
        "Source: CME Globex via TradingView (CME_MINI:NQ1!)."]

    # V2: drawdown, one note per episode at its trough
    dd = (df["Drawdown"] * 100).round(3)
    notes = {}
    for name, (start, end) in EPISODES.items():
        e = episode(c, start, end)
        extra = (f", regained {e['regained']:%b %Y}" if name == "Dot-com bust" else
                 f", regained in {(e['regained'] - e['peak']).days / 30.44:.0f} months"
                 if e["regained"] is not None and name != "GFC" else "")
        notes[e["trough"]] = f"{name} {pct(e['depth'])}{extra}"
    pd.DataFrame({"Date": dd.index, "Drawdown_Pct": dd.values,
                  "Note": [notes.get(t, "") for t in dd.index]}).to_csv(
        DATA_DIR / "V2_drawdown.csv", index=False, date_format="%Y-%m-%d")
    SUBTITLES["V2 Drawdown"] = [
        "Percentage below the highest settlement so far; each label quotes the episode's own peak-to-trough fall",
        f"The GFC trough sits inside the dot-com drawdown, so its plotted depth is measured from 2000; "
        f"its own fall from the Oct 2007 high was {pct(gfc['depth'])}."]

    # V3: annual returns, partial years in lighter tints, labels on selected years
    ann = pd.read_csv(SRC / "NQ_annual_returns.csv", dtype={"Year": str})
    first, last = ann["Year"].iloc[0], ann["Year"].iloc[-1]
    partial = ann["Year_Type"].eq("Partial year")
    label_years = {first, "2000", "2001", "2002", "2003", "2008", "2009", "2022", "2023", last}
    tag = {first: " partial", last: " YTD"}
    pd.DataFrame({
        "Year": ann["Year"],
        "Annual_Return_Pct": (ann["Annual_Return"] * 100).round(1),
        "Full_Year_Return_Pct": (ann["Full_Year_Return"] * 100).round(1),
        "Result": ann["Result"].where(~partial, ann["Result"] + " (partial year)"),
        "Note": [pct(v, sign=True) + tag.get(y, "") if y in label_years else ""
                 for y, v in zip(ann["Year"], ann["Annual_Return"])],
    }).to_csv(DATA_DIR / "V3_annual.csv", index=False)
    SUBTITLES["V3 Annual returns"] = [
        f"Year-end to year-end change in settlement; {first} runs from {c.index[0]:%d %b}, "
        f"{last} is year-to-date (lighter bars). Dashed line: median of full years."]

    # V4: volatility, notes on the four storm peaks
    rv = (df["Rolling_Vol_21d_Ann"] * 100).dropna()
    notes = {}
    for start, end in [("2000-01", "2002-12"), ("2008-01", "2009-06"), ("2020-01", "2020-12"),
                       ("2025-01", "2025-12")]:
        t = rv[start:end].idxmax()
        notes[t] = f"{t:%b %Y}: {rv[t]:.0f}%"
    pd.DataFrame({"Date": rv.index, "Volatility_Pct": rv.round(2).values,
                  "Note": [notes.get(t, "") for t in rv.index]}).to_csv(
        DATA_DIR / "V4_volatility.csv", index=False, date_format="%Y-%m-%d")
    global V4_MEDIAN, V4_P90
    V4_MEDIAN, V4_P90 = rv.median(), rv.quantile(0.9)
    SUBTITLES["V4 Volatility"] = [
        "Rolling 21-day standard deviation of daily log returns × √252; "
        "dashed lines are the median and the stress line (90th percentile)"]

    # V5: histogram (wide, for the dual axis), notes on the two most extreme days
    hist = pd.read_csv(SRC / "NQ_return_histogram.csv")
    r = df["Log_Return"].dropna() * 100
    lo, hi = r.idxmin(), r.idxmax()
    note = pd.Series("", index=hist.index)
    for t in (lo, hi):
        k = (hist["Return_Bin_Pct"] - r[t]).abs().idxmin()
        note[k] = f"{t.day} {t:%b %Y}: {pct(r[t] / 100, 1, sign=True)}"
    hist.assign(Note=note).to_csv(DATA_DIR / "V5_distribution.csv", index=False)
    z = (r - r.mean()) / r.std()
    m = r - r.mean()
    kurt = (m ** 4).mean() / (m ** 2).mean() ** 2 - 3
    expected = lambda k: len(r) * math.erfc(k / math.sqrt(2))   # two-sided normal tail count
    SUBTITLES["V5 Fat tails"] = [
        f"Histogram of {len(r):,} daily log returns against a normal curve with the same mean and s.d.",
        f"Excess kurtosis {kurt:.1f}  |  beyond ±3 s.d.: {(z.abs() > 3).sum()} days observed vs "
        f"{expected(3):.0f} expected  |  beyond ±4 s.d.: {(z.abs() > 4).sum()} vs {expected(4):.1f}"]

    # V6: regime scorecard with formatted value labels
    reg = pd.read_csv(SRC / "NQ_regime_summary.csv")
    is_return = reg["Metric"].str.contains("return")
    pd.DataFrame({"Metric": reg["Metric"], "Regime": reg["Regime"],
                  "Value_Pct": (reg["Value"] * 100).round(1),
                  "Note": [pct(v, sign=s) for v, s in zip(reg["Value"], is_return)]}).to_csv(
        DATA_DIR / "V6_regime.csv", index=False)
    SUBTITLES["V6 Regime scorecard"] = [
        f"Regime at today's settlement paired with the next day's return (no look-ahead), "
        f"{df['MA_252'].first_valid_index():%b %Y} – {c.index[-1]:%b %Y}",
        "Volatility gap statistically significant (Levene p < 0.001); return gap not significant "
        "(Welch p = 0.22) and reverses after 2013: a risk signal, not a return forecast."]


# ----------------------------------------------------------------------------------
# Workbook definition: one entry per chart.
#   fields: (name, datatype, role, type) as Tableau column metadata
#   cols/rows: (field, derivation, kind) placed on the shelves; a list of rows = dual axis
#   colour: (dimension, {member: hex}) or None; single_colour: mark colour without a legend
#   lod: measures put on Detail (needed by a reference line); note: label from ATTR([Note])
#   axes: (field instance, scope, title, extra encoding attributes)
#   reflines: (formula, value or None, label, colour) on the first rows measure
# ----------------------------------------------------------------------------------
SHEETS = [
    dict(sheet="V1 Price trend", file="V1_price.csv", mark="Line",
         title="E-mini Nasdaq-100: a 27-year climb from the dot-com peak, through two deep bear markets",
         fields=[("Date", "date", "dimension", "ordinal"), ("Series", "string", "dimension", "nominal"),
                 ("Price", "real", "measure", "quantitative"), ("Note", "string", "dimension", "nominal")],
         cols=("Date", "none", "qk"), rows=("Price", "sum", "qk"),
         colour=("Series", {"Daily settlement": BLUE, "252-day moving average": ORANGE}),
         axes=[(("Price", "sum", "qk"), "rows", "Price (index points, log scale)",
                "scale='log' range-type='fixed' min='400' max='60000'"),
               (("Date", "none", "qk"), "cols", "Date (trading day)", "")]),
    dict(sheet="V2 Drawdown", file="V2_drawdown.csv", mark="Area",
         title="Drawdown from previous high: the March 2000 peak took 16 years to regain",
         fields=[("Date", "date", "dimension", "ordinal"), ("Drawdown_Pct", "real", "measure", "quantitative"),
                 ("Note", "string", "dimension", "nominal")],
         cols=("Date", "none", "qk"), rows=("Drawdown_Pct", "sum", "qk"), single_colour=ORANGE,
         axes=[(("Drawdown_Pct", "sum", "qk"), "rows", "Drawdown from running peak (%)",
                "range-type='fixed' min='-100' max='2'"),
               (("Date", "none", "qk"), "cols", "Date (trading day)", "")]),
    dict(sheet="V3 Annual returns", file="V3_annual.csv", mark="Bar",
         title="Calendar-year return: 20 of 26 full years positive, but losses cluster in runs",
         fields=[("Year", "string", "dimension", "nominal"), ("Annual_Return_Pct", "real", "measure", "quantitative"),
                 ("Full_Year_Return_Pct", "real", "measure", "quantitative"),
                 ("Result", "string", "dimension", "nominal"), ("Note", "string", "dimension", "nominal")],
         cols=("Year", "none", "nk"), rows=("Annual_Return_Pct", "sum", "qk"),
         colour=("Result", {"Gain": BLUE, "Loss": ORANGE, "Gain (partial year)": LIGHT_BLUE}),
         lod=[("Full_Year_Return_Pct", "sum", "qk")],
         axes=[(("Annual_Return_Pct", "sum", "qk"), "rows", "Annual price return (%)",
                "range-type='fixed' min='-52' max='72'")],
         reflines=[("median", ("Full_Year_Return_Pct", "sum", "qk"), "Median, full years: 17%", REF)]),
    dict(sheet="V4 Volatility", file="V4_volatility.csv", mark="Line",
         title="Volatility clusters: calm regimes punctuated by short, violent storms",
         fields=[("Date", "date", "dimension", "ordinal"), ("Volatility_Pct", "real", "measure", "quantitative"),
                 ("Note", "string", "dimension", "nominal")],
         cols=("Date", "none", "qk"), rows=("Volatility_Pct", "sum", "qk"), single_colour=BLUE,
         axes=[(("Volatility_Pct", "sum", "qk"), "rows", "21-day realised volatility, annualised (%)",
                "range-type='fixed' min='0' max='115'"),
               (("Date", "none", "qk"), "cols", "Date (trading day)", "")],
         reflines="v4"),                                 # median and stress line, filled from the data
    dict(sheet="V5 Fat tails", file="V5_distribution.csv", mark=["Bar", "Line"],
         title="Daily returns have fat tails: extreme days are far more common than a bell curve predicts",
         fields=[("Return_Bin_Pct", "real", "dimension", "quantitative"),
                 ("Observed_Days", "real", "measure", "quantitative"),
                 ("Normal_Expected_Days", "real", "measure", "quantitative"),
                 ("Note", "string", "dimension", "nominal")],
         cols=("Return_Bin_Pct", "none", "qk"),
         rows=[("Observed_Days", "sum", "qk"), ("Normal_Expected_Days", "sum", "qk")],
         pane_colours=[BLUE, ORANGE],
         axes=[(("Observed_Days", "sum", "qk"), "rows", "Number of days (log scale)",
                "scale='log' range-type='fixedmin' min='0.7'"),
               (("Normal_Expected_Days", "sum", "qk"), "rows", "",
                "scale='log' fold='true' synchronized='true'"),
               (("Return_Bin_Pct", "none", "qk"), "cols", "Daily log return (%, bins of 0.25%)",
                "range-type='fixed' min='-14' max='18'")]),
    dict(sheet="V6 Regime scorecard", file="V6_regime.csv", mark="Bar",
         title="Trend regimes: below its 252-day average, risk more than doubles and most crash days occur",
         fields=[("Metric", "string", "dimension", "nominal"), ("Regime", "string", "dimension", "nominal"),
                 ("Value_Pct", "real", "measure", "quantitative"), ("Note", "string", "dimension", "nominal")],
         cols=[("Metric", "none", "nk"), ("Regime", "none", "nk")], rows=("Value_Pct", "sum", "qk"),
         colour=("Regime", {"Above 252-day MA": BLUE, "Below 252-day MA": ORANGE}),
         axes=[(("Value_Pct", "sum", "qk"), "rows", "", "")], hide_rows_axis=True),
]


def ds_name(i: int) -> str:
    return f"federated.nq1poster{i:02d}"


def inst(field, deriv, kind) -> str:
    return f"[{deriv}:{field}:{kind}]"


def col_xml(name, datatype, role, typ) -> str:
    return f"<column datatype='{datatype}' name='[{name}]' role='{role}' type='{typ}' />"


def instance_xml(field, deriv, kind) -> str:
    deriv_attr = {"sum": "Sum", "none": "None", "attr": "Attribute"}[deriv]
    typ = {"qk": "quantitative", "nk": "nominal"}[kind]
    return (f"<column-instance column='[{field}]' derivation='{deriv_attr}' "
            f"name='{inst(field, deriv, kind)}' pivot='key' type='{typ}' />")


def title_xml(sh) -> str:
    runs = f"<run bold='true' fontcolor='{TITLE_INK}' fontsize='14'>{escape(sh['title'])}</run>"
    for line in SUBTITLES.get(sh["sheet"], []):
        runs += f"<run>Æ&#10;</run><run fontcolor='{SUB_INK}' fontsize='10'>{escape(line)}</run>"
    return f"<layout-options><title><formatted-text>{runs}</formatted-text></title></layout-options>"


def mark_style(colour: str | None, labels: bool) -> str:
    rules = ""
    if colour:
        rules += f"<format attr='mark-color' value='{colour}' />"
    if labels:
        rules += "<format attr='mark-labels-show' value='true' /><format attr='mark-labels-cull' value='false' />"
    return f"<style><style-rule element='mark'>{rules}</style-rule></style>" if rules else ""


def refline_xml(ds, axis, value, formula, const, label, k) -> str:
    v = f" value='{const}'" if const is not None else ""
    return (f"<reference-line axis-column='[{ds}].{inst(*axis)}' enable-instant-analytics='true' "
            f"formula='{formula}' id='refline{k}' label={quoteattr(label)} label-type='custom' "
            f"scope='per-table' value-column='[{ds}].{inst(*value)}'{v} z-order='{k + 1}' />")


def build_twb(data_dir_attr: str) -> str:
    datasources, worksheets, windows = [], [], []
    for i, sh in enumerate(SHEETS):
        ds = ds_name(i)
        conn = f"textscan.nq1poster{i:02d}"
        table = sh["file"].replace(".csv", "#csv")
        relation_cols = "".join(
            f"<column datatype='{dt}' name='{n}' ordinal='{k}' />" for k, (n, dt, _, _) in enumerate(sh["fields"]))
        colour = sh.get("colour")
        style = ""
        if colour:
            maps = "".join(f"<map to='{hexv}'><bucket>{quoteattr(m)[1:-1].join(['&quot;', '&quot;'])}</bucket></map>"
                           for m, hexv in colour[1].items())
            style = (f"<style><style-rule element='mark'><encoding attr='color' "
                     f"field='{inst(colour[0], 'none', 'nk')}' type='palette'>{maps}</encoding>"
                     f"</style-rule></style>")
        datasources.append(
            f"<datasource caption={quoteattr(sh['file'][:-4])} inline='true' name='{ds}' version='18.1'>"
            f"<connection class='federated'><named-connections>"
            f"<named-connection caption={quoteattr(sh['file'][:-4])} name='{conn}'>"
            f"<connection class='textscan' directory={quoteattr(data_dir_attr)} filename={quoteattr(sh['file'])} "
            f"password='' server='' /></named-connection></named-connections>"
            f"<relation connection='{conn}' name={quoteattr(sh['file'])} table='[{table}]' type='table'>"
            f"<columns character-set='UTF-8' header='yes' locale='en_GB' separator=','>{relation_cols}</columns>"
            f"</relation></connection>"
            f"<aliases enabled='yes' />"
            + "".join(col_xml(*f) for f in sh["fields"])
            + "<layout dim-ordering='alphabetic' dim-percentage='0.5' measure-ordering='alphabetic' "
              "measure-percentage='0.4' show-structure='true' />"
            + style + "</datasource>")

        cols = sh["cols"] if isinstance(sh["cols"], list) else [sh["cols"]]
        rows = sh["rows"] if isinstance(sh["rows"], list) else [sh["rows"]]
        note = ("Note", "attr", "nk")
        extra = ([(colour[0], "none", "nk")] if colour else []) + sh.get("lod", []) + [note]
        used = cols + rows + extra
        deps = "".join(col_xml(*f) for f in sh["fields"] if f[0] in {u[0] for u in used})
        instances = "".join(dict.fromkeys(instance_xml(*u) for u in used))

        enc = ""
        if colour:
            enc += f"<color column='[{ds}].{inst(colour[0], 'none', 'nk')}' />"
        enc += f"<text column='[{ds}].{inst(*note)}' />"
        enc += "".join(f"<lod column='[{ds}].{inst(*m)}' />" for m in sh.get("lod", []))

        reflines = sh.get("reflines") or []
        if reflines == "v4":
            v = ("Volatility_Pct", "sum", "qk")
            reflines = [("median", v, f"Median: {V4_MEDIAN:.0f}%", REF),
                        ("constant", v, f"Stress line (90th percentile): {V4_P90:.0f}%", ORANGE)]
        refs = "".join(
            refline_xml(ds, rows[0], value, formula, round(V4_P90, 2) if formula == "constant" else None, label, k)
            for k, (formula, value, label, _) in enumerate(reflines))

        view = "<view><breakdown value='auto' /></view>"
        relax = "selection-relaxation-option='selection-relaxation-allow'"
        if len(rows) == 1:
            panes = (f"<pane {relax}>{view}<mark class='{sh['mark']}' /><encodings>{enc}</encodings>{refs}"
                     + mark_style(sh.get("single_colour"), True) + "</pane>")
        else:                                            # dual axis: an "All" pane plus one per measure
            panes = f"<pane {relax}>{view}<mark class='Automatic' /></pane>"
            for k, (r, mark, hexv) in enumerate(zip(rows, sh["mark"], sh["pane_colours"]), start=1):
                pane_enc = f"<encodings>{enc}</encodings>" if k == 1 else ""
                panes += (f"<pane id='{k}' {relax} y-axis-name='[{ds}].{inst(*r)}'>{view}"
                          f"<mark class='{mark}' />{pane_enc}" + mark_style(hexv, k == 1) + "</pane>")

        axis_rules = ""
        for axis, scope, title, attrs in sh.get("axes", []):
            field = f"[{ds}].{inst(*axis)}"
            axis_rules += (f"<encoding attr='space' class='0' field='{field}' field-type='quantitative' "
                           f"scope='{scope}' type='space' {attrs} />")
            if title:
                axis_rules += f"<format attr='title' class='0' field='{field}' scope='{scope}' value={quoteattr(title)} />"
            elif scope == "rows" and (sh.get("hide_rows_axis") or len(rows) > 1):
                axis_rules += f"<format attr='display' class='0' field='{field}' scope='{scope}' value='false' />"
        ref_rules = "".join(f"<format attr='stroke-color' id='refline{k}' value='{hexv}' />"
                            f"<format attr='line-pattern' id='refline{k}' value='dashed' />"
                            for k, (_, _, _, hexv) in enumerate(reflines))
        table_style = "<style>"
        if axis_rules:
            table_style += f"<style-rule element='axis'>{axis_rules}</style-rule>"
        if ref_rules:
            table_style += f"<style-rule element='refline'>{ref_rules}</style-rule>"
        table_style += ("<style-rule element='gridline'><format attr='stroke-color' value='#E6E6E6' /></style-rule>"
                        "<style-rule element='worksheet'><format attr='font-family' value='Arial' /></style-rule>"
                        "</style>")

        rows_xml = " + ".join(f"[{ds}].{inst(*r)}" for r in rows)
        cols_xml = " / ".join(f"[{ds}].{inst(*c)}" for c in cols)
        rows_xml = f"({rows_xml})" if len(rows) > 1 else rows_xml      # dual axis
        cols_xml = f"({cols_xml})" if len(cols) > 1 else cols_xml      # nested dimensions
        worksheets.append(
            f"<worksheet name={quoteattr(sh['sheet'])}>{title_xml(sh)}"
            f"<table><view><datasources><datasource caption={quoteattr(sh['file'][:-4])} name='{ds}' /></datasources>"
            f"<datasource-dependencies datasource='{ds}'>{deps}{instances}</datasource-dependencies>"
            f"<aggregation value='true' /></view>{table_style}"
            f"<panes>{panes}</panes>"
            f"<rows>{rows_xml}</rows><cols>{cols_xml}</cols></table>"
            f"</worksheet>")
        legend = (f"<edge name='right'><strip size='160'><card pane-specification-id='0' "
                  f"param='[{ds}].{inst(colour[0], 'none', 'nk')}' type='color' /></strip></edge>" if colour else "")
        windows.append(
            f"<window class='worksheet' name={quoteattr(sh['sheet'])}><cards>"
            f"<edge name='left'><strip size='160'><card type='pages' /><card type='filters' />"
            f"<card type='marks' /></strip></edge>"
            f"<edge name='top'><strip size='2147483647'><card type='columns' /></strip>"
            f"<strip size='2147483647'><card type='rows' /></strip>"
            f"<strip size='31'><card type='title' /></strip></edge>{legend}</cards>"
            f"</window>")

    return ("<?xml version='1.0' encoding='utf-8' ?>\n"
            "<workbook original-version='18.1' source-build='2023.1.0 (20231.23.0310.1045)' "
            "source-platform='win' version='18.1' xmlns:user='http://www.tableausoftware.com/xml/user'>"
            "<preferences><preference name='ui.encoding.shelf.height' value='24' />"
            "<preference name='ui.shelf.height' value='26' /></preferences>"
            f"<datasources>{''.join(datasources)}</datasources>"
            f"<worksheets>{''.join(worksheets)}</worksheets>"
            f"<windows source-height='30'>{''.join(windows)}</windows>"
            "</workbook>\n")


def main() -> None:
    write_chart_data()
    # .twb beside its Data folder; if Tableau can't resolve the relative path it asks you to locate the files
    TWB.write_text(build_twb("Data"), encoding="utf-8")
    # .twbx: workbook + data packaged together, paths relative to the package
    with zipfile.ZipFile(TWBX, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("NQ1_Poster.twb", build_twb("Data"))
        for f in sorted(DATA_DIR.glob("*.csv")):
            z.write(f, f"Data/{f.name}")
    print(f"Wrote {TWB.relative_to(HERE)}, {TWBX.relative_to(HERE)} and "
          f"{len(list(DATA_DIR.glob('*.csv')))} CSVs in {DATA_DIR.relative_to(HERE)}/")


if __name__ == "__main__":
    main()
