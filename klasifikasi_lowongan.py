import pandas as pd

df = pd.read_csv("FINAL_LOWONGAN_INDONESIA_OPTIMASI_LATLON.csv")

skills_iptek_df = pd.read_excel("skills_iptek.xlsx")
kategori_iptek_df = pd.read_excel("kategori_iptek.xlsx")

# NORMALISASI
skills_iptek = (
    skills_iptek_df.iloc[:, 0]
    .dropna()
    .str.lower()
    .str.strip()
    .tolist()
)

kategori_iptek = (
    kategori_iptek_df.iloc[:, 0]
    .dropna()
    .str.lower()
    .str.strip()
    .tolist()
)

# FUNGSI CEK IPTEK
# SYARAT: KATEGORI DAN SKILLS HARUS IPTEK

def cek_iptek(row):
    kategori = str(row["Kategori"]).lower().strip()
    skills_text = str(row["Skills"]).lower()

    # cek kategori IPTEK
    kategori_ok = kategori in kategori_iptek

    # cek skills IPTEK (parsial match)
    skill_ok = any(skill in skills_text for skill in skills_iptek)

    # HARUS KEDUANYA TRUE
    if kategori_ok and skill_ok:
        return "IPTEK"

    return "NON-IPTEK"

df["Klasifikasi"] = df.apply(cek_iptek, axis=1)

output_file = "FINAL_LOWONGAN_INDONESIA_IPTEK_LABEL.csv"
df.to_csv(output_file, index=False, encoding="utf-8")

print("Output:", output_file)
print(df["Klasifikasi"].value_counts())