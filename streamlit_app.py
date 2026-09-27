import io
import os
import random
import zoneinfo
from datetime import datetime

import pandas as pd
import streamlit as st

# Import library untuk pembuatan dokumen PDF
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

# --- KONFIGURASI HALAMAN ---
st.set_page_config(
    page_title="Perpustakaan SDN 13 Padang Panjang Timur",
    page_icon="📚",
    layout="centered",
)

# --- USER CREDENTIALS ---
VALID_USERNAME = "Herda_Putri"
VALID_PASSWORD = "110198"

KOLOM_DATA = ["Tanggal", "Jam (WIB)", "Nama Siswa", "Kelas", "Tujuan / Alasan"]
FILE_LOCAL_CSV = "rekap_presensi.csv"


# --- FUNGSI MANAJEMEN DATA LOKAL & SESSION STATE ---
def init_data():
    """Membaca data dari memori sesi atau file CSV lokal jika ada."""
    if "rekap_df" not in st.session_state:
        if os.path.exists(FILE_LOCAL_CSV):
            try:
                df = pd.read_csv(FILE_LOCAL_CSV)
                if len(df.columns) == 5:
                    df.columns = KOLOM_DATA
                    st.session_state.rekap_df = df
                else:
                    st.session_state.rekap_df = pd.DataFrame(columns=KOLOM_DATA)
            except Exception:
                st.session_state.rekap_df = pd.DataFrame(columns=KOLOM_DATA)
        else:
            st.session_state.rekap_df = pd.DataFrame(columns=KOLOM_DATA)


def save_data(df):
    """Menyimpan data ke session state dan file lokal."""
    st.session_state.rekap_df = df
    try:
        df.to_csv(FILE_LOCAL_CSV, index=False)
    except Exception:
        pass


# --- FUNGSI GENERATE PDF REKAP ---
def generate_pdf(df):
    """Menghasilkan buffer byte dari file PDF berisi laporan rekap presensi."""
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=landscape(A4),
        rightMargin=30,
        leftMargin=30,
        topMargin=30,
        bottomMargin=30,
    )
    elements = []

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "PDFTitle",
        parent=styles["Heading1"],
        fontName="Helvetica-Bold",
        fontSize=16,
        leading=20,
        alignment=1,
        textColor=colors.HexColor("#1E3A8A"),
    )

    subtitle_style = ParagraphStyle(
        "PDFSubtitle",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=11,
        leading=14,
        alignment=1,
        textColor=colors.HexColor("#D97706"),
    )

    cell_style = ParagraphStyle(
        "PDFCell",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=9,
        leading=11,
    )

    header_cell_style = ParagraphStyle(
        "PDFHeaderCell",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=10,
        leading=12,
        textColor=colors.white,
    )

    elements.append(
        Paragraph("REKAP PRESENSI SISWA PERPUSTAKAAN", title_style)
    )
    elements.append(
        Paragraph("SDN 13 PADANG PANJANG TIMUR", subtitle_style)
    )

    tgl_cetak = datetime.now(zoneinfo.ZoneInfo("Asia/Jakarta")).strftime(
        "%d-%m-%Y %H:%M WIB"
    )
    elements.append(
        Paragraph(
            f"Dicetak pada: {tgl_cetak} | Koordinator: Herda Putri S.Pd",
            subtitle_style,
        )
    )
    elements.append(Spacer(1, 15))

    table_data = [[
        Paragraph("**No**", header_cell_style),
        Paragraph("**Tanggal**", header_cell_style),
        Paragraph("**Jam (WIB)**", header_cell_style),
        Paragraph("**Nama Siswa**", header_cell_style),
        Paragraph("**Kelas**", header_cell_style),
        Paragraph("**Tujuan / Alasan**", header_cell_style),
    ]]

    for idx, row in df.iterrows():
        table_data.append([
            Paragraph(str(idx + 1), cell_style),
            Paragraph(str(row["Tanggal"]), cell_style),
            Paragraph(str(row["Jam (WIB)"]), cell_style),
            Paragraph(str(row["Nama Siswa"]), cell_style),
            Paragraph(str(row["Kelas"]), cell_style),
            Paragraph(str(row["Tujuan / Alasan"]), cell_style),
        ])

    col_widths = [35, 80, 75, 230, 90, 240]

    tabel_pdf = Table(table_data, colWidths=col_widths, repeatRows=1)
    tabel_pdf.setStyle(
        TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1E3A8A")),
            ("ALIGN", (0, 0), (-1, -1), "LEFT"),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
            ("BOTTOMPADDING", (0, 0), (-1, 0), 8),
            ("TOPPADDING", (0, 0), (-1, 0), 8),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
            (
                "ROWBACKGROUNDS",
                (0, 1),
                (-1, -1),
                [colors.white, colors.HexColor("#F8FAFC")],
            ),
        ])
    )

    elements.append(tabel_pdf)
    elements.append(Spacer(1, 12))
    elements.append(
        Paragraph(
            f"**Total Pengunjung Dicatat: {len(df)} Siswa**", cell_style
        )
    )

    doc.build(elements)
    pdf_value = buffer.getvalue()
    buffer.close()
    return pdf_value


# Inisialisasi data di awal
init_data()

# --- INISIALISASI SESSION STATE UNTUK LOGIN ---
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

# --- CSS STYLING ---
st.markdown(
    """
    
    """,
    unsafe_allow_html=True,
)

PESAN_LUCU = [
    "Wah, calon profesor dari SDN 13 datang! Selamat membaca! 📚✨",
    "Buku adalah jendela dunia, kamu baru saja membuka pintunya! 🚪🌟",
    "Jangan lupa kembalikan buku ya, nanti bukunya kangen! 🦉📖",
    "Hebat banget! Otak kamu makin cerdas hari ini! 🧠⚡",
    "Salam literasi dari SDN 13 Padang Panjang Timur! 🏆🎨",
]

# ==========================================
# HALAMAN LOGIN
# ==========================================
if not st.session_state.authenticated:
    st.markdown("
