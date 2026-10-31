"""Generate one illustrative figure per week of 7CS079 Data Visualisation.

Each figure applies that week's visualisation concept to an algorithmic
trading or network engineering scenario. All data is synthetic.

Run from any directory:
    python generate_weekly_visuals.py
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.lines import Line2D
from matplotlib.patches import FancyBboxPatch, PathPatch
from matplotlib.path import Path as MplPath

OUT_DIR = Path(__file__).resolve().parent
RNG = np.random.default_rng(7)

# Validated categorical order (light mode) and chart chrome.
SERIES = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100",
          "#e87ba4", "#008300", "#6250d6", "#e34948"]
BLUE_RAMP = ["#cde2fb", "#b7d3f6", "#9ec5f4", "#86b6ef", "#6da7ec",
             "#5598e7", "#3987e5", "#2a78d6", "#256abf", "#1c5cab",
             "#184f95", "#104281", "#0d366b"]
SURFACE = "#fcfcfb"
INK = "#0b0b0b"
INK_2 = "#52514e"
MUTED = "#898781"
GRID = "#e1e0d9"
AXIS = "#c3c2b7"
NEUTRAL = "#f0efec"
UP = SERIES[0]
DOWN = "#d03b3b"
DIVERGING = LinearSegmentedColormap.from_list(
    "red_blue", ["#b52f2f", "#f2a3a2", NEUTRAL, "#86b6ef", "#1c5cab"])

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
    "axes.titlesize": 11.5,
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
    "xtick.labelcolor": INK_2,
    "ytick.labelcolor": INK_2,
    "legend.frameon": False,
    "lines.linewidth": 2,
})


def save(fig, name):
    fig.savefig(OUT_DIR / name, dpi=150, bbox_inches="tight", pad_inches=0.25)
    plt.close(fig)
    print(f"wrote {name}")


def headline(fig, title, subtitle):
    fig.suptitle(title, x=0.01, y=1.0, ha="left", fontsize=15, fontweight="bold")
    fig.text(0.01, 0.955, subtitle, ha="left", va="top", fontsize=10.5, color=INK_2)


# Week 1: mapping data onto aesthetics -------------------------------------

def week1_aesthetics():
    """Trading venues: position, colour, size and shape each carry one variable."""
    classes = ["Equities", "Futures", "FX"]
    venues = []
    for i, cls in enumerate(classes):
        for j in range(6):
            latency = RNG.uniform(8, 220) * (0.6 if cls == "Futures" else 1.0)
            fill = np.clip(97 - 0.06 * latency + RNG.normal(0, 2.2), 70, 99.5)
            volume = RNG.uniform(0.5, 12)
            link = "Microwave" if latency < 60 and RNG.random() < 0.7 else "Fibre"
            venues.append((f"{cls[:2].upper()}-{chr(65 + j)}", cls, latency,
                           fill, volume, link))

    fig, ax = plt.subplots(figsize=(10, 6))
    headline(fig, "Mapping data onto aesthetics: trading venue quality",
             "One dataset, four aesthetics: x = round-trip latency, y = fill rate, "
             "colour = asset class, size = daily volume, shape = link type")
    markers = {"Fibre": "o", "Microwave": "^"}
    for i, cls in enumerate(classes):
        for name, c, lat, fill, vol, link in venues:
            if c != cls:
                continue
            ax.scatter(lat, fill, s=40 + vol * 45, color=SERIES[i], marker=markers[link],
                       alpha=0.85, edgecolor=SURFACE, linewidth=1.5, zorder=3)
    best = max(venues, key=lambda v: v[3] - 0.05 * v[2])
    worst = min(venues, key=lambda v: v[3] - 0.05 * v[2])
    for v, text in [(best, "best trade-off"), (worst, "slow and leaky")]:
        ax.annotate(f"{v[0]}: {text}", (v[2], v[3]), xytext=(14, 10),
                    textcoords="offset points", fontsize=9, color=INK_2,
                    arrowprops=dict(arrowstyle="-", color=MUTED, lw=0.8))
    ax.set_xlabel("Round-trip latency to venue (µs)")
    ax.set_ylabel("Order fill rate (%)")

    colour_handles = [Line2D([], [], marker="o", ls="", color=SERIES[i], ms=9, label=c)
                      for i, c in enumerate(classes)]
    shape_handles = [Line2D([], [], marker=m, ls="", color=MUTED, ms=9, label=k)
                     for k, m in markers.items()]
    size_handles = [plt.scatter([], [], s=40 + v * 45, color=MUTED, alpha=0.6,
                                label=f"{v} M shares") for v in (1, 6, 12)]
    legend_style = dict(loc="upper left", fontsize=9, title_fontsize=9,
                        alignment="left")
    leg1 = ax.legend(handles=colour_handles, title="Colour: asset class",
                     bbox_to_anchor=(1.02, 1), **legend_style)
    leg2 = ax.legend(handles=shape_handles, title="Shape: link type",
                     bbox_to_anchor=(1.02, 0.72), **legend_style)
    ax.legend(handles=size_handles, title="Size: daily volume",
              bbox_to_anchor=(1.02, 0.5), labelspacing=1.4, borderpad=0.8,
              **legend_style)
    ax.add_artist(leg1)
    ax.add_artist(leg2)
    ax.set_ylim(top=101)
    save(fig, "week1_mapping_data_onto_aesthetics.png")


# Week 2: visually emphasise what matters ----------------------------------

def week2_emphasis():
    """Router uplink utilisation: default chart vs an informative one."""
    hours = np.arange(0, 48)
    links = [f"core-{i // 4 + 1} → edge-{i % 4 + 1}" for i in range(8)]
    data = {}
    for i, link in enumerate(links):
        base = RNG.uniform(25, 55)
        daily = 12 * np.sin((hours - 9) / 24 * 2 * np.pi)
        data[link] = np.clip(base + daily + RNG.normal(0, 3, hours.size), 5, 100)
    hot = links[5]
    data[hot] = np.clip(data[hot] + np.where(hours > 30, (hours - 30) * 3.6, 0), 0, 97)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5.2), sharey=True)
    headline(fig, "Informative visualisation: visually emphasise what matters",
             "Same data, two charts. The right one states the intended message, "
             "greys out context and uses the axis to show the threshold.")
    for i, link in enumerate(links):
        ax1.plot(hours, data[link], color=SERIES[i], lw=1.4, label=link)
    ax1.set_title("Before: eight colours, no message", color=INK_2)
    ax1.legend(fontsize=7.5, ncol=2, loc="upper left")
    ax1.set_ylim(0, 105)

    for link in links:
        if link != hot:
            ax2.plot(hours, data[link], color=AXIS, lw=1.2)
    ax2.axhspan(80, 105, color="#fbe3e3", lw=0, zorder=0)
    ax2.axhline(80, color=DOWN, lw=1, ls=(0, (4, 3)))
    ax2.text(1, 76, "80% planning threshold", color=DOWN, fontsize=9)
    ax2.plot(hours, data[hot], color=SERIES[0], lw=2.6)
    over = hours[data[hot] > 80]
    ax2.text(1, 92, f"{hot}: above 80% for {over.size} of the last 48 h",
             fontsize=9.5, fontweight="bold", color=INK)
    ax2.text(47, 8, "7 other uplinks\n(normal range)", color=MUTED, fontsize=9,
             ha="right")
    ax2.set_title("After: core-2 → edge-2 needs capacity now")
    for ax in (ax1, ax2):
        ax.set_xlabel("Hours since Monday 00:00")
        ax.set_xticks(range(0, 49, 12))
    ax1.set_ylabel("Uplink utilisation (%)")
    fig.subplots_adjust(top=0.82, wspace=0.08)
    save(fig, "week2_emphasise_what_matters.png")


# Week 3: word cloud and colour palettes -----------------------------------

def word_cloud(ax, weights):
    """Place words on an elliptical spiral, largest first, without overlaps."""
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    fig = ax.figure
    renderer = fig.canvas.get_renderer()
    box = ax.get_window_extent(renderer)
    cx, cy = box.x0 + box.width / 2, box.y0 + box.height / 2
    placed = []
    top = max(weights.values())
    for word, w in sorted(weights.items(), key=lambda kv: -kv[1]):
        size = 9 + 34 * (w / top) ** 0.9
        shade = BLUE_RAMP[int(4 + 8 * w / top)]
        txt = ax.text(0, 0, word, fontsize=size, color=shade, fontweight="bold",
                      ha="center", va="center", transform=None)
        ext = txt.get_window_extent(renderer)
        half_w, half_h = ext.width / 2 + 12, ext.height / 2 + 2
        for step in range(4000):
            t = step * 0.12
            x = cx + 2.1 * t * np.cos(t) * 1.6
            y = cy + 2.1 * t * np.sin(t) * 0.75
            rect = (x - half_w, y - half_h, x + half_w, y + half_h)
            if rect[0] < box.x0 or rect[2] > box.x1 or rect[1] < box.y0 or rect[3] > box.y1:
                continue
            if all(rect[2] < r[0] or rect[0] > r[2] or rect[3] < r[1] or rect[1] > r[3]
                   for r in placed):
                placed.append(rect)
                txt.set_position(ax.transAxes.inverted().transform((x, y)))
                txt.set_transform(ax.transAxes)
                break
        else:
            txt.remove()


def week3_wordle_palettes():
    terms = {
        "latency": 100, "order book": 92, "alpha": 85, "slippage": 78,
        "market making": 72, "arbitrage": 68, "VWAP": 64, "liquidity": 62,
        "backtest": 58, "TWAP": 52, "spread": 50, "momentum": 48,
        "mean reversion": 46, "colocation": 44, "tick data": 42, "Sharpe": 40,
        "drawdown": 38, "FIX protocol": 36, "risk limits": 34, "hedging": 32,
        "execution": 31, "volatility": 30, "microwave": 28, "fill rate": 27,
        "market impact": 26, "signals": 24, "order routing": 23, "kdb+": 22,
        "jitter": 21, "multicast": 20, "rebates": 18, "dark pool": 17,
        "iceberg": 16, "co-integration": 15, "PnL": 14, "beta": 13,
    }
    fig = plt.figure(figsize=(13, 9.2))
    headline(fig, "Wordle and colour palettes in algorithmic trading",
             "Top: word size and shade both encode how often a term appears in "
             "trading-desk research notes. Bottom: the three palette types, each "
             "doing one job.")
    grid = fig.add_gridspec(2, 2, height_ratios=[1.15, 1], hspace=0.22, wspace=0.3,
                            top=0.9)
    word_cloud(fig.add_subplot(grid[0, :]), terms)

    pal = fig.add_subplot(grid[1, 0])
    pal.axis("off")
    pal.set_xlim(0, 9)
    pal.set_ylim(0, 3.3)
    rows = [
        ("Qualitative → identity (strategy type)", SERIES[:5],
         ["Market making", "Arbitrage", "Momentum", "Mean rev.", "Stat arb"]),
        ("Sequential → magnitude (latency, µs)", BLUE_RAMP[::2],
         ["5", "", "", "", "", "", "500"]),
        ("Diverging → polarity (daily return)",
         [DIVERGING(v) for v in np.linspace(0, 1, 7)],
         ["−3%", "", "", "0", "", "", "+3%"]),
    ]
    for r, (label, colours, ticks) in enumerate(rows):
        y = 2.35 - r * 1.1
        pal.text(0, y + 0.62, label, fontsize=10, fontweight="bold")
        w = 9 / len(colours)
        for k, c in enumerate(colours):
            pal.add_patch(FancyBboxPatch((k * w + 0.03, y), w - 0.06, 0.42,
                                         boxstyle="round,pad=0,rounding_size=0.06",
                                         fc=c, ec="none"))
            if ticks[k]:
                pal.text(k * w + w / 2, y - 0.14, ticks[k], ha="center", va="top",
                         fontsize=8, color=INK_2)
    pal.set_title("The three palette types", loc="left")

    heat = fig.add_subplot(grid[1, 1])
    strategies = ["Market making", "Arbitrage", "Momentum", "Mean rev.", "Stat arb"]
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep"]
    returns = RNG.normal(0.4, 1.3, (len(strategies), len(months)))
    im = heat.imshow(returns, cmap=DIVERGING, vmin=-3, vmax=3, aspect="auto")
    heat.set_xticks(range(len(months)), months)
    heat.set_yticks(range(len(strategies)), strategies)
    heat.grid(False)
    for s in heat.spines.values():
        s.set_visible(False)
    heat.tick_params(length=0)
    for (i, j), v in np.ndenumerate(returns):
        if abs(v) > 2:
            heat.text(j, i, f"{v:+.1f}", ha="center", va="center", fontsize=8,
                      color="white")
    cbar = fig.colorbar(im, ax=heat, fraction=0.04, pad=0.02)
    cbar.outline.set_visible(False)
    cbar.set_label("Monthly return (%)", color=INK_2)
    heat.set_title("Diverging palette in use: blue/red, never red/green (CVD-safe)")
    save(fig, "week3_wordle_and_colour_palettes.png")


# Week 4: tube map ---------------------------------------------------------

def week4_tube_map():
    """A low-latency trading network drawn with tube-map conventions."""
    stations = {
        "Dublin": (0, 5), "Slough": (3, 5), "Docklands": (6, 5), "Basildon": (8, 5),
        "Amsterdam": (11, 5), "Frankfurt": (13, 3), "Richborough": (7, 3),
        "Brussels": (10, 3), "Paris": (9, 1), "Zurich": (11.5, 1),
    }
    lines = [
        ("Fibre backbone", SERIES[0], "primary path, London–Frankfurt ≈ 4.2 ms",
         ["Dublin", "Slough", "Docklands", "Basildon", "Amsterdam", "Frankfurt"]),
        ("Microwave route", SERIES[1], "fastest, London–Frankfurt ≈ 2.9 ms, weather-sensitive",
         ["Slough", (5, 3), "Richborough", "Brussels", "Frankfurt"]),
        ("Market-data multicast", SERIES[2], "price feeds to continental venues",
         ["Docklands", (6, 1), "Paris", "Zurich", (13, 1), "Frankfurt"]),
        ("Backup route", MUTED, "failover between Paris, Brussels and Amsterdam",
         ["Paris", (9, 2), "Brussels", (10, 4), "Amsterdam"]),
    ]
    labels = {
        "Dublin": (0, 0.35, "center"), "Slough": (0, 0.35, "center"),
        "Docklands": (0, 0.35, "center"), "Basildon": (0, 0.35, "center"),
        "Amsterdam": (0, 0.35, "center"), "Frankfurt": (0.3, 0, "left"),
        "Richborough": (0, -0.38, "center"), "Brussels": (0.3, -0.25, "left"),
        "Paris": (-0.3, -0.25, "right"), "Zurich": (0, -0.38, "center"),
    }

    fig, ax = plt.subplots(figsize=(13, 6.6))
    headline(fig, "A trading network drawn as a tube map",
             "Octilinear lines, even spacing and interchange rings trade "
             "geographic accuracy for clarity, just like the London Underground map.")
    ax.axis("off")
    ax.set_aspect("equal")
    usage = {name: 0 for name in stations}
    for name, colour, _, route in lines:
        pts = [stations[p] if isinstance(p, str) else p for p in route]
        xs, ys = zip(*pts)
        ax.plot(xs, ys, color=colour, lw=9, solid_capstyle="round",
                solid_joinstyle="round", zorder=2)
        for p in route:
            if isinstance(p, str):
                usage[p] += 1
    for name, (x, y) in stations.items():
        if usage[name] > 1:
            ax.scatter(x, y, s=340, color="white", edgecolor=INK, linewidth=2.6,
                       zorder=4)
        else:
            ax.scatter(x, y, s=120, color="white", edgecolor=INK, linewidth=2,
                       zorder=4)
        dx, dy, ha = labels[name]
        ax.text(x + dx, y + dy, name, ha=ha, va="center", fontsize=10.5,
                fontweight="bold", color=INK, zorder=5)

    handles = [Line2D([], [], color=c, lw=7, solid_capstyle="round",
                      label=f"{n}: {role}")
               for n, c, role, _ in lines]
    handles.append(Line2D([], [], marker="o", ls="", ms=13, mfc="white",
                          mec=INK, mew=2.4, label="Interchange (shared PoP)"))
    ax.legend(handles=handles, loc="lower left", bbox_to_anchor=(-0.01, -0.12),
              fontsize=9.5, handlelength=2.4, labelspacing=0.9,
              title="Routes (illustrative one-way latencies)", title_fontsize=9.5,
              alignment="left")
    ax.set_xlim(-1, 14.8)
    ax.set_ylim(-1.6, 6)
    save(fig, "week4_trading_network_tube_map.png")


# Week 5: core chart types -------------------------------------------------

def week5_core_charts():
    days = 252
    market = RNG.normal(0.0003, 0.011, days)
    strategy = 0.35 * market + RNG.normal(0.0007, 0.006, days)
    eq_strat = 100 * np.cumprod(1 + strategy)
    eq_mkt = 100 * np.cumprod(1 + market)

    fig, axes = plt.subplots(2, 2, figsize=(13, 9))
    headline(fig, "Core chart types for one algorithmic strategy",
             "Line = change over time, bar = comparison, scatter = relationship, "
             "box plot = distribution.")
    fig.subplots_adjust(hspace=0.38, wspace=0.22, top=0.89)

    ax = axes[0, 0]
    ax.plot(eq_mkt, color=MUTED, lw=1.6)
    ax.plot(eq_strat, color=SERIES[0])
    ax.text(days + 3, eq_strat[-1], f"Strategy {eq_strat[-1] - 100:+.0f}%",
            color=INK, fontsize=9, va="center")
    ax.text(days + 3, eq_mkt[-1], f"Index {eq_mkt[-1] - 100:+.0f}%", color=INK_2,
            fontsize=9, va="center")
    ax.set_xlim(0, days + 45)
    ax.set_title("Line: equity curve vs benchmark")
    ax.set_xlabel("Trading day")
    ax.set_ylabel("Value of 100 invested")

    ax = axes[0, 1]
    monthly = np.array([strategy[i * 21:(i + 1) * 21].sum() * 100 for i in range(12)])
    months = list("JFMAMJJASOND")
    ax.bar(range(12), monthly, color=[UP if m >= 0 else DOWN for m in monthly],
           width=0.7, zorder=3)
    ax.axhline(0, color=AXIS, lw=0.8)
    ax.set_xticks(range(12), months)
    ax.grid(axis="x", visible=False)
    ax.set_title(f"Bar: monthly returns ({(monthly > 0).sum()} of 12 positive)")
    ax.set_ylabel("Return (%)")

    ax = axes[1, 0]
    beta, alpha = np.polyfit(market, strategy, 1)
    ax.scatter(market * 100, strategy * 100, s=14, color=SERIES[0], alpha=0.55,
               edgecolor="none", zorder=3)
    xs = np.linspace(market.min(), market.max(), 2)
    ax.plot(xs * 100, (alpha + beta * xs) * 100, color=INK, lw=1.4)
    ax.text(0.98, 0.06, f"β = {beta:.2f}  (low market exposure)",
            transform=ax.transAxes, ha="right", fontsize=9, color=INK_2)
    ax.set_title("Scatter: strategy vs market daily returns")
    ax.set_xlabel("Market return (%)")
    ax.set_ylabel("Strategy return (%)")

    ax = axes[1, 1]
    order_types = ["Market", "Limit", "Iceberg", "VWAP algo", "TWAP algo"]
    slippage = [RNG.gamma(k, 1.0, 400) for k in (6, 2, 3, 2.5, 3.2)]
    bp = ax.boxplot(slippage, patch_artist=True, widths=0.5, showfliers=False,
                    medianprops=dict(color=INK, lw=1.6))
    for patch in bp["boxes"]:
        patch.set(facecolor=BLUE_RAMP[2], edgecolor=SERIES[0], linewidth=1.2)
    for part in ("whiskers", "caps"):
        for line in bp[part]:
            line.set(color=SERIES[0], linewidth=1.2)
    ax.set_xticks(range(1, 6), order_types)
    ax.grid(axis="x", visible=False)
    ax.set_title("Box plot: slippage by order type")
    ax.set_ylabel("Slippage (basis points)")
    save(fig, "week5_core_chart_types.png")


# Week 6: waterfall and Sankey ---------------------------------------------

def sankey_band(ax, x0, y0a, y0b, x1, y1a, y1b, colour):
    mid = (x0 + x1) / 2
    verts = [(x0, y0a), (mid, y0a), (mid, y1a), (x1, y1a),
             (x1, y1b), (mid, y1b), (mid, y0b), (x0, y0b), (x0, y0a)]
    codes = [MplPath.MOVETO, MplPath.CURVE4, MplPath.CURVE4, MplPath.CURVE4,
             MplPath.LINETO, MplPath.CURVE4, MplPath.CURVE4, MplPath.CURVE4,
             MplPath.CLOSEPOLY]
    ax.add_patch(PathPatch(MplPath(verts, codes), fc=colour, ec="none", alpha=0.45))


def sankey(ax, columns, flows, colours):
    """Draw a multi-column Sankey. flows: (src, dst, value); band colour by source."""
    gap, width = 6, 0.12
    pos = {}
    for c, nodes in enumerate(columns):
        totals = {n: max(sum(v for s, d, v in flows if s == n),
                         sum(v for s, d, v in flows if d == n)) for n in nodes}
        y = sum(totals.values()) + gap * (len(nodes) - 1)
        top = y / 2
        for n in nodes:
            pos[n] = [c, top, top - totals[n], top, top]  # col, top, bottom, out, in
            top -= totals[n] + gap

    for s, d, v in flows:
        cs, cd = pos[s], pos[d]
        colour = colours[s]
        sankey_band(ax, cs[0] + width / 2, cs[3], cs[3] - v,
                    cd[0] - width / 2, cd[4], cd[4] - v, colour)
        cs[3] -= v
        cd[4] -= v

    span = 0
    for n, (c, top, bottom, _, _) in pos.items():
        ax.add_patch(FancyBboxPatch((c - width / 2, bottom), width, top - bottom,
                                    boxstyle="round,pad=0,rounding_size=0.02",
                                    fc=colours.get(n, INK_2), ec="none", zorder=3))
        last = c == len(columns) - 1
        span = max(span, abs(top), abs(bottom))
        ax.text(c + (width if last else -width) * 0.9, (top + bottom) / 2,
                f"{n}\n{top - bottom:.0f} Gbps", ha="left" if last else "right",
                va="center", fontsize=9, color=INK)
    ax.set_ylim(-span * 1.05, span * 1.05)


def week6_advanced_charts():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6.2),
                                   gridspec_kw=dict(width_ratios=[1, 1.15]))
    headline(fig, "Advanced charts: waterfall and Sankey",
             "Left: how gross alpha becomes net P&L. Right: where a trading "
             "firm's network traffic enters, crosses the core and ends up.")

    steps = [("Gross alpha", 4.2), ("Exchange rebates", 0.6), ("Commissions", -0.9),
             ("Slippage", -1.3), ("Market impact", -0.7), ("Financing", -0.4)]
    running = 0
    for i, (label, v) in enumerate(steps):
        bottom = running if v >= 0 else running + v
        ax1.bar(i, abs(v), bottom=bottom, color=UP if v >= 0 else DOWN, width=0.62,
                zorder=3)
        ax1.text(i, running + v + (0.08 if v >= 0 else -0.08), f"{v:+.1f}",
                 ha="center", va="bottom" if v >= 0 else "top", fontsize=9)
        if i:
            ax1.plot([i - 1.31, i - 0.31], [running, running], color=MUTED, lw=0.8)
        running += v
    n = len(steps)
    ax1.plot([n - 1.31, n - 0.31], [running, running], color=MUTED, lw=0.8)
    ax1.bar(n, running, color=INK_2, width=0.62, zorder=3)
    ax1.text(n, running + 0.08, f"{running:.1f}", ha="center", va="bottom",
             fontsize=9, fontweight="bold")
    ax1.set_xticks(range(n + 1), [s for s, _ in steps] + ["Net P&L"], rotation=30,
                   ha="right")
    ax1.grid(axis="x", visible=False)
    ax1.set_ylabel("Annual P&L ($ millions)")
    ax1.set_title("Waterfall: costs consume 2/3 of gross alpha")

    columns = [["Transit ISP A", "Transit ISP B", "IXP peering"],
               ["Core-1", "Core-2"],
               ["Market data", "Order entry", "Risk engine", "Back office"]]
    flows = [("Transit ISP A", "Core-1", 30), ("Transit ISP A", "Core-2", 10),
             ("Transit ISP B", "Core-1", 8), ("Transit ISP B", "Core-2", 17),
             ("IXP peering", "Core-1", 22), ("IXP peering", "Core-2", 13),
             ("Core-1", "Market data", 38), ("Core-1", "Order entry", 12),
             ("Core-1", "Risk engine", 10), ("Core-2", "Market data", 14),
             ("Core-2", "Order entry", 9), ("Core-2", "Risk engine", 8),
             ("Core-2", "Back office", 9)]
    colours = {"Transit ISP A": SERIES[0], "Transit ISP B": SERIES[1],
               "IXP peering": SERIES[2]}
    # Second-stage bands are coloured by core router, in neutral greys.
    colours.update({"Core-1": INK_2, "Core-2": MUTED})
    sankey(ax2, columns, flows, colours)
    ax2.axis("off")
    ax2.set_xlim(-0.75, 2.75)
    ax2.set_title("Sankey: 100 Gbps peak traffic, ingress → core → service")
    save(fig, "week6_waterfall_and_sankey.png")


# Week 7: forecasting and trend lines --------------------------------------

def week7_forecast():
    weeks = np.arange(78)
    trend = 3.2 + 0.052 * weeks
    seasonal = 0.35 * np.sin(weeks / 52 * 2 * np.pi)
    util = trend + seasonal + RNG.normal(0, 0.22, weeks.size)

    slope, intercept = np.polyfit(weeks, util, 1)
    resid_sd = np.std(util - (intercept + slope * weeks))
    future = np.arange(weeks[-1], weeks[-1] + 40)
    fc = intercept + slope * future
    horizon = future - weeks[-1]
    band = 1.96 * resid_sd * np.sqrt(1 + horizon / 26)
    threshold, capacity = 8.0, 10.0
    breach = future[np.argmax(fc + band >= threshold)]
    expected = future[np.argmax(fc >= threshold)]

    fig, ax = plt.subplots(figsize=(12, 6))
    headline(fig, "Forecasting and trend lines: when does the 10 Gbps uplink "
             "need upgrading?",
             "Weekly 95th-percentile utilisation of an exchange uplink, a linear "
             "trend line, and a forecast with a widening 95% interval.")
    ax.axhline(capacity, color=DOWN, lw=1.2)
    ax.axhline(threshold, color=DOWN, lw=1, ls=(0, (4, 3)))
    ax.text(1, capacity + 0.12, "Link capacity 10 Gbps", color=DOWN, fontsize=9)
    ax.text(1, threshold + 0.12, "Upgrade threshold (80%)", color=DOWN, fontsize=9)

    ax.plot(weeks, util, color=SERIES[0], lw=1.6)
    ax.plot(weeks, intercept + slope * weeks, color=INK, lw=1.2)
    ax.fill_between(future, fc - band, fc + band, color=SERIES[0], alpha=0.15, lw=0)
    ax.plot(future, fc, color=SERIES[0], lw=1.8, ls=(0, (5, 3)))
    ax.text(52, util[52] + 0.9, "Observed", color=SERIES[0], fontsize=9.5,
            fontweight="bold", ha="center")
    ax.text(18, intercept + slope * 18 - 0.55,
            f"Trend: +{slope * 52:.1f} Gbps per year", color=INK, fontsize=9)
    ax.text(future[-1], 7.0, "Forecast ± 95% interval", color=INK_2, fontsize=9,
            ha="right", va="top")
    for wk, text, ha in [(breach, "earliest breach", "right"),
                         (expected, "expected breach", "left")]:
        ax.axvline(wk, color=MUTED, lw=0.8, ymax=0.78)
        ax.text(wk + (-0.8 if ha == "right" else 0.8), 1.55, f"{text}\nweek {wk}",
                ha=ha, fontsize=8.5,
                color=INK_2, bbox=dict(fc=SURFACE, ec="none", pad=1))
    ax.annotate(f"Order the upgrade by week {breach - 12}\n(12-week lead time)",
                (breach, threshold), xytext=(-260, 30), textcoords="offset points",
                fontsize=10, fontweight="bold", color=INK,
                arrowprops=dict(arrowstyle="->", color=INK, lw=1))
    ax.set_xlim(0, future[-1] + 1)
    ax.set_ylim(1.2, capacity + 0.6)
    ax.set_xlabel("Week")
    ax.set_ylabel("95th-percentile utilisation (Gbps)")
    save(fig, "week7_capacity_forecast.png")


if __name__ == "__main__":
    week1_aesthetics()
    week2_emphasis()
    week3_wordle_palettes()
    week4_tube_map()
    week5_core_charts()
    week6_advanced_charts()
    week7_forecast()
