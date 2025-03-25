import streamlit as st
import requests
from bs4 import BeautifulSoup
from sklearn.preprocessing import MinMaxScaler
from dotenv import load_dotenv
import pandas as pd
import google.generativeai as genai
import joblib






def dic_pais(nombre_pais):
    X_train_dict_pais = pd.read_csv("data/datasets/processed/X_train_dict_pais.csv")
    dic = dict(zip(X_train_dict_pais["País"], X_train_dict_pais["País_encoded"]))
    return dic[nombre_pais]

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

def recomendacion_vino(url, precio, pais):

    # Carga de datos

    X_train = pd.read_csv("data/datasets/processed/X_train_imputed.csv")
    y_train = pd.read_csv("data/datasets/processed/y_train.csv")
    X_test = pd.read_csv("data/datasets/processed/X_test_imputed.csv")
    y_test = pd.read_csv("data/datasets/processed/y_test.csv")

    df_final_tintos_corregido = pd.read_csv("data/datasets/raw/FINAL_DF_TINTOS_PRECIO_CORREGIDO.csv")

    # Cepillado de datos 

    X_train["Valoración"] = y_train["Valoración"]
    X_test["Valoración"] = y_test["Valoración"]
    df_total =  pd.concat([X_train, X_test], ignore_index=True)
    df_total["ID"] = df_total["ID"].astype(int)
    df_total["Precio"] = df_total["Precio"].astype(float)
    df_total_cluster = df_total.drop(columns=["Unnamed: 0","ID","Precio"])
    


    # Escalado de datos
    scaler = MinMaxScaler()  # Crear el escalador
    df_total_scaled = pd.DataFrame(scaler.fit_transform(df_total_cluster), columns=df_total_cluster.columns)

    # Importamos el modelo kmeans
    model_KM = joblib.load("src/modelos/kmeans_model.pkl")
    predictions = model_KM.predict(df_total_scaled)

    # Añadimos la columna cluster al dataset
    df_total["cluster"] = predictions

    # Obtenemos la id del vino
    id = df_final_tintos_corregido.loc[df_final_tintos_corregido["Url"] == url, "ID"].values[0]
    id = int(id)

    # Obtenemos el cluster del vino asociado a la url
    cluster = df_total[df_total["ID"] == id]["cluster"].iloc[0]

   
    if pais == "Cualquier sitio":
        indice_min_precio = df_total[(df_total["cluster"] == cluster)]["Precio"].idxmin()
        fila_min_precio = df_total.loc[indice_min_precio]
        url_precion_min = df_final_tintos_corregido[df_final_tintos_corregido["ID"] == fila_min_precio["ID"].astype(int).astype(str)]["Url"]

        df_total_limite_precio = df_total[df_total["Precio"] < precio]
        indice_max_valoración = df_total_limite_precio[(df_total_limite_precio["cluster"] == cluster)]["Valoración"].idxmax()
        fila_max_valoracion = df_total.iloc[indice_max_valoración]
        url_max_val = df_final_tintos_corregido[df_final_tintos_corregido["ID"] == fila_max_valoracion["ID"].astype(int).astype(str)]["Url"]


    else:
   
        indice_min_precio = df_total[(df_total["cluster"] == cluster)&(df_total["País_encoded"] == dic_pais(pais))]["Precio"].idxmin()
        fila_min_precio = df_total.loc[indice_min_precio]
        url_precion_min = df_final_tintos_corregido[df_final_tintos_corregido["ID"] == fila_min_precio["ID"].astype(int).astype(str)]["Url"]
        

        # Cálculo de la url de máxima valoración para un precio dado
        df_total_limite_precio = df_total[df_total["Precio"] < precio]
        indice_max_valoración = df_total_limite_precio[(df_total_limite_precio["cluster"] == cluster) & (df_total["País_encoded"]==dic_pais(pais))]["Valoración"].idxmax()
        fila_max_valoracion = df_total.iloc[indice_max_valoración]
        url_max_val = df_final_tintos_corregido[df_final_tintos_corregido["ID"] == fila_max_valoracion["ID"].astype(int).astype(str)]["Url"]

        
    return url_precion_min.values[0], url_max_val.values[0]

def mostrar_tabla_vinos(Url1, Url2, df_mostrar_vinos):
    urls = [Url1, Url2]
    data = []
    
    for url in urls:
        if url is None:
            continue
        vino_info = df_mostrar_vinos[df_mostrar_vinos["Url"].fillna("").astype(str).str.strip() == str(url).strip()]
        if not vino_info.empty:
            img_url = obtener_imagen_vino(url)
            data.append({
                "Imagen": f"![Vino]({img_url})" if img_url else "No disponible",
                "Bodega": vino_info["Bodega"].values[0],
                "Región": vino_info["Región"].values[0],
                "País": vino_info["País"].values[0],
                "Precio": vino_info["Precio"].values[0],
                "URL": url
            })
    
    if data:
        df_display = pd.DataFrame(data)
        st.markdown(df_display.to_markdown(index=False), unsafe_allow_html=True)
    else:
        st.write("No se encontraron vinos recomendados.")



def recomendador_vinos():
    
    df_final_tintos_corregido = pd.read_csv("data/datasets/raw/FINAL_DF_TINTOS_PRECIO_CORREGIDO.csv")
    
    st.title('Buscar Vino 🍷')
    st.write(""" 
        ¡Bienvenido a la aplicación de búsqueda de vinos! 🍇  
        Selecciona un país (o "Cualquier sitio") y luego introduce la URL de un vino y su precio para obtener recomendaciones.  
    """)

  # Seleccionar el país o "Cualquier sitio"
    paises_disponibles = ["Cualquier sitio"] + list(df_final_tintos_corregido["País"].unique())  # Incluye la opción "Cualquier sitio"
    pais_seleccionado = st.selectbox("Selecciona el país de los vinos:", paises_disponibles).strip()


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
            url_precio_min, url_max_val = recomendacion_vino(url, precio, pais_seleccionado)
            mostrar_tabla_vinos(url_precio_min, url_max_val, df_final_tintos_corregido)