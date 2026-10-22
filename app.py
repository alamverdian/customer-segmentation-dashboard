
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
    try:
        # Prioritaskan file Excel jika tersedia
        df = pd.read_excel("FCM_LRFM_with_clusters.xlsx")
    except Exception:
        # Jika Excel tidak tersedia atau gagal dibaca, gunakan CSV
        try:
            df = pd.read_csv(
                "customer_segmentation_data.csv",
                sep=None,
                engine="python"
            )
        except Exception:
            df = pd.read_csv("customer_segmentation_data.csv")

    # Membersihkan nama kolom, termasuk BOM tersembunyi
    df.columns = (
        df.columns.astype(str)
        .str.replace("\ufeff", "", regex=False)
        .str.strip()
    )

    # Mengubah metrik LRFM menjadi numerik
    numeric_cols = [
        "Monetary",
        "Frequency",
        "Recency",
        "Length_of_stay"
    ]

    for col in numeric_cols:
        if col not in df.columns:
            continue

        values = df[col]

        if values.dtype == "object":
            values = values.astype(str).str.strip()

            if col == "Monetary":
                # CSV menggunakan koma sebagai pemisah desimal
                values = values.str.replace(
                    ",", ".", regex=False
                )

            values = values.str.replace(
                r"[^0-9.\-]", "", regex=True
            )

        df[col] = pd.to_numeric(
            values, errors="coerce"
        )

    # Mapping cadangan hanya jika nama segmen belum tersedia
    if (
        "Segment_Name" not in df.columns
        and "Cluster" in df.columns
    ):
        cluster_mapping = {
            0: "Champions",
            1: "Potential Loyalists",
            2: "Hibernating / Churn"
        }

        df["Segment_Name"] = df["Cluster"].map(
            cluster_mapping
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


# 3. Ringkasan Metrik Utama (KPI Cards)
total_customers = (
    df["Customer ID"].nunique()
    if "Customer ID" in df.columns
    else len(df)
)

total_revenue = (
    float(df["Monetary"].sum())
    if "Monetary" in df.columns
    else 0.0
)

avg_frequency = (
    float(df["Frequency"].mean())
    if "Frequency" in df.columns
    else 0.0
)

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


# 4. Sidebar Filter Segmen Pelanggan
st.sidebar.header("Filter Options")

seg_col = (
    "Segment_Name"
    if "Segment_Name" in df.columns
    else "Cluster"
    if "Cluster" in df.columns
    else None
)

if seg_col is None:
    st.error(
        "Kolom Segment_Name atau Cluster tidak ditemukan."
    )
    st.stop()

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


# 5. Visualisasi Interaktif
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
        title="Jumlah Pelanggan Tiap Klaster"
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

    if {"Recency", "Monetary"}.issubset(
        filtered_df.columns
    ):
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
    else:
        st.info(
            "Kolom Recency atau Monetary tidak ditemukan."
        )



# 6. Profil Karakteristik Setiap Segmen
st.divider()
st.subheader("Profil Karakteristik Setiap Segmen")

lrfm_cols = [
    col for col in [
        "Recency",
        "Length_of_stay",
        "Frequency",
        "Monetary"
    ]
    if col in df.columns
]

if lrfm_cols:
    # Menggunakan seluruh dataset untuk membandingkan segmen
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
else:
    st.info(
        "Kolom LRFM tidak ditemukan untuk membuat profil segmen."
    )


# 7. Rekomendasi Strategi Bisnis per Segmen
st.divider()
st.subheader("Rekomendasi Strategi Bisnis per Segmen")

st.markdown(
    "Rekomendasi berikut disusun berdasarkan karakteristik "
    "umum setiap segmen. Strategi perlu disesuaikan dengan "
    "kondisi bisnis dan hasil evaluasi lebih lanjut."
)

# Nama segmen disesuaikan dengan dataset yang digunakan
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

# Membuat rekomendasi berdasarkan segmen yang benar-benar tersedia
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


# 8. Tabel Detail Data Pelanggan
st.divider()
st.subheader("Detail Data Pelanggan")

st.markdown(
    f"Menampilkan data untuk: **{selected_segment}**"
)

st.dataframe(
    filtered_df,
    use_container_width=True,
    hide_index=True
)
