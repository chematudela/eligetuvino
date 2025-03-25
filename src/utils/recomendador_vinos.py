import streamlit as st
import pandas as pd
import joblib
import requests
from bs4 import BeautifulSoup
from sklearn.preprocessing import MinMaxScaler

def cargar_datos():
    X_train = pd.read_csv("data/datasets/processed/X_train_imputed.csv")
    y_train = pd.read_csv("data/datasets/processed/y_train.csv")
    X_test = pd.read_csv("data/datasets/processed/X_test_imputed.csv")
    y_test = pd.read_csv("data/datasets/processed/y_test.csv")
    df_final_tintos_corregido = pd.read_csv("data/datasets/raw/FINAL_DF_TINTOS_PRECIO_CORREGIDO.csv")

    X_train["Valoración"] = y_train["Valoración"]
    X_test["Valoración"] = y_test["Valoración"]
    df_total = pd.concat([X_train, X_test], ignore_index=True)
    
    df_total["ID"] = df_total["ID"].astype(int)
    df_total["Precio"] = df_total["Precio"].astype(float)
    df_total_cluster = df_total.drop(columns=["Unnamed: 0", "ID", "Precio"], errors='ignore')
    
    return df_total, df_total_cluster, df_final_tintos_corregido

def obtener_imagen_vino(url):
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            img_tag = soup.find("img", class_="wineLabel-module__image--3HOnd")
            if img_tag and "src" in img_tag.attrs:
                img_url = img_tag["src"]
                if img_url.startswith("//"):
                    img_url = "https:" + img_url  # Completar la URL si es relativa
                return img_url
    except Exception as e:
        print(f"Error obteniendo la imagen: {e}")
    return None

def recomendacion_vino(url, precio, df_total, df_total_cluster, df_final_tintos_corregido):
    scaler = MinMaxScaler()
    df_total_scaled = pd.DataFrame(scaler.fit_transform(df_total_cluster), columns=df_total_cluster.columns)

    model_KM = joblib.load("src/modelos/kmeans_model.pkl")
    df_total["cluster"] = model_KM.predict(df_total_scaled)

    df_final_tintos_corregido = df_final_tintos_corregido[pd.to_numeric(df_final_tintos_corregido["ID"], errors='coerce').notna()]
    df_final_tintos_corregido["ID"] = df_final_tintos_corregido["ID"].astype(int)
    df_total["ID"] = df_total["ID"].astype(int)

    id_vino = df_final_tintos_corregido.loc[df_final_tintos_corregido["Url"].str.strip() == url.strip(), "ID"].values
    if len(id_vino) == 0:
        return None, None
    id_vino = int(id_vino[0])

    if id_vino not in df_total["ID"].values:
        return None, None

    cluster = df_total.loc[df_total["ID"] == id_vino, "cluster"].iloc[0]
    vinos_cluster = df_total[df_total["cluster"] == cluster]
    if vinos_cluster.empty:
        return None, None
    
    indice_min_precio = vinos_cluster["Precio"].idxmin()
    url_precio_min = df_final_tintos_corregido.loc[df_final_tintos_corregido["ID"] == df_total.loc[indice_min_precio, "ID"], "Url"]

    df_total_limite_precio = df_total[(df_total["Precio"] < precio) & (df_total["cluster"] == cluster)]
    if df_total_limite_precio.empty:
        return url_precio_min.values[0] if not url_precio_min.empty else None, None

    indice_max_valoracion = df_total_limite_precio["Valoración"].idxmax()
    url_max_val = df_final_tintos_corregido.loc[df_final_tintos_corregido["ID"] == df_total.loc[indice_max_valoracion, "ID"], "Url"]

    return url_precio_min.values[0] if not url_precio_min.empty else None, url_max_val.values[0] if not url_max_val.empty else None

def mostrar_tabla_vinos(urls, df_final_tintos_corregido):
    data = []
    for url in urls:
        if url is None:
            continue
        vino_info = df_final_tintos_corregido[df_final_tintos_corregido["Url"].str.strip() == url.strip()]
        if not vino_info.empty:
            img_url = obtener_imagen_vino(url)
            data.append({
                "Imagen": f"![Vino]({img_url})" if img_url else "No disponible",
                "Bodega": vino_info["Bodega"].values[0],
                "Región": vino_info["Región"].values[0],
                "País": vino_info["País"].values[0],
                "Precio":vino_info["Precio"].values[0],
                "URL": url
            })

    if data:
        df_display = pd.DataFrame(data)
        st.markdown(df_display.to_markdown(index=False), unsafe_allow_html=True)
    else:
        st.write("No se encontraron vinos recomendados.")

def recomendador_vinos():
    st.title('Buscar Vino 🍷')
    st.write(""" 
        ¡Bienvenido a la aplicación de búsqueda de vinos! 🍇  
        Selecciona un país (o "Cualquier sitio") y luego introduce la URL de un vino y su precio para obtener recomendaciones.  
    """)

    # Cargar datos
    df_total, df_total_cluster, df_final_tintos_corregido = cargar_datos()

    # Seleccionar el país o "Cualquier sitio"
    paises_disponibles = ["Cualquier sitio"] + list(df_final_tintos_corregido["País"].unique())  # Incluye la opción "Cualquier sitio"
    pais_seleccionado = st.selectbox("Selecciona el país de los vinos:", paises_disponibles)

    # Filtrar vinos según el país seleccionado
    if pais_seleccionado == "Cualquier sitio":
        df_final_pais = df_final_tintos_corregido  # No aplicar filtro de país
    else:
        df_final_pais = df_final_tintos_corregido[df_final_tintos_corregido["País"] == pais_seleccionado]
    
    # Pedir la URL y el precio
    url = st.text_input("Introduce la URL del vino:")
    precio = st.number_input("Introduce el precio límite:", min_value=0.0, value=40.0, step=1.0)

    if st.button("Recomendar Vino"):
        # Si no hay vinos disponibles en el país seleccionado, mostrar mensaje
        if df_final_pais.empty:
            st.write(f"No hay vinos disponibles para el país seleccionado ({pais_seleccionado}).")
        else:
            url_precio_min, url_max_val = recomendacion_vino(url, precio, df_total, df_total_cluster, df_final_pais)
            mostrar_tabla_vinos([url_precio_min, url_max_val], df_final_pais)