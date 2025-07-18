import streamlit as st
from streamlit_echarts import st_echarts
import pandas as pd
import os
import streamlit.components.v1 as components
from streamlit_echarts import st_echarts

st.set_page_config(page_title="Sentiment Dashboard", layout="wide", page_icon="📈")

# --- Theme Configuration ---
themes = {
    "Cyber Dark": {
        "primaryColor": "#00ffff",
        "backgroundColor": "#0d1117",
        "secondaryBackgroundColor": "#161b22",
        "textColor": "#c9d1d9",
        "font": "'BulletSmallcaps', monospace",  
        "titleFont": "'BulletSmallcaps', monospace" 
    },
    "Matrix": {
        "primaryColor": "#39ff14",
        "backgroundColor": "#000000",
        "secondaryBackgroundColor": "#111111",
        "textColor": "#39ff14",
        "font": "'BulletSmallcaps', monospace",  
        "titleFont": "'BulletSmallcaps', monospace" 
    },
    "Bloomberg": {
        "primaryColor": "#ff6f00",
        "backgroundColor": "#1b1b1b",
        "secondaryBackgroundColor": "#2b2b2b",
        "textColor": "#ffffff",
        "font": "sans serif"
    }
}

with open("styles/fonts.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


# --- Page Setup ---
theme_choice = st.sidebar.selectbox("🎨 Choose Theme", list(themes.keys()))
theme = themes[theme_choice]

# --- Apply Custom Theme Styling ---
st.markdown(
    f"""
    <style>
        body, .stApp {{
            background-color: {theme['backgroundColor']} !important;
            color: {theme['textColor']} !important;
            font-family: {theme['font']};
        }}
        .stMarkdown, .stDataFrame, .stSubheader {{
            color: {theme['textColor']} !important;
        }}
        .stDownloadButton > button {{
            background-color: {theme['primaryColor']};
            color: black;
        }}
        .neon-box {{
            border: 2px solid {theme['primaryColor']};
            padding: 1.5rem;
            border-radius: 12px;
            box-shadow: 0 0 12px {theme['primaryColor']};
            margin-bottom: 1.5rem;
        }}
        .neon-title {{
            color: {theme['primaryColor']};
            font-family: {theme.get('titleFont', theme['font'])};
            font-weight: bold;
            font-size: 2.2rem;
            letter-spacing: 0.5px;
            margin-bottom: 1rem;
        }}

        table {{
            width: 100%;
            border-collapse: collapse;
        }}
        th, td {{
            padding: 0.5rem;
            border: 1px solid {theme['secondaryBackgroundColor']};
        }}
        ul {{
            margin-left: 1.5rem;
        }}
    </style>
    """,
    unsafe_allow_html=True
)

# --- Sidebar ---
st.sidebar.title("📁 Download")
ticker = st.sidebar.selectbox("Select Ticker", ["AAPL"])
csv_path = f"outputs/results/{ticker.lower()}_pipeline_output.csv"

if not os.path.exists(csv_path):
    st.sidebar.error("Sentiment data not found. Please run the pipeline.")
    st.stop()

df = pd.read_csv(csv_path)
df["sentiment"] = df["sentiment"].str.title()

st.sidebar.download_button(
    label="⬇️ Download Sentiment CSV",
    data=df.to_csv(index=False),
    file_name=f"{ticker.lower()}_sentiment_scores.csv",
    mime="text/csv"
)

st.markdown(
    "<p style='font-family: BulletSmallcaps; font-size: 28px;'>✅ This is a BulletSmallcaps test. If this looks custom, the font works.</p>",
    unsafe_allow_html=True
)


# --- Header ---
st.markdown(f"<h1 class='neon-title' style='color:{theme['primaryColor']}; font-size: 2.2rem;'>📘 {ticker} Stock Sentiment Analyzer</h1>", unsafe_allow_html=True)
st.markdown(
    """
    This dashboard uses **Google News headlines** and the **FinBERT model** to analyze investor sentiment.  
    It’s designed to scale — future phases will support price forecasting, portfolio decisions, and a full AI brain.
    """
)
st.markdown("---")

# --- Vision Section (Elite Layout) ---
# --- Vision & Phases Section (Elite + Native Version) ---
st.markdown("## 🧠 Vision & Phases: The Global Financial AI Command Center")

st.markdown(f"""
<div style="background-color: {theme['secondaryBackgroundColor']}; padding: 1.5rem; border-radius: 12px; border-left: 6px solid {theme['primaryColor']}; color: {theme['textColor']}; font-family: {theme['font']};">
    <h3 style="color:{theme['primaryColor']}">📡 Mission</h3>
    <p>Build a <strong>future-proof, AI-driven market intelligence and trading system</strong> capable of scaling to <strong>millions, billions, or trillions</strong> in trades, data, and revenue — with a self-improving decision core.</p>
</div>
""", unsafe_allow_html=True)

# --- Phases Table ---
st.markdown("### 🔭 Phases of Evolution")
phase_df = pd.DataFrame({
    "Phase": [1, 2, 3, 4, 5, 6],
    "Goal": [
        "Real-time sentiment extraction from news",
        "Price correlation and next-day return tracking",
        "Trend prediction using LSTM / XGBoost",
        "Reinforcement Learning for trade actions (DQN, PPO)",
        "Portfolio optimization with Greedy + Genetic Algorithms",
        "Global deployment of a centralized Decision Engine"
    ]
})
st.table(phase_df)

# --- Decision Engine Section: Upgraded Design ---
st.markdown("### 🧠 Decision Engine: AI Stack")
st.markdown("This is the central AI brain composed of tightly integrated AI models and layers, each with a mission-critical role:")

# Decision Engine Graph - ECharts
# Decision Engine Graph - ECharts (Updated for Full AI Stack)
graph_options = {
    "tooltip": {
        "show": True,
        "formatter": "{b}"
    },
    "legend": {
        "data": ["Short-Term", "Medium-Term", "Long-Term", "Meta Core", "Decision Engine"],
        "textStyle": {"color": "#fff"}
    },
    "series": [{
        "type": "graph",
        "layout": "force",
        "roam": True,
        "label": {"show": True, "color": "#ffffff"},
        "force": {
            "repulsion": 300,
            "gravity": 0.2,
            "edgeLength": 120
        },
        "categories": [
            {"name": "Short-Term"},
            {"name": "Medium-Term"},
            {"name": "Long-Term"},
            {"name": "Meta Core"},
            {"name": "Decision Engine"}
        ],
        "data": [
            # Short-Term
            {"name": "FinBERT", "itemStyle": {"color": "#00e5ff"}, "category": 0},
            {"name": "LSTM", "itemStyle": {"color": "#00e5ff"}, "category": 0},
            {"name": "XGBoost", "itemStyle": {"color": "#00e5ff"}, "category": 0},
            {"name": "CatBoost", "itemStyle": {"color": "#00e5ff"}, "category": 0},

            # Medium-Term
            {"name": "Prophet", "itemStyle": {"color": "#ff9100"}, "category": 1},
            {"name": "ARIMA", "itemStyle": {"color": "#ff9100"}, "category": 1},
            {"name": "TimesNet", "itemStyle": {"color": "#ff9100"}, "category": 1},

            # Long-Term
            {"name": "RLlib", "itemStyle": {"color": "#d500f9"}, "category": 2},
            {"name": "Markowitz", "itemStyle": {"color": "#d500f9"}, "category": 2},
            {"name": "HRP", "itemStyle": {"color": "#d500f9"}, "category": 2},

            # Meta Core
            {"name": "Model Ensembler", "itemStyle": {"color": "#ff4081"}, "category": 3},
            {"name": "Bayesian Net", "itemStyle": {"color": "#ff4081"}, "category": 3},
            {"name": "AutoML", "itemStyle": {"color": "#ff4081"}, "category": 3},
            {"name": "LLM Agent", "itemStyle": {"color": "#ff4081"}, "category": 3},

            # Decision Engine (Core)
            {
                "name": "Decision Engine",
                "itemStyle": {"color": "#ffffff"},
                "symbolSize": 60,
                "category": 4,
                "symbol": "circle"
            }
        ],
        "links": [
            {"source": name, "target": "Decision Engine"} for name in [
                "FinBERT", "LSTM", "XGBoost", "CatBoost",
                "Prophet", "ARIMA", "TimesNet",
                "RLlib", "Markowitz", "HRP",
                "Model Ensembler", "Bayesian Net", "AutoML", "LLM Agent"
            ]
        ],
        "lineStyle": {"color": "source"},
        "emphasis": {
            "focus": "adjacency",
            "lineStyle": {"width": 3}
        },
        "draggable": True,
        "focusNodeAdjacency": True
    }]
}



st_echarts(graph_options, height="600px")


# AI Stack Legend (Upgraded to match the new Decision Engine graph)
st.markdown("#### 🧬 Legend: What Each Model Does")

st.markdown("""
**⚪️ Central Node:**  
- `⚪ Decision Engine` — Fusion point of all intelligence; executes trades, updates weights, learns from outcomes  
            
**🩵 Short-Term Alpha Models (Sentiment & Price Prediction):**  
- `🟦 FinBERT` — Financial sentiment classification from news and tweets  
- `🟦 LSTM` — Sequential price movement prediction  
- `🟦 XGBoost` — Price/sentiment regression from structured inputs  
- `🟦 CatBoost` — Handles categorical features like sectors or tickers  

**🟧 Medium-Term Forecast Models (Swing/Position Trading):**  
- `🟨 Prophet` — Detects seasonality and macro patterns  
- `🟨 ARIMA / SARIMA` — Classical time series forecasting  
- `🟨 TimesNet / Informer` — Transformer-based multi-day prediction  

**💜 Long-Term Intelligence Models (Macro Strategy):**  
- `💜 RLlib / DQN / PPO` — Reinforcement Learning for optimal trade decisions  
- `💜 Markowitz Optimizer` — Classical risk-return capital allocation  
- `💜 HRP` — Hierarchical diversification for asset clusters  

**💖 Meta / Decision Core Models (Command Logic):**  
- `💖 Model Ensembler` — Combines signals from all models (stacking/blending)  
- `💖 Bayesian Net` — Probabilistic decision logic with uncertainty quantification  
- `💖 AutoML / TPOT` — Auto-selects the best pipeline per region  
- `💖 LLM Agent (GPT-based)` — Reads charts, reacts to changes, commands strategies  


""")




# --- Sentiment Chart + Legend ---
col1, col2 = st.columns([2, 1])
with col1:
    st.subheader("📊 Sentiment Distribution Chart")
    sentiment_counts = df["sentiment"].value_counts()
    option = {
        "title": {"text": "Headline Sentiment Overview"},
        "tooltip": {},
        "xAxis": {"type": "category", "data": sentiment_counts.index.tolist()},
        "yAxis": {"type": "value"},
        "series": [{
            "data": sentiment_counts.values.tolist(),
            "type": "bar",
            "itemStyle": {"color": theme['primaryColor']},
        }]
    }
    st_echarts(options=option, height="400px")

with col2:
    st.subheader("📌 How to Read FinBERT Scores")
    st.markdown(
        """
        **Score Ranges:**
        - 🟡 0.50 – 0.65: Low confidence  
        - 🟠 0.65 – 0.80: Moderate sentiment  
        - 🟢 0.80 – 1.00: Strong sentiment  
        - 🔴 < 0.50 or > 1.00: Outliers (rare)  

        These scores are softmax based — higher = stronger confidence.
        """
    )

# --- Tabs ---
tab1, tab2, tab3 = st.tabs([
    "🗞 Headlines Table",
    "🚨 Extreme Scores",
    "📈 Sentiment Over Time (Coming Soon)"
])

with tab1:
    st.subheader("🗞 News Headlines and Sentiment")
    st.dataframe(df[["title", "sentiment", "score", "published", "link"]], use_container_width=True)

with tab2:
    st.subheader("🚨 Extremely High or Low Sentiment")
    extremes = df[(df["score"] > 0.95) | (df["score"] < 0.55)]
    if extremes.empty:
        st.success("✅ No extreme sentiment headlines detected.")
    else:
        st.dataframe(extremes[["title", "sentiment", "score", "published", "link"]], use_container_width=True)

with tab3:
    st.subheader("📈 Sentiment Over Time (Coming Soon)")
    st.markdown("This chart will visualize sentiment momentum across multiple trading days.")

# --- Footer ---
st.markdown("---")
st.caption("Built with FinBERT • Streamlit • ECharts • Tailwind UX • Global AI Decision Engine • Theme Switcher Powered")