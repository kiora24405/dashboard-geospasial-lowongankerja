import streamlit as st
import pandas as pd

# =========================
# KONFIGURASI AWAL
# =========================
st.set_page_config(
    page_title="Dashboard Pasar Kerja IPTEK Indonesia",
    layout="wide"
)

st.title("📊 Dashboard Inteligensi Pasar Kerja Indonesia")
st.caption("Visualisasi Persebaran Lowongan IPTEK vs Non-IPTEK Berbasis Data")

# =========================
# SIDEBAR MENU
# =========================
menu = st.sidebar.radio(
    "📌 Pilih Tampilan",
    [
        "Peta Persebaran",
        "Analisis Kesenjangan",
        "Analisis Statistik",
        "Insight & Rekomendasi"
    ]
)

st.sidebar.markdown("---")
st.sidebar.caption("⚙️ Tools: Folium, PyDeck, Matplotlib")

@st.cache_data
def load_data():
    return pd.read_csv("FINAL_LOWONGAN_INDONESIA_IPTEK_LABEL.csv")

df = load_data()

def classify_digital_status(total, iptek):
    if total == 0:
        return "🔴 Digital Desert"

    ratio = iptek / total

    # 🟢 DIGITAL HUB
    if total >= 50 and (iptek >= 10 or ratio >= 0.15):
        return "🟢 Digital Hub"

    # 🟡 DIGITAL TRANSITION
    elif total >= 20 and (iptek >= 3 or ratio >= 0.10):
        return "🟡 Digital Transition"

    # 🔴 DIGITAL DESERT
    else:
        return "🔴 Digital Desert"

# =========================
# HALAMAN 1: FOLIUM
# =========================
if menu == "Peta Persebaran":
    st.subheader("🗺️ Peta Persebaran Lowongan Kerja")

    try:
        from streamlit_folium import st_folium
        import folium2

        st_folium(
            folium2.create_simple_folium_map(df),
            width=1200,
            height=600,
            returned_objects=["last_object_clicked_popup"]
        )

        st.caption(
            "🔵 Biru: IPTEK | 🔴 Merah: NON-IPTEK — "
            "Gunakan zoom & klik marker untuk melihat informasi lowongan."
        )

    except Exception as e:
        st.error("Gagal memuat peta Folium")
        st.code(str(e))
# =========================
# HALAMAN 2: PYDECK
# =========================
elif menu == "Analisis Kesenjangan":
    st.subheader("🗺️ Peta 3D Kesenjangan Digital IPTEK")

    try:
        import pydeck1

        # =========================
        # TAMPILKAN PYDECK
        # =========================
        deck = pydeck1.create_3d_map_pydeck(df)
        st.pydeck_chart(deck)

        st.caption(
            "🟢 Digital Hub | 🟡 Digital Transition | 🔴 Digital Desert — "
            "Tinggi kolom menunjukkan total lowongan per wilayah."
        )

        st.markdown("---")

        # =========================
        # DIGITAL DIVIDE REPORT NASIONAL
        # =========================
        st.subheader("📊 Digital Divide Report Nasional")

        summary = (
            df.groupby("Lokasi")
            .agg(
                total=("Klasifikasi", "count"),
                iptek=("Klasifikasi", lambda x: (x == "IPTEK").sum())
            )
            .reset_index()
        )

        summary["ratio"] = summary.apply(
            lambda r: r["iptek"] / r["total"] if r["total"] > 0 else 0,
            axis=1
        )

        summary["status"] = summary.apply(
            lambda r: classify_digital_status(r["total"], r["iptek"]),
            axis=1
        )

        # =========================
        # TOP DIGITAL HUB NASIONAL
        # =========================
        st.markdown("### 🏆 Top Wilayah Digital Hub Nasional")

        top_hub = summary[summary["status"] == "🟢 Digital Hub"] \
            .sort_values("iptek", ascending=False) \
            .head(3)

        if top_hub.empty:
            st.info("Belum ada wilayah yang memenuhi kriteria Digital Hub nasional.")
        else:
            for _, row in top_hub.iterrows():
                st.markdown(f"""
*{row['Lokasi']}* — 🟢 Digital Hub  
- Total Lowongan: *{row['total']}*  
- Lowongan IPTEK: *{row['iptek']}* ({row['ratio']*100:.1f}%)  
- Implikasi: pusat pertumbuhan talenta & industri digital nasional  
""")

        # =========================
        # PRIORITAS INTERVENSI NASIONAL
        # =========================
        st.markdown("### 🚨 Wilayah Prioritas Intervensi Nasional")

        priority = summary[summary["status"] == "🔴 Digital Desert"] \
            .sort_values("ratio") \
            .head(3)

        if priority.empty:
            st.success("Tidak ada wilayah dengan status Digital Desert ekstrem.")
        else:
            for _, row in priority.iterrows():
                st.markdown(f"""
        *{row['Lokasi']}* — 🔴 Digital Desert  
        - Total Lowongan: *{row['total']}*  
        - Lowongan IPTEK: *{row['iptek']}* ({row['ratio']*100:.1f}%)  
        - Implikasi: risiko ketertinggalan digital & brain drain  
        """)

        # =========================
        # REKOMENDASI STRATEGIS NASIONAL
        # =========================
        st.markdown("### 💡 Rekomendasi Intervensi Strategis Nasional")

        st.markdown("""
        *🏛️ Pemerintah*
        - Program Digital Affirmative Action untuk wilayah Digital Desert  
        - Insentif perusahaan teknologi membuka cabang di luar pusat ekonomi  
        - Pembangunan infrastruktur & ruang inovasi daerah  

        *🎓 Pendidikan*
        - Sinkronisasi kurikulum SMK/PT dengan kebutuhan IPTEK nasional  
        - Beasiswa & bootcamp digital berbasis wilayah prioritas  
        - Program magang industri teknologi lintas daerah  

        *👩‍💻 Pencari Kerja*
        - Fokus skill dasar: data, IT support, digital marketing  
        - Upskilling bertahap ke Python, UI/UX, Cloud  
        - Manfaatkan peluang kerja remote lintas wilayah  
        """)

        st.caption(
            "Catatan: Intervensi di atas berskala nasional. "
            "Rekomendasi spesifik per kota tersedia pada menu Insight & Rekomendasi."
        )

    except Exception as e:
        st.error("❌ Gagal memuat peta 3D PyDeck")
        st.code(str(e))

# =========================
# HALAMAN 3: MATPLOTLIB
# =========================
elif menu == "Analisis Statistik":
    st.subheader("📊 Analisis Statistik Lowongan Kerja")
    st.caption(
        "Visualisasi statistik untuk memahami struktur pasar kerja "
        "IPTEK dan Non-IPTEK di Indonesia."
    )

    import visualisasi_matplotlib as vm

    # =========================
    # KELOMPOK 1: GAMBARAN UMUM
    # =========================
    st.markdown("### Gambaran Umum Pasar Kerja")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("Perbandingan IPTEK vs Non-IPTEK")
        st.pyplot(vm.chart_iptek_vs_noniptek())
        st.markdown("""
        Insight:  
        Pasar kerja Indonesia masih didominasi lowongan *NON-IPTEK (75,4%)*
        dibandingkan *IPTEK (24,6%)*.  
        Ketimpangan ini menunjukkan bahwa kebutuhan tenaga kerja berbasis
        teknologi masih relatif rendah.
        """)

    with col2:
        st.markdown("Distribusi Persentase Lowongan")
        st.pyplot(vm.chart_donut_iptek_vs_noniptek())
        st.markdown("""
        Dari total *1.221 lowongan kerja*, sektor Non-IPTEK mendominasi
        *75,4% (921 lowongan), sementara IPTEK hanya 24,6% (300 lowongan)*.  
        Rasio *1 : 3,07* menunjukkan ketimpangan kebutuhan tenaga kerja
        antara sektor teknologi dan non-teknologi.
        """)

    # =========================
    # KELOMPOK 2: KOMPARATIF NASIONAL
    # =========================
    st.markdown("---")
    st.markdown("### Analisis Komparatif Nasional")

    st.pyplot(vm.chart_horizontal_comparison())
    st.markdown("""
    Grafik menunjukkan ketimpangan signifikan antara sektor IPTEK dan Non-IPTEK.
    Jumlah lowongan Non-IPTEK (*921) jauh lebih tinggi dibandingkan IPTEK (300*),
    dengan selisih mencapai *621 lowongan*.  
    Hal ini menandakan dominasi sektor non-teknologi dalam struktur
    pasar kerja Indonesia saat ini.
    """)

    # =========================
    # KELOMPOK 3: KOTA & SKILL
    # =========================
    st.markdown("---")
    st.markdown("### Konsentrasi Wilayah & Kebutuhan Skill")

    col3, col4 = st.columns(2)

    with col3:
        st.markdown("Top Kota dengan Lowongan IPTEK Terbanyak")
        st.pyplot(vm.chart_top_kota_iptek(df, len(df)))
        st.markdown("""
        Lowongan IPTEK masih terkonsentrasi di *kota besar*, terutama Jakarta.
        Kota penyangga seperti *Tangerang, Bandung, dan Bekasi* berperan
        sebagai pusat pendukung, sementara kota lain menunjukkan
        peluang IPTEK yang masih terbatas.
        """)

    with col4:
        st.markdown("IPTEK Opportunity Index (IOI)")

        st.pyplot(vm.chart_ioi())
        st.markdown("""
        Distribusi *IPTEK Opportunity Index (IOI)* menunjukkan bahwa sebagian
        besar wilayah Indonesia masih berada pada kategori peluang IPTEK
        *rendah hingga menengah*.  
        Hal ini mengindikasikan perlunya intervensi kebijakan dan pendidikan
        untuk mendorong pemerataan peluang kerja berbasis teknologi.
        """)
        

    # =========================
    # KELOMPOK 4: PERBANDINGAN SKILL (PENUTUP)
    # =========================
    st.markdown("---")
    st.markdown("Perbandingan Kebutuhan Skill IPTEK vs Non-IPTEK")
    st.pyplot(vm.chart_top_skill_iptek_vs_noniptek(df))
    st.markdown("""
    Grafik memperlihatkan perbedaan kebutuhan skill antara sektor IPTEK
    dan Non-IPTEK.  
    IPTEK didominasi *skill teknis & digital*, sedangkan Non-IPTEK
    lebih banyak membutuhkan *skill pemasaran dan operasional*.  
    Temuan ini menegaskan adanya *kesenjangan kompetensi tenaga kerja*
    yang perlu direspon melalui peningkatan pelatihan skill digital.
    """)

# =========================
# HALAMAN 4: INSIGHT
# =========================
elif menu == "Insight & Rekomendasi":
    st.subheader("Insight & Rekomendasi Berbasis Wilayah")

    st.markdown(
        "Pilih kota untuk melihat *kondisi pasar kerja IPTEK*, "
        "kesenjangan digital, serta rekomendasi kebijakan & skill."
    )

    # =========================
    # PILIH KOTA
    # =========================
    kota_list = sorted(df['Lokasi'].dropna().unique())
    selected_city = st.selectbox("📍 Pilih Kota", kota_list)

    df_city = df[df['Lokasi'] == selected_city]

    total = len(df_city)
    iptek = len(df_city[df_city['Klasifikasi'] == 'IPTEK'])
    non_iptek = total - iptek
    ratio = iptek / total if total > 0 else 0

    # =========================
    # MODE KHUSUS: REMOTE
    # =========================
    if selected_city.lower() == "remote":

        st.markdown("---")
        st.subheader("🌐 Insight Lowongan Kerja Remote")

        col1, col2 = st.columns(2)
        col1.metric("🌍 Total Lowongan Remote", total)
        col2.metric("💻 Proporsi IPTEK", f"{ratio*100:.1f}%")

        st.markdown("---")

        st.subheader("🛠️ Skill yang Paling Dibutuhkan (Remote)")

        if 'Skills' in df_city.columns:
            top_skills = (
                df_city['Skills']
                .dropna()
                .str.lower()
                .str.split(',')
                .explode()
                .str.strip()
                .value_counts()
                .head(5)
            )

            if not top_skills.empty:
                for skill, count in top_skills.items():
                    st.markdown(f"- *{skill}* → {count} lowongan")
            else:
                st.info("Belum tersedia data skill remote yang signifikan.")

        st.markdown("---")

        st.subheader("📌 Interpretasi Remote")
        st.markdown("""
        - Lowongan remote tidak terikat wilayah geografis.
        - Distribusi IPTEK menunjukkan peluang kerja lintas daerah.
        - Remote berperan sebagai penyeimbang kesenjangan digital wilayah.
        """)

        st.subheader("🎯 Rekomendasi")
        st.markdown("""
        *👩‍💻 Pencari Kerja*
        - Mulai dari skill platform digital (content, social media, sales online).
        - Naik kelas bertahap ke skill IPTEK: data, automation, programming.
        - Bangun portofolio digital & pengalaman kerja remote.

        *🏛️ Pemerintah*
        - Jadikan kerja remote sebagai strategi pengurangan pengangguran daerah.
        - Fasilitasi pelatihan kerja digital berbasis platform.
        - Regulasi perlindungan pekerja remote & freelance.

        *🎓 Pendidikan*
        - Kurikulum adaptif: content digital → data → teknologi.
        - Sertifikasi skill praktis & berbasis proyek.
        """)

    else:
        # =========================
        # STATUS DIGITAL (SAMA DENGAN PYDECK)
        # =========================
        status = classify_digital_status(total, iptek)

        # =========================
        # DIGITAL GAP INDEX
        # =========================
        digital_gap_index = round((ratio / 0.5), 2) if total > 0 else 0

        # =========================
        # METRIK UTAMA
        # =========================
        col1, col2, col3 = st.columns(3)
        col1.metric("📊 Total Lowongan", total)
        col2.metric("💻 Proporsi IPTEK", f"{ratio*100:.1f}%")
        col3.metric(
            "📉 Digital Gap Index",
            digital_gap_index,
            help="Rasio kematangan IPTEK terhadap ambang ekosistem digital sehat"
        )

        st.markdown("---")

        # =========================
        # STATUS DIGITAL
        # =========================
        st.subheader("🌍 Status Digital Wilayah")

        if "Hub" in status:
            st.success(
                f"*{selected_city}* tergolong *Digital Hub*. "
                "Ekosistem IPTEK sudah relatif matang dan berkelanjutan."
            )
        elif "Transition" in status:
            st.warning(
                f"*{selected_city}* berada pada fase *Digital Transition*. "
                "IPTEK tumbuh, namun belum dominan."
            )
        else:
            st.error(
                f"*{selected_city}* tergolong *Digital Desert*. "
                "Kesenjangan IPTEK masih signifikan."
            )

        st.markdown(f"*Klasifikasi Wilayah:* {status}")

        st.markdown("---")

        # =========================
        # TOP SKILL IPTEK
        # =========================
        st.subheader("🛠️ Skill IPTEK Paling Dibutuhkan")

        top_skills = None
        if 'Skills' in df_city.columns:
            top_skills = (
                df_city[df_city['Klasifikasi'] == 'IPTEK']['Skills']
                .dropna()
                .str.lower()
                .str.split(',')
                .explode()
                .str.strip()
                .value_counts()
                .head(5)
            )

            if not top_skills.empty:
                for skill, count in top_skills.items():
                    st.markdown(f"- *{skill}* → {count} lowongan")
            else:
                st.info("Belum tersedia data skill IPTEK yang signifikan.")
        else:
            st.info("Kolom Skills tidak tersedia pada dataset.")

        st.markdown("---")

        # =========================
        # INTERPRETASI OTOMATIS
        # =========================
        st.subheader("📌 Interpretasi Otomatis")

        if "Desert" in status:
            st.markdown(
                "- IPTEK masih sangat minim dan belum menjadi motor ekonomi.\n"
                "- Fokus utama: literasi digital & skill dasar.\n"
                "- Risiko brain drain relatif tinggi."
            )
        elif "Transition" in status:
            st.markdown(
                "- IPTEK menunjukkan tren pertumbuhan positif.\n"
                "- Momentum tepat untuk intervensi kebijakan & pendidikan.\n"
                "- Potensi naik kelas ke Digital Hub cukup besar."
            )
        else:
            st.markdown(
                "- IPTEK sudah menjadi penggerak utama ekonomi lokal.\n"
                "- Fokus kebijakan dapat diarahkan ke inovasi lanjutan.\n"
                "- Kota berpotensi menjadi hub regional."
            )

        st.markdown("---")

        # =========================
        # REKOMENDASI TERARAH
        # =========================
        st.subheader("🎯 Rekomendasi Intervensi")

        # =========================
        # PEMERINTAH DAERAH
        # =========================
        st.markdown("### 🏛️ Pemerintah Daerah")
        if "Desert" in status:
            st.markdown(
                "- Program literasi & pelatihan digital dasar.\n"
                "- Insentif awal bagi perusahaan teknologi.\n"
                "- Pusat pelatihan berbasis komunitas."
            )
        elif "Transition" in status:
            st.markdown(
                "- Insentif startup & UMKM digital.\n"
                "- Coworking space & inkubator lokal.\n"
                "- Kolaborasi industri–kampus."
            )
        else:
            st.markdown(
                "- Dorong R&D dan deep-tech.\n"
                "- Program ekspor talenta digital.\n"
                "- Penguatan ekosistem startup mature."
            )

        # =========================
        # PENDIDIKAN & KURIKULUM
        # =========================
        st.markdown("### 🎓 Pendidikan & Kurikulum")
        if "Desert" in status:
            st.markdown(
                "- Penguatan literasi digital dasar di sekolah.\n"
                "- Pelatihan vokasi IT tingkat pemula.\n"
                "- Akses internet & perangkat belajar digital."
            )
        elif "Transition" in status:
            st.markdown(
                "- Penyesuaian kurikulum sesuai skill IPTEK dominan.\n"
                "- Program reskilling NON-IPTEK → IPTEK.\n"
                "- Kolaborasi aktif SMK/PT dengan industri lokal."
            )
        else:
            st.markdown(
                "- Kurikulum advanced (AI, data, cloud).\n"
                "- Program riset terapan kampus–industri.\n"
                "- Inkubator inovasi berbasis universitas."
            )

        # =========================
        # PENCARI KERJA
        # =========================
        st.markdown("### 👩‍💻 Pencari Kerja")
        if top_skills is not None and not top_skills.empty:
            st.markdown(
                "- Prioritaskan skill berikut:\n"
                + "\n".join([f"  - {s}" for s in top_skills.index[:3]])
                + "\n- Bangun portofolio proyek nyata."
            )
        else:
            st.markdown(
                "- Fokus skill digital umum (IT support, data dasar).\n"
                "- Ikuti bootcamp & sertifikasi.\n"
                "- Bangun portofolio mandiri."
            )

# =========================
# DATASET VIEWER
# =========================
st.markdown("---")
st.subheader("📂 Dataset Lowongan Kerja Indonesia")

with st.expander("📄 Lihat Dataset Lowongan Kerja"):
    st.markdown(
        "Dataset berikut merupakan *data utama* yang digunakan dalam "
        "visualisasi Folium, PyDeck, dan analisis statistik."
    )

    # =========================
    # PREVIEW DATA
    # =========================
    st.dataframe(
        df.head(20),
        use_container_width=True
    )

    # =========================
    # INFO DATASET
    # =========================
    col1, col2, col3 = st.columns(3)
    col1.metric("📊 Total Data", len(df))
    col2.metric("🏙️ Jumlah Kota", df['Lokasi'].nunique())
    col3.metric(
        "💻 IPTEK (%)",
        f"{(df['Klasifikasi'] == 'IPTEK').mean() * 100:.1f}%"
    )

    st.markdown("---")

    # =========================
    # DOWNLOAD
    # =========================
    st.download_button(
        label="⬇️ Download Dataset (CSV)",
        data=df.to_csv(index=False),
        file_name="FINAL_LOWONGAN_INDONESIA_IPTEK_LABEL.csv",
        mime="text/csv"
    )