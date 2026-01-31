import pandas as pd

# Ganti nama file sesuai datamu
df = pd.read_csv("FINAL_LOWONGAN_INDONESIA_LATLON_CLEAN.csv")

# =========================
# KATEGORI (case-insensitive)
# =========================
kategori_unik = (
    df["Kategori"]
    .dropna()
    .astype(str)
    .str.strip()
    .str.lower()          # ⬅️ ini kuncinya
    .unique()
    .tolist()
)

# =========================
# SKILLS (case-insensitive)
# =========================
skills_split = (
    df["Skills"]
    .dropna()
    .astype(str)
    .str.split(",")
)

skills_flat = [
    s.strip().lower()     # ⬅️ ini kuncinya
    for sub in skills_split
    for s in sub
    if isinstance(s, str)
]

skills_unik = sorted(set(skills_flat))

# =========================
# SIMPAN KE CSV
# =========================
pd.DataFrame({"Kategori": kategori_unik}).to_csv(
    "kategori_unique.csv", index=False, encoding="utf-8"
)

pd.DataFrame({"Skills": skills_unik}).to_csv(
    "skills_unique.csv", index=False, encoding="utf-8"
)

print("🎉 Berhasil!")
print(f"📁 Kategori unik tersimpan: kategori_unique.csv   (total {len(kategori_unik)})")
print(f"📁 Skills unik tersimpan: skills_unique.csv       (total {len(skills_unik)})")