import pandas as pd
import re

df = pd.read_csv("FINAL_LOWONGAN_INDONESIA_LATLON_CLEAN.csv")

print("Data awal:", len(df), "baris")

# MANUAL FIX LOKASI NYASAR
manual_fix = {
    "gresik": {
        "Lat": -7.1566,
        "Lon": 112.6555
    },
    "kab. ketapang": {
        "Lat": -1.8500,
        "Lon": 109.9714
    },
    "ketapang": {
        "Lat": -1.8500,
        "Lon": 109.9714
    },
    "kab. bantul": {
        "Lat": -7.8754,
        "Lon": 110.3289
    },
    "bantul": {
        "Lat": -7.8754,
        "Lon": 110.3289
    },
    "jawa barat": {
        "Lokasi": "Bandung",
        "Lat": -6.9218457,
        "Lon": 107.6070833
    },
    "Belitung": {
        "Lokasi": "Bangka Belitung",
        "Lat": -2.8333333,
        "Lon": 107.9167
    }
}

total_fixed = 0

for lokasi_key, coord in manual_fix.items():
    mask = df["Lokasi"].str.contains(lokasi_key, case=False, na=False)
    count = mask.sum()

    if count > 0:
        if "Lokasi" in coord:
            df.loc[mask, "Lokasi"] = coord["Lokasi"]

        df.loc[mask, "Lat"] = coord["Lat"]
        df.loc[mask, "Lon"] = coord["Lon"]

        print(f"{count} baris '{lokasi_key}' diperbaiki")

    total_fixed += count

# NORMALISASI
def normalize_lokasi(lokasi):
    if pd.isna(lokasi):
        return lokasi

    l = str(lokasi).lower().strip()

    # hapus kata administratif
    l = re.sub(r'\b(kab\.?|kabupaten|kota|city)\b', '', l)

    # rapikan spasi
    l = re.sub(r'\s+', ' ', l).strip()

    # hapus simbol aneh sisa di awal (AKIBAT kab.)
    l = re.sub(r'^[^a-z0-9]+', '', l)

    return l.title()

df["Lokasi"] = df["Lokasi"].apply(normalize_lokasi)

# Remote tidak dipaksa ke kota manapun
remote_mask = df["Lokasi"].str.contains("remote", case=False, na=False)
df.loc[remote_mask, ["Lat", "Lon"]] = None

print("Remote jobs:", remote_mask.sum(), "baris (tidak dipetakan ke kota)")

# SIMPAN DATA FINAL
output_file = "FINAL_LOWONGAN_INDONESIA_OPTIMASI_LATLON.csv"
df.to_csv(output_file, index=False)

print("\n==============================")
print(f"✅ Total lokasi diperbaiki manual : {total_fixed}")
print("✅ Normalisasi simbol & administratif selesai")
print(f"📁 File akhir: {output_file}")
print("==============================")