import streamlit as st
import pandas as pd
import pickle

st.title("Dashboard Prediksi Inflasi Pangan")

# =========================
# LOAD DATA
# =========================
df = pd.read_csv('../dataset/final_dataset.csv')
df['date'] = pd.to_datetime(df['date'])

# =========================
# KPI SECTION
# =========================
st.subheader("Ringkasan Inflasi")

col1, col2, col3 = st.columns(3)

col1.metric("Rata-rata Inflasi", f"{df['inflation'].mean():.2f}%")
col2.metric("Inflasi Terakhir", f"{df['inflation'].iloc[-1]:.2f}%")
col3.metric("Perubahan Bulanan", f"{df['inflation'].diff().iloc[-1]:.2f}%")

# =========================
# FILTER
# =========================
year = st.selectbox("Pilih Tahun", sorted(df['date'].dt.year.unique()))
filtered_df = df[df['date'].dt.year == year]

# =========================
# TREND
# =========================
st.subheader("Tren Inflasi")

st.line_chart(filtered_df.set_index('date')['inflation'])

# =========================
# DAMPAK CABAI
# =========================
st.subheader("Hubungan Inflasi dan Perubahan Harga Cabai")

st.line_chart(
    filtered_df.set_index('date')[['inflation', 'chili_price_pct_change']]
)

# =========================
# FEATURE IMPORTANCE
# =========================
st.subheader("Faktor Utama yang Mempengaruhi Inflasi")

with open('../model/xgb_model.pkl', 'rb') as f:
    xgb_model = pickle.load(f)

feature_cols = df.drop(columns=['date', 'inflation']).columns

feature_importance = pd.Series(
    xgb_model.feature_importances_,
    index=feature_cols
).sort_values(ascending=False)

st.bar_chart(feature_importance.head(10))

# =========================
# AUTO INSIGHT
# =========================
top_feature = feature_importance.index[0]

if "chili" in top_feature:
    insight = "Perubahan harga cabai merupakan faktor paling dominan dalam mempengaruhi inflasi."
elif "rice" in top_feature:
    insight = "Harga beras memiliki pengaruh besar terhadap inflasi."
elif "rolling" in top_feature or "lag" in top_feature:
    insight = "Inflasi dipengaruhi kuat oleh pola historis atau tren sebelumnya."
else:
    insight = "Beberapa faktor lain juga berkontribusi terhadap perubahan inflasi."

st.info(f"Insight Utama: {insight}")

# =========================
# KONDISI INFLASI
# =========================
latest_inflation = df['inflation'].iloc[-1]

if latest_inflation > 1:
    st.error("⚠️ Inflasi tinggi terdeteksi. Perlu perhatian dan intervensi kebijakan.")
elif latest_inflation < -1:
    st.warning("📉 Deflasi signifikan terdeteksi.")
else:
    st.success("✅ Inflasi berada dalam kondisi relatif stabil.")

# =========================
# SIMULASI
# =========================
st.subheader("Simulasi Dampak Perubahan Harga Cabai")

chili_input = st.slider(
    "Perubahan Harga Cabai (%)",
    -50, 100, 0
)

latest = df.iloc[-1].copy()
latest['chili_price_pct_change'] = chili_input

input_data = latest.drop(['date', 'inflation'])

prediction = xgb_model.predict([input_data])[0]

st.metric("Prediksi Inflasi", f"{prediction:.2f}%")

# =========================
# NARASI INSIGHT
# =========================
st.markdown("""
### 📊 Ringkasan Analisis

- Inflasi sangat dipengaruhi oleh volatilitas harga cabai  
- Lonjakan harga cabai dapat memicu peningkatan inflasi secara signifikan  
- Pola historis menunjukkan bahwa inflasi memiliki kecenderungan mengikuti tren sebelumnya  

### 🎯 Implikasi Kebijakan

- Stabilitas harga cabai menjadi faktor kunci dalam pengendalian inflasi  
- Diperlukan penguatan rantai pasok (supply chain) untuk menghindari lonjakan harga  
- Sistem monitoring berbasis data dapat membantu deteksi dini potensi inflasi  
""")