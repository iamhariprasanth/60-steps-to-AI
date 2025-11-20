import streamlit as st
import pandas as pd
import json
from pathlib import Path
from datetime import date, datetime, timedelta

DATA_FILE = Path(__file__).parents[0] / "data.json"
GOAL_ML = 3000


def ensure_data_file():
    if not DATA_FILE.exists():
        DATA_FILE.write_text(json.dumps({}))


def load_data():
    ensure_data_file()
    with open(DATA_FILE, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return {}


def save_data(d):
    with open(DATA_FILE, "w") as f:
        json.dump(d, f, indent=2)


def add_intake(amount_ml: int, for_date: date):
    d = load_data()
    key = for_date.isoformat()
    d[key] = d.get(key, 0) + int(amount_ml)
    save_data(d)


def get_last_n_days(n=7):
    today = date.today()
    days = [(today - timedelta(days=i)) for i in range(n - 1, -1, -1)]
    return days


def dataframe_for_week():
    d = load_data()
    days = get_last_n_days(7)
    rows = []
    for dt in days:
        rows.append({"date": dt.isoformat(), "ml": int(d.get(dt.isoformat(), 0))})
    df = pd.DataFrame(rows)
    df["date_display"] = pd.to_datetime(df["date"]).dt.date
    return df


def main():
    st.set_page_config(page_title="Water Intake Tracker", layout="centered")
    st.title("💧 Water Intake Tracker")

    # ----- Custom color theme (applies across the app) -----
    custom_css = """
    <style>
    :root{
        --bg1: #f5f7ff;
        --bg2: #e9f7ff;
        --card: transparent;
        --primary: #6C5CE7;
        --accent1: #00b894;
        --accent2: #0984e3;
        --accent3: #fdcb6e;
        --muted: #6b6b6b;
    }
    /* Broad selectors for app background (covers variations across Streamlit versions) */
    div[data-testid="stAppViewContainer"], .stApp, main, body {
        background: linear-gradient(135deg, var(--bg1) 0%, var(--bg2) 100%) !important;
    }
    /* Card-like containers - transparent background */
    .css-1outpf7, .element-container, .stContainer, [data-testid="stMetricContainer"] {
        background: transparent !important;
    }
    
    /* Remove white bg from charts and plotly containers */
    .plotly-graph-div { background: transparent !important; }
    div[data-testid="stPlotlyChart"] { background: transparent !important; }
    .stPlotlyChart { background: transparent !important; }
    svg { background: transparent !important; }
    
    /* Text and input backgrounds */
    .stText, .stMarkdown, p, span { background: transparent !important; }
    .stNumberInput, .stDateInput, input { background: rgba(255,255,255,0.1) !important; }

    /* Buttons: apply to native buttons and Streamlit button wrappers */
    button, .stButton>button, .stDownloadButton>button, div.stButton>button {
        background: linear-gradient(90deg, var(--primary), var(--accent2)) !important;
        color: #ffffff !important;
        border: none !important;
        box-shadow: 0 4px 12px rgba(108,92,231,0.15) !important;
    }

    /* Headings and titles */
    h1, h2, h3, .stTitle, .css-1v0mbdj, .css-10trblm { 
        color: var(--primary) !important;
        background: transparent !important;
    }

    /* Metric and numeric values */
    [data-testid="metric-container"] span, .stMetricValue, [data-testid="stMetricValue"] {
        color: var(--accent1) !important;
    }

    /* Progress bar */
    div[role="progressbar"] > div, .stProgress>div>div {
        background: linear-gradient(90deg, var(--accent1), var(--primary)) !important;
    }

    /* Muted text */
    .css-1d391kg, .muted, .stText { color: var(--muted) !important; }

    </style>
    """
    st.markdown(custom_css, unsafe_allow_html=True)

    st.markdown("Log daily water intake (ml). Goal: **3,000 ml** per day.")

    # Input area
    with st.form("log_form"):
        col1, col2 = st.columns([2, 1])
        with col1:
            amount = st.number_input("Amount (ml)", min_value=1, value=250, step=50)
        with col2:
            chosen_date = st.date_input("Date", value=date.today())
        submitted = st.form_submit_button("Add Intake")

    if submitted:
        add_intake(amount, chosen_date)
        st.success(f"Added {amount} ml for {chosen_date.isoformat()}")

    # Display today's progress
    data = load_data()
    today_key = date.today().isoformat()
    today_total = int(data.get(today_key, 0))

    st.header("Today's Progress")
    st.metric("Total (ml)", f"{today_total} ml")
    pct = min(today_total / GOAL_ML, 1.0)
    st.progress(pct)
    remaining = max(GOAL_ML - today_total, 0)
    st.write(f"Goal: {GOAL_ML} ml — Remaining: {remaining} ml")

    # Funny mouth character if intake is too low
    if today_total < 10:
        mouth_html = """
        <div style="text-align: center; margin: 20px 0; animation: bounce 1s infinite;">
            <div style="font-size: 80px; animation: mouth-talk 0.6s infinite;">
                👄
            </div>
            <div style="font-size: 16px; color: #6C5CE7; font-weight: bold; margin-top: 10px;">
                "Hey! I'm thirsty! 💧 Drink some water please!"
            </div>
        </div>
        <style>
        @keyframes bounce {
            0%, 100% { transform: translateY(0px); }
            50% { transform: translateY(-10px); }
        }
        @keyframes mouth-talk {
            0%, 100% { transform: scaleY(1); }
            50% { transform: scaleY(1.3); }
        }
        </style>
        """
        st.markdown(mouth_html, unsafe_allow_html=True)

    # Weekly hydration - Water Tank Visualization
    st.header("💧 Weekly Hydration - Water Tanks")
    df = dataframe_for_week()
    
    # Create a water tank for each day
    cols = st.columns(7)
    for i, (col, row) in enumerate(zip(cols, df.iterrows())):
        day_data = row[1]
        date_str = str(day_data['date_display'])
        ml = int(day_data['ml'])
        pct = min(ml / GOAL_ML, 1.0)
        is_overflow = ml > GOAL_ML
        overflow_amount = max(0, ml - GOAL_ML)
        
        with col:
            # Water tank HTML/CSS visualization with overflow
            tank_html = f"""
            <div style="text-align: center; font-size: 12px;">
                <div style="margin-bottom: 8px; color: #6C5CE7; font-weight: bold;">{date_str.split('-')[2]}</div>
                <div style="position: relative; width: 40px; height: 120px; margin: 0 auto;">
                    <!-- Tank container -->
                    <div style="position: relative; width: 100%; height: 120px; border: 2px solid #6C5CE7; border-radius: 4px; background: rgba(100, 100, 200, 0.05); overflow: {'visible' if is_overflow else 'hidden'};">
                        <div style="position: absolute; bottom: 0; width: 100%; height: {min(pct * 100, 100)}%; background: linear-gradient(180deg, #00b894, #6C5CE7); animation: wave 2s infinite;">
                        </div>
                    </div>
                    <!-- Overflow drops (visible only when ml > 3000) -->
                    {''.join([f'<div style="position: absolute; top: -8px; left: {10 + (j % 2) * 15}px; width: 8px; height: 8px; background: #00b894; border-radius: 50%; animation: overflow-drop {0.5 + j * 0.15}s infinite;"></div>' for j in range(min(3, (overflow_amount // 500) + 1))])}
                </div>
                <div style="margin-top: 8px; font-size: 11px; color: #6b6b6b;">
                    {ml} ml {'🚰' if is_overflow else ''}
                </div>
            </div>
            """
            st.markdown(tank_html, unsafe_allow_html=True)
    
    # Wave animation CSS + Overflow drop animation
    wave_css = """
    <style>
    @keyframes wave {
        0%, 100% { transform: translateX(0px); }
        25% { transform: translateX(2px); }
        50% { transform: translateX(0px); }
        75% { transform: translateX(-2px); }
    }
    @keyframes overflow-drop {
        0% {
            opacity: 1;
            transform: translateY(0px);
        }
        100% {
            opacity: 0;
            transform: translateY(20px);
        }
    }
    </style>
    """
    st.markdown(wave_css, unsafe_allow_html=True)

    # Summary numbers
    week_sum = int(df["ml"].sum())
    st.write(f"Total last 7 days: **{week_sum} ml** | Average: **{week_sum // 7} ml/day**")

    # Download CSV
    csv = df.to_csv(index=False)
    st.download_button("Download week CSV", data=csv, file_name="water_last7.csv", mime="text/csv")


if __name__ == "__main__":
    main()
