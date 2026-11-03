import folium
import streamlit as st
from streamlit_folium import st_folium


def app() -> None:
    st.header("🗺️ Gestão Espacial e Talhões da Lavoura")
    st.markdown(
        "Visualização cartográfica dos talhões, variedades plantadas "
        "e estimativas de produtividade."
    )

    latitude_centro = -21.4250
    longitude_centro = -48.2400

    mapa = folium.Map(
        location=[latitude_centro, longitude_centro],
        zoom_start=14,
        tiles="OpenStreetMap",
    )

    folium.TileLayer(
        tiles=(
            "https://server.arcgisonline.com/ArcGIS/rest/services/"
            "World_Imagery/MapServer/tile/{z}/{y}/{x}"
        ),
        attr=(
            "Esri &mdash; Source: Esri, i-cubed, USDA, USGS, AEX, "
            "GeoEye, Getmapping, Aerogrid, IGN, IGP, UPR-EGP, and the "
            "GIS User Community"
        ),
        name="Satélite (Esri)",
        overlay=False,
        control=True,
    ).add_to(mapa)

    talhao_1_coords = [
        [-21.4186, -48.2469],
        [-21.4186, -48.2419],
        [-21.4236, -48.2419],
        [-21.4236, -48.2469],
    ]
    talhao_2_coords = [
        [-21.4246, -48.2399],
        [-21.4246, -48.2339],
        [-21.4296, -48.2339],
        [-21.4296, -48.2399],
    ]

    folium.Polygon(
        locations=talhao_1_coords,
        color="green",
        weight=2,
        fill=True,
        fill_color="#2ecc71",
        fill_opacity=0.4,
        popup=(
            "<b>Talhão 01</b><br>Variedade: RB966928<br>Área: 18.5 ha"
            "<br>TCH Estimado: 85 t/ha"
        ),
        tooltip="Talhão 01 (Clique para detalhes)",
    ).add_to(mapa)

    folium.Polygon(
        locations=talhao_2_coords,
        color="orange",
        weight=2,
        fill=True,
        fill_color="#f39c12",
        fill_opacity=0.4,
        popup=(
            "<b>Talhão 02</b><br>Variedade: CTC4<br>Área: 22.0 ha"
            "<br>TCH Estimado: 92 t/ha"
        ),
        tooltip="Talhão 02 (Clique para detalhes)",
    ).add_to(mapa)

    folium.LayerControl().add_to(mapa)
    st_folium(mapa, width=700, height=500)

    st.info(
        "💡 **Dica:** Clique sobre os polígonos coloridos no mapa para "
        "visualizar os dados agronômicos de cada talhão."
    )


if __name__ == "__main__":
    app()
