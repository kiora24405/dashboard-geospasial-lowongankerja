import requests
import csv
import time
import pandas as pd

BASE_URL = "https://api.kemnaker.go.id/karirhub/catalogue/v1/industrial-vacancies"

params = {
    "query": "",
    "page": 1,
    "limit": 1000   
}

all_rows = []

while True:
    print(f"Page {params['page']} | Terkumpul: {len(all_rows)}")

    try:
        r = requests.get(BASE_URL, params=params, timeout=15)
        data = r.json().get("data", [])
    except Exception as e:
        print(f"⚠️ Error API: {e}")
        time.sleep(2)
        continue

    if not data:
        print("\nData habis\n")
        break

    for job in data:

        lokasi = job.get("city_name") or job.get("district_name") or job.get("province_name")
        if not lokasi:
            continue

        skills_raw = job.get("skills")
        if not skills_raw:
            continue

        skill_list = []
        for s in skills_raw:
            if isinstance(s, dict):
                skill_list.append(s.get("value", ""))
            elif isinstance(s, str):
                skill_list.append(s)

        skills = ", ".join(skill_list) if skill_list else "-"

        # UBAH URUTAN
        row = [
            job.get("title", "-"),              # Title
            job.get("company_name", "-"),       # Perusahaan
            job.get("job_function_name", "-"),  # Kategori
            lokasi,                             # Lokasi
            skills                              # Skills
        ]

        all_rows.append(row)

    params["page"] += 1
    time.sleep(0.5)

print(f"\nTOTAL DATA SELURUH BIDANG (RAW): {len(all_rows)}")

# SIMPAN RAW CSV
raw_file = "karirhub_5cols_raw.csv"
with open(raw_file, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow([
        "Title", "Perusahaan", "Kategori", "Lokasi", "Skills"
    ])
    writer.writerows(all_rows)

print(f"CSV RAW tersimpan → {raw_file}")

# CLEANING DUPLIKAT + NO EMPTY
df = pd.DataFrame(all_rows, columns=[
    "Title", "Perusahaan", "Kategori", "Lokasi", "Skills"
])

df_clean = (
    df.drop_duplicates()    
      .replace("-", None)   
      .dropna()             
)

clean_file = "karirhub_finall.csv"
df_clean.to_csv(clean_file, index=False, encoding="utf-8")

print("\n✨ CLEANING SELESAI!")
print(f"   Total Awal     : {len(df)}")
print(f"   Setelah Bersih  : {len(df_clean)} (tanpa duplikat & tanpa kosong)")