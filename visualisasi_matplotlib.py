import pandas as pd
import matplotlib.pyplot as plt

def chart_iptek_vs_noniptek():
    df = pd.read_csv("FINAL_LOWONGAN_INDONESIA_IPTEK_LABEL.csv")

    counts = df["Klasifikasi"].value_counts()
    iptek_count = counts.get("IPTEK", 0)
    non_iptek_count = counts.get("NON-IPTEK", 0)
    total_count = iptek_count + non_iptek_count

    iptek_pct = (iptek_count / total_count) * 100
    non_iptek_pct = (non_iptek_count / total_count) * 100

    # PLOT
    fig, ax1 = plt.subplots(figsize=(12, 7))

    labels = ["IPTEK", "NON-IPTEK"]
    values = [iptek_count, non_iptek_count]  
    colors = ['#2E86AB', '#A23B72']

    bars = ax1.bar(
        labels, values,
        color=colors,
        edgecolor='black',
        linewidth=1.5,
        alpha=0.85,
        width=0.6
    )

    for i, bar in enumerate(bars):
        height = bar.get_height()
        ax1.text(
            bar.get_x() + bar.get_width()/2,
            height + (max(values)*0.02),
            f"{height:,}",
            ha='center',
            va='bottom',
            fontsize=13,
            fontweight='bold'
        )
        ax1.text(
            bar.get_x() + bar.get_width()/2,
            height - (max(values)*0.05),
            f"({[iptek_pct, non_iptek_pct][i]:.1f}%)",
            ha='center',
            va='top',
            fontsize=11,
            fontweight='bold',
            color='white'
        )

    ax1.set_title(
        "PERBANDINGAN LOWONGAN IPTEK vs NON-IPTEK",
        fontsize=18,
        fontweight='bold'
    )

    ax1.set_xlabel("Klasifikasi")
    ax1.set_ylabel("Jumlah Lowongan")
    ax1.grid(axis='y', alpha=0.2)

    plt.tight_layout()
    return fig

print("\n" + "="*50)
print("PIE CHART")
print("="*50)

import pandas as pd
import matplotlib.pyplot as plt

def chart_donut_iptek_vs_noniptek():
    df = pd.read_csv("FINAL_LOWONGAN_INDONESIA_IPTEK_LABEL.csv")

    counts = df["Klasifikasi"].value_counts()
    iptek_count = counts.get("IPTEK", 0)
    non_iptek_count = counts.get("NON-IPTEK", 0)
    total_count = iptek_count + non_iptek_count

    iptek_pct = (iptek_count / total_count) * 100
    non_iptek_pct = (non_iptek_count / total_count) * 100
    ratio = non_iptek_count / iptek_count if iptek_count > 0 else 0

    # PLOT
    fig, ax2 = plt.subplots(figsize=(7, 10))

    sizes = [iptek_count, non_iptek_count]
    labels = ["IPTEK", "NON-IPTEK"]
    colors_pie = ['#3498db', '#e74c3c']
    explode = (0.05, 0)

    wedges, texts, autotexts = ax2.pie(
        sizes,
        labels=labels,
        colors=colors_pie,
        autopct=lambda pct: f'{pct:.1f}%\n({round(pct*total_count/100):,})',
        startangle=90,
        explode=explode,
        wedgeprops=dict(width=0.4, edgecolor='white', linewidth=2),
        textprops=dict(fontsize=11, fontweight='bold'),
        pctdistance=0.85
    )

    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_fontsize(8)
        autotext.set_fontweight('bold')

    center_text = (
        f"TOTAL\n{total_count:,} LOWONGAN\n\n"
        f"RASIO\n1 : {ratio:.2f}"
    )

    ax2.text(
        0, 0,
        center_text,
        ha='center',
        va='center',
        fontsize=8,
        fontweight='bold',
        color='#2c3e50',
        linespacing=1.8
    )

    ax2.set_title(
        "DISTRIBUSI PERSENTASE LOWONGAN\nIPTEK vs NON-IPTEK",
        fontsize=14,
        fontweight='bold',
        pad=30
    )

    legend_labels = [
        f'{label} ({value:,} = {pct:.1f}%)'
        for label, value, pct in zip(
            labels, sizes, [iptek_pct, non_iptek_pct]
        )
    ]

    ax2.legend(
        wedges,
        legend_labels,
        title="Detail",
        loc="center left",
        bbox_to_anchor=(1, 0, 0.5, 1),
        fontsize=12,
        title_fontsize=12,
        frameon=True,
        shadow=True,
        fancybox=True
    )

    plt.tight_layout()
    return fig

print("\n" + "="*50)
print("HORIZONTAL COMPARISON")
print("="*50)

def chart_horizontal_comparison():
    import pandas as pd
    import matplotlib.pyplot as plt

    df = pd.read_csv("FINAL_LOWONGAN_INDONESIA_IPTEK_LABEL.csv")

    counts = df["Klasifikasi"].value_counts()
    iptek_count = counts.get("IPTEK", 0)
    non_iptek_count = counts.get("NON-IPTEK", 0)

    labels = ["IPTEK", "NON-IPTEK"]
    values = [iptek_count, non_iptek_count]
    colors = ['#2E86AB', '#A23B72']

    fig = plt.figure(figsize=(14, 6))

    # === Horizontal Bar ===
    ax3 = plt.subplot(1, 2, 1)
    bars_h = ax3.barh(labels, values, color=colors, height=0.5)

    for bar in bars_h:
        width = bar.get_width()
        ax3.text(
            width - (max(values) * 0.03),
            bar.get_y() + bar.get_height() / 2,
            f"{width:,}",
            va='center',
            ha='right',
            color='white',
            fontweight='bold',
            fontsize=12
        )

    ax3.set_xlabel('Jumlah Lowongan', fontsize=12)
    ax3.set_title('Jumlah Lowongan per Kategori', fontsize=14, fontweight='bold', pad=15)
    ax3.grid(axis='x', alpha=0.2)

    # === Perbandingan Detail ===
    ax4 = plt.subplot(1, 2, 2)

    comparison_data = {
        'IPTEK': iptek_count,
        'NON-IPTEK': non_iptek_count,
        'Selisih': non_iptek_count - iptek_count
    }

    colors_comp = ['#3498db', '#e74c3c', '#2ecc71']
    bars_comp = ax4.bar(
        comparison_data.keys(),
        comparison_data.values(),
        color=colors_comp,
        alpha=0.8
    )

    for bar in bars_comp:
        height = bar.get_height()
        ax4.text(
            bar.get_x() + bar.get_width() / 2,
            height,
            f'{height:,}',
            ha='center',
            va='bottom',
            fontweight='bold',
            fontsize=11
        )

    ax4.set_title('Perbandingan Detail', fontsize=14, fontweight='bold', pad=15)
    ax4.set_ylabel('Jumlah', fontsize=12)
    ax4.grid(axis='y', alpha=0.2)

    plt.suptitle(
        'ANALISIS KOMPARATIF LOWONGAN KERJA INDONESIA',
        fontsize=16,
        fontweight='bold',
        y=1.02
    )

    plt.tight_layout()
    return fig

print("\n" + "="*50)
print("TOP 10 KOTA")
print("="*50)

def chart_top_kota_iptek(df, total_count):
    import matplotlib.pyplot as plt
    import numpy as np

    if 'Lokasi' not in df.columns:
        return None

    df_kota = df[
        ~df['Lokasi'].str.contains('remote|hybrid|wfh', case=False, na=False)
    ]

    df_kota = df_kota[df_kota['Klasifikasi'] == 'IPTEK']

    top_lokasi = df_kota['Lokasi'].value_counts().head(10)

    fig = plt.figure(figsize=(12, 8))

    bars_cat = plt.barh(
        range(len(top_lokasi)),
        top_lokasi.values,
        color=plt.cm.Set3(np.arange(len(top_lokasi)))
    )

    plt.yticks(range(len(top_lokasi)), top_lokasi.index)
    plt.xlabel('Jumlah Lowongan', fontsize=12)
    plt.title(
        'TOP 10 KOTA DENGAN LOWONGAN IPTEK TERBANYAK',
        fontsize=16,
        fontweight='bold',
        pad=20
    )

    # Label nilai di ujung bar
    for bar, value in zip(bars_cat, top_lokasi.values):
        plt.text(
            value + (max(top_lokasi.values) * 0.01),
            bar.get_y() + bar.get_height() / 2,
            f'{value:,}',
            va='center',
            fontsize=10
        )

    plt.grid(axis='x', alpha=0.2)
    plt.tight_layout()

    return fig

print("\n" + "="*50)
print("TOP SKILL IPTEK vs NON-IPTEK")
print("="*50)

def chart_top_skill_iptek_vs_noniptek(df):
    import matplotlib.pyplot as plt
    import numpy as np

    if 'Skills' not in df.columns:
        return None

    df_skills = df.dropna(subset=['Skills']).copy()
    df_skills['Skills'] = (
        df_skills['Skills']
        .str.lower()
        .str.split(',')
    )

    # IPTEK skills
    iptek_skills = (
        df_skills[df_skills['Klasifikasi'] == 'IPTEK']
        .explode('Skills')['Skills']
        .str.strip()
        .value_counts()
        .head(10)
    )

    # NON-IPTEK skills
    non_iptek_skills = (
        df_skills[df_skills['Klasifikasi'] == 'NON-IPTEK']
        .explode('Skills')['Skills']
        .str.strip()
        .value_counts()
        .head(10)
    )

    fig, axes = plt.subplots(1, 2, figsize=(16, 7))

    # IPTEK
    axes[0].barh(
        iptek_skills.index[::-1],
        iptek_skills.values[::-1],
        color='#3498db'
    )
    axes[0].set_title('TOP 10 SKILL IPTEK', fontsize=14, fontweight='bold')
    axes[0].set_xlabel('Jumlah Lowongan')

    # NON-IPTEK
    axes[1].barh(
        non_iptek_skills.index[::-1],
        non_iptek_skills.values[::-1],
        color='#e74c3c'
    )
    axes[1].set_title('TOP 10 SKILL NON-IPTEK', fontsize=14, fontweight='bold')
    axes[1].set_xlabel('Jumlah Lowongan')

    for ax in axes:
        ax.grid(axis='x', alpha=0.2)

    plt.suptitle(
        'PERBANDINGAN KEBUTUHAN SKILL IPTEK vs NON-IPTEK',
        fontsize=16,
        fontweight='bold'
    )

    plt.tight_layout()

    return fig

print("\n" + "="*50)
print("🔍 PIE CHART IOI")
print("="*50)

def chart_ioi():
    df = pd.read_csv("HASIL_IOI_IPTEK.csv")

    # Urutkan berdasarkan IOI
    df_sorted = df.sort_values(by="ioi", ascending=False).head(15)

    kategori_count = df["Kategori"].value_counts()

    fig, ax = plt.subplots(figsize=(9,6))
    ax.pie(kategori_count, labels=kategori_count.index, autopct='%1.1f%%', startangle=90)
    ax.set_title("Distribusi Kategori IPTEK Opportunity Index")
    ax.axis("equal")

    return fig