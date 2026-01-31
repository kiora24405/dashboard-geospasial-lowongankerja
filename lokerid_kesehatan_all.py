from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time, csv
import pandas as pd

BASE = [
    "https://www.loker.id/lowongan-kerja/kesehatan-dan-kedokteran/page/1",
    "https://www.loker.id/lowongan-kerja/kesehatan-dan-kedokteran/page/2",
    "https://www.loker.id/lowongan-kerja/kesehatan-dan-kedokteran/page/3",
    "https://www.loker.id/lowongan-kerja/kesehatan-dan-kedokteran/page/4",
    "https://www.loker.id/lowongan-kerja/kesehatan-dan-kedokteran/page/5",
    "https://www.loker.id/lowongan-kerja/kesehatan-dan-kedokteran/page/6",
    "https://www.loker.id/lowongan-kerja/kesehatan-dan-kedokteran/page/7",
    "https://www.loker.id/lowongan-kerja/kesehatan-dan-kedokteran/page/8"
]

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

def text(el):
    return el.text.strip() if el else "-"

def ambil(soup, label):
    tag = soup.find("div", string=lambda x: x and label in x)
    return text(tag.find_next("a") or tag.find_next("div")) if tag else "-"

rows = []

for page_url in BASE:
    print(f"\n🌐 Scraping halaman: {page_url}")
    driver.get(page_url)
    time.sleep(3)

    soup = BeautifulSoup(driver.page_source, "html.parser")
    job_cards = soup.select("article.card a[data-discover='true']")
    links = []

    for a in job_cards:
        href = a.get("href")
        if href and href.startswith("/"):
            links.append("https://www.loker.id" + href)

    print(f"🔗 Link ditemukan: {len(links)}")

    for i, link in enumerate(links, 1):
        print(f"📥 Scrape {i}/{len(links)} : {link}")
        driver.get(link)
        time.sleep(2)

        page = BeautifulSoup(driver.page_source, "html.parser")

        title = text(page.find("h1"))
        company = text(page.find("span", class_="text-primary-500"))
        lokasi = ambil(page, "Lokasi")

        kategori = ambil(page, "Kategori")
        if kategori == "-":
            kategori = ambil(page, "Fungsi")

        skills = ", ".join([x.text.strip() for x in page.select("div.badge")])

        rows.append([title, company, kategori, lokasi, skills])

driver.quit()

raw_file = "lokerid_kesehatan_raw.csv"
with open(raw_file, "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["Title", "Perusahaan", "Kategori", "Lokasi", "Skills"])
    w.writerows(rows)

df = pd.DataFrame(rows, columns=["Title", "Perusahaan", "Kategori", "Lokasi", "Skills"])

# =========================
# 🧼 CLEANING FIXED
# =========================
df = df.replace("-", None)  # ubah "-" jadi NaN
df = df.dropna(subset=["Title", "Perusahaan", "Kategori", "Lokasi", "Skills"])  # hapus baris kosong
df_clean = df.drop_duplicates()  # barulah hapus duplikat

clean_file = "lokerid_kesehatan_clean.csv"
df_clean.to_csv(clean_file, index=False, encoding="utf-8")

print("\n✨ CLEANING SELESAI!")
print(f"   Total data asli  : {len(rows)}")
print(f"   Setelah cleaning : {len(df_clean)}")
print(f"   CSV bersih → {clean_file}")