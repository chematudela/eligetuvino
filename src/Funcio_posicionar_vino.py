from dotenv import load_dotenv
import os
from tqdm import tqdm
import pandas as pd
import pytesseract
from PIL import Image
import pandas as pd
import os
import google.generativeai as genai
import ast
import joblib

# Importación y cepillado de set de datos
X_train_dict_pais = pd.read_csv("/Users/josetudela/Projects/EligeTuVino/eligetuvino/Archivos/X_train_dict_pais.csv")
df_selected = pd.read_csv("/Users/josetudela/Projects/EligeTuVino/eligetuvino/Archivos/X_train_selected.csv")
df_train = pd.read_csv("/Users/josetudela/Projects/EligeTuVino/eligetuvino/Archivos/df_merged.csv")
df = pd.read_csv("/Users/josetudela/Projects/EligeTuVino/eligetuvino/Archivos/FINAL_DF_TINTOS_PRECIO_CORREGIDO.csv")
df_selected = df_selected.rename(columns={'País_encoded': 'País'})


# Función para extraer texto de una imagen
def extraer_texto_de_imagen(ruta_imagen):
    imagen = Image.open(ruta_imagen)
    texto = pytesseract.image_to_string(imagen)
    return texto


#Funciones para convertir variables proporcianadas por LLM a formato numérico usado por nuestro modelo
def dic_pais(nombre_pais):
    dic = dict(zip(X_train_dict_pais["País"], X_train_dict_pais["País_encoded"]))
    return dic[nombre_pais]

def conversor_precio(precio):
    return precio/df["Precio"].max()

def conversor_sabor(sabor):
    return sabor/8.5

def valora_tu_vino(delantera,trasera,precio):
    
    #Funciones para convertir variables proporcianadas por LLM a formato numérico usado por nuestro modelo
    def dic_pais(nombre_pais):
        dic = dict(zip(X_train_dict_pais["País"], X_train_dict_pais["País_encoded"]))
        return dic[nombre_pais]
    
    def conversor_precio(precio):
        return precio/df["Precio"].max()

    def conversor_sabor(sabor):
        return sabor/8.5

    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")

    # Configurar la API de Gemini
    genai.configure(api_key=api_key)


    # Importación y cepillado de set de datos
    X_train_dict_pais = pd.read_csv("/Users/josetudela/Projects/EligeTuVino/eligetuvino/Archivos/X_train_dict_pais.csv")
    df_selected = pd.read_csv("/Users/josetudela/Projects/EligeTuVino/eligetuvino/Archivos/X_train_selected.csv")
    df_train = pd.read_csv("/Users/josetudela/Projects/EligeTuVino/eligetuvino/Archivos/df_merged.csv")
    df = pd.read_csv("/Users/josetudela/Projects/EligeTuVino/eligetuvino/Archivos/FINAL_DF_TINTOS_PRECIO_CORREGIDO.csv")
    df_selected = df_selected.rename(columns={'País_encoded': 'País'})
    
    
    # Creación de tabla de contexto para guíar al LLM
    df_prompt = df_train[df_selected.columns]
    df_prompt = df_prompt.drop(columns="Precio")
    df_prompt = df_prompt[20:30]

    

    # Configurar la API de Gemini
    genai.configure(api_key=api_key)

  
    # Cargar y extraer texto de las dos imágenes
    ruta_imagen1 = delantera
    ruta_imagen2 = trasera

    texto_imagen1 = extraer_texto_de_imagen(ruta_imagen1)
    texto_imagen2 = extraer_texto_de_imagen(ruta_imagen2)

    # Combinamos el texto de ambas imágenes
    texto_combinado = f"{texto_imagen1}\n{texto_imagen2}"

    # Definir un DataFrame vacío con las columnas que esperas
    tabla_texto = df_prompt.to_csv(index=False, header=True)



    # Construir el prompt para Gemini
    prompt = f"""
        Tengo una tabla con las siguientes columnas: 'País', 'roble', 'cuero', 'polvo de vainilla', 'cereza',
        'Ligero/Poderoso', 'Carneadobada', 'Seco/Dulce', 'NerelloMascalese',
        'chocolate', 'Montepulciano', 'Cerdo', 'Quesodelechedecabra'.

        Aquí están algunos ejemplos de las filas existentes en la tabla:
        {tabla_texto}

        Ahora, completa una nueva fila basada en este texto extraído de dos imágenes:
        "{texto_combinado}"

        Devuelve solo un lista con los 13 valores separados por comas, sin encabezados. Si no puedes rellenar algún elemento, complétalo con "no encontrado". Quiero que lo devuelvas como una lista de Python.
        intenta completar con tu criterio estimado el valor de seco/dulce y ligero/poderoso del 0 al 10. que la salida sea una lista con 12 campos únicamente y nada más, tal como esta [1,	Italia,	0,	1,	0,	6.2,	2.0,	0,	0,	0,	1,	0] no como esta ["['España'", '1', '1', '0', '0', '7', '0.5', '0', '0', '0', '0', '0', '0]']. Quiero que los números de la lista tengan formato numerico.
        """

    # Llamar a la API de Gemini
    modelo = genai.GenerativeModel("gemini-1.5-pro")
    respuesta = modelo.generate_content(prompt)

    # Sacar y adecuar la respuesta del LLM para meter en nuestro modelo
    nueva_fila = ast.literal_eval(respuesta.text)

    nueva_fila = nueva_fila.insert(0,precio) #falta guardar la variable que se meterá por pantalla

    nueva_fila = [conversor_precio(nueva_fila[0]),dic_pais(nueva_fila[1]), 1, 0, 0, 0, conversor_sabor(nueva_fila[6]), conversor_sabor(nueva_fila[7]), 0, 0, 0, 0, 0, 0]

    prediccion = pd.DataFrame([nueva_fila], columns=df_selected.columns)
    
    # Cargar el modelo y hacer la predicción
    modelo = joblib.load("random_forest_model.joblib")

    prediccion_nota = modelo.predict(prediccion)

    return prediccion_nota






