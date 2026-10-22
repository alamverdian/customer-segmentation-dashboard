import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Konfigurasi Halaman Dashboard
st.set_page_config(page_title="Customer Segmentation Dashboard", layout="wide")

st.title("📊 LRFM Customer Segmentation Dashboard")
st.markdown("Dashboard interaktif berbasis aplikasi web untuk menganalisis hasil klasterisasi segmentasi pelanggan.")

# 2. Fungsi Membaca & Membersihkan Data
@st.cache_data
def load_data():
    try:
        # Jika filenya Excel
        df = pd.read_excel("FCM_LRFM_with_clusters.xlsx")
    except:
        # Jika filenya CSV
        try:
            df = pd.read_csv("customer_segmentation_data.csv", sep=None, engine='python')
        except:
            df = pd.read_csv("customer_segmentation_data.csv")
            
    # --- PROSES MEMBERSIHKAN DATA (Agar kolom terbaca sebagai angka) ---
    for col in ['Monetary', 'Frequency', 'Recency', 'Length_of_stay']:
        if col in df.columns:
            # Jika tipenya teks, bersihkan karakter non-angka (kecuali titik desimal)
            if df[col].dtype == 'object':
                df[col] = df[col].astype(str).str.replace(r'[^\d.]', '', regex=True)
            # Ubah paksa menjadi angka numerik, jika gagal diubah jadi NaN
            df[col] = pd.to_numeric(df[col], errors='coerce')
            
    # Buat nama kolom segment_name bawaan jika tidak sengaja kosong
    if 'Segment_Name' not in df.columns and 'Cluster' in df.columns:
        cluster_mapping = {0: 'Champions', 1: 'Potential Loyalists', 2: 'Hibernating / Churn'}
        df['Segment_Name'] = df['Cluster'].map(cluster_mapping)
        
    return df

df = load_data()

# 3. BAGIAN ATAS: Ringkasan Metrik Utama (KPI Cards)
# Menggunakan pd.to_numeric dengan errors='coerce' memastikan hasil .sum() atau .mean() aman
total_customers = df['Customer ID'].nunique() if 'Customer ID' in df.columns else len(df)
total_revenue = float(df['Monetary'].sum()) if 'Monetary' in df.columns else 0.0
avg_frequency = float(df['Frequency'].mean()) if 'Frequency' in df.columns else 0.0

col1, col2, col3 = st.columns(3)
col1.metric(label="👥 Total Customers", value=f"{total_customers:,}")
col2.metric(label="💰 Total Revenue (Monetary)", value=f"${total_revenue:,.2f}")
col3.metric(label="🛒 Avg. Purchase Frequency", value=f"{avg_frequency:.1f} times")

st.divider()

# 4. SIDEBAR FILTER: Memilih Segmen Pelanggan
st.sidebar.header("⚙️ Filter Options")
seg_col = 'Segment_Name' if 'Segment_Name' in df.columns else ('Cluster' if 'Cluster' in df.columns else None)

if seg_col:
    available_segments = ["All Segments"] + list(df[seg_col].dropna().unique())
    selected_segment = st.sidebar.selectbox("Pilih Segmen Pelanggan:", available_segments)
    
    # Logika Filter
    if selected_segment != "All Segments":
        filtered_df = df[df[seg_col] == selected_segment]
    else:
        filtered_df = df
else:
    selected_segment = "All Data"
    filtered_df = df

# 5. BAGIAN TENGAH: Visualisasi Interaktif
col_chart1, col_chart2 = st.columns(2)

with col_chart1:
    st.subheader("📌 Distribusi Pelanggan per Segmen")
    if seg_col:
        segment_counts = df[seg_col].value_counts().reset_index()
        segment_counts.columns = ['Segment', 'Total']
        fig_bar = px.bar(segment_counts, x='Segment', y='Total', color='Segment',
                         text_auto=True, title="Total Pelanggan Tiap Klaster")
        st.plotly_chart(fig_bar, use_container_width=True)
    else:
        st.info("Kolom Cluster/Segment_Name tidak ditemukan untuk membuat grafik batang.")

with col_chart2:
    st.subheader("🔍 Analisis Karakteristik Perilaku Belanja")
    if 'Recency' in df.columns and 'Monetary' in df.columns:
        color_param = seg_col if seg_col else None
        fig_scatter = px.scatter(filtered_df, x='Recency', y='Monetary', color=color_param,
                                 hover_data=['Customer ID'] if 'Customer ID' in df.columns else None,
                                 title="Pola Hubungan Recency vs Monetary")
        st.plotly_chart(fig_scatter, use_container_width=True)
    else:
        st.info("Kolom Recency atau Monetary tidak ditemukan untuk membuat grafik scatter.")

# 6. BAGIAN BAWAH: Tabel Data Detail
st.divider()
st.subheader("📋 Detail Data Pelanggan")
st.markdown(f"Menampilkan data untuk: **{selected_segment}**")
st.dataframe(filtered_df, use_container_width=True)
