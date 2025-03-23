import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

def vino_perfecto():
    st.title("Características del vino perfecto")
    
    # Botón para subir el archivo CSV
    uploaded_file = st.file_uploader("Elige un archivo CSV", type="csv")

    # Verificar si se ha subido un archivo
    if uploaded_file is not None:
        # Leer el archivo CSV en un DataFrame
        df = pd.read_csv(uploaded_file)
        
        st.write("Gráficos de dispersión sobre características de sabor")

        # Definir características sensoriales
        features = ['Ligero/Poderoso', 'Suave/Tánico', 'Seco/Dulce', 'Débil/Ácido']

        # Ordenar el DataFrame por valoración y tomar los 50 mejores vinos
        top_50_vinos = df.sort_values(by='Valoración', ascending=False).head(50)

        # Calcular los valores promedio de las características en los 50 mejores vinos
        mean_values = top_50_vinos[features].mean()

        # Graficar la relación entre cada característica y la valoración
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        axes = axes.flatten()

        for i, feature in enumerate(features):
            sns.scatterplot(data=df, x=feature, y='Valoración', alpha=0.5, ax=axes[i], label="Todos los vinos")
            sns.scatterplot(data=top_50_vinos, x=feature, y='Valoración', color='red', ax=axes[i], label="Top 50 vinos")
            axes[i].set_title(f'Valoración vs {feature}')
            axes[i].set_xlabel(feature)
            axes[i].set_ylabel('Valoración')

        plt.tight_layout()
        st.pyplot(fig)

        # Mostrar los valores en la aplicación
        st.write("**Valores promedio en los 50 vinos mejor valorados:**")
        for feature, value in mean_values.items():
            st.write(f"- {feature}: {value:.2f}")
        
    
    st.title("🍷 Características promedio de los 100 vinos mejor valorados")

    # Tomar los 100 mejores vinos según la valoración
    top_100_vinos = df.sort_values(by='Valoración', ascending=False).head(100)
    # Características a analizar
    features = ['Ligero/Poderoso', 'Suave/Tánico', 'Seco/Dulce', 'Débil/Ácido']

    # Calcular la media de cada característica
    media_caracteristicas = top_100_vinos[features].mean()

    # Convertir valores en lista
    values = media_caracteristicas.tolist()

    # Nombres de las características
    labels = features

        # Número de variables (lados del gráfico)
    num_vars = len(labels)

        # Ángulos para el gráfico de araña
    angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()

        # Cerrar el gráfico de araña
    values += values[:1]
    angles += angles[:1]

        # Crear la figura y los ejes en modo polar
    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))

        # Dibujar el gráfico con colores de vino
    ax.fill(angles, values, color='#8B0000', alpha=0.4)  # Relleno color vino tinto (granate)
    ax.plot(angles, values, color='#4B0000', linewidth=2)  # Bordes más oscuros (burdeos)

        # Agregar etiquetas con los valores
    for i, value in enumerate(values[:-1]):
        ax.text(angles[i], value + 0.2, f"{value:.2f}", ha='center', fontsize=10, fontweight='bold', color='#4B0000')

        # Ajustar los labels y los ticks
    ax.set_yticklabels([])  # No mostrar etiquetas en el eje radial
    ax.set_xticks(angles[:-1])  # No incluir el último ángulo porque lo hemos duplicado
    ax.set_xticklabels(labels, fontsize=12, fontweight='bold', color='#8B0000')

        # Título del gráfico
    ax.set_title('🍷 Características promedio de los 100 vinos mejor valorados', size=15, color='#4B0000', y=1.1)

        # Mostrar en Streamlit
    st.pyplot(fig)

    st.title("🍇 Correlación entre Tipos de Uva y Valoración")

    # Lista de columnas de tipos de uva
    uva_columns = ['Aglianico', 'Barbera', 'Blaufränkisch', 'CabernetFranc', 'CabernetSauvignon', 'Carignan',
                       'Cariñena', 'Corvina', 'Corvinone', 'Gamay', 'Garnacha', 'Graciano', 'Grenache', 'Malbec',
                       'Mencia', 'Merlot', 'Monastrell', 'Montepulciano', 'Mourvedre', 'Nebbiolo', 'NerelloMascalese',
                       "Nerod'Avola", 'PetitVerdot', 'PinotNero', 'PinotNoir', 'Primitivo', 'Rondinella', 'Sangiovese',
                       'Shiraz/Syrah', 'Tempranillo', 'TourigaNacional', 'Zweigelt']

        # Asegurar que las columnas son numéricas
    df[uva_columns] = df[uva_columns].apply(pd.to_numeric, errors='coerce', downcast='integer')

        # Calcular la correlación con la valoración
    correlaciones = df[uva_columns].corrwith(df['Valoración']).sort_values(ascending=False)

    tab1, tab2 = st.columns(2)

    with tab1:    # Obtener las 10 mejores correlaciones
        top_10_correlaciones = correlaciones.head(10)
    # Mostrar las 10 mejores correlaciones en la app
        st.write(top_10_correlaciones)
    with tab2:
    # Crear el gráfico de barras
        fig, ax = plt.subplots(figsize=(12, 6))
        sns.barplot(x=top_10_correlaciones.index, y=top_10_correlaciones.values, palette='magma', ax=ax)

        # Personalización del gráfico
        ax.set_title('🍷 Correlación entre Tipos de Uva y Valoración', fontsize=16)
        ax.set_xlabel('Tipo de Uva', fontsize=14)
        ax.set_ylabel('Correlación con Valoración', fontsize=14)
        ax.set_xticklabels(top_10_correlaciones.index, rotation=45, ha='right')

        # Mostrar gráfico en Streamlit
        st.pyplot(fig)