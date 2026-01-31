import pandas as pd

# ==============================
# 1. LOAD DATA
# ==============================
FILE_SKILL = "skills_unique-Copy.csv"
df = pd.read_csv(FILE_SKILL)

# ==============================
# 2. NORMALISASI SKILL
#    - lowercase
#    - strip spasi
#    - tanpa mengubah kolom IPTEK
# ==============================
df["Skill_CLEAN"] = (
    df["Skills"]
    .astype(str)
    .str.strip()
    .str.lower()
)

# ==============================
# 3. HAPUS DUPLIKAT
#    (berdasarkan skill_clean + IPTEK)
# ==============================
df_clean = df.drop_duplicates(subset=["Skill_CLEAN", "IPTEK"])

# ==============================
# 4. URUTKAN BIAR RAPIH
# ==============================
df_clean = df_clean.sort_values("Skill_CLEAN")

# ==============================
# 5. SIMPAN HASIL
# ==============================
OUTPUT_FILE = "skills_unique_clean_casefold.csv"
df_clean.to_csv(OUTPUT_FILE, index=False, encoding="utf-8")

# ==============================
# 6. INFO
# ==============================
print("✅ RAPPIH SKILLS SELESAI")
print(f"Total awal     : {len(df)}")
print(f"Setelah bersih : {len(df_clean)}")
print(f"📁 File output : {OUTPUT_FILE}")