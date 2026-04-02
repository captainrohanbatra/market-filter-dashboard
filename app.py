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
.block-container { padding: 2rem 2.5rem !important; max-width: 1600px !important; }

.db-title {
    font-size: 28px; font-weight: 700; color: #111827;
    letter-spacing: -0.5px; margin-bottom: 3px;
}
.db-sub {
    font-size: 13px; color: #6b7280; margin-bottom: 28px;
    font-family: 'JetBrains Mono', monospace;
}

.sum-card {
    background: #ffffff; border: 1px solid #e5e7eb;
    border-radius: 12px; padding: 16px 20px; text-align: center;
    box-shadow: 0 1px 3px rgba(0,0,0,0.05);
}
.sum-label { font-size: 11px; color: #9ca3af; text-transform: uppercase; letter-spacing: 0.8px; font-weight: 600; }
.sum-val { font-size: 32px; font-weight: 700; margin-top: 4px; }

.section-hdr {
    font-size: 11px; color: #9ca3af; text-transform: uppercase;
    letter-spacing: 1.5px; font-weight: 700;
    padding: 20px 0 12px; border-bottom: 1px solid #e5e7eb; margin-bottom: 16px;
}

.card {
    background: #ffffff; border: 1px solid #e5e7eb;
    border-radius: 14px; padding: 16px 18px 14px 20px;
    box-shadow: 0 1px 4px rgba(0,0,0,0.06);
    margin-bottom: 4px; position: relative; overflow: hidden;
}
.card-bar {
    position: absolute; top: 0; left: 0;
    width: 4px; height: 100%;
}
.card-name { font-size: 15px; font-weight: 700; color: #111827; margin-bottom: 1px; }
.card-ticker { font-size: 11px; color: #9ca3af; font-family: 'JetBrains Mono', monospace; margin-bottom: 10px; }
.card-note { font-size: 11px; color: #d1d5db; margin-top: -8px; margin-bottom: 8px; }
.card-price { font-size: 22px; font-weight: 700; color: #111827; font-family: 'JetBrains Mono', monospace; margin-bottom: 2px; }
.chg-up { font-size: 13px; color: #059669; font-weight: 500; margin-bottom: 12px; }
.chg-dn { font-size: 13px; color: #dc2626; font-weight: 500; margin-bottom: 12px; }

.badges { display: flex; gap: 6px; flex-wrap: wrap; align-items: center; margin-bottom: 10px; }
.lbl { font-size: 10px; color: #9ca3af; font-weight: 600; letter-spacing: 0.5px; }

.b { display: inline-block; padding: 4px 10px; border-radius: 6px; font-size: 12px; font-weight: 700; letter-spacing: 0.3px; }
.b-on      { background: #dcfce7; color: #15803d; border: 1px solid #bbf7d0; }
.b-off     { background: #fee2e2; color: #b91c1c; border: 1px solid #fecaca; }
.b-top     { background: #fef3c7; color: #b45309; border: 1px solid #fde68a; }
.b-bas     { background: #ede9fe; color: #6d28d9; border: 1px solid #ddd6fe; }

.b-stage   { background: #f3f4f6; color: #374151; border: 1px solid #e5e7eb; font-size: 11px; padding: 4px 8px; }
.b-weak    { background: #f9fafb; color: #9ca3af; border: 1px solid #f3f4f6; font-size: 11px; }
.b-normal  { background: #eff6ff; color: #1d4ed8; border: 1px solid #bfdbfe; font-size: 11px; }
.b-strong  { background: #f0fdf4; color: #15803d; border: 1px solid #bbf7d0; font-size: 11px; }
.b-ext     { background: #fff7ed; color: #c2410c; border: 1px solid #fed7aa; font-size: 11px; }
.b-inv     { background: #faf5ff; color: #7e22ce; border: 1px solid #e9d5ff; font-size: 10px; padding: 3px 7px; }
.b-lev     { background: #eff6ff; color: #1d4ed8; border: 1px solid #bfdbfe; font-size: 10px; padding: 3px 7px; }

.vs-ma { font-size: 12px; color: #9ca3af; font-family: 'JetBrains Mono', monospace; margin-top: 6px; }
.err-msg { font-size: 12px; color: #dc2626; margin-top: 8px; }

.legend {
    display: flex; gap: 20px; flex-wrap: wrap;
    margin: 12px 0 4px; font-size: 12px; color: #6b7280;
}
.leg-item { display: flex; align-items: center; gap: 6px; }
.leg-dot { width: 8px; height: 8px; border-radius: 50%; display: inline-block; }

.footer { font-size: 11px; color: #d1d5db; text-align: right; margin-top: 24px; font-family: 'JetBrains Mono', monospace; }

div[data-testid="column"] { padding: 0 5px !important; }
</style>
""", unsafe_allow_html=True)

# ── Asset definitions ──────────────────────────────────────────────
GLOBAL_ASSETS = [
    ("NSE Nifty 500", "^CRSLDX",   "INR", False, False, "India market filter"),
    ("S&P 500",       "^GSPC",     "USD", False, False, ""),
    ("NASDAQ 100",    "^NDX",      "USD", False, False, ""),
    ("Nikkei 225",    "^N225",     "JPY", False, False, ""),
    ("Hang Seng",     "^HSI",      "HKD", False, False, ""),
    ("CSI 300",       "000300.SS", "CNY", False, False, "Mainland China"),
    ("DFM Dubai",     "^DFMGI",   "AED", False, False, "Dubai Financial Market"),
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

INV_PERIOD = 30
TRA_PERIOD = 10
SLOPE_WEAK   = 0.20
SLOPE_NORMAL = 0.50
EXTENDED_PCT = 20.0

# ── Maths ──────────────────────────────────────────────────────────
def wma(series, period):
    w = np.arange(1, period + 1, dtype=float)
    return series.rolling(period).apply(lambda x: np.dot(x, w) / w.sum(), raw=True)

def stage(price, ma30, slope):
    a, r = price > ma30, slope > 0
    if a and r:  return 2
    if a and not r: return 3
    if not a and r: return 1
    return 4

def inv_label(s): return {2:"ON", 3:"TOPPING", 1:"BASING", 4:"OFF"}[s]

def tra_label(price, ma10, slope10):
    a, r = price > ma10, slope10 > 0
    if a and r:  return "ON"
    if a and not r: return "TOPPING"
    if not a and r: return "BASING"
    return "OFF"

def trend(slope_val, pct):
    if pct >= EXTENDED_PCT: return "EXTENDED"
    s = abs(slope_val)
    if s < SLOPE_WEAK:   return "WEAK"
    if s < SLOPE_NORMAL: return "NORMAL"
    return "STRONG"

def fmt_price(p):
    if p >= 10000: return f"{p:,.0f}"
    if p >= 100:   return f"{p:,.1f}"
    if p >= 1:     return f"{p:,.2f}"
    return f"{p:.4f}"

def accent(inv):
    return {"ON":"#16a34a","OFF":"#dc2626","TOPPING":"#d97706","BASING":"#7c3aed"}.get(inv,"#9ca3af")

def b_cls(status):
    return {"ON":"b-on","OFF":"b-off","TOPPING":"b-top","BASING":"b-bas"}.get(status,"b-stage")

def t_cls(t):
    return {"WEAK":"b-weak","NORMAL":"b-normal","STRONG":"b-strong","EXTENDED":"b-ext"}.get(t,"b-weak")

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
        gc  = yf.download("GC=F",     period="130wk", interval="1wk", progress=False, auto_adjust=True)['Close'].squeeze().dropna()
        fx  = yf.download("USDINR=X", period="130wk", interval="1wk", progress=False, auto_adjust=True)['Close'].squeeze().dropna()
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
        st_  = stage(p, m30, s30)
        return dict(price=p, ma30=m30, ma10=m10, slope30=s30, slope10=s10,
                    pct=pct, wchg=wchg, stage=st_,
                    inv=inv_label(st_), tra=tra_label(p,m10,s10),
                    trend=trend(s30,pct), date=close.index[-1].strftime("%d %b %Y"), error=None)
    except Exception as e:
        return dict(error=str(e))

# ── Card renderer ──────────────────────────────────────────────────
def card(name, ticker, currency, is_inv, is_lev, note, d):
    if d is None or d.get("error"):
        err = (d.get("error","") if d else "No data")[:50]
        html = f"""<div class="card">
<div class="card-bar" style="background:#e5e7eb"></div>
<div class="card-name">{name}</div>
<div class="card-ticker">{ticker} &middot; {currency}</div>
<div class="err-msg">&#9888; {err}</div>
</div>"""
        st.markdown(html, unsafe_allow_html=True)
        return

    price_s = fmt_price(d['price'])
    chg_cls = "chg-up" if d['wchg'] >= 0 else "chg-dn"
    chg_arr = "&#9650;" if d['wchg'] >= 0 else "&#9660;"
    chg_s   = f"{chg_arr} {abs(d['wchg']):.1f}% wk"
    ma_arr  = "&#8593;" if d['slope30'] > 0 else "&#8595;"
    pct_s   = f"{'+' if d['pct']>=0 else ''}{d['pct']:.1f}%"
    ac      = accent(d['inv'])

    flags = ""
    if is_inv: flags += ' <span class="b b-inv">INVERSE</span>'
    if is_lev: flags += ' <span class="b b-lev">LEVERAGED</span>'

    note_h = f'<div class="card-note">{note}</div>' if note else ''

    inv_c = b_cls(d['inv'])
    tra_c = b_cls(d['tra'])
    tr_c  = t_cls(d['trend'])

    html = f"""<div class="card">
<div class="card-bar" style="background:{ac}"></div>
<div class="card-name">{name}{flags}</div>
<div class="card-ticker">{ticker} &middot; {currency}</div>
{note_h}
<div class="card-price">{price_s}</div>
<div class="{chg_cls}">{chg_s}</div>
<div class="badges">
<span class="lbl">INV</span><span class="b {inv_c}">{d['inv']}</span>
<span class="lbl">TRA</span><span class="b {tra_c}">{d['tra']}</span>
<span class="b b-stage">S{d['stage']}</span>
<span class="b {tr_c}">{d['trend']}</span>
</div>
<div class="vs-ma">{pct_s} vs 30wMA {ma_arr} &middot; {d['date']}</div>
</div>"""
    st.markdown(html, unsafe_allow_html=True)

# ── Main ───────────────────────────────────────────────────────────
def main():
    now = datetime.now().strftime("%A %d %b %Y &middot; %H:%M")

    st.markdown(f'<div class="db-title">Global Market Filter</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="db-sub">Weinstein Stage Analysis &middot; INV (30w WMA) &middot; TRA (10w SMA) &middot; {now}</div>', unsafe_allow_html=True)

    with st.spinner("Fetching live market data..."):
        results = {}
        for name, ticker, cur, ii, il, note in GLOBAL_ASSETS:
            if ticker == "MCX_GOLD":
                c = fetch_mcx()
            else:
                c = fetch(ticker)
            results[ticker] = analyze(c) if c is not None else dict(error="Data unavailable")

        for name, ticker, cur, ii, il, note in ETF_ASSETS:
            if ticker not in results:
                c = fetch(ticker)
                results[ticker] = analyze(c) if c is not None else dict(error="Data unavailable")

    gd = [results.get("MCX_GOLD" if t=="MCX_GOLD" else t, {}) for _,t,*_ in GLOBAL_ASSETS]
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

    st.markdown("""<div class="legend">
<div class="leg-item"><div class="leg-dot" style="background:#16a34a"></div> ON &mdash; Stage 2 (above rising MA)</div>
<div class="leg-item"><div class="leg-dot" style="background:#d97706"></div> TOPPING &mdash; Stage 3 (above flat/falling MA)</div>
<div class="leg-item"><div class="leg-dot" style="background:#7c3aed"></div> BASING &mdash; Stage 1 (below rising MA)</div>
<div class="leg-item"><div class="leg-dot" style="background:#dc2626"></div> OFF &mdash; Stage 4 (below falling MA)</div>
<div class="leg-item"><div class="leg-dot" style="background:#c2410c"></div> EXTENDED &mdash; 20%+ above 30wMA</div>
</div>""", unsafe_allow_html=True)

    st.markdown('<div class="section-hdr">Global Indices &amp; Assets</div>', unsafe_allow_html=True)
    cols = st.columns(4)
    for i, (name, ticker, cur, ii, il, note) in enumerate(GLOBAL_ASSETS):
        t = ticker
        with cols[i % 4]:
            card(name, ticker, cur, ii, il, note, results.get(t))

    st.markdown('<div class="section-hdr">Tradeable ETFs &middot; IBKR</div>', unsafe_allow_html=True)
    cols2 = st.columns(4)
    for i, (name, ticker, cur, ii, il, note) in enumerate(ETF_ASSETS):
        with cols2[i % 4]:
            card(name, ticker, cur, ii, il, note, results.get(ticker))

    st.markdown(f"""<div class="footer">
INV = 30w Weighted MA &middot; TRA = 10w Simple MA &middot; Slope: Weak &lt;0.2%/wk &middot; Normal 0.2&ndash;0.5%/wk &middot; Strong &gt;0.5%/wk &middot; Data: Yahoo Finance &middot; Refreshes hourly
</div>""", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
