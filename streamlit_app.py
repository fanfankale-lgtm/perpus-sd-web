from datetime import datetime
import io
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
KOLOM_DATA = ["Tanggal Presensi", "Hari", "Nama Siswa", "Kelas", "Tujuan / Alasan"]

# --- KAMUS TRANSLASI HARI & BULAN KE BAHASA INDONESIA ---
HARI_INDONESIA = {
    "Monday": "Senin",
    "Tuesday": "Selasa",
    "Wednesday": "Rabu",
    "Thursday": "Kamis",
    "Friday": "Jumat",
    "Saturday": "Sabtu",
    "Sunday": "Minggu",
}

BULAN_INDONESIA = {
    1: "Januari",
    2: "Februari",
    3: "Maret",
    4: "April",
    5: "Mei",
    6: "Juni",
    7: "Juli",
    8: "Agustus",
    9: "September",
    10: "Oktober",
    11: "November",
    12: "Desember",
}


# --- FUNGSI LOAD & SAVE DATA PERMANEN ---
def load_data():
    """Membaca data rekap dari file CSV lokal jika ada, atau buat DataFrame kosong."""
    if os.path.exists(DATA_FILE):
        try:
            df = pd.read_csv(DATA_FILE)
            # Pastikan kolom sesuai dengan struktur terbaru
            if list(df.columns) != KOLOM_DATA:
                return pd.DataFrame(columns=KOLOM_DATA)
            return df
        except Exception:
            return pd.DataFrame(columns=KOLOM_DATA)
    else:
        return pd.DataFrame(columns=KOLOM_DATA)


def save_data(df):
    """Menyimpan DataFrame ke file CSV lokal secara permanen."""
    df.to_csv(DATA_FILE, index=False)


def to_excel(df):
    """Mengonversi DataFrame menjadi byte stream Excel (.xlsx)."""
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="Rekap_Presensi")
    processed_data = output.getvalue()
    return processed_data


# --- INISIALISASI SESSION STATE ---
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if "rekap_data" not in st.session_state:
    st.session_state.rekap_data = load_data()

# --- CSS CUSTOM: BACKGROUND TAMAN & EFEK ANIMASI KEREN & LUCU ---
st.markdown(
    """
