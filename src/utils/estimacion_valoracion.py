import streamlit as st
import os
from PIL import Image
import tempfile
from utils.valora_vinos import valoravinos  # Importa solo la función


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

                st.success(f"La valoración estimada del vino es: {valoracion[0]:.2f}")

                os.remove(ruta_delantera)
                os.remove(ruta_trasera)

            except ValueError:
                st.error("Por favor, ingresa un valor numérico válido para el precio.")
        else:
            st.warning("Por favor, sube ambas imágenes y proporciona el precio.")