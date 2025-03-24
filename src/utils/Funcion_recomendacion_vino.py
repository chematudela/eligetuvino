import streamlit as st
import pandas as pd
import joblib
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

def recomendacion_vino(url, precio, df_total, df_total_cluster, df_final_tintos_corregido):
    scaler = MinMaxScaler()
    df_total_scaled = pd.DataFrame(scaler.fit_transform(df_total_cluster), columns=df_total_cluster.columns)
    
    model_KM = joblib.load("src/kmeans_model.pkl")
    df_total["cluster"] = model_KM.predict(df_total_scaled)
    
    id_vino = df_final_tintos_corregido.loc[df_final_tintos_corregido["Url"] == url, "ID"].values
    if len(id_vino) == 0:
        return "URL no encontrada", ""
    id_vino = int(id_vino[0])
    
    cluster = df_total.loc[df_total["ID"] == id_vino, "cluster"].iloc[0]
    
    indice_min_precio = df_total[df_total["cluster"] == cluster]["Precio"].idxmin()
    url_precio_min = df_final_tintos_corregido.loc[df_final_tintos_corregido["ID"] == df_total.loc[indice_min_precio, "ID"].astype(str), "Url"]
    
    df_total_limite_precio = df_total[df_total["Precio"] < precio]
    if df_total_limite_precio.empty:
        return url_precio_min.values[0] if not url_precio_min.empty else "No encontrado", "No hay vinos por debajo de ese precio"
    
    indice_max_valoracion = df_total_limite_precio[df_total_limite_precio["cluster"] == cluster]["Valoración"].idxmax()
    url_max_val = df_final_tintos_corregido.loc[df_final_tintos_corregido["ID"] == df_total.loc[indice_max_valoracion, "ID"].astype(str), "Url"]
    
    return url_precio_min.values[0] if not url_precio_min.empty else "No encontrado", url_max_val.values[0] if not url_max_val.empty else "No encontrado"