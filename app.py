import streamlit as st
import pandas as pd
from datetime import date

# Configuración de la página
st.set_page_config(page_title="Tienda de Electrodomésticos - Examen Jose Manuel Ramirez Casco", layout="wide")

# 1. Datos del catálogo (Mínimo 8 productos)
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
st.markdown("---")

# A) Catálogo y Filtros
st.header("🛒 Catálogo de Productos")
precio_max = st.slider("Filtrar por precio máximo", 0, 20000, 20000)
df_filtrado = df_productos[df_productos["Precio"] <= precio_max]

st.dataframe(df_filtrado, use_container_width=True)

# B) Selección de productos
col1, col2 = st.columns(2)

with col1:
    st.subheader("Selección de Compra")
    producto_nombre = st.selectbox("Seleccione un producto:", df_filtrado["Nombre"])
    # Obtener info del producto seleccionado
    info_prod = df_filtrado[df_filtrado["Nombre"] == producto_nombre].iloc[0]
    precio_unitario = info_prod["Precio"]
    
    cantidad = st.number_input("Cantidad:", min_value=1, value=1, step=1)
    subtotal_prod = precio_unitario * cantidad
    
    st.write(f"**Precio Unitario:** L. {precio_unitario:,.2f}")
    st.write(f"**Subtotal del producto:** L. {subtotal_prod:,.2f}")

# C) Datos del Cliente
with col2:
    st.subheader("Datos del Cliente")
    nombre_cliente = st.text_input("Nombre completo:")
    rtn_cliente = st.text_input("RTN / Identidad:")
    fecha_compra = st.date_input("Fecha de compra", date.today())

# D) Resumen de Facturación
st.markdown("---")
if st.button("Generar Factura"):
    if nombre_cliente == "" or rtn_cliente == "":
        st.error("Por favor, ingrese los datos del cliente.")
    else:
        st.header("📄 Resumen de Facturación")
        
        # Cálculos finales
        isv = subtotal_prod * 0.15
        total_pagar = subtotal_prod + isv
        
        # Mostrar factura en un formato limpio
        c1, c2 = st.columns(2)
        with c1:
            st.write(f"**Cliente:** {nombre_cliente}")
            st.write(f"**RTN:** {rtn_cliente}")
            st.write(f"**Fecha:** {fecha_compra}")
        
        with c2:
            st.write(f"**Producto:** {producto_nombre}")
            st.write(f"**Cantidad:** {cantidad}")
            st.table(pd.DataFrame({
                "Descripción": ["Subtotal General", "ISV (15%)", "TOTAL A PAGAR"],
                "Monto (L.)": [f"{subtotal_prod:,.2f}", f"{isv:,.2f}", f"**{total_pagar:,.2f}**"]
            }))
        
        st.success("¡Factura generada con éxito!")