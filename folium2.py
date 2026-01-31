import folium
from folium.plugins import MarkerCluster, HeatMap
import pandas as pd

df = pd.read_csv("FINAL_LOWONGAN_INDONESIA_IPTEK_LABEL.csv")

def create_simple_folium_map(df):
    df_map = df.dropna(subset=['Lat', 'Lon']).copy()
    
    # Peta dasar Indonesia
    m = folium.Map(
        location=[-2.5489, 118.0149],
        zoom_start=5,
        tiles='OpenStreetMap',
        control_scale=True
    )

    marker_cluster = MarkerCluster().add_to(m)

    for idx, row in df_map.iterrows():
        color = 'blue' if row['Klasifikasi'] == 'IPTEK' else 'red'
        
        popup_html = f"""
        <div style='font-family: Arial; width: 250px;'>
            <h4 style='color:{color};'>{row['Title'][:30]}...</h4>
            <b>🏢Perusahaan:</b> {row['Perusahaan']}<br>
            <b>📍Lokasi:</b> {row['Lokasi']}<br>
            <b>🛠️Klasifikasi:</b> {row['Klasifikasi']}<br>
            <b>🗂️Kategori:</b> {row['Kategori']}
        </div>
        """
        
        folium.CircleMarker(
            location=[row['Lat'], row['Lon']],
            radius=6,
            popup=folium.Popup(popup_html, max_width=300),
            color=color,
            fill=True,
            fill_color=color,
            fill_opacity=0.7
        ).add_to(marker_cluster)
    
    # heatmap
    heat_data = [[row['Lat'], row['Lon']] for idx, row in df_map.iterrows()]
    HeatMap(
        heat_data,
        name='Heatmap',
        min_opacity=0.2,
        radius=20,
        blur=15
    ).add_to(m)
    
    folium.LayerControl(collapsed=True).add_to(m)
    
    return m

# Jika dijalankan langsung, simpan ke HTML
if __name__ == "__main__":
    peta = create_simple_folium_map(df)
    peta.save('peta_folium_simple.html')
    print("Peta disimpan: peta_folium_simple.html")