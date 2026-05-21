# -*- coding: utf-8 -*-
"""
Created on Thu May 21 10:12:30 2026

@author: petuser
"""

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# 1. Configuración de la página web
st.set_page_config(page_title="Laboratorio Virtual - Unidad 0", layout="wide")

st.title("🔬 Laboratorio Virtual: Fundamentos Matemáticos")
st.write("Bienvenido al módulo interactivo de nivelación. Modificá los controles de cada sección para ver cómo se transforman los gráficos en tiempo real.")
st.markdown("---")

# 2. Creamos dos columnas
col1, col2 = st.columns(2)

# --- COLUMNA 1: DECAIMIENTO EXPONENCIAL ---
with col1:
    st.header("1. Comportamiento Exponencial Negativo")
    st.write(r"Esencial para comprender el futuro concepto de decaimiento radiactivo ($A = A_0 \cdot e^{-\lambda \cdot t}$).")
    
    a0 = st.slider("Actividad Inicial (A0):", min_value=10, max_value=1000, value=100, step=10)
    t_medio = st.slider("Período de Semidesintegración (T 1/2) en horas:", min_value=1.0, max_value=24.0, value=6.0, step=0.5)
    escala = st.radio("Seleccioná la Escala del eje Y:", ["Lineal Decimal", "Logarítmica (Semilog)"])
    
    t = np.linspace(0, 50, 500)
    lam = np.log(2) / t_medio
    A = a0 * np.exp(-lam * t)
    
    fig1, ax1 = plt.subplots(figsize=(6, 4))
    ax1.plot(t, A, color='crimson', lw=3, label=f"λ = {lam:.4f} h⁻¹")
    ax1.set_xlabel("Tiempo (horas)", fontsize=10)
    ax1.set_ylabel("Actividad (Bq / cpm)", fontsize=10)
    ax1.grid(True, which="both", ls="--", alpha=0.5)
    ax1.legend()
    
    if escala == "Logarítmica (Semilog)":
        ax1.set_yscale('log')
        ax1.set_ylim(bottom=0.1)
    else:
        ax1.set_ylim(bottom=0)
        
    st.pyplot(fig1)

# --- COLUMNA 2: FILTRADO DE IMÁGENES ---
with col2:
    st.header("2. Análisis de Frecuencias y Filtrado")
    st.write("Introducción visual al Análisis de Fourier. Así es como los algoritmos limpian el ruido de fondo en los estudios de SPECT y PET.")
    
    filtro = st.select_slider("Seleccioná el tipo de Filtro Matemático:", 
                              options=["Sin Filtro (Señal Ruidosa)", "Filtro Suave (Pasa-Bajos)", "Filtro Estricto (Señal Limpia)"])
    
    x = np.linspace(0, 10, 500)
    senal_limpia = np.sin(2 * np.pi * 0.2 * x)
    ruido = 0.4 * np.sin(2 * np.pi * 3.0 * x) + 0.2 * np.sin(2 * np.pi * 5.0 * x)
    
    fig2, ax2 = plt.subplots(figsize=(6, 4))
    
    if filtro == "Sin Filtro (Señal Ruidosa)":
        ax2.plot(x, senal_limpia + ruido, color='orange', lw=2, label="Imagen Cruda (Alta Frecuencia / Ruido)")
        ax2.plot(x, senal_limpia, color='black', ls='--', alpha=0.7, label="Información Clínica Real")
    elif filtro == "Filtro Suave (Pasa-Bajos)":
        ax2.plot(x, senal_limpia + 0.3 * ruido, color='royalblue', lw=2, label="Filtrado Intermedio")
        ax2.plot(x, senal_limpia, color='black', ls='--', alpha=0.7, label="Información Clínica Real")
    else:
        ax2.plot(x, senal_limpia, color='forestgreen', lw=2.5, label="Frecuencias Altas Eliminadas por Completo")
        
    ax2.set_xlabel("Espacio (Píxeles de la Matriz)", fontsize=10)
    ax2.set_ylabel("Intensidad de la Señal", fontsize=10)
    ax2.grid(True, ls="--", alpha=0.5)
    ax2.legend()
    
    st.pyplot(fig2)