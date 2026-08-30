from datetime import datetime
import pandas as pd
import streamlit as st

# --- KONFIGURASI HALAMAN ---
st.set_page_config(
    page_title="Perpustakaan Ceria SD", page_icon="🦁", layout="centered"
)

# --- DATABASE SEDERHANA (Session State) ---
if "rekap_data" not in st.session_state:
    st.session_state.rekap_data = pd.DataFrame(
        columns=["Waktu", "Nama Siswa", "Kelas", "Tujuan / Alasan"]
    )

# --- DAFTAR PESAN LUCU ---
PESAN_LUCU = [
    "Wah, calon profesor datang! Selamat membaca! 📚✨",
    "Buku adalah jendela dunia, kamu baru saja membuka pintunya! 🚪🌟",
    "Jangan lupa kembalikan buku ya, nanti bukunya kangen! 🦉📖",
    "Hebat banget! Otak kamu makin cerdas hari ini! 🧠⚡",
    "Ssstt... jangan berisik ya, buku-bukunya lagi tidur! 🤫💤",
]

# --- TAMPILAN UTAMA ---
st.title("🦁 PERPUSTAKAAN CERIA SD 🦁")
st.subheader("Satu Buku, Jutaan Petualangan! ✨")
st.write("---")

# Tab untuk Presensi dan Rekap
tab1, tab2 = st.tabs(
    ["📝 Isi Daftar Hadir", "📊 Rekap Kehadiran (Pak/Bu Guru)"]
)

with tab1:
    st.write("### 👤 Data Pengunjung")

    with st.form(key="form_presensi", clear_on_submit=True):
        nama = st.text_input("Nama Lengkap Kamu:")

        kelas = st.selectbox(
            "Kelas Berapa?",
            [
                "-- Pilih Kelas --",
                "1-A",
                "1-B",
                "2-A",
                "2-B",
                "3-A",
                "3-B",
                "4-A",
                "4-B",
                "5-A",
                "5-B",
                "6-A",
                "6-B",
            ],
        )

        tujuan = st.selectbox(
            "Mau Ngapain di Perpus?",
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
            label="✨ Masuk & Catat Kehadiran ✨"
        )

    if submit_button:
        if (
            not nama
            or kelas == "-- Pilih Kelas --"
            or tujuan == "-- Pilih Tujuan --"
        ):
            st.warning("⚠️ Eits, isi dulu nama, kelas, dan tujuanmu ya!")
        else:
            # Simpan Data
            waktu_sekarang = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            data_baru = pd.DataFrame(
                [[waktu_sekarang, nama, kelas, tujuan]],
                columns=["Waktu", "Nama Siswa", "Kelas", "Tujuan / Alasan"],
            )

            st.session_state.rekap_data = pd.concat(
                [st.session_state.rekap_data, data_baru], ignore_index=True
            )

            # Efek Lucu & Pesan Sukses
            st.balloons()
            st.success(f"🎉 Yeay! Data **{nama}** berhasil dicatat!")

            # Pesan acak
            import random

            st.info(random.choice(PESAN_LUCU))

with tab2:
    st.write("### 📋 Rekap Kehadiran Hari Ini")

    if st.session_state.rekap_data.empty:
        st.write("Belum ada pengunjung yang mencatatkan kehadiran.")
    else:
        st.dataframe(st.session_state.rekap_data, use_container_width=True)

        # Tombol Download Excel/CSV
        csv = st.session_state.rekap_data.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="📥 Download Data Rekap (CSV)",
            data=csv,
            file_name=f"rekap_perpus_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv",
        )
