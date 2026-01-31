import requests
import csv
import time
import pandas as pd

BASE_URL = "https://219wx3mpv4-dsn.algolia.net/1/indexes/*/queries"

HEADERS = {
    "x-algolia-agent": "Algolia for vanilla JavaScript 3.33.0;JS Helper 2.26.1",
    "x-algolia-application-id": "219WX3MPV4",
    "x-algolia-api-key": "b528008a75dc1c4402bfe0d8db8b3f8e",
    "content-type": "application/json",
    "accept": "application/json"
}

print("Mulai Scraping TechInAsia (FULL SKILLS dari API)...\n")

all_jobs = []
page = 0

while True:
    print(f"Ambil halaman {page}...")

    payload = {
        "requests": [
            {
                "indexName": "job_postings",
                "params": f"query=&hitsPerPage=100&page={page}&facetFilters=%5B%5B%22city.country_name%3AIndonesia%22%5D%5D"
            }
        ]
    }

    r = requests.post(BASE_URL, headers=HEADERS, json=payload)

    try:
        res = r.json()
    except:
        time.sleep(3)
        continue

    hits = res.get("results", [{}])[0].get("hits", [])

    if not hits:
        print("Tidak ada data lagi")
        break

    for job in hits:
        title = job.get("title", "-")
        company = job.get("company", {}).get("name", "-")
        location = job.get("city", {}).get("name", "-")
        category = job.get("position", {}).get("name", "-")

        skill_list = job.get("job_skills", [])
        skills = ", ".join([s.get("name", "").strip() for s in skill_list]) if skill_list else "-"
  
        
        all_jobs.append([title, company, category, location, skills])

    page += 1
    time.sleep(0.7)

# SIMPAN CSV RAW
filename = "techinasia_jobs_raw.csv"
with open(filename, mode="w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["Title", "Perusahaan", "Kategori", "Lokasi", "Skills"])
    writer.writerows(all_jobs)

print("\nRAW CSV tersimpan:", filename)

# CLEANING DATA DUPLIKAT
df = pd.DataFrame(all_jobs, columns=["Title", "Perusahaan", "Kategori", "Lokasi", "Skills"])
df_clean = df.drop_duplicates()

clean_file = "techinasia_finall.csv"
df_clean.to_csv(clean_file, index=False, encoding="utf-8")

print("\nCLEANING SELESAI!")
print(f"   Total awal   : {len(df)}")
print(f"   Setelah bersih: {len(df_clean)}")
print(f"   CSV CLEAN → {clean_file}")