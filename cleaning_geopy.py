import pandas as pd

# 1. baca file gabungan final kamu
df = pd.read_csv("FINAL_LOWONGAN_INDONESIA_LATLON.csv")

# 2. hapus baris yang lat/lon kosong atau NaN
df_clean = df.dropna(subset=["Lat", "Lon"])

# 3. simpan file bersih
df_clean.to_csv("FINAL_LOWONGAN_INDONESIA_LATLON_CLEAN.csv", index=False, encoding="utf-8")

print("✨ CLEANING SELESAI!")
print("Total sebelum   :", len(df))
print("Total sesudah   :", len(df_clean))
print("Data dibuang    :", len(df) - len(df_clean))