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

html, body, [class*="css"], .stApp { font-family: 'Inter', sans-serif !important; background-color: #f8f9fa !important; }
.main, .block-container { background-color: #f8f9fa !important; }
.block-container { padding: 2rem 2.5rem !important; max-width: 1400px !important; }

.db-title { font-size: 26px; font-weight: 700; color: #111827; letter-spacing: -0.5px; margin-bottom: 3px; }
.db-sub   { font-size: 12px; color: #9ca3af; margin-bottom: 24px; font-family: 'JetBrains Mono', monospace; }

.sum-card  { background: #fff; border: 1px solid #e5e7eb; border-radius: 10px; padding: 14px 18px; text-align: center; }
.sum-label { font-size: 10px; color: #9ca3af; text-transform: uppercase; letter-spacing: 0.8px; font-weight: 600; }
.sum-val   { font-size: 30px; font-weight: 700; margin-top: 3px; }

.section-hdr { font-size: 10px; color: #9ca3af; text-transform: uppercase; letter-spacing: 1.5px; font-weight: 700; padding: 20px 0 10px; border-bottom: 1px solid #e5e7eb; margin-bottom: 0; }

.dt { width: 100%; border-collapse: collapse; background: #fff; border-radius: 12px; overflow: hidden; border: 1px solid #e5e7eb; box-shadow: 0 1px 4px rgba(0,0,0,0.05); }
.dt thead th { background: #f9fafb; text-align: left; padding: 9px 14px; font-size: 10px; color: #6b7280; text-transform: uppercase; letter-spacing: 0.7px; font-weight: 600; border-bottom: 1px solid #e5e7eb; }
.dt tbody tr { border-bottom: 0.5px solid #f3f4f6; }
.dt tbody tr:hover { background: #f9fafb !important; }
.dt tbody tr:last-child { border-bottom: none; }
.dt td { padding: 8px 14px; vertical-align: middle; }

.an { font-size: 13px; font-weight: 600; color: #111827; }
.at { font-size: 10px; color: #9ca3af; font-family: 'JetBrains Mono', monospace; }
.ap { font-family: 'JetBrains Mono', monospace; font-size: 13px; font-weight: 600; color: #111827; white-space: nowrap; }
.up { color: #059669; font-size: 11px; font-weight: 500; white-space: nowrap; }
.dn { color: #dc2626; font-size: 11px; font-weight: 500; white-space: nowrap; }
.mv { font-family: 'JetBrains Mono', monospace; font-size: 11px; color: #6b7280; white-space: nowrap; }

.b     { display: inline-block; padding: 3px 8px; border-radius: 5px; font-size: 11px; font-weight: 700; white-space: nowrap; }
.b-on  { background: #dcfce7; color: #15803d; border: 1px solid #bbf7d0; }
.b-off { background: #fee2e2; color: #b91c1c; border: 1px solid #fecaca; }
.b-top { background: #fef3c7; color: #b45309; border: 1px solid #fde68a; }
.b-bas { background: #ede9fe; color: #6d28d9; border: 1px solid #ddd6fe; }
.b-s   { background: #f3f4f6; color: #374151; border: 1px solid #e5e7eb; font-size: 11px; }
.b-tw  { background: #f9fafb; color: #9ca3af; border: 1px solid #f3f4f6; font-size: 10px; }
.b-tn  { background: #eff6ff; color: #1d4ed8; border: 1px solid #bfdbfe; font-size: 10px; }
.b-ts  { background: #f0fdf4; color: #15803d; border: 1px solid #bbf7d0; font-size: 10px; }
.b-te  { background: #fff7ed; color: #c2410c; border: 1px solid #fed7aa; font-size: 10px; }
.b-inv { background: #faf5ff; color: #7e22ce; border: 1px solid #e9d5ff; font-size: 9px; padding: 2px 5px; }
.b-lev { background: #eff6ff; color: #1d4ed8; border: 1px solid #bfdbfe; font-size: 9px; padding: 2px 5px; }

.lt { width: 100%; border-collapse: collapse; background: #fff; border-radius: 12px; overflow: hidden; border: 1px solid #e5e7eb; box-shadow: 0 1px 4px rgba(0,0,0,0.05); }
.lt thead th { background: #f9fafb; text-align: left; padding: 9px 16px; font-size: 10px; color: #6b7280; text-transform: uppercase; letter-spacing: 0.7px; font-weight: 600; border-bottom: 1px solid #e5e7eb; }
.lt tbody tr { border-bottom: 0.5px solid #f3f4f6; }
.lt tbody tr:last-child { border-bottom: none; }
.lt td { padding: 9px 16px; vertical-align: middle; font-size: 12px; }
.lt .cr td { background: #f9fafb; font-size: 9px; color: #9ca3af; text-transform: uppercase; letter-spacing: 1.2px; font-weight: 700; padding: 6px 16px; }
.ld { color: #374151; font-size: 12px; }
.la { color: #6b7280; font-size: 11px; font-style: italic; }

.footer { font-size: 10px; color: #d1d5db; text-align: right; margin-top: 20px; font-family: 'JetBrains Mono', monospace; line-height: 1.8; }
div[data-testid="column"] { padding: 0 5px !important; }
</style>
""", unsafe_allow_html=True)

GLOBAL_ASSETS = [
    ("NSE Nifty 500", "^CRSLDX",   "INR", False, False, ""),
    ("S&P 500",       "^GSPC",     "USD", False, False, ""),
    ("NASDAQ 100",    "^NDX",      "USD", False, False, ""),
    ("Nikkei 225",    "^N225",     "JPY", False, False, ""),
    ("Hang Seng",     "^HSI",      "HKD", False, False, ""),
    ("CSI 300",       "000300.SS", "CNY", False, False, ""),
    ("Gold (USD)",    "GC=F",      "USD", False, False, ""),
    ("Gold (MCX)",    "MCX_GOLD",  "INR", False, False, ""),
    ("Oil WTI",       "CL=F",      "USD", False, False, ""),
    ("USD/INR",       "USDINR=X",  "INR", False, False, ""),
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

INV_PERIOD=30; TRA_PERIOD=10; SLOPE_WEAK=0.20; SLOPE_NORMAL=0.50; EXTENDED_PCT=20.0

TINT = {"ON":"#f0fdf4","OFF":"#fef2f2","TOPPING":"#fffbeb","BASING":"#faf5ff"}
ACCENT = {"ON":"#16a34a","OFF":"#dc2626","TOPPING":"#d97706","BASING":"#7c3aed"}

def wma(s, p):
    w = np.arange(1, p+1, dtype=float)
    return s.rolling(p).apply(lambda x: np.dot(x,w)/w.sum(), raw=True)

def stage(price, m30, s30):
    a,r = price>m30, s30>0
    if a and r: return 2
    if a and not r: return 3
    if not a and r: return 1
    return 4

def inv_lbl(s): return {2:"ON",3:"TOPPING",1:"BASING",4:"OFF"}[s]

def tra_lbl(price, m10, s10):
    a,r = price>m10, s10>0
    if a and r: return "ON"
    if a and not r: return "TOPPING"
    if not a and r: return "BASING"
    return "OFF"

def trend_lbl(s, pct):
    if pct >= EXTENDED_PCT: return "EXTENDED"
    if abs(s) < SLOPE_WEAK: return "WEAK"
    if abs(s) < SLOPE_NORMAL: return "NORMAL"
    return "STRONG"

def fmt(p):
    if p>=10000: return f"{p:,.0f}"
    if p>=100:   return f"{p:,.1f}"
    if p>=1:     return f"{p:,.2f}"
    return f"{p:.4f}"

def bc(status): return {"ON":"b-on","OFF":"b-off","TOPPING":"b-top","BASING":"b-bas"}.get(status,"b-s")
def tc(t):      return {"WEAK":"b-tw","NORMAL":"b-tn","STRONG":"b-ts","EXTENDED":"b-te"}.get(t,"b-tw")

@st.cache_data(ttl=3600)
def fetch(ticker):
    try:
        df = yf.download(ticker, period="130wk", interval="1wk", progress=False, auto_adjust=True)
        if df.empty or len(df)<36: return None
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
        m30 = wma(close, INV_PERIOD)
        m10 = close.rolling(TRA_PERIOD).mean()
        p   = float(close.iloc[-1])
        v30 = float(m30.iloc[-1])
        v10 = float(m10.iloc[-1])
        s30 = float((m30.iloc[-1]-m30.iloc[-2])/m30.iloc[-2]*100) if len(m30.dropna())>=2 else 0.0
        s10 = float((m10.iloc[-1]-m10.iloc[-2])/m10.iloc[-2]*100) if len(m10.dropna())>=2 else 0.0
        pct = (p-v30)/v30*100
        wch = float((close.iloc[-1]-close.iloc[-2])/close.iloc[-2]*100) if len(close)>=2 else 0.0
        st_ = stage(p, v30, s30)
        return dict(price=p, pct=pct, wchg=wch, stage=st_, slope30=s30,
                    inv=inv_lbl(st_), tra=tra_lbl(p,v10,s10),
                    trend=trend_lbl(s30,pct), date=close.index[-1].strftime("%d %b %Y"), error=None)
    except Exception as e:
        return dict(error=str(e))

def row(name, ticker, currency, is_inv, is_lev, note, d):
    if d is None or d.get("error"):
        err = (d.get("error","") if d else "No data")[:50]
        return f'<tr><td class="an">{name}<br><span class="at">{ticker}</span></td><td colspan="7" style="font-size:11px;color:#dc2626">&#9888; {err}</td></tr>'

    inv   = d['inv']
    bg    = TINT.get(inv, "#ffffff")
    dot   = ACCENT.get(inv, "#9ca3af")
    chg_c = "up" if d['wchg']>=0 else "dn"
    chg_s = f"{'&#9650;' if d['wchg']>=0 else '&#9660;'} {abs(d['wchg']):.1f}%"
    pct_s = f"{'+' if d['pct']>=0 else ''}{d['pct']:.1f}%"
    arr   = "&#8593;" if d['slope30']>0 else "&#8595;"
    flags = (' <span class="b b-inv">INVERSE</span>' if is_inv else '') + (' <span class="b b-lev">3x</span>' if is_lev else '')
    note_s= f'<br><span style="font-size:10px;color:#6b7280">{note}</span>' if note else ''
    trend_s = f'<span class="b {tc(d["trend"])}">{d["trend"]}</span>' if inv=="ON" else '<span style="color:#d1d5db">&#8212;</span>'

    return (f'<tr style="background:{bg}">'
            f'<td><span style="display:inline-block;width:8px;height:8px;border-radius:50%;background:{dot};margin-right:7px;vertical-align:middle"></span>'
            f'<span class="an">{name}</span>{flags}{note_s}<br><span class="at">{ticker} &middot; {currency}</span></td>'
            f'<td class="ap">{fmt(d["price"])}</td>'
            f'<td class="{chg_c}">{chg_s}</td>'
            f'<td><span class="b {bc(inv)}">{inv}</span></td>'
            f'<td><span class="b {bc(d["tra"])}">{d["tra"]}</span></td>'
            f'<td><span class="b b-s">Stage {d["stage"]}</span></td>'
            f'<td>{trend_s}</td>'
            f'<td class="mv">{pct_s} {arr} &middot; {d["date"]}</td>'
            f'</tr>')

LEGEND = """<table class="lt">
<thead><tr><th style="width:90px">Signal</th><th style="width:80px">Badge</th><th>What it means</th><th>What to do</th></tr></thead>
<tbody>
<tr class="cr"><td colspan="4">INV Filter — 30-week Weighted MA</td></tr>
<tr><td><strong>ON</strong></td><td><span class="b b-on">ON</span></td><td class="ld">Price above a rising 30wMA. Stage 2 — healthy uptrend in place.</td><td class="la">New entries and adds permitted.</td></tr>
<tr><td><strong>TOPPING</strong></td><td><span class="b b-top">TOPPING</span></td><td class="ld">Price above 30wMA but MA flattening or declining. Stage 3 — trend losing momentum.</td><td class="la">No new entries. Tighten stops. Be alert.</td></tr>
<tr><td><strong>BASING</strong></td><td><span class="b b-bas">BASING</span></td><td class="ld">Price below 30wMA but MA still rising. Stage 1 — building a floor, not broken yet.</td><td class="la">On watch. Wait for price to reclaim the MA.</td></tr>
<tr><td><strong>OFF</strong></td><td><span class="b b-off">OFF</span></td><td class="ld">Price below a declining 30wMA. Stage 4 — confirmed downtrend.</td><td class="la">No entries. Move capital to cash, gold, or inverse instruments.</td></tr>
<tr class="cr"><td colspan="4">TRA Filter — 10-week Simple MA</td></tr>
<tr><td><strong>ON</strong></td><td><span class="b b-on">ON</span></td><td class="ld">Price above a rising 10wMA. Short-term trend healthy.</td><td class="la">Good timing for entries within a Stage 2 asset.</td></tr>
<tr><td><strong>TOPPING</strong></td><td><span class="b b-top">TOPPING</span></td><td class="ld">Price above 10wMA but momentum fading. Short-term trend rolling over.</td><td class="la">Pullback to 10wMA may be coming — potential add opportunity in Stage 2.</td></tr>
<tr><td><strong>BASING</strong></td><td><span class="b b-bas">BASING</span></td><td class="ld">Price dipped below 10wMA but MA still rising. Short-term pullback within longer uptrend.</td><td class="la">Watch for bounce back above 10wMA — potential Type B setup.</td></tr>
<tr><td><strong>OFF</strong></td><td><span class="b b-off">OFF</span></td><td class="ld">Price below a declining 10wMA. Short-term downtrend confirmed.</td><td class="la">Avoid new entries. Wait for both MAs to turn back up.</td></tr>
<tr class="cr"><td colspan="4">Stage — Weinstein Stage Classification</td></tr>
<tr><td><strong>Stage 1</strong></td><td><span class="b b-s">Stage 1</span></td><td class="ld">Basing. Price consolidating near a flat/rising 30wMA after a decline.</td><td class="la">Watch. Do not buy yet.</td></tr>
<tr><td><strong>Stage 2</strong></td><td><span class="b b-s">Stage 2</span></td><td class="ld">Advancing. Price above a rising 30wMA. The only stage to hold or add.</td><td class="la">The buy zone. All entries must be Stage 2 only.</td></tr>
<tr><td><strong>Stage 3</strong></td><td><span class="b b-s">Stage 3</span></td><td class="ld">Topping. Price above 30wMA but MA rolling over. Distribution underway.</td><td class="la">Reduce positions. Tighten stops. Do not add.</td></tr>
<tr><td><strong>Stage 4</strong></td><td><span class="b b-s">Stage 4</span></td><td class="ld">Declining. Price below a falling 30wMA. Sellers in full control.</td><td class="la">Never hold. Never buy. Exit if still in.</td></tr>
<tr class="cr"><td colspan="4">Trend Strength — 30wMA Weekly Slope (only shown when INV is ON)</td></tr>
<tr><td><strong>WEAK</strong></td><td><span class="b b-tw">WEAK</span></td><td class="ld">30wMA moving less than 0.2% per week. Trend exists but low momentum.</td><td class="la">Valid but cautious — easy to stall or reverse.</td></tr>
<tr><td><strong>NORMAL</strong></td><td><span class="b b-tn">NORMAL</span></td><td class="ld">30wMA moving 0.2–0.5% per week. Healthy, sustainable trend.</td><td class="la">Ideal conditions. Trend strong enough to trust.</td></tr>
<tr><td><strong>STRONG</strong></td><td><span class="b b-ts">STRONG</span></td><td class="ld">30wMA moving more than 0.5% per week. Powerful trend with momentum.</td><td class="la">High conviction. Ride it — watch for Extended developing.</td></tr>
<tr><td><strong>EXTENDED</strong></td><td><span class="b b-te">EXTENDED</span></td><td class="ld">Price more than 20% above 30wMA. Stretched — moved too far too fast.</td><td class="la">Do not chase. Wait for pullback. Consider partial profit-taking.</td></tr>
</tbody></table>"""

TABLE_HEAD = """<table class="dt"><thead><tr>
<th>Asset</th><th>Price</th><th>Week</th>
<th>INV (30w)</th><th>TRA (10w)</th><th>Stage</th><th>Trend</th><th>vs 30wMA</th>
</tr></thead><tbody>"""

def main():
    now = datetime.now().strftime("%A %d %b %Y · %H:%M")
    st.markdown('<div class="db-title">Global Market Filter</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="db-sub">Weinstein Stage Analysis · INV (30w WMA) · TRA (10w SMA) · {now}</div>', unsafe_allow_html=True)

    with st.spinner("Fetching live market data..."):
        R = {}
        for _, t, *_ in GLOBAL_ASSETS:
            c = fetch_mcx() if t=="MCX_GOLD" else fetch(t)
            R[t] = analyze(c) if c is not None else dict(error="Data unavailable")
        for _, t, *_ in ETF_ASSETS:
            if t not in R:
                c = fetch(t)
                R[t] = analyze(c) if c is not None else dict(error="Data unavailable")

    gd = [R.get(t,{}) for _,t,*_ in GLOBAL_ASSETS]
    c1,c2,c3,c4,c5 = st.columns(5)
    for col,lbl,val,clr in [
        (c1,"INV On",  sum(1 for d in gd if d.get("inv")=="ON"),      "#16a34a"),
        (c2,"INV Off", sum(1 for d in gd if d.get("inv")=="OFF"),     "#dc2626"),
        (c3,"Topping", sum(1 for d in gd if d.get("inv")=="TOPPING"), "#d97706"),
        (c4,"Basing",  sum(1 for d in gd if d.get("inv")=="BASING"),  "#7c3aed"),
        (c5,"TRA On",  sum(1 for d in gd if d.get("tra")=="ON"),      "#2563eb"),
    ]:
        col.markdown(f'<div class="sum-card"><div class="sum-label">{lbl}</div><div class="sum-val" style="color:{clr}">{val}</div></div>', unsafe_allow_html=True)

    st.markdown('<div class="section-hdr">Global Indices &amp; Assets</div>', unsafe_allow_html=True)
    rows = "".join(row(n,t,c,ii,il,no,R.get(t)) for n,t,c,ii,il,no in GLOBAL_ASSETS)
    st.markdown(TABLE_HEAD + rows + "</tbody></table>", unsafe_allow_html=True)

    st.markdown('<div class="section-hdr">Tradeable ETFs · IBKR</div>', unsafe_allow_html=True)
    rows2 = "".join(row(n,t,c,ii,il,no,R.get(t)) for n,t,c,ii,il,no in ETF_ASSETS)
    st.markdown(TABLE_HEAD + rows2 + "</tbody></table>", unsafe_allow_html=True)

    st.markdown('<div class="section-hdr">Signal Reference Guide</div>', unsafe_allow_html=True)
    st.markdown(LEGEND, unsafe_allow_html=True)

    st.markdown(f'<div class="footer">INV = 30w WMA · TRA = 10w SMA · Weak &lt;0.2%/wk · Normal 0.2–0.5%/wk · Strong &gt;0.5%/wk · Extended = 20%+ above MA<br>Data: Yahoo Finance · Weekly candles · Refreshes hourly · {now}</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
