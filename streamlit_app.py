from datetime import datetime
import os
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

# --- USER CREDENTIALS ---
VALID_USERNAME = "Herda_Putri"
VALID_PASSWORD = "Bukuadalahpintudunia"

# --- NAMA FILE PENYIMPANAN PERMANEN ---
DATA_FILE = "rekap_presensi.csv"
KOLOM_DATA = ["Waktu (WIB)", "Nama Siswa", "Kelas", "Tujuan / Alasan"]


# --- FUNGSI LOAD & SAVE DATA PERMANEN ---
def load_data():
    """Membaca data rekap dari file CSV lokal jika ada, atau buat DataFrame kosong."""
    if os.path.exists(DATA_FILE):
        try:
            return pd.read_csv(DATA_FILE)
        except Exception:
            return pd.DataFrame(columns=KOLOM_DATA)
    else:
        return pd.DataFrame(columns=KOLOM_DATA)


def save_data(df):
    """Menyimpan DataFrame ke file CSV lokal secara permanen."""
    df.to_csv(DATA_FILE, index=False)


# --- INISIALISASI SESSION STATE ---
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if "rekap_data" not in st.session_state:
    st.session_state.rekap_data = load_data()

# --- CSS CUSTOM: BACKGROUND TAMAN & EFEK ANIMASI KEREN & LUCU ---
st.markdown(
    """
    <style>
    /* Background Taman Anak-anak Bergerak Gradien */
    .stApp {
        background: linear-gradient(-45deg, #87CEEB, #E0F6FF, #A8E6CF, #DCEDC1, #FFD3B6);
        background-size: 400% 400%;
        animation: gradientBG 15s ease infinite;
        background-attachment: fixed;
    }

    @keyframes gradientBG {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    /* Element Animasi di Background */
    .animated-bg-container {
        position: fixed;
        top: 0;
        left: 0;
        width: 100vw;
        height: 100vh;
        pointer-events: none;
        z-index: 0;
        overflow: hidden;
    }

    /* Animasi Awan Melayang */
    @keyframes cloudMove {
        0% { transform: translateX(-150px); }
        100% { transform: translateX(105vw); }
    }
    .cloud1 {
        position: absolute;
        top: 8%;
        font-size: 45px;
        animation: cloudMove 25s linear infinite;
        opacity: 0.85;
    }
    .cloud2 {
        position: absolute;
        top: 18%;
        font-size: 60px;
        animation: cloudMove 35s linear infinite;
        animation-delay: -12s;
        opacity: 0.75;
    }

    /* Animasi Lebah Terbang Memutar */
    @keyframes beeFly {
        0% { transform: translate(0px, 0px) rotate(0deg); }
        25% { transform: translate(120px, -30px) rotate(15deg); }
        50% { transform: translate(250px, 10px) rotate(-10deg); }
        75% { transform: translate(100px, 40px) rotate(10deg); }
        100% { transform: translate(0px, 0px) rotate(0deg); }
    }
    .bee-animation {
        font-size: 38px;
        display: inline-block;
        animation: beeFly 8s infinite ease-in-out;
    }

    /* Animasi Kupu-kupu Terbang Naik-Turun */
    @keyframes butterflyFly {
        0% { transform: translate(-50px, 80vh) scale(0.8); }
        50% { transform: translate(50vw, 40vh) scale(1.1) rotate(20deg); }
        100% { transform: translate(105vw, 10vh) scale(0.8); }
    }
    .butterfly {
        position: absolute;
        font-size: 35px;
        animation: butterflyFly 18s linear infinite;
    }

    /* Animasi Balon Udara Mengapung */
    @keyframes balloonFloat {
        0% { transform: translateY(0px) rotate(-3deg); }
        50% { transform: translateY(-25px) rotate(3deg); }
        100% { transform: translateY(0px) rotate(-3deg); }
    }
    .floating-balloon {
        display: inline-block;
        font-size: 40px;
        animation: balloonFloat 4s infinite ease-in-out;
    }

    /* Styling Header */
    .main-header {
        text-align: center;
        color: #1E3A8A;
        font-family: 'Comic Sans MS', cursive, sans-serif;
        text-shadow: 2px 2px 4px #ffffff;
        margin-bottom: 10px;
    }
    .sub-header {
        text-align: center;
        color: #D97706;
        font-weight: bold;
        text-shadow: 1px 1px 2px #ffffff;
        margin-top: 15px;
    }

    /* Card Profil Guru */
    .teacher-card {
        background: rgba(255, 255, 255, 0.95);
        border: 4px solid #F59E0B;
        border-radius: 20px;
        padding: 15px;
        text-align: center;
        box-shadow: 0px 8px 20px rgba(0,0,0,0.15);
        margin: 10px auto;
    }
    .teacher-name {
        color: #1E3A8A;
        font-family: 'Comic Sans MS', cursive, sans-serif;
        font-size: 18px;
        font-weight: bold;
        margin-top: 10px;
        margin-bottom: 2px;
    }
    .teacher-title {
        color: #D97706;
        font-size: 14px;
        font-weight: 600;
    }

    /* Card Form Transparan Ceria */
    .stForm {
        background-color: rgba(255, 255, 255, 0.92);
        padding: 25px;
        border-radius: 20px;
        box-shadow: 0px 8px 16px rgba(0, 0, 0, 0.15);
        border: 3px solid #78C850;
    }

    /* Box Login */
    .login-box {
        background-color: rgba(255, 255, 255, 0.95);
        padding: 30px;
        border-radius: 25px;
        box-shadow: 0px 10px 25px rgba(0,0,0,0.2);
        border: 4px dashed #3B82F6;
        text-align: center;
    }

    /* Styling Tab */
    .stTabs [data-baseweb="tab-list"] {
        background-color: rgba(255, 255, 255, 0.85);
        border-radius: 12px;
    }
    </style>

    <!-- HTML ELement Animasi Background -->
    <div class="animated-bg-container">
        <div class="cloud1">☁️</div>
        <div class="cloud2">🌤️</div>
        <div class="butterfly">🦋</div>
    </div>
    """,
    unsafe_allow_html=True,
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

# ==========================================
# HALAMAN LOGIN (JIKA BELUM LOG IN)
# ==========================================
if not st.session_state.authenticated:
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown(
        "<div style='text-align: center; font-size: 45px;'>🏫 🔑 📚</div>",
        unsafe_allow_html=True,
    )
    st.markdown(
        "<h1 class='main-header'>PERPUSTAKAAN DIGITAL<br>SDN 13 PADANG PANJANG TIMUR</h1>",
        unsafe_allow_html=True,
    )
    st.write("---")

    col_l1, col_l2, col_l3 = st.columns([1, 2, 1])
    with col_l2:
        with st.form("login_form"):
            st.markdown(
                "<h3 style='text-align: center; color: #1E3A8A;'>🔐 Silakan Login Terlebih Dahulu</h3>",
                unsafe_allow_html=True,
            )
            input_user = st.text_input(
                "👤 Username", placeholder="Masukkan Username"
            )
            input_pass = st.text_input(
                "🔑 Password", type="password", placeholder="Masukkan Password"
            )
            btn_login = st.form_submit_button(
                "🚀 Masuk Ke Aplikasi 🚀", use_container_width=True
            )

            if btn_login:
                if (
                    input_user == VALID_USERNAME
                    and input_pass == VALID_PASSWORD
                ):
                    st.session_state.authenticated = True
                    st.success(
                        "🎉 Login Berhasil! Selamat datang Ibu Herda Putri."
                    )
                    st.balloons()
                    st.rerun()
                else:
                    st.error(
                        "❌ Username atau Password salah! Periksa kembali ya."
                    )

# ==========================================
# HALAMAN UTAMA (JIKA SUDAH LOG IN)
# ==========================================
else:
    # --- SIDEBAR / OPTION LOGOUT ---
    with st.sidebar:
        st.write(f"👤 Login sebagai: **{VALID_USERNAME}**")
        if st.button("🔒 Keluar (Logout)", use_container_width=True):
            st.session_state.authenticated = False
            st.rerun()

    # --- TAMPILAN UTAMA & DEKORASI TAMAN ---
    st.markdown(
        "<div style='text-align: center;'>☁️ <span class='floating-balloon'>🎈</span> ☁️ <span class='bee-animation'>🐝</span> ☁️</div>",
        unsafe_allow_html=True,
    )

    # 1. JUDUL UTAMA
    st.markdown(
        "<h1 class='main-header'>🏫 SDN 13 PADANG PANJANG TIMUR 📚</h1>",
        unsafe_allow_html=True,
    )

    # 2. FOTO & KARTU PROFIL GURU KOORDINATOR PERPUSTAKAAN
    col_left, col_center, col_right = st.columns([1, 1.6, 1])
    with col_center:
        st.markdown("<div class='teacher-card'>", unsafe_allow_html=True)
        try:
            st.image(
                "WhatsApp Image 2026-08-30 at 13.01.42.jpeg",
                use_container_width=True,
            )
        except Exception:
            st.write("📷 *(Foto Guru/Koordinator Perpustakaan)*")

        st.markdown(
            """
            <div class='teacher-name'>👩‍🏫 Herda Putri S.Pd</div>
            <div class='teacher-title'>📖 Koordinator Perpustakaan</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # 3. SUB-HEADER & DEKORASI
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
                    [[waktu_wib, nama, kelas, tujuan]], columns=KOLOM_DATA
                )

                # Gabungkan data lama dan data baru
                st.session_state.rekap_data = pd.concat(
                    [st.session_state.rekap_data, data_baru], ignore_index=True
                )

                # Simpan PERMANEN ke file CSV lokal
                save_data(st.session_state.rekap_data)

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
        col1.metric("Total Pengunjung", f"{total_pengunjung} Siswa")

        if not st.session_state.rekap_data.empty:
            kelas_terbanyak = st.session_state.rekap_data["Kelas"].mode()[0]
            col2.metric("Kelas Paling Ramai", kelas_terbanyak)

        st.write("---")

        if st.session_state.rekap_data.empty:
            st.info("📌 Belum ada pengunjung yang mencatatkan kehadiran.")
        else:
            st.dataframe(st.session_state.rekap_data, use_container_width=True)

            # Tombol Download Data Rekap
            csv = st.session_state.rekap_data.to_csv(index=False).encode(
                "utf-8"
            )
            waktu_file = datetime.now(
                zoneinfo.ZoneInfo("Asia/Jakarta")
            ).strftime("%Y%m%d")
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
                    "Tindakan ini akan menghapus seluruh data presensi baik di tampilan maupun di penyimpanan file!"
                )
                konfirmasi = st.checkbox(
                    "Saya yakin ingin menghapus data rekap"
                )

                if st.button("🔴 Reset Seluruh Data", disabled=not konfirmasi):
                    # Kosongkan data di session state dan file CSV
                    st.session_state.rekap_data = pd.DataFrame(
                        columns=KOLOM_DATA
                    )
                    save_data(st.session_state.rekap_data)

                    st.snow()
                    st.success(
                        "Berhasil! Seluruh data rekap telah dibersihkan secara permanen."
                    )
                    st.rerun()
