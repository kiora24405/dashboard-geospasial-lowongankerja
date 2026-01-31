import pandas as pd
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderUnavailable
import time

INPUT_FILE = "FINAL_LOWONGAN_INDONESIA.csv"
OUTPUT_FILE = "FINAL_LOWONGAN_INDONESIA_LATLON.csv"

# LOAD DATA
df = pd.read_csv(INPUT_FILE)

# Tambah kolom kosong Lat dan Lon
if "Lat" not in df.columns:
    df["Lat"] = None
if "Lon" not in df.columns:
    df["Lon"] = None

# INISIASI GEOPY
geolocator = Nominatim(user_agent="joblocation_mapper")
cache = {} 

def get_lat_lon(lokasi):
    if lokasi in cache:
        return cache[lokasi]

    for attempt in range(3):  # coba 3 kali kalau gagal
        try:
            result = geolocator.geocode(f"{lokasi}, Indonesia", timeout=10)
            if result:
                lat_lon = (result.latitude, result.longitude)
                cache[lokasi] = lat_lon
                return lat_lon
            else:
                cache[lokasi] = (None, None)
                return (None, None)
        except (GeocoderTimedOut, GeocoderUnavailable):
            print(f"Timeout {lokasi}, coba lagi ({attempt+1}/3)...")
            time.sleep(2)

    cache[lokasi] = (None, None)
    return (None, None)

# PROSES SEMUA BARIS
start_index = df[df["Lat"].isna()].index.min() or 0 

for i in range(start_index, len(df)):
    lokasi = df.at[i, "Lokasi"]

    # Skip jika sudah ada nilai
    if pd.notna(df.at[i, "Lat"]):
        continue

    print(f"{i+1}/{len(df)} : {lokasi}")

    lat, lon = get_lat_lon(lokasi)

    df.at[i, "Lat"] = lat
    df.at[i, "Lon"] = lon

    time.sleep(1.2)

    # SAVE TIAP 50 BARIS
    if i % 50 == 0:
        temp_file = OUTPUT_FILE.replace(".csv", "_backup.csv")
        df.to_csv(temp_file, index=False, encoding="utf-8")
        print(f"Auto-save backup di: {temp_file}")

df.to_csv(OUTPUT_FILE, index=False, encoding="utf-8")
print("\n🎉 SELESAI TOTAL!")
print(f"File final disimpan sebagai: {OUTPUT_FILE}")
print(f"Total baris: {len(df)}")