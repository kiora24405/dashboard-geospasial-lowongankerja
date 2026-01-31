import pandas as pd

# 📂 Daftar file yang mau digabung
files = [
    "karirhub_finall.csv",
    "lokerid_IT_clean.csv",
    "lokerid_kesehatan_clean.csv",
    "lokerid_pemasaran_clean.csv",
    "techinasia_finall.csv"
]

df_list = []

for file in files:
    try:
        print(f"Import: {file}")
        df = pd.read_csv(file)
        df_list.append(df)
    except Exception as e:
        print(f"ERROR baca {file}: {e}")

combined = pd.concat(df_list, ignore_index=True)

print(f"\nTOTAL DATA sebelum cleaning: {len(combined)}")

combined_clean = combined.drop_duplicates()

print(f"TOTAL DATA sesudah hapus duplikat: {len(combined_clean)}")

# NORMALISASI NAMA LOKASI
def normalize_location(loc):
    if pd.isna(loc):
        return loc

    loc_lower = str(loc).lower()

    # JAKARTA (SEMUA JENIS)
    if "jakarta" in loc_lower:
        return "Jakarta"

    # BANDUNG
    elif "bandung" in loc_lower:
        return "Bandung"

    else:
        return loc

combined_clean["Lokasi"] = combined_clean["Lokasi"].apply(normalize_location)

# SIMPAN HASIL FINAL
out_file = "FINAL_LOWONGAN_INDONESIA.csv"
combined_clean.to_csv(out_file, index=False, encoding="utf-8")

print(f"\nFile sudah digabungkan → {out_file}")