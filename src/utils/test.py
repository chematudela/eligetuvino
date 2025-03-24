from dotenv import load_dotenv
import os
import pandas as pd
import pytesseract
from PIL import Image
import google.generativeai as genai
import ast
import joblib

def valoravinos(delantera, trasera, precio):
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")
    genai.configure(api_key=api_key)
    
    # Cargar datasets
    X_train_dict_pais = pd.read_csv("data/datasets/processed/X_train_dict_pais.csv")
    df_selected = pd.read_csv("data/datasets/processed/X_train_selected.csv")
    df_train = pd.read_csv("data/datasets/processed/df_merged.csv")
    df = pd.read_csv("data/datasets/raw/FINAL_DF_TINTOS_PRECIO_CORREGIDO.csv")
    df_selected = df_selected.rename(columns={'País_encoded': 'País'})

    df_selected = df_selected.drop(columns="Unnamed: 0")
    df_train = df_train.drop(columns="Unnamed: 0")  
    
    # Extraer texto de imágenes
    texto_imagen1 = pytesseract.image_to_string(Image.open(delantera))
    texto_imagen2 = pytesseract.image_to_string(Image.open(trasera))
    texto_combinado = f"{texto_imagen1}\n{texto_imagen2}"
    
    # Crear tabla de contexto para LLM
    df_prompt = df_train[df_selected.columns].drop(columns="Precio")[20:30]
    tabla_texto = df_prompt.to_csv(index=False, header=True)
    
    # Construir el prompt
    prompt = f"""
        Tengo una tabla con las siguientes columnas: 'País_encoded', 'roble', 'cuero', 'polvo de vainilla', 'cereza',
        'Ligero/Poderoso', 'Carneadobada', 'Seco/Dulce', 'NerelloMascalese',
        'chocolate', 'Montepulciano', 'Cerdo', 'Quesodelechedecabra'.

        Aquí están algunos ejemplos de las filas existentes en la tabla:
        {tabla_texto}

        Ahora, completa una nueva fila basada en este texto extraído de dos imágenes:
        "{texto_combinado}"

        Devuelve solo un lista con los 13 valores separados por comas, sin encabezados. Si no puedes rellenar algún elemento, complétalo con "no encontrado". Quiero que lo devuelvas como una lista de Python.
        Intenta completar con tu criterio estimado el valor de seco/dulce y ligero/poderoso del 0 al 8.5. Que la salida sea una lista con 13 campos únicamente y nada más, tal como esta:
        ["Italia", 0, 1, 0, 0, 6.2, 0, 2.0, 0, 0, 0, 1, 0] no como esta ["['España'", '1', '1', '0', '0', '7', '0.5', '0', '0', '0', '0', '0', '0]'].
        Quiero que los números de la lista tengan formato numérico.
    """
    
    df_selected = df_selected.rename(columns={'País':'País_encoded'})

    # Llamar a la API de Gemini
    modelo = genai.GenerativeModel("gemini-1.5-pro")
    respuesta = modelo.generate_content(prompt)
    nueva_fila = ast.literal_eval(respuesta.text)
    
    # Procesar la nueva fila
    def dic_pais(nombre_pais):
        dic = dict(zip(X_train_dict_pais["País"], X_train_dict_pais["País_encoded"]))
        return  dic[nombre_pais]
    
    def conversor_precio(precio):
        return precio / df["Precio"].max()
    
    def conversor_sabor(sabor):
        return sabor / 8.5
    
    nueva_fila.insert(0, precio)
    nueva_fila= [
        conversor_precio(nueva_fila[0]), dic_pais(nueva_fila[1]), nueva_fila[2], nueva_fila[3], nueva_fila[4], nueva_fila[5],
        conversor_sabor(nueva_fila[6]), nueva_fila[7], conversor_sabor(nueva_fila[8]), nueva_fila[9], nueva_fila[10], nueva_fila[11], nueva_fila[12], nueva_fila[13]
    ]
    
    # Cargar modelo y predecir
    modelo = joblib.load("src/modelos/modelo_RF_vinos.joblib")
    prediccion = pd.DataFrame([nueva_fila], columns=df_selected.columns)
    prediccion_nota = modelo.predict(prediccion)
    return prediccion_nota

valoravinos("/Users/josetudela/Projects/EligeTuVino/eligetuvino/data/fotos/sommosdelantero.png","/Users/josetudela/Projects/EligeTuVino/eligetuvino/data/fotos/sommostrasera.png", 20)