import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

st.set_page_config(
    page_title="Global Market Filter",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

html, body, [class*="css"], .stApp {
    font-family: 'Inter', sans-serif !important;
    background-color: #f8f9fa !important;
}
.main, .block-container { background-color: #f8f9fa !important; }
.block-container { padding: 2rem 2.5rem !important; max-width: 1400px !important; }

.db-title { font-size: 26px; font-weight: 700; color: #111827; letter-spacing: -0.5px; margin-bottom: 3px; }
.db-sub { font-size: 12px; color: #9ca3af; margin-bottom: 24px; font-family: 'JetBrains Mono', monospace; }

.sum-card {
    background: #ffffff; border: 1px solid #e5e7eb;
    border-radius: 10px; padding: 14px 18px; text-align: center;
    box-shadow: 0 1px 3px rgba(0,0,0,0.04);
}
.sum-label { font-size: 10px; color: #9ca3af; text-transform: uppercase; letter-spacing: 0.8px; font-weight: 600; }
.sum-val { font-size: 30px; font-weight: 700; margin-top: 3px; }

.section-hdr {
    font-size: 10px; color: #9ca3af; text-transform: uppercase;
    letter-spacing: 1.5px; font-weight: 700;
    padding: 20px 0 10px; border-bottom: 1px solid #e5e7eb; margin-bottom: 0;
}

/* ── Main data table ── */
.data-table { width: 100%; border-collapse: collapse; background: #ffffff; border-radius: 12px; overflow: hidden; border: 1px solid #e5e7eb; box-shadow: 0 1px 4px rgba(0,0,0,0.05); }
.data-table thead th {
    background: #f9fafb; text-align: left; padding: 9px 14px;
    font-size: 10px; color: #6b7280; text-transform: uppercase;
    letter-spacing: 0.7px; font-weight: 600;
    border-bottom: 1px solid #e5e7eb;
}
.data-table tbody tr { border-bottom: 0.5px solid #f3f4f6; transition: background 0.1s; }
.data-table tbody tr:hover { background: #f9fafb; }
.data-table tbody tr:last-child { border-bottom: none; }
.data-table td { padding: 7px 14px; vertical-align: middle; }

.sec-row td { background: #f9fafb; font-size: 9px; color: #9ca3af; text-transform: uppercase; letter-spacing: 1.2px; font-weight: 700; padding: 6px 14px; }

.a-name { font-size: 13px; font-weight: 600; color: #111827; }
.a-tick { font-size: 10px; color: #9ca3af; font-family: 'JetBrains Mono', monospace; margin-top: 1px; }
.a-price { font-family: 'JetBrains Mono', monospace; font-size: 13px; font-weight: 600; color: #111827; white-space: nowrap; }
.up { color: #059669; font-size: 11px; font-weight: 500; white-space: nowrap; }
.dn { color: #dc2626; font-size: 11px; font-weight: 500; white-space: nowrap; }
.ma-val { font-family: 'JetBrains Mono', monospace; font-size: 11px; color: #6b7280; white-space: nowrap; }

.dot { width: 8px; height: 8px; border-radius: 50%; display: inline-block; margin-right: 7px; vertical-align: middle; flex-shrink: 0; }

.b { display: inline-block; padding: 3px 8px; border-radius: 5px; font-size: 11px; font-weight: 700; white-space: nowrap; }
.b-on  { background: #dcfce7; color: #15803d; border: 1px solid #bbf7d0; }
.b-off { background: #fee2e2; color: #b91c1c; border: 1px solid #fecaca; }
.b-top { background: #fef3c7; color: #b45309; border: 1px solid #fde68a; }
.b-bas { background: #ede9fe; color: #6d28d9; border: 1px solid #ddd6fe; }
.b-s   { background: #f3f4f6; color: #374151; border: 1px solid #e5e7eb; font-size: 10px; }
.b-tw  { background: #f9fafb; color: #9ca3af; border: 1px solid #f3f4f6; font-size: 10px; }
.b-tn  { background: #eff6ff; color: #1d4ed8; border: 1px solid #bfdbfe; font-size: 10px; }
.b-ts  { background: #f0fdf4; color: #15803d; border: 1px solid #bbf7d0; font-size: 10px; }
.b-te  { background: #fff7ed; color: #c2410c; border: 1px solid #fed7aa; font-size: 10px; }
.b-inv { background: #faf5ff; color: #7e22ce; border: 1px solid #e9d5ff; font-size: 9px; padding: 2px 6px; }
.b-lev { background: #eff6ff; color: #1d4ed8; border: 1px solid #bfdbfe; font-size: 9px; padding: 2px 6px; }

/* ── Legend table ── */
.legend-table { width: 100%; border-collapse: collapse; background: #ffffff; border-radius: 12px; overflow: hidden; border: 1px solid #e5e7eb; box-shadow: 0 1px 4px rgba(0,0,0,0.05); }
.legend-table thead th {
    background: #f9fafb; text-align: left; padding: 9px 16px;
    font-size: 10px; color: #6b7280; text-transform: uppercase;
    letter-spacing: 0.7px; font-weight: 600;
    border-bottom: 1px solid #e5e7eb;
}
.legend-table tbody tr { border-bottom: 0.5px solid #f3f4f6; }
.legend-table tbody tr:last-child { border-bottom: none; }
.legend-table td { padding: 9px 16px; vertical-align: middle; font-size: 12px; }
.legend-table .cat-row td { background: #f9fafb; font-size: 9px; color: #9ca3af; text-transform: uppercase; letter-spacing: 1.2px; font-weight: 700; padding: 6px 16px; }
.leg-desc { color: #374151; font-size: 12px; }
.leg-action { color: #6b7280; font-size: 11px; font-style: italic; }

.footer { font-size: 10px; color: #d1d5db; text-align: right; margin-top: 20px; font-family: 'JetBrains Mono', monospace; line-height: 1.8; }

div[data-testid="column"] { padding: 0 5px !important; }
div[data-testid="stHorizontalBlock"] { gap: 0 !important; }
</style>
""", unsafe_allow_html=True)

# ── Assets ─────────────────────────────────────────────────────────
GLOBAL_ASSETS = [
    ("NSE Nifty 500", "^CRSLDX",   "INR", False, False, "India market filter"),
    ("S&P 500",       "^GSPC",     "USD", False, False, ""),
    ("NASDAQ 100",    "^NDX",      "USD", False, False, ""),
    ("TOPIX",         "^TOPX",     "JPY", False, False, "Japan broad market"),
    ("Hang Seng",     "^HSI",      "HKD", False, False, ""),
    ("CSI 300",       "000300.SS", "CNY", False, False, "Mainland China"),
    ("Gold (USD)",    "GC=F",      "USD", False, False, ""),
    ("Gold (MCX)",    "MCX_GOLD",  "INR", False, False, "GC=F x USDINR"),
    ("Oil WTI",       "CL=F",      "USD", False, False, ""),
    ("USD / INR",     "USDINR=X",  "INR", False, False, "S2 = rupee weakening"),
    ("Bitcoin",       "BTC-USD",   "USD", False, False, ""),
]

ETF_ASSETS = [
    ("SPY",  "SPY",  "USD", False, False, "S&P 500"),
    ("QQQ",  "QQQ",  "USD", False, False, "NASDAQ 100"),
    ("TQQQ", "TQQQ", "USD", False, True,  "3x Long NASDAQ"),
    ("SQQQ", "SQQQ", "USD", True,  True,  "3x Inverse NASDAQ"),
    ("XLE",  "XLE",  "USD", False, False, "Energy"),
    ("XLF",  "XLF",  "USD", False, False, "Financials"),
    ("XLK",  "XLK",  "USD", False, False, "Technology"),
    ("XLV",  "XLV",  "USD", False, False, "Healthcare"),
    ("XLI",  "XLI",  "USD", False, False, "Industrials"),
    ("XLB",  "XLB",  "USD", False, False, "Materials"),
    ("XLP",  "XLP",  "USD", False, False, "Consumer Staples"),
    ("GLD",  "GLD",  "USD", False, False, "Gold ETF"),
    ("USO",  "USO",  "USD", False, False, "Oil ETF"),
    ("UNG",  "UNG",  "USD", False, False, "Natural Gas"),
    ("PDBC", "PDBC", "USD", False, False, "Diversified Commodities"),
    ("TLT",  "TLT",  "USD", False, False, "Long-Duration Bonds"),
    ("TBT",  "TBT",  "USD", True,  True,  "2x Inverse Long Bonds"),
]

INV_PERIOD   = 30
TRA_PERIOD   = 10
SLOPE_WEAK   = 0.20
SLOPE_NORMAL = 0.50
EXTENDED_PCT = 20.0

# ── Maths ──────────────────────────────────────────────────────────
def wma(series, period):
    w = np.arange(1, period + 1, dtype=float)
    return series.rolling(period).apply(lambda x: np.dot(x, w) / w.sum(), raw=True)

def get_stage(price, ma30, slope):
    a, r = price > ma30, slope > 0
    if a and r:      return 2
    if a and not r:  return 3
    if not a and r:  return 1
    return 4

def inv_label(s): return {2:"ON", 3:"TOPPING", 1:"BASING", 4:"OFF"}[s]

def tra_label(price, ma10, slope10):
    a, r = price > ma10, slope10 > 0
    if a and r:      return "ON"
    if a and not r:  return "TOPPING"
    if not a and r:  return "BASING"
    return "OFF"

def trend_label(slope_val, pct):
    if pct >= EXTENDED_PCT: return "EXTENDED"
    s = abs(slope_val)
    if s < SLOPE_WEAK:   return "WEAK"
    if s < SLOPE_NORMAL: return "NORMAL"
    return "STRONG"

def fmt(p):
    if p >= 10000: return f"{p:,.0f}"
    if p >= 100:   return f"{p:,.1f}"
    if p >= 1:     return f"{p:,.2f}"
    return f"{p:.4f}"

def accent(inv):
    return {"ON":"#16a34a","OFF":"#dc2626","TOPPING":"#d97706","BASING":"#7c3aed"}.get(inv,"#9ca3af")

def b(status):
    return {"ON":"b-on","OFF":"b-off","TOPPING":"b-top","BASING":"b-bas"}.get(status,"b-s")

def tb(t):
    return {"WEAK":"b-tw","NORMAL":"b-tn","STRONG":"b-ts","EXTENDED":"b-te"}.get(t,"b-tw")

# ── Data ───────────────────────────────────────────────────────────
@st.cache_data(ttl=3600)
def fetch(ticker):
    try:
        df = yf.download(ticker, period="130wk", interval="1wk", progress=False, auto_adjust=True)
        if df.empty or len(df) < 36: return None
        return df['Close'].squeeze().dropna()
    except: return None

@st.cache_data(ttl=3600)
def fetch_mcx():
    try:
        gc = yf.download("GC=F",     period="130wk", interval="1wk", progress=False, auto_adjust=True)['Close'].squeeze().dropna()
        fx = yf.download("USDINR=X", period="130wk", interval="1wk", progress=False, auto_adjust=True)['Close'].squeeze().dropna()
        return (gc.reindex(fx.index, method='ffill') * fx).dropna()
    except: return None

def analyze(close):
    try:
        ma30 = wma(close, INV_PERIOD)
        ma10 = close.rolling(TRA_PERIOD).mean()
        p    = float(close.iloc[-1])
        m30  = float(ma30.iloc[-1])
        m10  = float(ma10.iloc[-1])
        s30  = float((ma30.iloc[-1]-ma30.iloc[-2])/ma30.iloc[-2]*100) if len(ma30.dropna())>=2 else 0.0
        s10  = float((ma10.iloc[-1]-ma10.iloc[-2])/ma10.iloc[-2]*100) if len(ma10.dropna())>=2 else 0.0
        pct  = (p-m30)/m30*100
        wchg = float((close.iloc[-1]-close.iloc[-2])/close.iloc[-2]*100) if len(close)>=2 else 0.0
        st_  = get_stage(p, m30, s30)
        return dict(price=p, ma30=m30, ma10=m10, slope30=s30, slope10=s10,
                    pct=pct, wchg=wchg, stage=st_,
                    inv=inv_label(st_), tra=tra_label(p,m10,s10),
                    trend=trend_label(s30,pct), date=close.index[-1].strftime("%d %b %Y"), error=None)
    except Exception as e:
        return dict(error=str(e))

# ── Row builder ────────────────────────────────────────────────────
ROW_TINT = {
    "ON":      "background:#f0fdf4",
    "OFF":     "background:#fef2f2",
    "TOPPING": "background:#fffbeb",
    "BASING":  "background:#faf5ff",
}

def build_row(name, ticker, currency, is_inv, is_lev, note, d):
    if d is None or d.get("error"):
        err = (d.get("error","") if d else "No data")[:40]
        return f"""<tr>
<td><div class="a-name">{name}</div><div class="a-tick">{ticker}</div></td>
<td colspan="7" style="font-size:11px;color:#dc2626">&#9888; {err}</td>
</tr>"""

    flags = ""
    if is_inv: flags += ' <span class="b b-inv">INV</span>'
    if is_lev: flags += ' <span class="b b-lev">3x</span>'

    chg_cls = "up" if d['wchg'] >= 0 else "dn"
    chg_arr = "&#9650;" if d['wchg'] >= 0 else "&#9660;"
    ma_arr  = "&#8593;" if d['slope30'] > 0 else "&#8595;"
    pct_s   = f"{'+' if d['pct']>=0 else ''}{d['pct']:.1f}%"
    ac      = accent(d['inv'])

    tint = ROW_TINT.get(d['inv'], "")
    trend_cell = f'<span class="b {tb(d["trend"])}">{d["trend"]}</span>' if d['inv'] == "ON" else '<span style="font-size:12px;color:#d1d5db">&mdash;</span>'
    return f"""<tr style="{tint}">
<td>
  <div style="display:flex;align-items:center">
    <span class="dot" style="background:{ac}"></span>
    <div>
      <div class="a-name">{name}{flags}</div>
      <div class="a-tick">{ticker} &middot; {currency}</div>
    </div>
  </div>
</td>
<td class="a-price">{fmt(d['price'])}</td>
<td class="{chg_cls}">{chg_arr} {abs(d['wchg']):.1f}%</td>
<td><span class="b {b(d['inv'])}">{d['inv']}</span></td>
<td><span class="b {b(d['tra'])}">{d['tra']}</span></td>
<td><span class="b b-s">S{d['stage']}</span></td>
<td>{trend_cell}</td>
<td class="ma-val">{pct_s} {ma_arr} &middot; {d['date']}</td>
</tr>"""

# ── Legend HTML ────────────────────────────────────────────────────
LEGEND_HTML = """
<table class="legend-table">
  <thead>
    <tr>
      <th style="width:100px">Signal</th>
      <th style="width:80px">Badge</th>
      <th>What it means</th>
      <th>What to do</th>
    </tr>
  </thead>
  <tbody>
    <tr class="cat-row"><td colspan="4">INV Filter &mdash; Based on 30-week Weighted MA</td></tr>
    <tr>
      <td><strong>ON</strong></td>
      <td><span class="b b-on">ON</span></td>
      <td class="leg-desc">Price is above its rising 30wMA. Market is in Stage 2 &mdash; a healthy uptrend is in place.</td>
      <td class="leg-action">Conditions are right. New entries and adds are permitted.</td>
    </tr>
    <tr>
      <td><strong>TOPPING</strong></td>
      <td><span class="b b-top">TOPPING</span></td>
      <td class="leg-desc">Price is still above the 30wMA but the MA has started flattening or declining. Stage 3 &mdash; trend losing momentum.</td>
      <td class="leg-action">No new entries. Tighten stops on existing positions. Be alert.</td>
    </tr>
    <tr>
      <td><strong>BASING</strong></td>
      <td><span class="b b-bas">BASING</span></td>
      <td class="leg-desc">Price is below the 30wMA but the MA is still rising. Stage 1 &mdash; building a floor, not broken yet.</td>
      <td class="leg-action">On watch. Not actionable yet. Wait for price to reclaim the MA.</td>
    </tr>
    <tr>
      <td><strong>OFF</strong></td>
      <td><span class="b b-off">OFF</span></td>
      <td class="leg-desc">Price is below a declining 30wMA. Stage 4 &mdash; a confirmed downtrend. The worst place to hold.</td>
      <td class="leg-action">No entries. Capital should be in cash, gold, or inverse instruments.</td>
    </tr>
    <tr class="cat-row"><td colspan="4">TRA Filter &mdash; Based on 10-week Simple MA</td></tr>
    <tr>
      <td><strong>ON</strong></td>
      <td><span class="b b-on">ON</span></td>
      <td class="leg-desc">Price is above its rising 10wMA. Short-term trend is healthy.</td>
      <td class="leg-action">Momentum is with you. Good timing for entries within a Stage 2 asset.</td>
    </tr>
    <tr>
      <td><strong>TOPPING</strong></td>
      <td><span class="b b-top">TOPPING</span></td>
      <td class="leg-desc">Price is above the 10wMA but momentum is fading. Short-term trend rolling over.</td>
      <td class="leg-action">Watch closely. A pullback to the 10wMA may be coming &mdash; can be a buy opportunity in strong Stage 2 assets.</td>
    </tr>
    <tr>
      <td><strong>BASING</strong></td>
      <td><span class="b b-bas">BASING</span></td>
      <td class="leg-desc">Price has dipped below the 10wMA but MA is still rising. Short-term pullback in a longer uptrend.</td>
      <td class="leg-action">Potential Type B setup if the asset is also Stage 2 on INV. Watch for a bounce back above the 10wMA.</td>
    </tr>
    <tr>
      <td><strong>OFF</strong></td>
      <td><span class="b b-off">OFF</span></td>
      <td class="leg-desc">Price is below a declining 10wMA. Short-term downtrend confirmed.</td>
      <td class="leg-action">Avoid new entries. Wait for both MAs to turn back up before acting.</td>
    </tr>
    <tr class="cat-row"><td colspan="4">Stage &mdash; Weinstein Stage Classification</td></tr>
    <tr>
      <td><strong>Stage 1</strong></td>
      <td><span class="b b-s">S1</span></td>
      <td class="leg-desc">Basing phase. Price is consolidating below or near a flat/rising 30wMA after a decline.</td>
      <td class="leg-action">Watch. The setup is being built. Do not buy yet.</td>
    </tr>
    <tr>
      <td><strong>Stage 2</strong></td>
      <td><span class="b b-s">S2</span></td>
      <td class="leg-desc">Advancing phase. Price is above a rising 30wMA. The only stage where you should hold or add.</td>
      <td class="leg-action">The buy zone. All entries must be in Stage 2 only.</td>
    </tr>
    <tr>
      <td><strong>Stage 3</strong></td>
      <td><span class="b b-s">S3</span></td>
      <td class="leg-desc">Topping phase. Price is still above the 30wMA but the MA is rolling over. Distribution happening.</td>
      <td class="leg-action">Reduce positions. Tighten stops. Do not add.</td>
    </tr>
    <tr>
      <td><strong>Stage 4</strong></td>
      <td><span class="b b-s">S4</span></td>
      <td class="leg-desc">Declining phase. Price is below a falling 30wMA. Sellers are in full control.</td>
      <td class="leg-action">Never hold. Never buy. Exit if still in.</td>
    </tr>
    <tr class="cat-row"><td colspan="4">Trend Strength &mdash; Based on 30wMA Weekly Slope</td></tr>
    <tr>
      <td><strong>WEAK</strong></td>
      <td><span class="b b-tw">WEAK</span></td>
      <td class="leg-desc">30wMA rising or falling less than 0.2% per week. Trend exists but has little momentum behind it.</td>
      <td class="leg-action">Valid but be cautious. Easy for the trend to stall or reverse.</td>
    </tr>
    <tr>
      <td><strong>NORMAL</strong></td>
      <td><span class="b b-tn">NORMAL</span></td>
      <td class="leg-desc">30wMA moving 0.2% to 0.5% per week. A healthy, sustainable trend with good momentum.</td>
      <td class="leg-action">Ideal conditions. Trend is strong enough to be trusted.</td>
    </tr>
    <tr>
      <td><strong>STRONG</strong></td>
      <td><span class="b b-ts">STRONG</span></td>
      <td class="leg-desc">30wMA moving more than 0.5% per week. A powerful, fast-moving trend.</td>
      <td class="leg-action">High conviction. Ride it but watch for EXTENDED conditions developing.</td>
    </tr>
    <tr>
      <td><strong>EXTENDED</strong></td>
      <td><span class="b b-te">EXTENDED</span></td>
      <td class="leg-desc">Price is more than 20% above the 30wMA. The asset has moved too far too fast and is stretched.</td>
      <td class="leg-action">Do not chase. Wait for a pullback towards the MA before entering. Consider partial profit-taking.</td>
    </tr>
  </tbody>
</table>
"""

# ── Main ───────────────────────────────────────────────────────────
def main():
    now = datetime.now().strftime("%A %d %b %Y &middot; %H:%M")

    st.markdown(f'<div class="db-title">Global Market Filter</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="db-sub">Weinstein Stage Analysis &middot; INV (30w WMA) &middot; TRA (10w SMA) &middot; {now}</div>', unsafe_allow_html=True)

    with st.spinner("Fetching live market data..."):
        results = {}
        for _, ticker, *_ in GLOBAL_ASSETS:
            t = ticker
            if ticker == "MCX_GOLD":
                c = fetch_mcx()
            else:
                c = fetch(ticker)
            results[t] = analyze(c) if c is not None else dict(error="Data unavailable")

        for _, ticker, *_ in ETF_ASSETS:
            if ticker not in results:
                c = fetch(ticker)
                results[ticker] = analyze(c) if c is not None else dict(error="Data unavailable")

    # Summary metrics
    gd = [results.get(t if t != "MCX_GOLD" else "MCX_GOLD", {}) for _,t,*_ in GLOBAL_ASSETS]
    inv_on  = sum(1 for d in gd if d.get("inv")=="ON")
    inv_off = sum(1 for d in gd if d.get("inv")=="OFF")
    topping = sum(1 for d in gd if d.get("inv")=="TOPPING")
    basing  = sum(1 for d in gd if d.get("inv")=="BASING")
    tra_on  = sum(1 for d in gd if d.get("tra")=="ON")

    c1,c2,c3,c4,c5 = st.columns(5)
    for col, lbl, val, clr in [
        (c1,"INV On",  inv_on,  "#16a34a"),
        (c2,"INV Off", inv_off, "#dc2626"),
        (c3,"Topping", topping, "#d97706"),
        (c4,"Basing",  basing,  "#7c3aed"),
        (c5,"TRA On",  tra_on,  "#2563eb"),
    ]:
        col.markdown(f"""<div class="sum-card">
<div class="sum-label">{lbl}</div>
<div class="sum-val" style="color:{clr}">{val}</div>
</div>""", unsafe_allow_html=True)

    # ── Global assets table ────────────────────────────────────────
    st.markdown('<div class="section-hdr">Global Indices &amp; Assets</div>', unsafe_allow_html=True)

    global_rows = ""
    for name, ticker, cur, ii, il, note in GLOBAL_ASSETS:
        t = ticker
        global_rows += build_row(name, ticker, cur, ii, il, note, results.get(t))

    st.markdown(f"""
<table class="data-table">
  <thead>
    <tr>
      <th>Asset</th><th>Price</th><th>Week</th>
      <th>INV (30w)</th><th>TRA (10w)</th><th>Stage</th><th>Trend</th><th>vs 30wMA</th>
    </tr>
  </thead>
  <tbody>{global_rows}</tbody>
</table>""", unsafe_allow_html=True)

    # ── ETF table ──────────────────────────────────────────────────
    st.markdown('<div class="section-hdr">Tradeable ETFs &middot; IBKR</div>', unsafe_allow_html=True)

    etf_rows = ""
    for name, ticker, cur, ii, il, note in ETF_ASSETS:
        etf_rows += build_row(name, ticker, cur, ii, il, note, results.get(ticker))

    st.markdown(f"""
<table class="data-table">
  <thead>
    <tr>
      <th>Asset</th><th>Price</th><th>Week</th>
      <th>INV (30w)</th><th>TRA (10w)</th><th>Stage</th><th>Trend</th><th>vs 30wMA</th>
    </tr>
  </thead>
  <tbody>{etf_rows}</tbody>
</table>""", unsafe_allow_html=True)

    # ── Legend ─────────────────────────────────────────────────────
    st.markdown('<div class="section-hdr">Signal Reference Guide</div>', unsafe_allow_html=True)
    st.markdown(LEGEND_HTML, unsafe_allow_html=True)

    st.markdown(f"""<div class="footer">
INV = 30w Weighted MA &middot; TRA = 10w Simple MA &middot; Slope bands: Weak &lt;0.2%/wk &middot; Normal 0.2&ndash;0.5%/wk &middot; Strong &gt;0.5%/wk &middot; Extended = price 20%+ above 30wMA<br>
Data: Yahoo Finance &middot; Weekly candles (Friday close) &middot; Cache refreshes every hour &middot; {now}
</div>""", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
