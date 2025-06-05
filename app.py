import streamlit as st
import pandas as pd
import psycopg2
import matplotlib.pyplot as plt
from model import detect_anomalies  # Importing the model logic from separate file

# Page setup
st.set_page_config(page_title="Crypto Price Anomaly Detection", layout="wide")
st.title("📊 Crypto Price Anomaly Detection")
st.write("Live monitoring of crypto prices with anomaly detection using Isolation Forest.")

# Load data from PostgreSQL
def load_data():
    conn = psycopg2.connect(
        host="localhost",
        database="crypto_data",
        user="crypto_user",
        password="369"
    )
    cursor = conn.cursor()
    cursor.execute("""
        SELECT timestamp, coin, price FROM crypto_prices
        WHERE timestamp > NOW() - INTERVAL '10 minutes'
    """)
    rows = cursor.fetchall()
    conn.close()

    df = pd.DataFrame(rows, columns=["timestamp", "coin", "price"])
    return df

# Centered button
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    run_model = st.button("🚀 Generate Anomaly Report")

if run_model:
    df = load_data()
    st.write("### 🔄 Latest Data (Last 10 Minutes)")
    st.dataframe(df.tail(20))

    anomalies = detect_anomalies(df)
    st.write("### ⚠️ Detected Anomalies")
    if anomalies.empty:
        st.success("No anomalies detected in the last 10 minutes.")
    else:
        st.dataframe(anomalies)

        # Plot anomalies
        fig, ax = plt.subplots()
        for coin in df['coin'].unique():
            coin_data = df[df['coin'] == coin]
            ax.plot(coin_data['timestamp'], coin_data['price'], label=coin)

        ax.scatter(anomalies['timestamp'], anomalies['price'], color='red', label='Anomaly', zorder=5)
        ax.legend()
        ax.set_title("Price with Anomalies")
        ax.set_xlabel("Timestamp")
        ax.set_ylabel("Price")
        plt.xticks(rotation=45)
        st.pyplot(fig)
else:
    st.info("Click the button above to generate a report using the latest data.")
