"""Redraw the six poster visualisations (V1-V6) in the look of Tableau worksheet exports.

Reads the cleaned file written by NQ1_Poster_Analysis.ipynb
(spreadsheets_assessment/NQ_clean_for_tableau.csv) and writes 300-dpi PNGs to
poster_visuals_v2/. The statistics are the same as the notebook's; only the styling changes:

- Tableau's built-in "Color Blind" palette (blue #1170AA / orange #C85200, lighter
  tints #A3CCE9 / #FFBC79 for secondary marks), never red/green;
- a worksheet title with a grey subtitle line, Tableau-grey axes and light gridlines;
- a legend card on the right, labelled reference lines and boxed "Annotate Point" notes;
- Tableau-style discrete headers (V3 years, V6 metric panes) and K-formatted axes.

Run from the assessment folder:
    uv run --no-project --with pandas --with numpy --with scipy --with matplotlib \
        python build_tableau_style_visuals.py
"""

import logging
from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import numpy as np
import pandas as pd
from matplotlib.lines import Line2D
from matplotlib.patches import Patch
from scipy import stats

HERE = Path(__file__).resolve().parent
CLEAN = HERE / "spreadsheets_assessment" / "NQ_clean_for_tableau.csv"
FIG_DIR = HERE / "poster_visuals_v2"
FIG_DIR.mkdir(exist_ok=True)

logging.getLogger("matplotlib.font_manager").setLevel(logging.ERROR)   # fallback fonts lack semibold

# Tableau "Color Blind" palette and worksheet chrome
BLUE, ORANGE = "#1170AA", "#C85200"
LIGHT_BLUE, LIGHT_ORANGE = "#A3CCE9", "#FFBC79"
TITLE = "#333333"
TEXT = "#555555"
TICK_INK = "#666666"
GRID = "#E6E6E6"
RULER = "#C8C8C8"
REF = "#7F7F7F"
WHITE = "#FFFFFF"

plt.rcParams.update({
    "font.family": ["Lato", "Liberation Sans", "DejaVu Sans"],
    "font.size": 9.5,
    "figure.facecolor": WHITE,
    "axes.facecolor": WHITE,
    "savefig.facecolor": WHITE,
    "text.color": TITLE,
    "axes.labelcolor": TEXT,
    "axes.labelsize": 9.5,
    "axes.edgecolor": RULER,
    "axes.linewidth": 0.7,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.grid": True,
    "axes.axisbelow": True,
    "grid.color": GRID,
    "grid.linewidth": 0.6,
    "xtick.color": RULER,
    "ytick.color": RULER,
    "xtick.labelcolor": TICK_INK,
    "ytick.labelcolor": TICK_INK,
    "xtick.labelsize": 9,
    "ytick.labelsize": 9,
    "xtick.major.size": 3,
    "ytick.major.size": 0,
    "legend.frameon": False,
})

EPISODES = {"Dot-com bust": ("2000-01", "2003-12"), "GFC": ("2007-09", "2009-12"),
            "COVID-19": ("2020-02", "2020-04"), "2022 rate shock": ("2021-11", "2022-12"),
            "2025 tariff shock": ("2025-01", "2025-05")}


# ----------------------------------------------------------------------------------
# Data and metrics (same definitions as the notebook)
# ----------------------------------------------------------------------------------
def load() -> pd.DataFrame:
    return pd.read_csv(CLEAN, parse_dates=["Date"], index_col="Date")


def annual_returns(df: pd.DataFrame) -> pd.Series:
    year_end = df["Close"].resample("YE").last()
    ann = year_end.pct_change()
    ann.iloc[0] = year_end.iloc[0] / df["Close"].iloc[0] - 1
    ann.index = ann.index.year
    return ann


def regime_table(df: pd.DataFrame) -> pd.DataFrame:
    g = pd.DataFrame({"regime": df["Trend_Regime"], "next": df["Log_Return"].shift(-1)}).dropna()
    g = g[g["regime"] != "n/a"]
    worst = g["next"] <= g["next"].quantile(0.01)
    return g.groupby("regime").agg(
        days=("next", "size"),
        ann_return=("next", lambda x: x.mean() * 252),
        ann_vol=("next", lambda x: x.std() * np.sqrt(252)),
    ).assign(share_days=lambda t: t["days"] / t["days"].sum(),
             share_worst_1pct=g[worst].groupby("regime").size() / worst.sum())


def regime_p_return(df: pd.DataFrame) -> float:
    ma = df["Close"].rolling(252).mean()
    above = (df["Close"] > ma).where(ma.notna())
    g = pd.DataFrame({"above": above, "next": df["Log_Return"].shift(-1)}).dropna()
    return stats.ttest_ind(g.loc[g["above"] == 1, "next"], g.loc[g["above"] == 0, "next"],
                           equal_var=False).pvalue


def episode(close: pd.Series, start: str, end: str) -> dict:
    s = close[start:end]
    trough = (s / s.cummax() - 1).idxmin()
    peak = s[:trough].idxmax()
    after = close[trough:]
    regained = after[after >= close[peak]]
    return {"peak": peak, "trough": trough, "depth": close[trough] / close[peak] - 1,
            "regained": regained.index[0] if len(regained) else None}


def pct(v: float, decimals: int = 0, sign: bool = False) -> str:
    return f"{v:{'+' if sign else ''}.{decimals}%}".replace("-", "−")


# ----------------------------------------------------------------------------------
# Tableau worksheet chrome
# ----------------------------------------------------------------------------------
def worksheet(figsize=(11, 5), legend=True):
    """Figure with a title band, a plot pane and (optionally) a legend column on the right."""
    fig = plt.figure(figsize=figsize)
    right = 0.80 if legend else 0.975
    ax = fig.add_axes([0.075, 0.13, right - 0.075, 0.68])
    return fig, ax


def titles(fig, title: str, subtitle: str) -> None:
    fig.text(0.012, 0.965, title, fontsize=14.5, fontweight="semibold", color=TITLE, va="top")
    fig.text(0.012, 0.895, subtitle, fontsize=10, color=TEXT, va="top")


def legend_card(fig, heading: str, handles, x=0.815, y=0.80) -> None:
    fig.text(x, y, heading, fontsize=9.5, fontweight="bold", color=TITLE, va="top")
    fig.legend(handles=handles, loc="upper left", bbox_to_anchor=(x - 0.008, y - 0.03),
               fontsize=9, labelcolor=TITLE, handlelength=1.6, handleheight=0.9,
               borderaxespad=0, labelspacing=0.6)


def caption(fig, text: str, y=0.02) -> None:
    fig.text(0.012, y, text, fontsize=8.5, color=TICK_INK, va="bottom", linespacing=1.4)


def annotate(ax, text, xy, xytext, ha="center", **kw) -> None:
    """Tableau 'Annotate Point': white box with a thin grey border and a leader line."""
    ax.annotate(text, xy, xytext, fontsize=8.5, color=TITLE, ha=ha, va="center",
                bbox=dict(boxstyle="square,pad=0.35", fc=WHITE, ec="#BDBDBD", lw=0.6),
                arrowprops=dict(arrowstyle="-", color="#8C8C8C", lw=0.7, shrinkA=0, shrinkB=1),
                zorder=6, **kw)


def ref_line(ax, y, label, color=REF) -> None:
    """Tableau reference line: dashed line with its value label at the end of the pane."""
    ax.axhline(y, color=color, lw=1, ls=(0, (4, 3)), zorder=3)
    ax.text(1.008, y, label, transform=ax.get_yaxis_transform(), fontsize=8.5, color=TITLE,
            ha="left", va="center", clip_on=False)


def k_fmt(v, _=None) -> str:
    return f"{v / 1000:g}K" if v >= 1000 else f"{v:g}"


def date_axis(ax, df) -> None:
    ax.set_xlim(pd.Timestamp("1999-01-01"), pd.Timestamp("2027-01-01"))
    ax.xaxis.set_major_locator(mtick.FixedLocator(
        [pd.Timestamp(f"{y}-01-01").toordinal() - 719163 for y in range(2000, 2028, 2)]))
    ax.xaxis.set_major_formatter(mtick.FuncFormatter(
        lambda v, _: f"{pd.Timestamp('1970-01-01') + pd.Timedelta(days=v):%Y}"))
    ax.set_xlabel("Date (trading day)", labelpad=6)


def save(fig, name: str) -> None:
    fig.savefig(FIG_DIR / name, dpi=300, bbox_inches="tight", pad_inches=0.15)
    plt.close(fig)
    print(f"wrote {FIG_DIR.name}/{name}")


# ----------------------------------------------------------------------------------
# V1-V6
# ----------------------------------------------------------------------------------
def fig_price(df):
    c = df["Close"]
    fig, ax = worksheet()
    ax.plot(c, color=BLUE, lw=1.1, zorder=4)
    ax.plot(df["MA_252"], color=ORANGE, lw=2, zorder=5)
    ax.set_yscale("log")
    ax.set_ylim(400, 60000)
    ax.yaxis.set_major_locator(mtick.FixedLocator([500, 1000, 2000, 5000, 10000, 20000, 50000]))
    ax.yaxis.set_minor_locator(mtick.NullLocator())
    ax.yaxis.set_major_formatter(mtick.FuncFormatter(k_fmt))
    date_axis(ax, df)
    ax.set_ylabel("Price (index points, log scale)")

    dot = episode(c, *EPISODES["Dot-com bust"])
    gfc = episode(c, *EPISODES["GFC"])
    ath = c.idxmax()
    years = (c.index[-1] - c.index[0]).days / 365.25
    annotate(ax, f"Dot-com peak  {dot['peak']:%b %Y}\n{c[dot['peak']]:,.0f}",
             (dot["peak"], c[dot["peak"]]), (pd.Timestamp("2003-06-01"), 14000))
    annotate(ax, f"Trough  {dot['trough']:%b %Y}\n{pct(dot['depth'])} from peak",
             (dot["trough"], c[dot["trough"]]), (pd.Timestamp("2004-06-01"), 560))
    annotate(ax, f"GFC low  {gfc['trough']:%b %Y}\n{pct(gfc['depth'])}",
             (gfc["trough"], c[gfc["trough"]]), (pd.Timestamp("2011-06-01"), 700))
    annotate(ax, f"All-time high  {ath:%b %Y}\n{c[ath]:,.0f}",
             (ath, c[ath]), (pd.Timestamp("2019-06-01"), 42000))
    annotate(ax, "2022: the only sustained\nbreak below the average\nsince 2009",
             (pd.Timestamp("2022-10-15"), c["2022-10-15":].iloc[0]),
             (pd.Timestamp("2024-03-01"), 3200))

    titles(fig, "E-mini Nasdaq-100: a 27-year climb from the dot-com peak, through two deep bear markets",
           f"Daily settlement of the front-month NQ contract and its 252-day moving average, "
           f"{c.index[0]:%b %Y} – {c.index[-1]:%b %Y}  |  ×{c.iloc[-1] / c.iloc[0]:.1f} "
           f"(≈{(c.iloc[-1] / c.iloc[0]) ** (1 / years) - 1:.1%} a year)")
    legend_card(fig, "Measure Names", [
        Line2D([], [], color=BLUE, lw=2, label="Daily settlement"),
        Line2D([], [], color=ORANGE, lw=2.5, label="252-day moving average")])
    caption(fig, "Log scale: equal vertical distances are equal percentage moves.  "
                 "Source: CME Globex via TradingView (CME_MINI:NQ1!).", y=0.0)
    save(fig, "V1_price_trend_log_ma252.png")


def fig_drawdown(df):
    c = df["Close"]
    dd = df["Drawdown"] * 100
    fig, ax = worksheet(legend=False)
    ax.fill_between(dd.index, dd, 0, color=ORANGE, alpha=0.78, lw=0, zorder=3)
    ax.axhline(0, color="#9E9E9E", lw=0.8, zorder=4)
    ax.set_ylim(-100, 2)
    ax.yaxis.set_major_locator(mtick.MultipleLocator(20))
    ax.yaxis.set_major_formatter(mtick.FuncFormatter(lambda v, _: f"{v:.0f}%".replace("-", "−")))
    date_axis(ax, df)
    ax.set_ylabel("Drawdown from running peak")

    text_pos = {"Dot-com bust": (pd.Timestamp("2005-09-01"), -92),
                "GFC": (pd.Timestamp("2011-03-01"), -86),
                "COVID-19": (pd.Timestamp("2017-09-01"), -44),
                "2022 rate shock": (pd.Timestamp("2020-10-01"), -60),
                "2025 tariff shock": (pd.Timestamp("2024-12-01"), -42)}
    for name, (start, end) in EPISODES.items():
        e = episode(c, start, end)
        extra = (f"\nregained {e['regained']:%b %Y}" if name == "Dot-com bust" else
                 f"\nregained in {(e['regained'] - e['peak']).days / 30.44:.0f} months"
                 if e["regained"] is not None and name != "GFC" else "")
        annotate(ax, f"{name}  {pct(e['depth'])}{extra}", (e["trough"], dd[e["trough"]]),
                 text_pos[name])

    dot = episode(c, *EPISODES["Dot-com bust"])
    wait = (dot["regained"] - dot["peak"]).days / 365.25
    titles(fig, f"Drawdown from previous high: the March 2000 peak took {wait:.0f} years to regain",
           "Percentage below the highest settlement so far; each label quotes the episode's own "
           "peak-to-trough fall")
    caption(fig, "The GFC trough sits inside the dot-com drawdown, so its plotted depth is measured "
                 "from 2000; its own fall from the Oct 2007 high was "
                 f"{pct(episode(c, *EPISODES['GFC'])['depth'])}.", y=0.0)
    save(fig, "V2_drawdown_underwater.png")


def fig_annual(df):
    ann = annual_returns(df) * 100
    first, last = ann.index.min(), ann.index.max()
    full = ann.loc[first + 1: last - 1]
    fig, ax = worksheet()
    x = np.arange(len(ann))
    partial = ann.index.isin([first, last])
    colours = np.where(ann >= 0, np.where(partial, LIGHT_BLUE, BLUE),
                       np.where(partial, LIGHT_ORANGE, ORANGE))
    ax.bar(x, ann.values, color=colours, width=0.72, zorder=3)
    ax.axhline(0, color="#9E9E9E", lw=0.8, zorder=4)
    ref_line(ax, full.median(), f"Median, full years: {full.median():.0f}%")

    annotate(ax, f"{last} year-to-date\n{pct(ann[last] / 100, sign=True)}", (len(ann) - 1, 0),
             (len(ann) - 2.4, -24))
    label_years = {2000, 2001, 2002, 2003, 2008, 2009, 2022, 2023, first}
    for i, (yr, v) in enumerate(ann.items()):
        if yr in label_years:
            tag = " partial" if yr == first else ""
            ax.text(i, v + (2 if v >= 0 else -2), pct(v / 100, sign=True) + tag,
                    ha="center", va="bottom" if v >= 0 else "top", fontsize=7.8, color=TITLE,
                    rotation=0, zorder=5)
    ax.set_xticks(x, ann.index.astype(str), rotation=90, fontsize=8.5)
    ax.tick_params(axis="x", length=0, pad=4)
    ax.set_xlim(-0.6, len(ann) - 0.4)
    ax.set_ylim(-52, 72)
    ax.grid(axis="x", visible=False)
    ax.spines["bottom"].set_visible(False)
    ax.yaxis.set_major_formatter(mtick.FuncFormatter(lambda v, _: f"{v:.0f}%".replace("-", "−")))
    ax.set_ylabel("Annual price return")
    ax.set_xlabel("Year", labelpad=6)

    titles(fig, f"Calendar-year return: {(full > 0).sum()} of {len(full)} full years positive, "
                "but losses cluster in runs",
           f"Year-end to year-end change in settlement; {first} runs from {df.index[0]:%d %b}, "
           f"{last} is year-to-date (lighter bars)")
    legend_card(fig, "Result", [
        Patch(color=BLUE, label="Gain"), Patch(color=ORANGE, label="Loss"),
        Patch(color=LIGHT_BLUE, label="Gain (partial year)")])
    save(fig, "V3_annual_returns.png")


def fig_volatility(df):
    rv = df["Rolling_Vol_21d_Ann"].dropna() * 100
    med, p90 = rv.median(), rv.quantile(0.9)
    fig, ax = worksheet()
    ax.fill_between(rv.index, p90, rv, where=rv > p90, color=LIGHT_ORANGE, lw=0,
                    interpolate=True, zorder=2)
    ax.plot(rv, color=BLUE, lw=0.9, zorder=4)
    ref_line(ax, med, f"Median: {med:.0f}%")
    ref_line(ax, p90, f"Stress line: {p90:.0f}%", color=ORANGE)
    date_axis(ax, df)
    ax.set_ylim(0, 115)
    ax.yaxis.set_major_locator(mtick.MultipleLocator(20))
    ax.yaxis.set_major_formatter(mtick.PercentFormatter(decimals=0))
    ax.set_ylabel("21-day realised volatility (annualised)")

    for (start, end), dx, dy in [(("2000-01", "2002-12"), 900, 5), (("2008-01", "2009-06"), 700, 8),
                                 (("2020-01", "2020-12"), -1100, 4), (("2025-01", "2025-12"), -500, 30)]:
        t = rv[start:end].idxmax()
        annotate(ax, f"{t:%b %Y}\n{rv[t]:.0f}%", (t, rv[t]), (t + pd.Timedelta(days=dx), rv[t] + dy))

    titles(fig, "Volatility clusters: calm regimes punctuated by short, violent storms",
           "Rolling 21-day standard deviation of daily log returns × √252; "
           "shaded where volatility is above the stress line")
    legend_card(fig, "Measure Names", [
        Line2D([], [], color=BLUE, lw=2, label="21-day realised volatility"),
        Patch(color=LIGHT_ORANGE, label="Above stress line"),
        Line2D([], [], color=REF, lw=1.2, ls=(0, (4, 3)), label="Median"),
        Line2D([], [], color=ORANGE, lw=1.2, ls=(0, (4, 3)), label="Stress line (90th pct)")])
    save(fig, "V4_rolling_volatility_regimes.png")


def fig_distribution(df):
    r = df["Log_Return"].dropna() * 100
    bins = np.arange(-12.5, 16.75, 0.25)
    counts, edges = np.histogram(r, bins=bins)
    centres = edges[:-1] + 0.125
    fig, ax = worksheet()
    ax.bar(centres, np.where(counts > 0, counts, np.nan), width=0.25, color=BLUE,
           edgecolor=WHITE, linewidth=0.25, zorder=3)
    x = np.linspace(-6, 6, 600)
    ax.plot(x, stats.norm.pdf(x, r.mean(), r.std()) * len(r) * 0.25, color=ORANGE, lw=2.2, zorder=4)
    ax.set_yscale("log")
    ax.set_ylim(0.7, counts.max() * 1.8)
    ax.yaxis.set_major_locator(mtick.FixedLocator([1, 10, 100, 1000]))
    ax.yaxis.set_minor_locator(mtick.NullLocator())
    ax.yaxis.set_major_formatter(mtick.FuncFormatter(k_fmt))
    ax.set_xlim(-14, 18)
    ax.xaxis.set_major_locator(mtick.MultipleLocator(2))
    ax.xaxis.set_major_formatter(mtick.FuncFormatter(lambda v, _: f"{v:.0f}%".replace("-", "−")))
    ax.set_xlabel("Daily log return (bins of 0.25%)", labelpad=6)
    ax.set_ylabel("Number of days (log scale)")

    z = (r - r.mean()) / r.std()
    ax.text(0.985, 0.95,
            f"Excess kurtosis  {stats.kurtosis(r):.1f}\n"
            f"Beyond ±3 s.d.   {(z.abs() > 3).sum()} days observed  vs  "
            f"{len(r) * 2 * stats.norm.sf(3):.0f} expected\n"
            f"Beyond ±4 s.d.   {(z.abs() > 4).sum()} days observed  vs  "
            f"{len(r) * 2 * stats.norm.sf(4):.1f} expected",
            transform=ax.transAxes, ha="right", va="top", fontsize=8.8, color=TITLE,
            linespacing=1.6, zorder=6,
            bbox=dict(boxstyle="square,pad=0.6", fc="#F5F5F5", ec="#BDBDBD", lw=0.6))
    lo, hi = r.idxmin(), r.idxmax()
    annotate(ax, f"{lo.day} {lo:%b %Y}\n{pct(r[lo] / 100, 1, sign=True)}", (r[lo], 1.05), (r[lo] + 1.2, 40))
    annotate(ax, f"{hi.day} {hi:%b %Y}\n{pct(r[hi] / 100, 1, sign=True)}", (r[hi], 1.05), (r[hi] - 1.2, 40))

    titles(fig, "Daily returns have fat tails: extreme days are far more common than a bell curve predicts",
           f"Histogram of {len(r):,} daily log returns against a normal curve with the same mean "
           "and standard deviation")
    legend_card(fig, "Measure Names", [
        Patch(color=BLUE, label="Observed daily returns"),
        Line2D([], [], color=ORANGE, lw=2.5, label="Normal curve\n(same mean and s.d.)")])
    save(fig, "V5_return_distribution_fat_tails.png")


def fig_regime(df):
    t = regime_table(df).loc[["Above 252-day MA", "Below 252-day MA"]]
    metrics = [("share_days", "Share of trading days"),
               ("ann_return", "Annualised next-day return"),
               ("ann_vol", "Annualised volatility"),
               ("share_worst_1pct", "Share of worst 1% of days")]
    fig = plt.figure(figsize=(11, 5))
    left, right, bottom, top = 0.012, 0.80, 0.17, 0.71
    w = (right - left) / 4
    lo = min(0, (t["ann_return"] * 100).min() * 2.8)
    hi = (t[[m for m, _ in metrics]] * 100).max().max() * 1.18
    for k, (col, name) in enumerate(metrics):
        ax = fig.add_axes([left + k * w, bottom, w, top - bottom])
        vals = t[col].values * 100
        ax.bar([0, 1], vals, color=[BLUE, ORANGE], width=0.62, zorder=3)
        ax.axhline(0, color="#9E9E9E", lw=0.8, zorder=4)
        for i, v in enumerate(vals):
            ax.text(i, v + (2 if v >= 0 else -2), pct(v / 100), ha="center",
                    va="bottom" if v >= 0 else "top", fontsize=11, fontweight="semibold", color=TITLE)
        ax.set_ylim(lo, hi)
        ax.set_xlim(-0.6, 1.6)
        ax.set_xticks([0, 1], ["Above", "Below"], fontsize=9.5)
        ax.tick_params(axis="x", length=0, pad=6)
        ax.yaxis.set_visible(False)
        ax.grid(False)
        for s in ("left", "bottom"):
            ax.spines[s].set_visible(False)
        # Tableau column divider between panes
        if k:
            fig.add_artist(Line2D([left + k * w] * 2, [bottom - 0.08, top + 0.075], color="#D9D9D9", lw=0.8))
        fig.text(left + (k + 0.5) * w, top + 0.04, name, ha="center", va="center", fontsize=10,
                 fontweight="semibold", color=TITLE)
    # Header band rules, as Tableau draws them around a discrete column header
    for y in (top + 0.075, top + 0.005, bottom - 0.08):
        fig.add_artist(Line2D([left, right], [y, y], color="#D9D9D9", lw=0.8))
    fig.text(left, top + 0.10, "Metric", fontsize=8.5, color=TICK_INK, va="bottom")
    fig.text(left, bottom - 0.095, "Regime (settlement vs its 252-day moving average)",
             fontsize=8.5, color=TICK_INK, va="top")

    titles(fig, "Trend regimes: below its 252-day average, risk more than doubles and most crash days occur",
           "Regime at today's settlement paired with the next day's return (no look-ahead), "
           f"{df['MA_252'].first_valid_index():%b %Y} – {df.index[-1]:%b %Y}")
    legend_card(fig, "Regime", [Patch(color=BLUE, label="Above 252-day MA"),
                                Patch(color=ORANGE, label="Below 252-day MA")])
    caption(fig, "The volatility gap is statistically significant (Levene p < 0.001); the return gap is not "
                 f"(Welch p = {regime_p_return(df):.2f}) and reverses after 2013.\n"
                 "Read the regime as a risk signal, not a return forecast.", y=-0.04)
    save(fig, "V6_trend_regime_scorecard.png")


if __name__ == "__main__":
    data = load()
    for build in (fig_price, fig_drawdown, fig_annual, fig_volatility, fig_distribution, fig_regime):
        build(data)
