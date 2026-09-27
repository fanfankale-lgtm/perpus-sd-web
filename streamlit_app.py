from datetime import datetime
import os
import random
import zoneinfo
import pandas as pd
import streamlit as st

# ==========================================
# 1. KONFIGURASI HALAMAN STREAMLIT
# ==========================================
st.set_page_config(
    page_title="Perpustakaan SDN 13 Padang Panjang Timur",
    page_icon="📚",
    layout="centered",
)

# ==========================================
# 2. CREDENTIALS & KONFIGURASI PENYIMPANAN
# ==========================================
VALID_USERNAME = "Herda_Putri"
VALID_PASSWORD = "110198"

DATA_FILE = "rekap_presensi.csv"
KOLOM_DATA = ["Waktu (WIB)", "Nama Siswa", "Kelas", "Tujuan / Alasan"]


# ==========================================
# 3. FUNGSI LOAD & SAVE DATA PERMANEN
# ==========================================
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


# ==========================================
# 4. INISIALISASI SESSION STATE
# ==========================================
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if "rekap_data" not in st.session_state:
    st.session_state.rekap_data = load_data()

# ==========================================
# 5. CSS CUSTOM: BACKGROUND & ANIMASI
# ==========================================
st.markdown(
    """
    """,
unsafe_allow_html=True,
    col_l1, col_l2, col_l3 = st.columns([1, 2, 1])
with col_l2:
    with st.form("login_form"):
        st.markdown(
            "
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
                # Sidebar Logout
with st.sidebar:
    st.write(f"👤 Login sebagai: **{VALID_USERNAME}**")
    if st.button("🔒 Keluar (Logout)", use_container_width=True):
        st.session_state.authenticated = False
        st.rerun()

# Tampilan Dekorasi Top
st.markdown(
    "
    # 1. Judul Utama
st.markdown(
    "
    # 2. Foto & Kartu Profil Guru
col_left, col_center, col_right = st.columns([1, 1.6, 1])
with col_center:
    st.markdown("
                st.markdown(
        """
        """,
    unsafe_allow_html=True,
)
        # Tab Navigasi: Form Presensi & Dashboard Rekap
tab1, tab2 = st.tabs(
    ["📝 Isi Daftar Hadir", "📊 Rekap Kehadiran (Pak/Bu Guru)"]
)

# ======================================
# TAB 1: FORM PRESENSI SISWA
# ======================================
with tab1:
    st.write("### 🎈 Halo Anak-Anak Hebat! Yuk Isi Absen Dulu")

    with st.form(key="form_presensi", clear_on_submit=True):
        # Input Tanggal & Jam Manual Sistem Kalender
        col_tgl, col_jam = st.columns(2)
        with col_tgl:
            tgl_pilihan = st.date_input(
                "📅 Pilih Tanggal Kunjungan:",
                value=datetime.now(zoneinfo.ZoneInfo("Asia/Jakarta")).date(),
                format="DD/MM/YYYY"
            )
        with col_jam:
            jam_pilihan = st.time_input(
                "⏰ Pilih Jam Kunjungan:",
                value=datetime.now(zoneinfo.ZoneInfo("Asia/Jakarta")).time()
            )

        nama = st.text_input("👤 Nama Lengkap Kamu:")

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
            # Format Tanggal dan Jam Gabungan
            waktu_wib = f"{tgl_pilihan.strftime('%Y-%m-%d')} {jam_pilihan.strftime('%H:%M:%S')}"

            data_baru = pd.DataFrame(
                [[waktu_wib, nama, kelas, tujuan]], columns=KOLOM_DATA
            )

            # Simpan ke Session State & CSV
            st.session_state.rekap_data = pd.concat(
                [st.session_state.rekap_data, data_baru], ignore_index=True
            )
            save_data(st.session_state.rekap_data)

            # Notifikasi & Efek
            st.balloons()
            st.toast("Data kehadiran berhasil disimpan! 🎉", icon="✅")
            st.success(
                f"🎉 Yeay! Data **{nama}** berhasil dicatat untuk tanggal **{tgl_pilihan.strftime('%d-%m-%Y')}** jam **{jam_pilihan.strftime('%H:%M')} WIB**!"
            )
            st.info(random.choice(PESAN_LUCU))

# ======================================
# TAB 2: REKAP DATA & DASHBOARD GURU
# ======================================
with tab2:
    st.write("### 📋 Dashboard Rekap Kehadiran Guru")

    # Ringkasan Statistik
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

        # Tombol Unduh CSV
        csv = st.session_state.rekap_data.to_csv(index=False).encode("utf-8")
        waktu_file = datetime.now(
            zoneinfo.ZoneInfo("Asia/Jakarta")
        ).strftime("%Y%m%d")
        st.download_button(
            label="📥 Download Data Rekap (CSV)",
            data=csv,
            file_name=f"rekap_perpus_sdn13_{waktu_file}.csv",
            mime="text/csv",
        )

        # Area Kontrol Hapus Data
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
                st.session_state.rekap_data = pd.DataFrame(
                    columns=KOLOM_DATA
                )
                save_data(st.session_state.rekap_data)

                st.snow()
                st.success(
                    "Berhasil! Seluruh data rekap telah dibersihkan secara permanen."
                )
                st.rerun()
