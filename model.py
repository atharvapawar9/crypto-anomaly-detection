import pandas as pd
import psycopg2
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler

# Connect to PostgreSQL and fetch recent price data
def get_data():
    conn = psycopg2.connect(
        host="localhost",
        database="crypto_data",
        user="crypto_user",
        password="369"
    )
    query = """
    SELECT timestamp, coin, price FROM crypto_prices
    WHERE timestamp >= NOW() - INTERVAL '6 HOURS'
    ORDER BY timestamp ASC;
    """
    df = pd.read_sql(query, conn)
    conn.close()
    return df

# Run Isolation Forest to detect anomalies per coin
def detect_anomalies(df):
    results = []

    for coin in df['coin'].unique():
        coin_df = df[df['coin'] == coin].copy()
        coin_df['timestamp'] = pd.to_datetime(coin_df['timestamp'])
        coin_df['price'] = coin_df['price'].astype(float)

        # Standardize price
        scaler = StandardScaler()
        price_scaled = scaler.fit_transform(coin_df[['price']])

        # Isolation Forest
        model = IsolationForest(contamination=0.03, random_state=42)
        coin_df['anomaly'] = model.fit_predict(price_scaled)
        coin_df['anomaly_score'] = model.decision_function(price_scaled)

        results.append(coin_df)

    return pd.concat(results)

# Main
if __name__ == "__main__":
    df = get_data()

    if df.empty:
        print("⚠️ No data fetched.")
    else:
        result_df = detect_anomalies(df)
        anomalies = result_df[result_df['anomaly'] == -1]

        if anomalies.empty:
            print("✅ No anomalies detected.")
        else:
            print("🚨 Anomalies detected:\n")
            print(anomalies[['timestamp', 'coin', 'price', 'anomaly_score']].to_string(index=False))
