import streamlit as st

# Título de la aplicación
st.title("Prueba básica de Streamlit")

# Contador interactivo
if "count" not in st.session_state:
    st.session_state.count = 0

# Botones para aumentar o resetear el contador
if st.button("Aumentar"):
    st.session_state.count += 1

if st.button("Resetear"):
    st.session_state.count = 0

# Mostrar el valor actual del contador
st.write(f"El valor actual del contador es: {st.session_state.count}")
