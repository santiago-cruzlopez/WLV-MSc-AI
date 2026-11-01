"""Clean the E-mini Nasdaq-100 continuous futures file (CME NQ1!, daily), export a
Tableau-ready CSV, print the statistics quoted in the poster report, and render
reference versions of the six poster visualisations (to be rebuilt in Tableau).

Data issues handled (found by profiling CME_MINI_DL_NQ1!_1D.csv):
  * 38 rows fall on days the NYSE was closed (holidays, Good Fridays, 9/11,
    Hurricane Sandy, state funerals). These are abbreviated futures-only
    sessions; they are dropped so every row is a full regular session.
  * 10 Apr 2000 is a bad print: an off-tick open equal to the high, close equal
    to the low, -15.8% then +6.5% (the cash index fell 7.1% that day). Dropped.
  * Returns that would span a missing NYSE session (2 Jul 1999 is absent, plus
    the dropped bad print) are set to missing rather than counted as one day.
  * Bars with off-tick prices (not on the 0.25 grid) or High == Low are flagged
    and excluded from the daily-range measure.
  * Moving averages are recomputed on the cleaned closes (the file's own MAs
    include the holiday rows and the bad print).
  * NQ1! is an unadjusted continuous contract: quarterly roll jumps remain in
    the series, and futures returns exclude dividends net of financing.

Run:
    uv run --no-project --with pandas --with numpy --with scipy --with matplotlib \
        --with exchange_calendars python ndx_poster_analysis.py
"""

from pathlib import Path

import textwrap

import exchange_calendars as xc
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import numpy as np
import pandas as pd
from scipy import stats

HERE = Path(__file__).resolve().parent
RAW = HERE / "CME_MINI_DL_NQ1!_1D.csv"
CLEAN = HERE / "NQ_clean_for_tableau.csv"
FIG_DIR = HERE / "poster_visuals"
PRICES = ["Open", "High", "Low", "Close"]
TICK = 0.25
BAD_PRINTS = [pd.Timestamp("2000-04-10")]

# Same validated palette and chart chrome as Weekly_Visuals/generate_weekly_visuals.py
SERIES = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100",
          "#e87ba4", "#008300", "#6250d6", "#e34948"]
SURFACE = "#fcfcfb"
INK = "#0b0b0b"
INK_2 = "#52514e"
MUTED = "#898781"
GRID = "#e1e0d9"
AXIS = "#c3c2b7"
NEUTRAL = "#f0efec"
UP = SERIES[0]
DOWN = "#d03b3b"

plt.rcParams.update({
    "figure.facecolor": SURFACE,
    "axes.facecolor": SURFACE,
    "savefig.facecolor": SURFACE,
    "font.family": "DejaVu Sans",
    "font.size": 10,
    "text.color": INK,
    "axes.labelcolor": INK_2,
    "axes.edgecolor": AXIS,
    "axes.linewidth": 0.8,
    "axes.titlesize": 12,
    "axes.titleweight": "bold",
    "axes.titlelocation": "left",
    "axes.titlepad": 10,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.grid": True,
    "grid.color": GRID,
    "grid.linewidth": 0.6,
    "xtick.color": MUTED,
    "ytick.color": MUTED,
    "legend.frameon": False,
})


def load_raw() -> pd.DataFrame:
    raw = pd.read_csv(RAW)
    raw.index = pd.to_datetime(raw.pop("time"), format="%m/%d/%Y")
    raw.index.name = "Date"
    return raw.rename(columns=str.capitalize)


def nyse_sessions(index: pd.DatetimeIndex) -> pd.DatetimeIndex:
    cal = xc.get_calendar("XNYS", start=index[0] - pd.Timedelta(days=10), end=index[-1])
    return cal.sessions_in_range(index[0], index[-1]).tz_localize(None)


def load_clean() -> pd.DataFrame:
    raw = load_raw()
    assert raw.index.is_unique and raw.index.is_monotonic_increasing
    sessions = nyse_sessions(raw.index)

    off_tick = ((raw[PRICES] / TICK) % 1 > 1e-6).any(axis=1)
    flat = raw["High"] == raw["Low"]
    df = raw.loc[raw.index.isin(sessions) & ~raw.index.isin(BAD_PRINTS), PRICES].copy()

    for n in (21, 63, 252, 756):
        df[f"MA_{n}"] = df["Close"].rolling(n).mean()
    log_ret = np.log(df["Close"]).diff()
    prev_session = pd.Series(sessions, index=sessions).shift().reindex(df.index)
    log_ret[df.index.to_series().shift() != prev_session] = np.nan   # spans a missing session
    df["Log_Return"] = log_ret
    df["Rolling_Vol_21d_Ann"] = log_ret.rolling(21, min_periods=15).std() * np.sqrt(252)
    df["Drawdown"] = df["Close"] / df["Close"].cummax() - 1
    df["Data_Flag"] = np.select([off_tick.reindex(df.index), flat.reindex(df.index)],
                                ["off-tick price", "flat bar (High = Low)"], "")
    df["Daily_Range_Pct"] = ((df["High"] - df["Low"]) / df["Close"]).where(df["Data_Flag"] == "")
    df["Trend_Regime"] = np.where(df["MA_252"].isna(), "n/a",
                                  np.where(df["Close"] > df["MA_252"],
                                           "Above 252-day MA", "Below 252-day MA"))
    df["Year"] = df.index.year
    return df


def annual_returns(df: pd.DataFrame) -> pd.Series:
    year_end = df["Close"].resample("YE").last()
    ann = year_end.pct_change()
    ann.iloc[0] = year_end.iloc[0] / df["Close"].iloc[0] - 1    # first year from first close
    ann.index = ann.index.year
    return ann


def regime_table(df: pd.DataFrame) -> pd.DataFrame:
    # Regime known at today's close, applied to tomorrow's return (no look-ahead).
    g = pd.DataFrame({"regime": df["Trend_Regime"],
                      "next": df["Log_Return"].shift(-1)}).dropna()
    g = g[g["regime"] != "n/a"]
    worst = g["next"] <= g["next"].quantile(0.01)
    return g.groupby("regime").agg(
        days=("next", "size"),
        ann_return=("next", lambda x: x.mean() * 252),
        ann_vol=("next", lambda x: x.std() * np.sqrt(252)),
    ).assign(share_days=lambda t: t["days"] / t["days"].sum(),
             share_worst_1pct=g[worst].groupby("regime").size() / worst.sum())


def regime_split(df: pd.DataFrame, window: int = 252) -> pd.DataFrame:
    """Above/below a moving average at today's close, paired with tomorrow's return."""
    ma = df["Close"].rolling(window).mean()
    above = (df["Close"] > ma).where(ma.notna())
    return pd.DataFrame({"above": above, "next": df["Log_Return"].shift(-1)}).dropna()


def regime_tests(g: pd.DataFrame) -> dict:
    a, b = g.loc[g["above"] == 1, "next"], g.loc[g["above"] == 0, "next"]
    worst = g["next"] <= g["next"].quantile(0.01)
    return {"share_below": len(b) / len(g),
            "ret_above": a.mean() * 252, "ret_below": b.mean() * 252,
            "vol_above": a.std() * np.sqrt(252), "vol_below": b.std() * np.sqrt(252),
            "worst1pct_below": (g.loc[worst, "above"] == 0).mean(),
            "p_return": stats.ttest_ind(a, b, equal_var=False).pvalue,    # Welch t-test
            "p_volatility": stats.levene(a, b).pvalue}


ROBUSTNESS = {"50-day MA": (50, None), "100-day MA": (100, None), "200-day MA": (200, None),
              "252-day MA": (252, None), "252-day MA, 2000–2012": (252, ("2000", "2012")),
              "252-day MA, 2013–2026": (252, ("2013", "2026"))}


def regime_robustness(df: pd.DataFrame) -> pd.DataFrame:
    rows = {}
    for label, (window, span) in ROBUSTNESS.items():
        g = regime_split(df, window)
        rows[label] = regime_tests(g.loc[span[0]:span[1]] if span else g)
    return pd.DataFrame(rows).T


def episode(close: pd.Series, start: str, end: str) -> dict:
    s = close[start:end]
    trough = (s / s.cummax() - 1).idxmin()
    peak = s[:trough].idxmax()
    after = close[trough:]
    regained = after[after >= close[peak]]
    return {"peak": peak, "trough": trough, "depth": close[trough] / close[peak] - 1,
            "regained": regained.index[0] if len(regained) else None}


EPISODES = {"Dot-com bust": ("2000-01", "2003-12"), "GFC": ("2007-09", "2009-12"),
            "COVID-19": ("2020-02", "2020-04"), "2022 rate shock": ("2021-11", "2022-12"),
            "2025 tariff shock": ("2025-01", "2025-05")}


def print_stats(df: pd.DataFrame) -> None:
    c, r = df["Close"], df["Log_Return"].dropna()
    years = (c.index[-1] - c.index[0]).days / 365.25
    z = (r - r.mean()) / r.std()
    ann = annual_returns(df)
    full = ann.loc[c.index[0].year + 1: c.index[-1].year - 1]
    print(f"Rows {len(df)}, {c.index[0].date()} to {c.index[-1].date()}")
    print(f"Close {c.iloc[0]:,.2f} -> {c.iloc[-1]:,.2f} (x{c.iloc[-1] / c.iloc[0]:.1f}), "
          f"price CAGR {(c.iloc[-1] / c.iloc[0]) ** (1 / years) - 1:.1%}")
    print(f"Ann. vol {r.std() * np.sqrt(252):.1%}, skew {stats.skew(r):.2f}, "
          f"excess kurtosis {stats.kurtosis(r):.2f}")
    print(f">3 sd days {(z.abs() > 3).sum()} (normal expects {len(r) * 2 * stats.norm.sf(3):.0f}); "
          f">4 sd {(z.abs() > 4).sum()} (expects {len(r) * 2 * stats.norm.sf(4):.1f})")
    print(f"ACF(1) returns {r.autocorr(1):.3f}; ACF(1/21) |returns| "
          f"{r.abs().autocorr(1):.3f}/{r.abs().autocorr(21):.3f}")
    print(f"Max drawdown {df['Drawdown'].min():.1%} on {df['Drawdown'].idxmin().date()}; "
          f"ATH {c.max():,.2f} on {c.idxmax().date()}")
    print(f"Up full years {(full > 0).sum()}/{len(full)}, median {full.median():.1%}")
    print(f"21d vol median {df['Rolling_Vol_21d_Ann'].median():.1%}, "
          f"p90 {df['Rolling_Vol_21d_Ann'].quantile(.9):.1%}")
    print(regime_table(df).round(3).to_string())


def pct(v: float, decimals: int = 0, sign: bool = False) -> str:
    """Percentage with a typographic minus sign (v is a fraction)."""
    return f"{v:{'+' if sign else ''}.{decimals}%}".replace("-", "−")


def save(fig, name: str) -> None:
    fig.savefig(FIG_DIR / name, dpi=300, bbox_inches="tight")
    plt.close(fig)


def fig_price(df):
    c = df["Close"]
    fig, ax = plt.subplots(figsize=(10, 4.8))
    ax.plot(c, color=UP, lw=1.4, label="Daily settlement (front-month NQ)")
    ax.plot(df["MA_252"], color=SERIES[1], lw=2, label="252-day moving average")
    ax.set_yscale("log")
    ax.set_ylim(350, c.max() * 1.6)
    ax.yaxis.set_major_formatter(mtick.FuncFormatter(lambda v, _: f"{v:,.0f}"))
    dot = episode(c, *EPISODES["Dot-com bust"])
    gfc = episode(c, *EPISODES["GFC"])
    for t, text, xy_text in [
            (dot["peak"], f"Dot-com peak\n{dot['peak']:%b %Y}", (dot["peak"], c[dot["peak"]] * 1.9)),
            (dot["trough"], f"Trough {dot['trough']:%b %Y}\n{pct(dot['depth'])}",
             (dot["trough"], c[dot["trough"]] * 0.55)),
            (gfc["trough"], f"GFC low\n{gfc['trough']:%b %Y}", (gfc["trough"], c[gfc["trough"]] * 0.55)),
            (c.idxmax(), f"All-time high\n{c.idxmax():%b %Y}", (pd.Timestamp("2021-06-01"), c.max() * 1.05))]:
        ax.annotate(text, (t, c[t]), xy_text, fontsize=8.5, color=INK_2, ha="center",
                    arrowprops=dict(arrowstyle="-", color=MUTED, lw=0.7))
    ax.set_title("E-mini Nasdaq-100: a 27-year climb from the dot-com peak, through two deep bear markets")
    ax.set_ylabel("Futures price, index points (log scale)")
    ax.legend(loc="upper left")
    save(fig, "V1_price_trend_log_ma252.png")


def fig_drawdown(df):
    c = df["Close"]
    fig, ax = plt.subplots(figsize=(10, 4))
    dd = df["Drawdown"] * 100
    ax.fill_between(dd.index, dd, 0, color=DOWN, alpha=0.25, lw=0)
    ax.plot(dd, color=DOWN, lw=1)
    # Each label quotes the episode's own peak-to-trough fall; the GFC trough sits
    # inside the dot-com drawdown, so its plotted depth is measured from 2000.
    offsets = {"Dot-com bust": (pd.Timedelta(days=0), -9), "GFC": (pd.Timedelta(days=550), -8),
               "COVID-19": (pd.Timedelta(days=-900), -10), "2022 rate shock": (pd.Timedelta(days=-650), -16),
               "2025 tariff shock": (pd.Timedelta(days=250), -22)}
    for name, (start, end) in EPISODES.items():
        e = episode(c, start, end)
        regained = f"\n(regained {e['regained']:%b %Y})" if name == "Dot-com bust" else ""
        y = dd[e["trough"]]
        dx, dy = offsets[name]
        ax.annotate(f"{name} {pct(e['depth'])}{regained}", (e["trough"], y),
                    (e["trough"] + dx, max(y + dy, -97)), fontsize=8.5, color=INK_2, ha="center",
                    va="center", arrowprops=dict(arrowstyle="-", color=MUTED, lw=0.7))
    ax.set_ylim(-100, 3)
    ax.yaxis.set_major_formatter(mtick.PercentFormatter(decimals=0))
    dot = episode(c, *EPISODES["Dot-com bust"])
    wait = (dot["regained"] - dot["peak"]).days / 365.25
    ax.set_title(f"Drawdown from previous high: the March 2000 peak took {wait:.0f} years to regain")
    ax.set_ylabel("Decline from running peak (%)")
    save(fig, "V2_drawdown_underwater.png")


def fig_annual(df):
    ann = annual_returns(df) * 100
    first, last = ann.index.min(), ann.index.max()
    full = ann.loc[first + 1: last - 1]
    fig, ax = plt.subplots(figsize=(10, 4.2))
    colors = np.where(ann >= 0, UP, DOWN)
    bars = ax.bar(ann.index, ann.values, color=colors, width=0.8)
    for yr in (first, last):                            # partial years drawn lighter
        bars[ann.index.get_loc(yr)].set_alpha(0.4)
        ax.text(yr, ann[yr] + 1.5, "partial" if yr == first else "YTD", ha="center", va="bottom",
                fontsize=7.5, color=MUTED)
    ax.axhline(0, color=AXIS, lw=0.8)
    ax.axhline(full.median(), color=MUTED, lw=1, ls="--")
    ax.text(2005.5, full.median() + 1, f"median {full.median():.0f}%", fontsize=8, color=INK_2,
            ha="center", va="bottom")
    for yr in (2003, 2008, 2022, 2023):
        v = ann[yr]
        ax.text(yr, v + (3 if v > 0 else -3), pct(v / 100, sign=True), ha="center",
                va="bottom" if v > 0 else "top", fontsize=8, color=INK_2)
    ax.yaxis.set_major_formatter(mtick.PercentFormatter(decimals=0))
    ax.set_title(f"Calendar-year return: {(full > 0).sum()} of {len(full)} full years positive, "
                 "but losses cluster in runs")
    ax.set_ylabel("Annual price return (%)")
    ax.set_xlabel(f"Year ({first} from {df.index[0]:%d %b}; {last} year-to-date; median of full years)")
    ax.grid(axis="x", visible=False)
    save(fig, "V3_annual_returns.png")


def fig_volatility(df):
    rv = df["Rolling_Vol_21d_Ann"] * 100
    med, p90 = rv.median(), rv.quantile(0.9)
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.fill_between(rv.index, p90, rv, where=rv > p90, color=SERIES[1], alpha=0.35,
                    lw=0, interpolate=True)
    ax.plot(rv, color=UP, lw=1)
    for y, lab in ((med, f"median {med:.0f}%"), (p90, f"stress line (90th pct) {p90:.0f}%")):
        ax.axhline(y, color=MUTED, lw=0.9, ls="--")
        ax.text(pd.Timestamp("2013-06-01"), y + 1, lab, fontsize=8, color=INK_2, va="bottom",
                bbox=dict(fc=SURFACE, ec="none", pad=1.5))
    for start, end, text in [("2000-01", "2002-12", "2000–02"), ("2008-01", "2009-06", "2008"),
                             ("2020-01", "2020-12", "2020"), ("2025-01", "2025-12", "2025")]:
        t = rv[start:end].idxmax()
        ax.text(t, rv[t] + 3, f"{text}\n{rv[t]:.0f}%", ha="center", fontsize=8.5, color=INK_2)
    ax.set_ylim(0, 118)
    ax.yaxis.set_major_formatter(mtick.PercentFormatter(decimals=0))
    ax.set_title("Volatility clusters: calm regimes punctuated by short, violent storms")
    ax.set_ylabel("21-day realised volatility\n(annualised, %)")
    save(fig, "V4_rolling_volatility_regimes.png")


def fig_distribution(df):
    r = df["Log_Return"].dropna() * 100
    bins = np.arange(-12.5, 16.75, 0.25)
    fig, ax = plt.subplots(figsize=(10, 4.2))
    counts, edges, _ = ax.hist(r, bins=bins, color=UP, alpha=0.85, label="Observed daily returns",
                               edgecolor=SURFACE, linewidth=0.3)
    x = np.linspace(bins[0], bins[-1], 600)
    ax.plot(x, stats.norm.pdf(x, r.mean(), r.std()) * len(r) * 0.25, color=SERIES[1], lw=2,
            label="Normal curve, same mean and s.d.")
    ax.set_yscale("log")
    ax.set_ylim(0.8, counts.max() * 1.6)
    z = (r - r.mean()) / r.std()
    ax.text(0.99, 0.95, f"Excess kurtosis {stats.kurtosis(r):.1f}\n"
            f"Days beyond ±3 s.d.: {(z.abs() > 3).sum()} observed vs "
            f"{len(r) * 2 * stats.norm.sf(3):.0f} expected\n"
            f"Days beyond ±4 s.d.: {(z.abs() > 4).sum()} observed vs "
            f"{len(r) * 2 * stats.norm.sf(4):.1f} expected",
            transform=ax.transAxes, ha="right", va="top", fontsize=8.5, color=INK_2)
    lo, hi = r.idxmin(), r.idxmax()
    ax.annotate(f"{lo.day} {lo:%b %Y}\n{pct(r[lo] / 100, 1, sign=True)}", (r[lo], 1), (r[lo] + 1.5, 30),
                fontsize=8, color=INK_2, ha="center", arrowprops=dict(arrowstyle="-", color=MUTED, lw=0.7))
    ax.annotate(f"{hi.day} {hi:%b %Y}\n{r[hi]:+.1f}%", (r[hi], 1), (r[hi] - 1.5, 30), fontsize=8,
                color=INK_2, ha="center", arrowprops=dict(arrowstyle="-", color=MUTED, lw=0.7))
    ax.xaxis.set_major_formatter(mtick.PercentFormatter(decimals=0))
    ax.set_title("Daily returns have fat tails: extreme days are far more common than a bell curve predicts")
    ax.set_xlabel("Daily log return (%), 0.25-point bins")
    ax.set_ylabel("Number of days (log scale)")
    ax.legend(loc="upper left")
    save(fig, "V5_return_distribution_fat_tails.png")


def fig_regime(df):
    t = regime_table(df).loc[["Above 252-day MA", "Below 252-day MA"]]
    colors = [UP, SERIES[1]]
    metrics = [("share_days", "Share of trading days"),
               ("ann_return", "Annualised next-day return"),
               ("ann_vol", "Annualised volatility"),
               ("share_worst_1pct", "Share of worst 1% of days")]
    fig, axes = plt.subplots(1, 4, figsize=(10, 3.6), sharey=False)
    for ax, (col, title) in zip(axes, metrics):
        vals = t[col] * 100
        ax.bar([0, 1], vals, color=colors, width=0.6)
        top = vals.abs().max()
        for i, v in enumerate(vals):
            ax.text(i, v + (top * 0.03 if v >= 0 else -top * 0.03), pct(v / 100),
                    ha="center", va="bottom" if v >= 0 else "top", fontsize=9.5, color=INK)
        ax.axhline(0, color=AXIS, lw=0.8)
        ax.set_title(title, fontsize=9.5, loc="center")
        ax.set_xticks([0, 1], ["Above", "Below"])
        ax.set_ylim(min(0, vals.min() * 1.4), top * 1.22)
        ax.yaxis.set_visible(False)
        ax.spines["left"].set_visible(False)
        ax.spines["bottom"].set_visible(False)
        ax.grid(False)
    fig.suptitle("Trend regimes: below its 252-day average, risk more than doubles and most crash days occur",
                 x=0.01, ha="left", fontweight="bold", fontsize=12)
    first = df["MA_252"].first_valid_index()
    tests = regime_tests(regime_split(df))
    fig.text(0.01, -0.07, "Regime = settlement above/below its 252-day moving average, applied to the "
             f"next day's return (no look-ahead), {first:%b %Y}–{df.index[-1]:%b %Y}. The volatility gap is "
             f"statistically significant (Levene p < 0.001);\nthe return gap is not "
             f"(Welch p = {tests['p_return']:.2f}) and reverses after 2013, so read the regime as a risk "
             "signal, not a return forecast.", fontsize=8, color=MUTED)
    fig.tight_layout()
    save(fig, "V6_trend_regime_scorecard.png")


def fig_poster_layout(df):
    """A1 portrait layout reference (594 x 841 mm) composed from the six chart PNGs."""
    c, r = df["Close"], df["Log_Return"].dropna()
    years = (c.index[-1] - c.index[0]).days / 365.25
    z = (r - r.mean()) / r.std()
    dot = episode(c, *EPISODES["Dot-com bust"])
    t = regime_tests(regime_split(df))
    ann = annual_returns(df)
    full = ann.loc[c.index[0].year + 1: c.index[-1].year - 1]
    rv = df["Rolling_Vol_21d_Ann"]

    fig = plt.figure(figsize=(23.39, 33.11))
    fig.patch.set_facecolor(SURFACE)

    def box(x, y, w, h, heading, body, width, size=19):
        ax = fig.add_axes([x, y, w, h])
        ax.axis("off")
        ax.add_patch(plt.Rectangle((0, 0), 1, 1, transform=ax.transAxes, fc=NEUTRAL, ec="none"))
        ax.text(0.04, 0.94, heading, fontsize=26, fontweight="bold", color=UP, va="top",
                transform=ax.transAxes)
        ax.text(0.04, 0.78, "\n".join(textwrap.fill(p, width) for p in body.split("\n")),
                fontsize=size, color=INK, va="top", linespacing=1.35, transform=ax.transAxes)

    def chart(x, y, w, h, png, caption):
        ax = fig.add_axes([x, y + 0.028, w, h - 0.028])
        ax.imshow(mpimg.imread(FIG_DIR / png))
        ax.axis("off")
        fig.text(x + 0.005, y + 0.024, textwrap.fill(caption, 92), fontsize=16, color=INK_2,
                 va="top", linespacing=1.35)

    # Header band
    fig.text(0.03, 0.978, "Trend, Volatility and Market States in E-mini Nasdaq-100 Futures, 1999–2026",
             fontsize=33, fontweight="bold", color=INK, va="top")
    fig.text(0.03, 0.955, "Santiago Cruz  ·  Student ID 2584023  ·  7CS079 Data Visualisation  ·  "
             "University of Wolverhampton", fontsize=22, color=INK_2, va="top")
    fig.add_artist(plt.Line2D([0.03, 0.97], [0.938, 0.938], color=UP, lw=4))

    # Row 1: introduction, data & method, headline numbers
    box(0.03, 0.765, 0.30, 0.165, "Introduction",
        "The E-mini Nasdaq-100 future (NQ) is the most traded derivative on the leading "
        "technology-stock index. Since 1999 it has grown twelvefold, through crashes that "
        "averages hide.\nRQ1 How deep and long were the trend's interruptions?\n"
        "RQ2 How is risk spread over time and across days?\n"
        "RQ3 Does the 252-day average separate calm from turbulent markets?", 40)
    box(0.35, 0.765, 0.30, 0.165, "Data and Method",
        f"Daily OHLC of CME NQ1!, {c.index[0]:%b %Y}–{c.index[-1]:%b %Y} (TradingView, 2026). "
        "A Python audit removed 38 futures-only holiday sessions and one bad print and "
        f"flagged nine anomalous bars, leaving {len(df):,} sessions.\nTableau: calculated fields "
        "(LOOKUP, WINDOW_STDEV, RUNNING_MAX, LOD), reference lines, bins and a "
        "filter-linked dashboard. Colour-blind-safe palette, one axis per chart.", 40)
    tiles = [(f"×{c.iloc[-1] / c.iloc[0]:.1f}", f"price growth\n({(c.iloc[-1] / c.iloc[0]) ** (1 / years) - 1:.1%} a year)"),
             (pct(dot["depth"]), f"worst fall; regained\nafter {(dot['regained'] - dot['peak']).days / 365.25:.0f} years"),
             (f"{(z.abs() > 3).sum()} vs {len(r) * 2 * stats.norm.sf(3):.0f}", "3-sigma days:\nactual vs bell curve"),
             (f"{t['vol_below'] / t['vol_above']:.1f}×", "volatility below\nthe 252-day average")]
    for i, (big, small) in enumerate(tiles):
        ax = fig.add_axes([0.67 + (i % 2) * 0.153, 0.850 - (i // 2) * 0.085, 0.147, 0.080])
        ax.axis("off")
        ax.add_patch(plt.Rectangle((0, 0), 1, 1, transform=ax.transAxes, fc=NEUTRAL, ec="none"))
        ax.text(0.5, 0.66, big, fontsize=38, fontweight="bold", color=UP, ha="center", va="center")
        ax.text(0.5, 0.24, small, fontsize=16, color=INK_2, ha="center", va="center")

    # Rows 2-4: the six charts, two per row
    captions = [
        ("V1_price_trend_log_ma252.png", f"O1 · Twelvefold growth, but the March 2000 peak was not regained until "
         f"{dot['regained']:%Y}. Since 2009 the trend has been steeper and steadier."),
        ("V2_drawdown_underwater.png", "O1 · Depth and duration differ: the dot-com bust lasted 16 years, while "
         "COVID (−28%) and the 2025 tariff shock (−23%) recovered within months."),
        ("V3_annual_returns.png", f"O1 · {(full > 0).sum()} of {len(full)} full years rose (median "
         f"{full.median():+.0%}), but losses cluster: 2000–02 fell three years running."),
        ("V4_rolling_volatility_regimes.png", f"O2 · Volatility clusters around an {rv.median():.0%} median, "
         "with storms near 100%. In stress, there is a 65% chance of still being in stress a month later."),
        ("V5_return_distribution_fat_tails.png", f"O2 · Fat tails: {(z.abs() > 4).sum()} four-sigma days where "
         "a bell curve expects fewer than one. Normal-based risk models understate crash risk."),
        ("V6_trend_regime_scorecard.png", f"O3 · Below the 252-day average, volatility is {t['vol_below']:.0%} vs "
         f"{t['vol_above']:.0%} and {t['worst1pct_below']:.0%} of the worst days occur. A risk signal, not a "
         "return forecast."),
    ]
    for i, (png, cap) in enumerate(captions):
        chart(0.03 + (i % 2) * 0.48, 0.570 - (i // 2) * 0.183, 0.46, 0.183, png, cap)

    # Row 5: discussion, conclusion, references
    box(0.03, 0.025, 0.30, 0.150, "Discussion",
        "Averages hide very different investor experiences: entry date mattered as much as "
        "holding period. Clustering and fat tails reproduce the stylised facts of returns "
        "(Mandelbrot, 1963; Cont, 2001). The trend regime robustly separates risk states across "
        "every average length tested, but return differences are not significant, which fits "
        "the Adaptive Markets view (Lo, 2004) better than a simple trading rule.", 44, 17)
    box(0.35, 0.025, 0.30, 0.150, "Conclusion",
        "Long-run growth came with episodic, clustered and fat-tailed risk. Market dashboards "
        "should show drawdown and rolling volatility beside price; risk and margin planning "
        "should not assume normality; and a visible 252-day line is a useful context layer for "
        "non-specialists. Future work: roll-adjusted data, GARCH and regime-switching models, "
        "and a Tableau Public dashboard.", 44, 17)
    box(0.67, 0.025, 0.30, 0.150, "References",
        "Cont (2001) Quant. Finance 1(2).\nLo (2004) J. Portfolio Mgmt 30(5).\n"
        "Mandelbrot (1963) J. Business 36(4).\nMoskowitz et al. (2012) J. Fin. Econ. 104(2).\n"
        "Munzner (2014) Visualization Analysis and Design.\nTradingView (2026) CME_MINI:NQ1! data.\n"
        "Tufte (2001) Visual Display of Quantitative Information.", 48, 15)
    fig.text(0.97, 0.008, "Layout reference: replace the chart images with the Tableau exports.",
             fontsize=12, color=MUTED, ha="right")
    fig.savefig(FIG_DIR / "poster_layout_A1_reference.png", dpi=100)
    plt.close(fig)


def main() -> None:
    FIG_DIR.mkdir(exist_ok=True)
    df = load_clean()
    df.round(6).to_csv(CLEAN, index_label="Date")
    print_stats(df)
    for fig in (fig_price, fig_drawdown, fig_annual, fig_volatility, fig_distribution, fig_regime,
                fig_poster_layout):
        fig(df)
    print(f"Wrote {CLEAN.name} and {len(list(FIG_DIR.glob('*.png')))} figures to {FIG_DIR.name}/")


if __name__ == "__main__":
    main()
