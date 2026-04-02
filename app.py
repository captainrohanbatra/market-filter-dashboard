import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# ─────────────────────────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Global Market Filter",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ─────────────────────────────────────────────────────────────────
# CUSTOM CSS
# ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=DM+Sans:wght@300;400;500;600&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

.main { background-color: #0a0e1a; }
.block-container { padding: 1.5rem 2rem; max-width: 1400px; }

.dashboard-title {
    font-size: 24px; font-weight: 600; color: #f0f4ff;
    letter-spacing: -0.3px; margin-bottom: 2px;
}
.dashboard-sub {
    font-size: 12px; color: #4a5a7a; margin-bottom: 24px;
    font-family: 'DM Mono', monospace;
}

.summary-metric {
    background: #111827; border: 0.5px solid #1e2d45;
    border-radius: 10px; padding: 14px 18px; text-align: center;
}
.summary-metric .label {
    font-size: 10px; color: #4a5a7a; text-transform: uppercase;
    letter-spacing: 0.8px; margin-bottom: 4px;
}
.summary-metric .value {
    font-size: 28px; font-weight: 600;
}

.section-header {
    font-size: 10px; color: #3d5a80; text-transform: uppercase;
    letter-spacing: 1.5px; font-weight: 600;
    padding: 16px 0 10px; border-bottom: 0.5px solid #1e2d45;
    margin-bottom: 12px;
}

.asset-card {
    background: #111827; border: 0.5px solid #1e2d45;
    border-radius: 12px; padding: 14px 16px 12px;
    position: relative; overflow: hidden; height: 100%;
    transition: border-color 0.2s;
}
.asset-card:hover { border-color: #2d4a6a; }

.card-accent {
    position: absolute; top: 0; left: 0;
    width: 3px; height: 100%; border-radius: 4px 0 0 4px;
}

.card-inner { padding-left: 10px; }

.card-name {
    font-size: 13px; font-weight: 600; color: #e0e6f0;
    margin-bottom: 1px;
}
.card-ticker {
    font-size: 10px; color: #3d5a80;
    font-family: 'DM Mono', monospace; margin-bottom: 8px;
}
.card-price {
    font-size: 16px; font-weight: 600; color: #f0f4ff;
    font-family: 'DM Mono', monospace; margin-bottom: 2px;
}
.card-chg-pos { font-size: 11px; color: #10b981; margin-bottom: 10px; }
.card-chg-neg { font-size: 11px; color: #ef4444; margin-bottom: 10px; }

.pills-row { display: flex; gap: 5px; flex-wrap: wrap; align-items: center; margin-bottom: 8px; }

.pill {
    font-size: 10px; font-weight: 600; padding: 2px 8px;
    border-radius: 20px; letter-spacing: 0.3px; display: inline-block;
}
.pill-label {
    font-size: 9px; color: #3d5a80; margin-right: 1px;
    font-family: 'DM Mono', monospace;
}

.pill-on      { background: #064e3b; color: #34d399; border: 0.5px solid #065f4620; }
.pill-off     { background: #450a0a; color: #f87171; border: 0.5px solid #7f1d1d20; }
.pill-topping { background: #451a03; color: #fbbf24; border: 0.5px solid #78350f20; }
.pill-basing  { background: #2e1065; color: #a78bfa; border: 0.5px solid #4c1d9520; }

.pill-stage {
    background: #1e2d45; color: #6b8ab0; border: 0.5px solid #2d4060;
    font-size: 9px; padding: 2px 6px; border-radius: 4px;
}
.pill-weak    { background: #1e2d45; color: #4a6a8a; }
.pill-normal  { background: #1a3040; color: #38bdf8; }
.pill-strong  { background: #1a2e20; color: #4ade80; }
.pill-extended { background: #2d1a00; color: #fb923c; }
.pill-inverse  { background: #2d1040; color: #c084fc; font-size: 9px; }

.vs-ma {
    font-size: 10px; color: #3d5a80;
    font-family: 'DM Mono', monospace; margin-top: 4px;
}

.flag-inverse {
    font-size: 9px; background: #2d1040; color: #c084fc;
    padding: 1px 6px; border-radius: 3px; margin-left: 4px;
}
.flag-leveraged {
    font-size: 9px; background: #1a2a10; color: #86efac;
    padding: 1px 6px; border-radius: 3px; margin-left: 4px;
}

.timestamp {
    font-size: 11px; color: #2d4060;
    font-family: 'DM Mono', monospace;
    text-align: right; margin-top: 20px;
}

.legend-row {
    display: flex; gap: 16px; flex-wrap: wrap;
    margin: 16px 0 8px; font-size: 11px; color: #3d5a80;
}
.legend-item { display: flex; align-items: center; gap: 5px; }
.legend-dot {
    width: 8px; height: 8px; border-radius: 50%; display: inline-block;
}

div[data-testid="stHorizontalBlock"] > div { padding: 0 4px; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────
# ASSET DEFINITIONS
# ─────────────────────────────────────────────────────────────────
GLOBAL_ASSETS = [
    ("NSE Nifty 500", "^CRSLDX",  "INR",  False, False, "India market filter"),
    ("S&P 500",       "^GSPC",    "USD",  False, False, ""),
    ("NASDAQ 100",    "^NDX",     "USD",  False, False, ""),
    ("Nikkei 225",    "^N225",    "JPY",  False, False, ""),
    ("Hang Seng",     "^HSI",     "HKD",  False, False, ""),
    ("CSI 300",       "000300.SS","CNY",  False, False, "Mainland China"),
    ("DFM Dubai",     "^DFMGI",   "AED",  False, False, "Dubai Financial Market"),
    ("Gold (USD)",    "GC=F",     "USD",  False, False, ""),
    ("Gold (MCX)",    "MCX_GOLD", "INR",  False, False, "GC=F × USDINR"),
    ("Oil WTI",       "CL=F",     "USD",  False, False, ""),
    ("USD / INR",     "USDINR=X", "INR",  False, False, "S2 = rupee weakening"),
    ("Bitcoin",       "BTC-USD",  "USD",  False, False, ""),
]

ETF_ASSETS = [
    ("SPY",   "SPY",  "USD", False, False, "S&P 500"),
    ("QQQ",   "QQQ",  "USD", False, False, "NASDAQ 100"),
    ("TQQQ",  "TQQQ", "USD", False, True,  "3x Long NASDAQ"),
    ("SQQQ",  "SQQQ", "USD", True,  True,  "3x Inverse NASDAQ"),
    ("XLE",   "XLE",  "USD", False, False, "Energy"),
    ("XLF",   "XLF",  "USD", False, False, "Financials"),
    ("XLK",   "XLK",  "USD", False, False, "Technology"),
    ("XLV",   "XLV",  "USD", False, False, "Healthcare"),
    ("XLI",   "XLI",  "USD", False, False, "Industrials"),
    ("XLB",   "XLB",  "USD", False, False, "Materials"),
    ("XLP",   "XLP",  "USD", False, False, "Consumer Staples"),
    ("GLD",   "GLD",  "USD", False, False, "Gold ETF"),
    ("USO",   "USO",  "USD", False, False, "Oil ETF"),
    ("UNG",   "UNG",  "USD", False, False, "Natural Gas"),
    ("PDBC",  "PDBC", "USD", False, False, "Diversified Commodities"),
    ("TLT",   "TLT",  "USD", False, False, "Long-Duration Bonds"),
    ("TBT",   "TBT",  "USD", True,  True,  "2x Inverse Long Bonds"),
]

INV_PERIOD = 30
TRA_PERIOD = 10

# Slope thresholds (weekly % change of 30wMA)
SLOPE_WEAK     = 0.20
SLOPE_NORMAL   = 0.50
EXTENDED_PCT   = 20.0  # % above 30wMA

# ─────────────────────────────────────────────────────────────────
# INDICATOR FUNCTIONS
# ─────────────────────────────────────────────────────────────────

def weighted_ma(series, period):
    weights = np.arange(1, period + 1, dtype=float)
    return series.rolling(period).apply(
        lambda x: np.dot(x, weights) / weights.sum(), raw=True
    )

def get_stage(price, ma30, slope_pct):
    above  = price > ma30
    rising = slope_pct > 0
    if above and rising:     return 2
    if above and not rising: return 3
    if not above and rising: return 1
    return 4

def get_inv_status(stage):
    return {2: "ON", 3: "TOPPING", 1: "BASING", 4: "OFF"}[stage]

def get_tra_status(price, ma10, slope10):
    above  = price > ma10
    rising = slope10 > 0
    if above and rising:     return "ON"
    if above and not rising: return "TOPPING"
    if not above and rising: return "BASING"
    return "OFF"

def get_trend_strength(slope_pct_val, pct_vs_ma30):
    if pct_vs_ma30 >= EXTENDED_PCT:
        return "EXTENDED"
    abs_slope = abs(slope_pct_val)
    if abs_slope < SLOPE_WEAK:   return "WEAK"
    if abs_slope < SLOPE_NORMAL: return "NORMAL"
    return "STRONG"

def pill_class(status):
    return {
        "ON": "pill-on", "OFF": "pill-off",
        "TOPPING": "pill-topping", "BASING": "pill-basing"
    }.get(status, "pill-stage")

def trend_class(strength):
    return {
        "WEAK": "pill-weak", "NORMAL": "pill-normal",
        "STRONG": "pill-strong", "EXTENDED": "pill-extended"
    }.get(strength, "pill-weak")

def accent_color(inv_status):
    return {
        "ON": "#10b981", "OFF": "#ef4444",
        "TOPPING": "#f59e0b", "BASING": "#8b5cf6"
    }.get(inv_status, "#2d4060")

def format_price(price, ticker):
    if price >= 10000: return f"{price:,.0f}"
    if price >= 100:   return f"{price:,.1f}"
    if price >= 1:     return f"{price:,.2f}"
    return f"{price:.4f}"

# ─────────────────────────────────────────────────────────────────
# DATA FETCH
# ─────────────────────────────────────────────────────────────────

@st.cache_data(ttl=3600)  # cache 1 hour
def fetch_asset(ticker):
    try:
        df = yf.download(ticker, period="130wk", interval="1wk",
                         progress=False, auto_adjust=True)
        if df.empty or len(df) < INV_PERIOD + 5:
            return None
        close = df['Close'].squeeze().dropna()
        return close
    except:
        return None

@st.cache_data(ttl=3600)
def fetch_mcx_gold():
    """MCX Gold = USD Gold × USDINR"""
    try:
        gc  = yf.download("GC=F",     period="130wk", interval="1wk",
                          progress=False, auto_adjust=True)['Close'].squeeze().dropna()
        usd = yf.download("USDINR=X", period="130wk", interval="1wk",
                          progress=False, auto_adjust=True)['Close'].squeeze().dropna()
        combined = gc.reindex(usd.index, method='ffill') * usd
        return combined.dropna()
    except:
        return None

def analyze(close, name=""):
    try:
        wma30 = weighted_ma(close, INV_PERIOD)
        sma10 = close.rolling(TRA_PERIOD).mean()

        price     = float(close.iloc[-1])
        ma30_val  = float(wma30.iloc[-1])
        ma10_val  = float(sma10.iloc[-1])

        # Slopes as weekly % change
        slope30 = float((wma30.iloc[-1] - wma30.iloc[-2]) / wma30.iloc[-2] * 100) if len(wma30.dropna()) >= 2 else 0.0
        slope10 = float((sma10.iloc[-1] - sma10.iloc[-2]) / sma10.iloc[-2] * 100) if len(sma10.dropna()) >= 2 else 0.0

        pct_vs_ma30 = (price - ma30_val) / ma30_val * 100
        pct_vs_ma10 = (price - ma10_val) / ma10_val * 100

        weekly_chg = float((close.iloc[-1] - close.iloc[-2]) / close.iloc[-2] * 100) if len(close) >= 2 else 0.0

        stage       = get_stage(price, ma30_val, slope30)
        inv_status  = get_inv_status(stage)
        tra_status  = get_tra_status(price, ma10_val, slope10)
        trend_str   = get_trend_strength(slope30, pct_vs_ma30)

        return {
            "price": price, "ma30": ma30_val, "ma10": ma10_val,
            "slope30": slope30, "slope10": slope10,
            "pct_vs_ma30": pct_vs_ma30, "pct_vs_ma10": pct_vs_ma10,
            "weekly_chg": weekly_chg, "stage": stage,
            "inv_status": inv_status, "tra_status": tra_status,
            "trend_strength": trend_str,
            "last_date": close.index[-1].strftime("%d %b %Y"),
            "error": None
        }
    except Exception as e:
        return {"error": str(e)}

# ─────────────────────────────────────────────────────────────────
# CARD RENDERER
# ─────────────────────────────────────────────────────────────────

def render_card(name, ticker, currency, is_inverse, is_leveraged, note, data):
    if data is None or data.get("error"):
        err = data.get("error", "No data") if data else "No data"
        st.markdown(f"""
        <div class="asset-card">
            <div class="card-accent" style="background:#2d4060"></div>
            <div class="card-inner">
                <div class="card-name">{name}</div>
                <div class="card-ticker">{ticker}</div>
                <div style="font-size:11px;color:#ef4444;margin-top:8px">⚠ {err[:60]}</div>
            </div>
        </div>""", unsafe_allow_html=True)
        return

    d = data
    price_str  = format_price(d['price'], ticker)
    chg_class  = "card-chg-pos" if d['weekly_chg'] >= 0 else "card-chg-neg"
    chg_arrow  = "▲" if d['weekly_chg'] >= 0 else "▼"
    chg_str    = f"{chg_arrow} {abs(d['weekly_chg']):.1f}% wk"
    ma_arrow   = "↑" if d['slope30'] > 0 else "↓"
    pct_sign   = "+" if d['pct_vs_ma30'] >= 0 else ""
    accent     = accent_color(d['inv_status'])

    inv_cls    = pill_class(d['inv_status'])
    tra_cls    = pill_class(d['tra_status'])
    trend_cls  = trend_class(d['trend_strength'])

    flags = ""
    if is_inverse:   flags += '<span class="pill pill-inverse">INVERSE</span>'
    if is_leveraged: flags += '<span class="pill pill-inverse" style="background:#1a2840;color:#60a5fa">LEVERAGED</span>'

    note_html = f'<div class="card-ticker" style="margin-top:2px">{note}</div>' if note else ""

    st.markdown(f"""
    <div class="asset-card">
        <div class="card-accent" style="background:{accent}"></div>
        <div class="card-inner">
            <div class="card-name">{name} {flags}</div>
            <div class="card-ticker">{ticker} · {currency}</div>
            {note_html}
            <div class="card-price">{price_str}</div>
            <div class="{chg_class}">{chg_str}</div>
            <div class="pills-row">
                <span class="pill-label">INV</span>
                <span class="pill {inv_cls}">{d['inv_status']}</span>
                <span class="pill-label" style="margin-left:4px">TRA</span>
                <span class="pill {tra_cls}">{d['tra_status']}</span>
                <span class="pill pill-stage">S{d['stage']}</span>
                <span class="pill {trend_cls}">{d['trend_strength']}</span>
            </div>
            <div class="vs-ma">{pct_sign}{d['pct_vs_ma30']:.1f}% vs 30wMA {ma_arrow} · {d['last_date']}</div>
        </div>
    </div>""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────
# MAIN APP
# ─────────────────────────────────────────────────────────────────

def main():
    now = datetime.now().strftime("%A %d %b %Y · %H:%M")

    st.markdown(f"""
    <div class="dashboard-title">Global Market Filter</div>
    <div class="dashboard-sub">
        Weinstein Stage Analysis · INV (30w WMA) · TRA (10w SMA) · {now}
    </div>""", unsafe_allow_html=True)

    # ── Fetch all data ──────────────────────────────────────────
    with st.spinner("Fetching market data..."):
        all_results = {}

        for name, ticker, currency, is_inv, is_lev, note in GLOBAL_ASSETS:
            if ticker == "MCX_GOLD":
                close = fetch_mcx_gold()
            else:
                close = fetch_asset(ticker)
            all_results[ticker] = analyze(close, name) if close is not None else {"error": "Data unavailable"}

        for name, ticker, currency, is_inv, is_lev, note in ETF_ASSETS:
            if ticker not in all_results:
                close = fetch_asset(ticker)
                all_results[ticker] = analyze(close, name) if close is not None else {"error": "Data unavailable"}

    # ── Summary metrics ─────────────────────────────────────────
    global_data = [all_results.get(t, {}) for _, t, *_ in GLOBAL_ASSETS]
    inv_on      = sum(1 for d in global_data if d.get("inv_status") == "ON")
    inv_off     = sum(1 for d in global_data if d.get("inv_status") == "OFF")
    inv_top     = sum(1 for d in global_data if d.get("inv_status") == "TOPPING")
    inv_bas     = sum(1 for d in global_data if d.get("inv_status") == "BASING")
    tra_on      = sum(1 for d in global_data if d.get("tra_status") == "ON")

    c1, c2, c3, c4, c5 = st.columns(5)
    for col, label, val, color in [
        (c1, "INV On",    inv_on,  "#10b981"),
        (c2, "INV Off",   inv_off, "#ef4444"),
        (c3, "Topping",   inv_top, "#f59e0b"),
        (c4, "Basing",    inv_bas, "#8b5cf6"),
        (c5, "TRA On",    tra_on,  "#38bdf8"),
    ]:
        col.markdown(f"""
        <div class="summary-metric">
            <div class="label">{label}</div>
            <div class="value" style="color:{color}">{val}</div>
        </div>""", unsafe_allow_html=True)

    # ── Legend ──────────────────────────────────────────────────
    st.markdown("""
    <div class="legend-row">
        <div class="legend-item"><div class="legend-dot" style="background:#10b981"></div> ON — Stage 2 (above rising MA)</div>
        <div class="legend-item"><div class="legend-dot" style="background:#f59e0b"></div> TOPPING — Stage 3 (above flat/falling MA)</div>
        <div class="legend-item"><div class="legend-dot" style="background:#8b5cf6"></div> BASING — Stage 1 (below rising MA)</div>
        <div class="legend-item"><div class="legend-dot" style="background:#ef4444"></div> OFF — Stage 4 (below falling MA)</div>
        <div class="legend-item"><div class="legend-dot" style="background:#fb923c"></div> EXTENDED — 20%+ above 30wMA</div>
    </div>
    """, unsafe_allow_html=True)

    # ── Section 1: Global Indices & Assets ──────────────────────
    st.markdown('<div class="section-header">Global Indices & Assets</div>', unsafe_allow_html=True)

    cols = st.columns(4)
    for i, (name, ticker, currency, is_inv, is_lev, note) in enumerate(GLOBAL_ASSETS):
        with cols[i % 4]:
            t = "MCX_GOLD" if ticker == "MCX_GOLD" else ticker
            render_card(name, ticker, currency, is_inv, is_lev, note, all_results.get(t))

    # ── Section 2: Tradeable ETFs ────────────────────────────────
    st.markdown('<div class="section-header" style="margin-top:24px">Tradeable ETFs · IBKR</div>', unsafe_allow_html=True)

    cols2 = st.columns(4)
    for i, (name, ticker, currency, is_inv, is_lev, note) in enumerate(ETF_ASSETS):
        with cols2[i % 4]:
            render_card(name, ticker, currency, is_inv, is_lev, note, all_results.get(ticker))

    # ── Timestamp ───────────────────────────────────────────────
    st.markdown(f"""
    <div class="timestamp">
        INV = 30w Weighted MA · TRA = 10w Simple MA · Slope bands: Weak &lt;0.2%/wk · Normal 0.2–0.5%/wk · Strong &gt;0.5%/wk
        <br>Data: Yahoo Finance · Weekly candles · Refreshes every hour · {now}
    </div>""", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
