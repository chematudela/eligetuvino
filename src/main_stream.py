import streamlit as st 
import pandas as pd 
import numpy as np
import plotly.express as px
import altair as alt
import random
from PIL import Image
import requests
from io import BytesIO
import plotly.colors as pc
from collections import Counter
import matplotlib.pyplot as plt
import seaborn as sns
import json
from utils import pagina_principal,eda_1,bodega_perfecta,vino_perfecto,estimacion_valoracion,country_mapping
from utils.Funcion_recomendación_vino import recomendador_vinos



#with open('../data/datasets/processed/country_mapping.json', 'r', encoding="utf-8") as f:
    #country_mapping = json.load(f)

st.set_page_config(
    page_title="Dashboard sobre vino mundial",
    page_icon="🍷",
    layout="wide",
    initial_sidebar_state="expanded")

alt.themes.enable("dark")

st.sidebar.title("Navegación")

pagina= st.sidebar.selectbox("Selecciona una página", ["Página principal", "EDA 1", "Bodega Perfecta","Vino perfecto","Valoración de vino", "Recomendador de vinos"])

if pagina == "Página principal":
    pagina_principal()
elif pagina == "EDA 1":
    eda_1()
elif pagina == "Bodega Perfecta":
    bodega_perfecta()
elif pagina == "Vino perfecto":
    vino_perfecto()
elif pagina == "Valoración de vino":
    estimacion_valoracion()
elif pagina == "Recomendador de vinos":
    recomendador_vinos()