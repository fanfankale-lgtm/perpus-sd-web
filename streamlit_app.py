from datetime import datetime
import random
import zoneinfo
import pandas as pd
import streamlit as st

# --- KONFIGURASI HALAMAN ---
st.set_page_config(
    page_title="Perpustakaan SDN 13 Padang Panjang Timur",
    page_icon="📚",
    layout="centered",
)

# --- CSS CUSTOM: BACKGROUND TAMAN & ANIMASI ---
st.markdown(
    """
    <style>
    /* Background Taman Anak-anak */
    .stApp {
        background: linear-gradient(to bottom, #87CEEB 0%, #E0F6FF 50%, #90EE90 85%, #228B22 100%);
        background-attachment: fixed;
    }

    /* Animasi Lebah Terbang */
    @keyframes beeFly {
        0% { transform: translate(0px, 0px) rotate(0deg); }
        50% { transform: translate(150px, -20px) rotate(10deg); }
        100% { transform: translate(0px, 0px) rotate(0deg); }
    }
    .bee-animation {
        font-size: 30px;
        display: inline-block;
        animation: beeFly 6s infinite ease-in-out;
    }

    /* Styling Header */
    .main-header {
        text-align: center;
        color: #1E3A8A;
        font-family: 'Comic Sans MS', cursive, sans-serif;
        text-shadow: 2px 2px 4px #ffffff;
    }
    .sub-header {
        text-align: center;
        color: #D97706;
        font-weight: bold;
        text-shadow: 1px 1px 2px #ffffff;
    }

    /* Card Form dengan Efek Transparan Segar */
    .stForm {
        background-color: rgba(255, 255, 255, 0.92);
        padding: 25px;
        border-radius: 20px;
        box-shadow: 0px 8px 16px rgba(0, 0, 0, 0.15);
        border: 3px solid #78C850;
    }

    /* Styling Tab */
    .stTabs [data-baseweb="tab-list"] {
        background-color: rgba(255, 255, 255, 0.8);
        border-radius: 10px;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# --- DATABASE SEDERHANA (Session State) ---
if "rekap_data" not in st.session_state:
    st.session_state.rekap_data = pd.DataFrame(
        columns=["Waktu (WIB)", "Nama Siswa", "Kelas", "Tujuan / Alasan"]
    )

# --- DAFTAR PESAN LUCU ---
PESAN_LUCU = [
    "Wah, calon profesor dari SDN 13 datang! Selamat membaca! 📚✨",
    "Buku adalah jendela dunia, kamu baru saja membuka pintunya! 🚪🌟",
    "Jangan lupa kembalikan buku ya, nanti bukunya kangen! 🦉📖",
    "Hebat banget! Otak kamu makin cerdas hari ini! 🧠⚡",
    "Ssstt... jangan berisik ya, buku-bukunya lagi tidur! 🤫💤",
    "Salam literasi dari SDN 13 Padang Panjang Timur! 🏆🎨",
]

# --- TAMPILAN UTAMA & DEKORASI TAMAN ---
st.markdown(
    "<div style='text-align: center;'>☁️ 🎈 ☁️ <span class='bee-animation'>🐝</span> ☁️</div>",
    unsafe_allow_html=True,
)

# --- MENAMPILKAN FOTO DARI WHATSAPP ---
col_img1, col_img2, col_img3 = st.columns([1, 2, 1])
with col_img2:
    try:
        st.image("WhatsApp Image 2026-08-30 at 13.01.42.jpeg", width=160)
    except Exception:
        st.write("📷 *(Foto/Logo akan muncul di sini)*")

st.markdown(
    "<h1 class='main-header'>🏫 SDN 13 PADANG PANJANG TIMUR 📚</h1>",
    unsafe_allow_html=True,
)
st.markdown(
    "<h3 class='sub-header'>✨ Sistem Presensi Digital Perpustakaan Ceria ✨</h3>",
    unsafe_allow_html=True,
)
st.markdown(
    "<div style='text-align: center; font-size: 24px;'>🌻 🛝 🌸 🎡 🌷 🏰 🌼</div>",
    unsafe_allow_html=True,
)
st.write("---")

# Tab untuk Presensi dan Rekap
tab1, tab2 = st.tabs(
    ["📝 Isi Daftar Hadir", "📊 Rekap Kehadiran (Pak/Bu Guru)"]
)

with tab1:
    st.write("### 🎈 Halo Anak-Anak Hebat! Yuk Isi Absen Dulu")

    with st.form(key="form_presensi", clear_on_submit=True):
        nama = st.text_input("👤 Nama Lengkap Kamu:")

        # Pilihan Kelas Sederhana (Kelas 1 - Kelas 6)
        kelas = st.selectbox(
            "🏫 Kelas Berapa?",
            [
                "-- Pilih Kelas --",
                "Kelas 1",
                "Kelas 2",
                "Kelas 3",
                "Kelas 4",
                "Kelas 5",
                "Kelas 6",
            ],
        )

        tujuan = st.selectbox(
            "🎯 Mau Ngapain di Perpus?",
            [
                "-- Pilih Tujuan --",
                "Pinjam Buku 📚",
                "Kembalikan Buku 🔄",
                "Baca Komik / Cerita 🎨",
                "Belajar / Ngerjain Tugas ✍️",
                "Cuma Ngadem 😁",
            ],
        )

        # Fitur foto kamera untuk siswa
        st.write("📸 **Ambil Foto Kamu (Opsional):**")
        foto_siswa = st.camera_input("Senyum dulu sebelum masuk! 😃")

        submit_button = st.form_submit_button(
            label="🚀 Masuk & Catat Kehadiran 🚀"
        )

    if submit_button:
        if (
            not nama
            or kelas == "-- Pilih Kelas --"
            or tujuan == "-- Pilih Tujuan --"
        ):
            st.warning("⚠️ Eits, isi dulu nama, kelas, dan tujuanmu ya!")
        else:
            # Simpan Data dengan Waktu WIB (Asia/Jakarta)
            waktu_wib = datetime.now(
                zoneinfo.ZoneInfo("Asia/Jakarta")
            ).strftime("%Y-%m-%d %H:%M:%S")
            data_baru = pd.DataFrame(
                [[waktu_wib, nama, kelas, tujuan]],
                columns=[
                    "Waktu (WIB)",
                    "Nama Siswa",
                    "Kelas",
                    "Tujuan / Alasan",
                ],
            )

            st.session_state.rekap_data = pd.concat(
                [st.session_state.rekap_data, data_baru], ignore_index=True
            )

            # Jika siswa mengambil foto
            if foto_siswa is not None:
                st.image(
                    foto_siswa,
                    caption=f"Foto Presensi {nama}",
                    width=200,
                )

            # Efek Animasi Balon & Toast
            st.balloons()
            st.toast("Data kehadiran berhasil disimpan! 🎉", icon="✅")
            st.success(
                f"🎉 Yeay! Data **{nama}** berhasil dicatat pada jam **{waktu_wib} WIB**!"
            )

            # Pesan acak
            st.info(random.choice(PESAN_LUCU))

with tab2:
    st.write("### 📋 Dashboard Rekap Kehadiran Guru")

    # Statistik Ringkas
    total_pengunjung = len(st.session_state.rekap_data)
    col1, col2 = st.columns(2)
    col1.metric("Total Pengunjung Hari Ini", f"{total_pengunjung} Siswa")

    if not st.session_state.rekap_data.empty:
        kelas_terbanyak = st.session_state.rekap_data["Kelas"].mode()[0]
        col2.metric("Kelas Paling Ramai", kelas_terbanyak)

    st.write("---")

    if st.session_state.rekap_data.empty:
        st.info("📌 Belum ada pengunjung yang mencatatkan kehadiran.")
    else:
        st.dataframe(st.session_state.rekap_data, use_container_width=True)

        # Tombol Download Data Rekap
        csv = st.session_state.rekap_data.to_csv(index=False).encode("utf-8")
        waktu_file = datetime.now(zoneinfo.ZoneInfo("Asia/Jakarta")).strftime(
            "%Y%m%d"
        )
        st.download_button(
            label="📥 Download Data Rekap (CSV)",
            data=csv,
            file_name=f"rekap_perpus_sdn13_{waktu_file}.csv",
            mime="text/csv",
        )

        # Opsi Reset Data Rekap
        st.write("---")
        st.subheader("⚙️ Area Kontrol Guru")

        with st.expander("🗑️ Opsi Reset Data Rekap Kehadiran"):
            st.warning(
                "Tindakan ini akan menghapus seluruh data presensi di atas!"
            )
            konfirmasi = st.checkbox("Saya yakin ingin menghapus data rekap")

            if st.button("🔴 Reset Seluruh Data", disabled=not konfirmasi):
                st.session_state.rekap_data = pd.DataFrame(
                    columns=[
                        "Waktu (WIB)",
                        "Nama Siswa",
                        "Kelas",
                        "Tujuan / Alasan",
                    ]
                )
                st.snow()
                st.success("Berhasil! Seluruh data rekap telah dibersihkan.")
                st.rerun()
