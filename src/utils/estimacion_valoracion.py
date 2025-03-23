import streamlit as st

def estimacion_valoracion():
    st.title("Subir y mostrar imagen")

    # Widget para subir la imagen
    uploaded_file = st.file_uploader("Sube una etiqueta de vino DE FRENTE", type=["png", "jpg", "jpeg"])

    # Si se sube una imagen, se muestra en pantalla
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        delantera = image.resize((200, 200))

        # Mostrar la imagen redimensionada y centrada
        st.image(delantera, caption="Etiqueta delantera de vino subida", use_container_width=False)
    
    uploaded_file = st.file_uploader("Sube una etiqueta de vino TRASERA", type=["png", "jpg", "jpeg"])

    # Si se sube una imagen, se muestra en pantalla
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        trasera = image.resize((200, 200))

        # Mostrar la imagen redimensionada y centrada
        st.image(trasera, caption="Etiqueta trasera de vino subida", use_container_width=False)

    precio = st.text_input("¿Cuál es el precio del vino?")

    # Mostrar el precio ingresado
    if precio:
        try:
            precio_float = float(precio)  # Convertir el precio a float
            st.write(f"El precio ingresado es: ${precio_float:.2f}")
        except ValueError:
            st.error("Por favor, ingresa un valor numérico válido para el precio.")