import pydeck as pdk
import pandas as pd

df = pd.read_csv("FINAL_LOWONGAN_INDONESIA_IPTEK_LABEL.csv")

def create_3d_map_pydeck(df):
    # Filter data dengan koordinat
    df_3d = df.dropna(subset=['Lat', 'Lon']).copy()
    pivot = (
        df_3d.pivot_table(
            index=['Lokasi', 'Lat', 'Lon'],
            columns='Klasifikasi',
            aggfunc='size',
            fill_value=0
        )
        .reset_index()
    )

    # Pastikan kolom ada
    if 'IPTEK' not in pivot.columns:
        pivot['IPTEK'] = 0
    if 'NON-IPTEK' not in pivot.columns:
        pivot['NON-IPTEK'] = 0

    pivot['Total'] = pivot['IPTEK'] + pivot['NON-IPTEK']

    # STATUS DIGITAL
    def get_status(iptek, total):
        ratio = iptek / total

        # DIGITAL HUB
        if total >= 50 and (iptek >= 10 or ratio >= 0.15):
            return "Digital Hub", [40, 167, 69, 180]   # hijau

        # DIGITAL TRANSITION
        elif total >= 20 and (iptek >= 3 or ratio >= 0.10):
            return "Digital Transition", [255, 193, 7, 180]  # kuning

        # DIGITAL DESERT
        else:
            return "Digital Desert", [220, 53, 69, 180]  # merah

    column_data = []
    for _, row in pivot.iterrows():
        status, color = get_status(row['IPTEK'], row['Total'])

        column_data.append({
            'position': [row['Lon'], row['Lat']],
            'elevation': row['Total'] * 500,
            'color': color,
            'lokasi': row['Lokasi'],
            'iptek': int(row['IPTEK']),
            'non_iptek': int(row['NON-IPTEK']),
            'total': int(row['Total']),
            'status': status
        })

    hexagon_layer = pdk.Layer(
        "HexagonLayer",
        data=df_3d[['Lon', 'Lat']].values.tolist(),
        get_position='[Lon, Lat]',
        radius=20000,
        elevation_scale=50,
        extruded=True,
        pickable=True,
        coverage=0.9,
        opacity=0.5
    )

    column_layer = pdk.Layer(
        "ColumnLayer",
        data=column_data,
        get_position='position',
        get_elevation='elevation',
        elevation_scale=50,
        radius=8000,
        get_fill_color='color',
        pickable=True,
        auto_highlight=True,
        extruded=True
    )

    # View
    view_state = pdk.ViewState(
        longitude=df_3d['Lon'].mean(),
        latitude=df_3d['Lat'].mean(),
        zoom=4.5,
        pitch=40,
        bearing=0
    )

    # Deck
    deck = pdk.Deck(
        layers=[hexagon_layer, column_layer],
        initial_view_state=view_state,
        map_style='light',
        tooltip={
            "html": """
            <b>{lokasi}</b><br/>
            🟦 IPTEK: <b>{iptek}</b><br/>
            🟥 NON-IPTEK: <b>{non_iptek}</b><br/>
            📊 Total: <b>{total}</b><br/>
            🌍 Status: <b>{status}</b>
            """,
            "style": {
                "backgroundColor": "rgba(0,0,0,0.8)",
                "color": "white",
                "padding": "10px",
                "borderRadius": "6px"
            }
        }
    )

    deck.to_html("peta_3d_lowongan.html")
    print("Peta 3D disimpan: peta_3d_lowongan.html")

    return deck

# Jalankan
create_3d_map_pydeck(df)