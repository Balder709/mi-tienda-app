import streamlit as st
import pandas as pd
from datetime import date

# Configuración de la página
st.set_page_config(page_title="Tienda de Electrodomésticos - Examen Jose Manuel Ramirez", layout="wide")

# --- INICIALIZACIÓN DE VARIABLES DE SESIÓN ---
if 'carrito' not in st.session_state:
    st.session_state.carrito = []
if 'factura_generada' not in st.session_state:
    st.session_state.factura_generada = False

# 1. Datos del catálogo
productos = [
    {"Nombre": "Refrigeradora", "Precio": 15000.00, "Categoría": "Línea Blanca"},
    {"Nombre": "Lavadora", "Precio": 12000.00, "Categoría": "Línea Blanca"},
    {"Nombre": "Microondas", "Precio": 3500.00, "Categoría": "Cocina"},
    {"Nombre": "Licuadora", "Precio": 1200.00, "Categoría": "Cocina"},
    {"Nombre": "Aire acondicionado", "Precio": 18000.00, "Categoría": "Climatización"},
    {"Nombre": "Plancha", "Precio": 800.00, "Categoría": "Hogar"},
    {"Nombre": "Televisor", "Precio": 10000.00, "Categoría": "Electrónica"},
    {"Nombre": "Cafetera", "Precio": 2500.00, "Categoría": "Cocina"},
]

df_productos = pd.DataFrame(productos)

# --- INTERFAZ ---
st.title("⚡ Tienda de Electrodomésticos - Examen I Parcial")
st.subheader("Estudiante: José Manuel Ramirez")
st.markdown("---")

# A) Catálogo y Filtros
st.header("🛒 Catálogo de Productos")
precio_max = st.slider("Filtrar por precio máximo", 0, 20000, 20000)
df_filtrado = df_productos[df_productos["Precio"] <= precio_max]
st.dataframe(df_filtrado, use_container_width=True)

# B) Selección de productos y Carrito
col1, col2 = st.columns(2)

with col1:
    st.subheader("Selección de Compra")
    producto_nombre = st.selectbox("Seleccione un producto:", df_filtrado["Nombre"])
    info_prod = df_filtrado[df_filtrado["Nombre"] == producto_nombre].iloc[0]
    precio_unitario = info_prod["Precio"]
    cantidad = st.number_input("Cantidad:", min_value=1, value=1, step=1)
    
    if st.button("Añadir al Carrito ➕"):
        item = {
            "Producto": producto_nombre,
            "Precio Unitario": precio_unitario,
            "Cantidad": cantidad,
            "Subtotal": precio_unitario * cantidad
        }
        st.session_state.carrito.append(item)
        st.session_state.factura_generada = False # Resetear factura si agrega más cosas
        st.toast(f"{producto_nombre} añadido!")

with col2:
    st.subheader("Datos del Cliente")
    nombre_cliente = st.text_input("Nombre completo:")
    rtn_cliente = st.text_input("RTN / Identidad:")
    fecha_compra = st.date_input("Fecha de compra", date.today())
    
    if st.button("Vaciar Carrito 🗑️"):
        st.session_state.carrito = []
        st.session_state.factura_generada = False
        st.rerun()

# C) Mostrar Carrito Actual
if st.session_state.carrito:
    st.markdown("---")
    st.header("🛒 Detalle del Carrito")
    df_carrito = pd.DataFrame(st.session_state.carrito)
    st.table(df_carrito)

    # Botón para activar la factura
    if st.button("Generar Factura Final 📄"):
        if nombre_cliente == "" or rtn_cliente == "":
            st.error("Por favor, ingrese los datos del cliente.")
        else:
            st.session_state.factura_generada = True

    # D) Resumen de Facturación (Se muestra solo si se activó el estado)
    if st.session_state.factura_generada:
        st.markdown("---")
        st.header("🧾 FACTURA OFICIAL")
        
        subtotal_general = df_carrito["Subtotal"].sum()
        isv = subtotal_general * 0.15
        total_pagar = subtotal_general + isv
        
        c1, c2 = st.columns(2)
        with c1:
            st.write(f"**Cliente:** {nombre_cliente}")
            st.write(f"**RTN:** {rtn_cliente}")
            st.write(f"**Fecha:** {fecha_compra}")
        
        with c2:
            # Formateamos los números para que se vean como dinero
            resumen_data = {
                "Descripción": ["Subtotal Neto", "ISV (15%)", "TOTAL A PAGAR"],
                "Monto (L.)": [f"L. {subtotal_general:,.2f}", f"L. {isv:,.2f}", f"L. {total_pagar:,.2f}"]
            }
            st.table(pd.DataFrame(resumen_data))
        
        st.success("¡Venta procesada exitosamente!")
else:
    st.info("El carrito está vacío. Selecciona productos arriba.")
