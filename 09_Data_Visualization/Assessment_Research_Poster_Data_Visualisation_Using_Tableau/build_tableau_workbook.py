"""Build a ready-made Tableau workbook (NQ1_Poster.twbx) for the six poster charts.

Reads the outputs of NQ1_Poster_Analysis.ipynb from spreadsheets_assessment/
(NQ_clean_for_tableau.csv and the three summary tables), writes one tidy CSV per chart into Tableau_Workbook/Data/, then writes
a Tableau workbook that connects to them. Tableau renders every chart itself.

Each sheet uses only shelves, colour and labels (no calculated fields, filters or dual
axes), so the XML stays simple. Values are stored in percent units (e.g. -83.1) so
axes read correctly without number formatting.

Run from the assessment folder:
    uv run --no-project --with pandas python build_tableau_workbook.py
"""

import uuid
import zipfile
from pathlib import Path
from xml.sax.saxutils import quoteattr

import pandas as pd

HERE = Path(__file__).resolve().parent
SRC = HERE / "spreadsheets_assessment"          # where the notebook outputs are kept
OUT_DIR = HERE / "Tableau_Workbook"
DATA_DIR = OUT_DIR / "Data"
TWB = OUT_DIR / "NQ1_Poster.twb"
TWBX = OUT_DIR / "NQ1_Poster.twbx"

BLUE, ORANGE, RED, GREY = "#2a78d6", "#eb6834", "#d03b3b", "#898781"


def write_chart_data() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    df = pd.read_csv(SRC / "NQ_clean_for_tableau.csv", parse_dates=["Date"])

    price = df.melt(id_vars="Date", value_vars=["Close", "MA_252"], var_name="Series",
                    value_name="Price").dropna()
    price["Series"] = price["Series"].map({"Close": "Daily settlement",
                                           "MA_252": "252-day moving average"})
    price.to_csv(DATA_DIR / "V1_price.csv", index=False, date_format="%Y-%m-%d")

    dd = pd.DataFrame({"Date": df["Date"], "Drawdown_Pct": (df["Drawdown"] * 100).round(3)})
    dd.to_csv(DATA_DIR / "V2_drawdown.csv", index=False, date_format="%Y-%m-%d")

    ann = pd.read_csv(SRC / "NQ_annual_returns.csv", dtype={"Year": str})
    pd.DataFrame({"Year": ann["Year"],
                  "Annual_Return_Pct": (ann["Annual_Return"] * 100).round(1),
                  "Result": ann["Result"],
                  "Year_Type": ann["Year_Type"]}).to_csv(DATA_DIR / "V3_annual.csv", index=False)

    rv = (df.set_index("Date")["Rolling_Vol_21d_Ann"] * 100).dropna()
    med, p90 = rv.median(), rv.quantile(0.9)
    vol = pd.concat([
        pd.DataFrame({"Date": rv.index, "Series": "21-day realised volatility", "Volatility_Pct": rv.round(2)}),
        pd.DataFrame({"Date": rv.index, "Series": f"Median ({med:.0f}%)", "Volatility_Pct": round(med, 2)}),
        pd.DataFrame({"Date": rv.index, "Series": f"Stress line, 90th percentile ({p90:.0f}%)",
                      "Volatility_Pct": round(p90, 2)}),
    ])
    vol.to_csv(DATA_DIR / "V4_volatility.csv", index=False, date_format="%Y-%m-%d")

    hist = pd.read_csv(SRC / "NQ_return_histogram.csv")
    dist = hist.melt(id_vars="Return_Bin_Pct", var_name="Series", value_name="Days").dropna()
    dist["Series"] = dist["Series"].map({"Observed_Days": "Observed daily returns",
                                         "Normal_Expected_Days": "Normal curve (same mean and s.d.)"})
    dist.to_csv(DATA_DIR / "V5_distribution.csv", index=False)

    reg = pd.read_csv(SRC / "NQ_regime_summary.csv")
    pd.DataFrame({"Metric": reg["Metric"], "Regime": reg["Regime"],
                  "Value_Pct": (reg["Value"] * 100).round(1)}).to_csv(DATA_DIR / "V6_regime.csv", index=False)


# ----------------------------------------------------------------------------------
# Workbook definition: one entry per chart.
#   fields: (name, datatype, role, type) as Tableau column metadata
#   cols/rows: column-instance ids placed on the shelves
#   colour: (dimension, {member: hex}) or None; label: measure shown as mark label
# ----------------------------------------------------------------------------------
SHEETS = [
    dict(sheet="V1 Price trend", file="V1_price.csv", mark="Line",
         title="E-mini Nasdaq-100: a 27-year climb from the dot-com peak, through two deep bear markets",
         fields=[("Date", "date", "dimension", "ordinal"), ("Series", "string", "dimension", "nominal"),
                 ("Price", "real", "measure", "quantitative")],
         cols=("Date", "none", "qk"), rows=("Price", "sum", "qk"),
         colour=("Series", {"Daily settlement": BLUE, "252-day moving average": ORANGE}), label=None),
    dict(sheet="V2 Drawdown", file="V2_drawdown.csv", mark="Area",
         title="Drawdown from previous high: the March 2000 peak took 16 years to regain",
         fields=[("Date", "date", "dimension", "ordinal"), ("Drawdown_Pct", "real", "measure", "quantitative")],
         cols=("Date", "none", "qk"), rows=("Drawdown_Pct", "sum", "qk"),
         colour=None, single_colour=RED, label=None),
    dict(sheet="V3 Annual returns", file="V3_annual.csv", mark="Bar",
         title="Calendar-year return: 20 of 26 full years positive, but losses cluster in runs",
         fields=[("Year", "string", "dimension", "nominal"), ("Annual_Return_Pct", "real", "measure", "quantitative"),
                 ("Result", "string", "dimension", "nominal"), ("Year_Type", "string", "dimension", "nominal")],
         cols=("Year", "none", "nk"), rows=("Annual_Return_Pct", "sum", "qk"),
         colour=("Result", {"Gain": BLUE, "Loss": RED}), label=None),
    dict(sheet="V4 Volatility", file="V4_volatility.csv", mark="Line",
         title="Volatility clusters: calm regimes punctuated by short, violent storms",
         fields=[("Date", "date", "dimension", "ordinal"), ("Series", "string", "dimension", "nominal"),
                 ("Volatility_Pct", "real", "measure", "quantitative")],
         cols=("Date", "none", "qk"), rows=("Volatility_Pct", "sum", "qk"),
         colour=("Series", None), label=None),          # members filled from the data
    dict(sheet="V5 Fat tails", file="V5_distribution.csv", mark="Line",
         title="Daily returns have fat tails: extreme days are far more common than a bell curve predicts",
         fields=[("Return_Bin_Pct", "real", "dimension", "quantitative"), ("Series", "string", "dimension", "nominal"),
                 ("Days", "real", "measure", "quantitative")],
         cols=("Return_Bin_Pct", "none", "qk"), rows=("Days", "sum", "qk"),
         colour=("Series", {"Observed daily returns": BLUE, "Normal curve (same mean and s.d.)": ORANGE}),
         label=None),
    dict(sheet="V6 Regime scorecard", file="V6_regime.csv", mark="Bar",
         title="Trend regimes: below its 252-day average, risk more than doubles and most crash days occur",
         fields=[("Metric", "string", "dimension", "nominal"), ("Regime", "string", "dimension", "nominal"),
                 ("Value_Pct", "real", "measure", "quantitative")],
         cols=[("Metric", "none", "nk"), ("Regime", "none", "nk")], rows=("Value_Pct", "sum", "qk"),
         colour=("Regime", {"Above 252-day MA": BLUE, "Below 252-day MA": ORANGE}), label="Value_Pct"),
]


def ds_name(i: int) -> str:
    return f"federated.nq1poster{i:02d}"


def inst(field, deriv, kind) -> str:
    return f"[{deriv}:{field}:{kind}]"


def col_xml(name, datatype, role, typ) -> str:
    return f"<column datatype='{datatype}' name='[{name}]' role='{role}' type='{typ}' />"


def build_twb(data_dir_attr: str) -> str:
    v4_members = sorted(pd.read_csv(DATA_DIR / "V4_volatility.csv")["Series"].unique(),
                        key=lambda s: (not s.startswith("21-day"), s))
    v4_colours = dict(zip(v4_members, [BLUE, GREY, ORANGE]))

    datasources, worksheets, windows = [], [], []
    for i, sh in enumerate(SHEETS):
        ds = ds_name(i)
        conn = f"textscan.nq1poster{i:02d}"
        table = sh["file"].replace(".csv", "#csv")
        relation_cols = "".join(
            f"<column datatype='{dt}' name='{n}' ordinal='{k}' />" for k, (n, dt, _, _) in enumerate(sh["fields"]))
        colour = sh["colour"]
        style = ""
        if colour:
            members = colour[1] if colour[1] else v4_colours
            maps = "".join(f"<map to='{hexv}'><bucket>{quoteattr(m)[1:-1].join(['&quot;', '&quot;'])}</bucket></map>"
                           for m, hexv in members.items())
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
            + f"<layout dim-ordering='alphabetic' measure-ordering='alphabetic' show-structure='true' />"
            + style + "</datasource>")

        cols = sh["cols"] if isinstance(sh["cols"], list) else [sh["cols"]]
        shelf_fields = cols + [sh["rows"]]
        used = {c[0] for c in shelf_fields} | ({colour[0]} if colour else set())
        deps = "".join(col_xml(*f) for f in sh["fields"] if f[0] in used)
        instances = []
        for field, deriv, kind in shelf_fields:
            deriv_attr = "Sum" if deriv == "sum" else "None"
            typ = {"qk": "quantitative", "nk": "nominal"}[kind]
            instances.append(f"<column-instance column='[{field}]' derivation='{deriv_attr}' "
                             f"name='{inst(field, deriv, kind)}' pivot='key' type='{typ}' />")
        if colour and colour[0] not in {c[0] for c in shelf_fields}:
            instances.append(f"<column-instance column='[{colour[0]}]' derivation='None' "
                             f"name='{inst(colour[0], 'none', 'nk')}' pivot='key' type='nominal' />")
        encodings = ""
        if colour:
            encodings += f"<color column='[{ds}].{inst(colour[0], 'none', 'nk')}' />"
        if sh["label"]:
            encodings += f"<text column='[{ds}].{inst(sh['label'], 'sum', 'qk')}' />"
        pane_style = ""
        if sh["label"]:
            pane_style = "<style><style-rule element='mark'><format attr='mark-labels-show' value='true' /></style-rule></style>"
        elif sh.get("single_colour"):
            pane_style = (f"<style><style-rule element='mark'><format attr='mark-color' "
                          f"value='{sh['single_colour']}' /></style-rule></style>")
        cols_xml = " / ".join(f"[{ds}].{inst(*c)}" for c in cols)
        if len(cols) > 1:
            cols_xml = f"({cols_xml})"                        # nested dimensions
        uid = "{" + str(uuid.uuid5(uuid.NAMESPACE_URL, sh["sheet"])).upper() + "}"
        worksheets.append(
            f"<worksheet name={quoteattr(sh['sheet'])}>"
            f"<layout-options><title><formatted-text><run bold='true' fontsize='14'>{sh['title']}</run>"
            f"</formatted-text></title></layout-options>"
            f"<table><view><datasources><datasource caption={quoteattr(sh['file'][:-4])} name='{ds}' /></datasources>"
            f"<datasource-dependencies datasource='{ds}'>{deps}{''.join(instances)}</datasource-dependencies>"
            f"<aggregation value='true' /></view><style />"
            f"<panes><pane selection-relaxation-option='selection-relaxation-allow'>"
            f"<view><breakdown value='auto' /></view><mark class='{sh['mark']}' />"
            + (f"<encodings>{encodings}</encodings>" if encodings else "")
            + pane_style
            + f"</pane></panes>"
            f"<rows>[{ds}].{inst(*sh['rows'])}</rows><cols>{cols_xml}</cols></table>"
            f"<simple-id uuid='{uid}' /></worksheet>")
        windows.append(
            f"<window class='worksheet' name={quoteattr(sh['sheet'])}><cards>"
            f"<edge name='left'><strip size='160'><card type='pages' /><card type='filters' />"
            f"<card type='marks' /></strip></edge>"
            f"<edge name='top'><strip size='2147483647'><card type='columns' /></strip>"
            f"<strip size='2147483647'><card type='rows' /></strip>"
            f"<strip size='31'><card type='title' /></strip></edge></cards>"
            f"<simple-id uuid='{uid}' /></window>")

    return ("<?xml version='1.0' encoding='utf-8' ?>\n"
            "<workbook original-version='18.1' source-build='2026.1.0 (20261.26.0211.1127)' "
            "source-platform='win' version='18.1' xmlns:user='http://www.tableausoftware.com/xml/user'>"
            "<preferences><preference name='ui.encoding.shelf.height' value='24' />"
            "<preference name='ui.shelf.height' value='26' /></preferences>"
            f"<datasources>{''.join(datasources)}</datasources>"
            f"<worksheets>{''.join(worksheets)}</worksheets>"
            f"<windows source-height='30'>{''.join(windows)}</windows>"
            "<explain-data enabled-for-viewer='true' extreme-values-enabled-for-all='true'>"
            "<explanation-types /></explain-data>"
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
