import pandas as pd
import joblib
from sklearn.preprocessing import MinMaxScaler


# Carga de datos

X_train = pd.read_csv("/Users/josetudela/Projects/EligeTuVino/eligetuvino/data/datasets/processed/X_train_imputed.csv")
y_train = pd.read_csv("/Users/josetudela/Projects/EligeTuVino/eligetuvino/data/datasets/processed/y_train.csv")
X_test = pd.read_csv("/Users/josetudela/Projects/EligeTuVino/eligetuvino/data/datasets/processed/X_test_imputed.csv")
y_test = pd.read_csv("/Users/josetudela/Projects/EligeTuVino/eligetuvino/data/datasets/processed/y_test.csv")

df_final_tintos_corregido = pd.read_csv("/Users/josetudela/Projects/EligeTuVino/eligetuvino/data/datasets/raw/FINAL_DF_TINTOS_PRECIO_CORREGIDO.csv")

# Cepillado de datos 

X_train["Valoración"] = y_train["Valoración"]
X_test["Valoración"] = y_test["Valoración"]
df_total =  pd.concat([X_train, X_test], ignore_index=True)
df_total["ID"] = df_total["ID"].astype(int)
df_total["Precio"] = df_total["Precio"].astype(float)
df_total_cluster = df_total.drop(columns=["Unnamed: 0","ID","Precio"])

def recomendacion_vino(url, precio):

    # Escalado de datos
    scaler = MinMaxScaler()  # Crear el escalador
    df_total_scaled = pd.DataFrame(scaler.fit_transform(df_total_cluster), columns=df_total_cluster.columns)

    # Importamos el modelo kmeans
    model_KM = joblib.load("src/kmeans_model.pkl")
    predictions = model_KM.predict(df_total_scaled)

    # Añadimos la columna cluster al dataset
    df_total["cluster"] = predictions

    # Obtenemos la id del vino
    id = df_final_tintos_corregido.loc[df_final_tintos_corregido["Url"] == url, "ID"].values[0]
    id = int(id)

    # Obtenemos el cluster del vino asociado a la url
    cluster = df_total[df_total["ID"] == id]["cluster"].iloc[0]

    # Cálculo de la url de mínimo precio
    indice_min_precio = df_total[df_total["cluster"] == cluster]["Precio"].idxmin()
    fila_min_precio = df_total.loc[indice_min_precio]
    url_precion_min = df_final_tintos_corregido[df_final_tintos_corregido["ID"] == fila_min_precio["ID"].astype(int).astype(str)]["Url"]

    # Cálculo de la url de máxima valoración para un precio dado
    df_total_limite_precio = df_total[df_total["Precio"] < precio]
    indice_max_valoración = df_total_limite_precio[df_total_limite_precio["cluster"] == cluster]["Valoración"].idxmax()
    fila_max_valoracion = df_total.iloc[indice_max_valoración]
    url_max_val = df_final_tintos_corregido[df_final_tintos_corregido["ID"] == fila_max_valoracion["ID"].astype(int).astype(str)]["Url"]

    return url_precion_min, url_max_val

print(recomendacion_vino("https://www.vivino.com/ES/es/vega-sicilia-unico-reserva-especial-edicion/w/77136",40))