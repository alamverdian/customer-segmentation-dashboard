
import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Konfigurasi Halaman Dashboard
st.set_page_config(
    page_title="Customer Segmentation Dashboard",
    layout="wide"
)

st.title("LRFM Customer Segmentation Dashboard")
st.markdown(
    "Dashboard interaktif untuk menganalisis hasil "
    "klasterisasi segmentasi pelanggan."
)


# 2. Fungsi Membaca dan Membersihkan Data
@st.cache_data
def load_data():
    # Membaca CSV hasil clustering secara langsung
    df = pd.read_csv(
        "customer_segmentation_data.csv",
        sep=None,
        engine="python",
        dtype={"Customer ID": "string"}
    )

    # Membersihkan nama kolom, termasuk BOM tersembunyi
    df.columns = (
        df.columns.astype(str)
        .str.replace("\ufeff", "", regex=False)
        .str.strip()
    )

    # Memastikan kolom wajib tersedia
    required_cols = [
        "Customer ID",
        "Monetary",
        "Frequency",
        "Recency",
        "Length_of_stay",
        "Segment_Name"
    ]

    missing_cols = [
        col for col in required_cols
        if col not in df.columns
    ]

    if missing_cols:
        raise ValueError(
            f"Kolom berikut tidak ditemukan: {missing_cols}. "
            f"Kolom tersedia: {df.columns.tolist()}"
        )

    # Membersihkan metrik LRFM menjadi numerik
    numeric_cols = [
        "Monetary",
        "Frequency",
        "Recency",
        "Length_of_stay"
    ]

    missing_values = [
        "",
        "none",
        "null",
        "nan",
        "na",
        "n/a"
    ]

    for col in numeric_cols:
        # Ubah ke string agar format data konsisten
        values = df[col].astype("string").str.strip()

        # Samakan representasi nilai kosong
        values = values.mask(
            values.str.lower().isin(missing_values)
        )

        if col == "Monetary":
            # Format CSV: 77183,6 menjadi 77183.6
            values = values.str.replace(
                ",", ".", regex=False
            )

        # Bersihkan karakter selain angka, titik, dan minus
        values = values.str.replace(
            r"[^0-9.\-]",
            "",
            regex=True
        )

        # Konversi menjadi numerik
        df[col] = pd.to_numeric(
            values,
            errors="coerce"
        )

    # Pastikan Cluster numerik jika tersedia
    if "Cluster" in df.columns:
        df["Cluster"] = pd.to_numeric(
            df["Cluster"],
            errors="coerce"
        )

    # Nama segmen asli dari CSV tetap dipertahankan
    df["Segment_Name"] = (
        df["Segment_Name"]
        .astype("string")
        .str.strip()
    )

    return df


try:
    df = load_data()
except Exception as e:
    st.error(f"Gagal membaca dataset: {e}")
    st.stop()

if df.empty:
    st.error("Dataset kosong.")
    st.stop()


# 3. Pemeriksaan Kualitas Data
# Menampilkan peringatan jika ada Monetary yang gagal dikonversi
missing_monetary = int(df["Monetary"].isna().sum())

if missing_monetary > 0:
    st.warning(
        f"Ada {missing_monetary} baris dengan Monetary kosong "
        "atau tidak dapat dikonversi. Nilai tersebut tidak "
        "diubah menjadi nol agar hasil analisis tidak menyesatkan."
    )


# 4. Ringkasan Metrik Utama (KPI Cards)
total_customers = df["Customer ID"].nunique()

total_revenue = df["Monetary"].sum()

avg_frequency = df["Frequency"].mean()

col1, col2, col3 = st.columns(3)

col1.metric(
    label="Total Customers",
    value=f"{total_customers:,}"
)

col2.metric(
    label="Total Monetary",
    value=f"{total_revenue:,.2f}"
)

col3.metric(
    label="Avg. Purchase Frequency",
    value=(
        f"{avg_frequency:.1f} times"
        if pd.notna(avg_frequency)
        else "N/A"
    )
)

st.caption(
    "Total Monetary merupakan jumlah nilai Monetary "
    "dalam dataset, bukan otomatis pendapatan periode tertentu."
)

st.divider()


# 5. Sidebar Filter Segmen Pelanggan
st.sidebar.header("Filter Options")

seg_col = "Segment_Name"

available_segments = sorted(
    df[seg_col].dropna().unique().tolist(),
    key=str
)

selected_segment = st.sidebar.selectbox(
    "Pilih Segmen Pelanggan:",
    ["All Segments"] + available_segments
)

if selected_segment == "All Segments":
    filtered_df = df.copy()
else:
    filtered_df = df[
        df[seg_col] == selected_segment
    ].copy()


# 6. Visualisasi Interaktif
col_chart1, col_chart2 = st.columns(2)

with col_chart1:
    st.subheader("Distribusi Pelanggan per Segmen")

    segment_counts = (
        df[seg_col]
        .value_counts()
        .rename_axis("Segment")
        .reset_index(name="Total")
    )

    fig_bar = px.bar(
        segment_counts,
        x="Segment",
        y="Total",
        color="Segment",
        text="Total",
        title="Jumlah Pelanggan Tiap Segmen"
    )

    fig_bar.update_traces(
        textposition="outside"
    )

    fig_bar.update_layout(
        showlegend=False,
        xaxis_title="Segmen Pelanggan",
        yaxis_title="Jumlah Pelanggan"
    )

    st.plotly_chart(
        fig_bar,
        use_container_width=True
    )


with col_chart2:
    st.subheader("Analisis Perilaku Belanja")

    scatter_df = filtered_df.dropna(
        subset=["Recency", "Monetary"]
    )

    hover_cols = [
        col for col in [
            "Customer ID",
            "Frequency",
            "Length_of_stay"
        ]
        if col in scatter_df.columns
    ]

    fig_scatter = px.scatter(
        scatter_df,
        x="Recency",
        y="Monetary",
        color=seg_col,
        hover_data=hover_cols,
        title="Pola Recency vs Monetary",
        labels={
            "Recency": "Recency",
            "Monetary": "Monetary",
            seg_col: "Segmen"
        },
        opacity=0.7
    )

    st.plotly_chart(
        fig_scatter,
        use_container_width=True
    )

    st.caption(
        "Jika Recency dihitung dalam hari sejak transaksi "
        "terakhir, nilai lebih tinggi berarti transaksi "
        "terakhir terjadi lebih lama."
    )


# 7. Profil Karakteristik Setiap Segmen
st.divider()
st.subheader("Profil Karakteristik Setiap Segmen")

lrfm_cols = [
    "Recency",
    "Length_of_stay",
    "Frequency",
    "Monetary"
]

profile = (
    df.groupby(seg_col)[lrfm_cols]
    .mean()
    .round(2)
)

profile.insert(
    0,
    "Total Customers",
    df.groupby(seg_col).size()
)

profile.index.name = "Segment"

st.markdown(
    "Tabel berikut menunjukkan rata-rata nilai LRFM "
    "dan jumlah pelanggan pada setiap segmen."
)

st.dataframe(
    profile,
    use_container_width=True
)

st.caption(
    "Recency yang tinggi umumnya berarti pelanggan "
    "sudah lebih lama tidak bertransaksi. Interpretasi "
    "metrik lain mengikuti definisi pada penelitian."
)


# 8. Rekomendasi Strategi Bisnis per Segmen
st.divider()
st.subheader("Rekomendasi Strategi Bisnis per Segmen")

st.markdown(
    "Rekomendasi berikut disusun berdasarkan karakteristik "
    "umum setiap segmen. Strategi perlu disesuaikan dengan "
    "kondisi bisnis dan hasil evaluasi lebih lanjut."
)

strategy_mapping = {
    "Pelanggan Loyal": {
        "karakteristik": (
            "Memiliki recency relatif rendah dan frekuensi "
            "transaksi relatif tinggi dibandingkan segmen lain."
        ),
        "strategi": [
            (
                "Program loyalitas",
                "Berikan poin reward atau keuntungan khusus "
                "untuk mendorong pelanggan tetap bertransaksi."
            ),
            (
                "Penawaran eksklusif",
                "Berikan akses awal terhadap produk baru atau "
                "promo khusus bagi pelanggan loyal."
            )
        ]
    },
    "Pelanggan Potensial": {
        "karakteristik": (
            "Memiliki potensi untuk meningkatkan frekuensi "
            "pembelian dan nilai transaksi."
        ),
        "strategi": [
            (
                "Cross-selling dan bundling",
                "Tawarkan produk pelengkap atau paket produk "
                "untuk mendorong pembelian tambahan."
            ),
            (
                "Dorongan pembelian berulang",
                "Berikan reward atau penawaran setelah pelanggan "
                "mencapai jumlah transaksi tertentu."
            )
        ]
    },
    "Pelanggan Yang Hilang": {
        "karakteristik": (
            "Memiliki recency relatif tinggi, yang menunjukkan "
            "bahwa transaksi terakhir terjadi lebih lama "
            "dibandingkan segmen yang lebih aktif."
        ),
        "strategi": [
            (
                "Kampanye win-back",
                "Kirimkan penawaran yang relevan untuk mendorong "
                "pelanggan kembali melakukan transaksi."
            ),
            (
                "Evaluasi penyebab ketidakaktifan",
                "Analisis riwayat pembelian atau kumpulkan "
                "umpan balik untuk memahami alasan pelanggan "
                "tidak lagi bertransaksi."
            )
        ]
    }
}

for segment in available_segments:
    segment_name = str(segment)

    with st.expander(
        f"Strategi untuk {segment_name}",
        expanded=(selected_segment == segment_name)
    ):
        strategy_info = strategy_mapping.get(segment_name)

        if strategy_info:
            st.markdown("**Karakteristik umum**")
            st.write(strategy_info["karakteristik"])

            st.markdown("**Rekomendasi strategi**")

            for title, description in strategy_info["strategi"]:
                st.markdown(f"**{title}**")
                st.write(description)

        else:
            st.info(
                "Strategi khusus untuk segmen ini belum "
                "didefinisikan. Periksa nama segmen dan "
                "karakteristik LRFM untuk menyusun rekomendasi "
                "yang sesuai."
            )


# 9. Tabel Detail Data Pelanggan
st.divider()
st.subheader("Detail Data Pelanggan")

st.markdown(
    f"Menampilkan data untuk: **{selected_segment}**"
)

# Format Monetary agar mudah dibaca, tanpa mengubah data asli
display_df = filtered_df.copy()

display_df["Monetary"] = display_df["Monetary"].map(
    lambda value: (
        f"{value:,.2f}"
        if pd.notna(value)
        else "Data tidak tersedia"
    )
)

st.dataframe(
    display_df,
    use_container_width=True,
    hide_index=True
)
