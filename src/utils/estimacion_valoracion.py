import streamlit as st
import os
from PIL import Image
import tempfile
from utils.valora_vinos import valoravinos  # Importa solo la función
import pandas as pd



def estimacion_valoracion():
    
    uploaded_file_delantera = st.file_uploader("Sube una etiqueta de vino DE FRENTE", type=["png", "jpg", "jpeg"])
    uploaded_file_trasera = st.file_uploader("Sube una etiqueta de vino TRASERA", type=["png", "jpg", "jpeg"])
    precio = st.text_input("¿Cuál es el precio del vino?")

    if st.button("Calcular valoración"):
        if uploaded_file_delantera and uploaded_file_trasera and precio:
            try:
                precio_float = float(precio)

                with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as temp_delantera:
                    image_delantera = Image.open(uploaded_file_delantera)
                    image_delantera.save(temp_delantera.name)
                    ruta_delantera = temp_delantera.name
                   

                with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as temp_trasera:
                    image_trasera = Image.open(uploaded_file_trasera)
                    image_trasera.save(temp_trasera.name)
                    ruta_trasera = temp_trasera.name

                valoracion = valoravinos(ruta_delantera, ruta_trasera, precio_float)

                #st.success(f"La valoración estimada del vino es: {valoracion[0]:.2f}")
                st.markdown(
                    f"""
                    <div style="
                        background-color:#4B0F24;
                        padding: 15px;
                        border-radius: 10px;
                        text-align: center;
                        color: white;
                        font-size: 24px;
                    ">
                        🍷 <b>La valoración estimada para este vino es:</b> <br>
                        <span style="font-size: 32px;">⭐ {valoracion[0]:.1f}/5 ⭐</span>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                os.remove(ruta_delantera)
                os.remove(ruta_trasera)

            except ValueError:
                st.error("Por favor, ingresa un valor numérico válido para el precio.")
        else:
            st.warning("Por favor, sube ambas imágenes y proporciona el precio.")


               # Métricas del modelo
    metricas = pd.DataFrame({
        "Métrica": ["R²", "MAPE"],
        "Train": [0.73, 2.90],
        "Test": [0.61, 3.51],
    })
    st.markdown("### Métricas finales del modelo")
    st.table(metricas.set_index("Métrica"))