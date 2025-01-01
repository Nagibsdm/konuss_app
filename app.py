import streamlit as st
import random
import smtplib
from email.mime.text import MIMEText

# Configuración del correo
EMAIL = "asdfksnd57@gmail.com"
PASSWORD = "ckrj hrve aasd kncd"
TO_EMAIL = "konussfactory@gmail.com"

# Configuración inicial del estado
if "quantities" not in st.session_state:
    st.session_state["quantities"] = {product["name"]: 0 for product in [
        {"name": "Margarita", "price": 3.90},
        {"name": "Margarita con Jamón", "price": 3.90},
        {"name": "Campagnola", "price": 3.90},
        {"name": "Vegetariana", "price": 3.90},
        {"name": "Pepperoni", "price": 3.90}
    ]}
if "order_id" not in st.session_state:
    st.session_state["order_id"] = None
if "total" not in st.session_state:
    st.session_state["total"] = 0.0

# Catálogo de productos
products = [
    {"name": "Margarita", "price": 3.90, "description": "🍅 Salsa y mozzarella. Un clásico irresistible."},
    {"name": "Margarita con Jamón", "price": 3.90, "description": "🍖 Salsa, mozzarella y jamón. Delicioso."},
    {"name": "Campagnola", "price": 3.90, "description": "🌽 Salsa, mozzarella, jamón y maíz. Sabores únicos."},
    {"name": "Vegetariana", "price": 3.90, "description": "🥬 Salsa, mozzarella, cebolla y champiñones. Fresca."},
    {"name": "Pepperoni", "price": 3.90, "description": "🍕 Salsa, mozzarella y pepperoni. La que nunca falla."}
]

# Función para generar un ID único de pedido
def generate_order_id():
    return f"KON-{random.randint(1000, 9999)}"

# Función para enviar el pedido por correo
def send_order_email(order_id, cart, customer_name, customer_phone, customer_address):
    subject = f"Nuevo Pedido - {order_id}"
    body = f"""
    Nuevo Pedido Realizado:

    Orden ID: {order_id}
    Cliente: {customer_name}
    Teléfono: {customer_phone}
    Dirección: {customer_address}

    Detalles del Pedido:
    """
    total = 0
    for product_name, quantity in cart.items():
        product = next((p for p in products if p["name"] == product_name), None)
        if product and quantity > 0:
            subtotal = product["price"] * quantity
            total += subtotal
            body += f"- {product_name}: {quantity} x ${product['price']:.2f} = ${subtotal:.2f}\n"
    body += f"\nTotal: ${total:.2f}"

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = EMAIL
    msg["To"] = TO_EMAIL

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(EMAIL, PASSWORD)
            server.sendmail(EMAIL, TO_EMAIL, msg.as_string())
        st.success("¡Pedido enviado por correo exitosamente! 🚀")
    except Exception as e:
        st.error(f"❌ Error al enviar el correo: {e}")

# Estilo CSS actualizado
st.markdown("""
<style>
/* Fondo principal claro */
.stApp {
    background: linear-gradient(to bottom, #f9f9f9, #ffffff);
    font-family: 'Poppins', sans-serif;
    color: #000000 !important; /* Texto negro predeterminado */
    padding: 10px; /* Espaciado interno para pantallas más pequeñas */
}

/* Texto general */
body, div, p, span, label, h1, h2, h3, h4, h5, h6 {
    color: #000000 !important; /* Forzar texto negro */
    margin: 0; /* Reducir márgenes para mejor ajuste */
}

/* Estilo para separadores de sección */
.section-title {
    background-color: #e63946; /* Fondo rojo */
    color: white; /* Texto blanco */
    font-size: 18px; /* Ajuste de tamaño de fuente para pantallas pequeñas */
    font-weight: bold;
    text-align: center;
    padding: 8px; /* Reducción de padding */
    border-radius: 10px;
    margin-bottom: 15px; /* Espaciado menor */
    box-shadow: 0px 3px 5px rgba(0, 0, 0, 0.1);
}

/* Entradas de texto y áreas */
input, textarea {
    background-color: #ffffff !important; /* Fondo blanco */
    color: #000000 !important; /* Texto negro */
    border: 2px solid #e63946 !important; /* Borde rojo */
    border-radius: 8px !important; /* Bordes redondeados */
    padding: 8px !important; /* Reducción de padding */
    font-size: 14px !important; /* Ajuste de fuente */
    width: 100%; /* Asegura que ocupe el ancho completo */
    box-sizing: border-box; /* Previene desbordamiento horizontal */
}
input:focus, textarea:focus {
    outline: none !important;
    border: 2px solid #c22834 !important; /* Color del borde al enfocarse */
    box-shadow: 0px 0px 5px rgba(226, 57, 70, 0.5) !important;
}

/* Botones al lado del producto */
.stButton>button {
    background-color: #e63946; /* Fondo rojo */
    color: white; /* Texto blanco */
    border-radius: 8px; /* Botón ligeramente redondeado */
    padding: 5px 10px; /* Tamaño ajustado */
    font-size: 12px; /* Fuente más pequeña */
    border: none;
    box-shadow: 0px 3px 5px rgba(0, 0, 0, 0.1);
    margin-left: 10px; /* Espacio entre botón y texto */
}
.stButton>button:hover {
    background-color: #c22834; /* Cambio de color al pasar el mouse */
}

/* Ocultar header y footer innecesarios */
header, footer {
    visibility: hidden;
}
</style>
""", unsafe_allow_html=True)


# Encabezado
st.markdown("<h1 class='header'>🍕 Konuss - ¡Ahora la pizza se come en cono! 🎉</h1>", unsafe_allow_html=True)

# Sección Menú
st.markdown("<div class='section-title'>📋 Menú</div>", unsafe_allow_html=True)
for product in products:
    st.write(f"**{product['name']}** - ${product['price']:.2f}")
    st.write(f"{product['description']}")
    if st.button(f"Añadir {product['name']} al carrito", key=f"add_{product['name']}"):
        st.session_state["quantities"][product["name"]] += 1
        st.success(f"🎉 ¡{product['name']} añadido al carrito!")

# Sección Carrito
st.markdown("<div class='section-title'>🛒 Tu carrito</div>", unsafe_allow_html=True)
if any(quantity > 0 for quantity in st.session_state["quantities"].values()):
    st.session_state["total"] = 0
    for product_name, quantity in st.session_state["quantities"].items():
        if quantity > 0:
            product = next((p for p in products if p["name"] == product_name), None)
            if product:
                col1, col2, col3 = st.columns([2, 2, 1])
                with col1:
                    st.write(f"**{product_name}** - ${product['price']:.2f} c/u")
                with col2:
                    new_quantity = st.number_input(
                        f"Cantidad ({product_name})",
                        min_value=0,
                        max_value=100,
                        value=quantity,
                        step=1,
                        key=f"quantity_{product_name}"
                    )
                    st.session_state["quantities"][product_name] = new_quantity
                with col3:
                    subtotal = product['price'] * new_quantity
                    st.session_state["total"] += subtotal
                    st.write(f"${subtotal:.2f}")
    st.write(f"### Total: ${st.session_state['total']:.2f} 💵")
else:
    st.write("¡Tu carrito está vacío! 😢")

# Métodos de Pago
st.markdown("""
### Métodos de Pago 💳
1. **PagoMovil:**  
   - C.I: 8342252  
   - Teléfono: 0424-8943749  
   - Banco: Banesco  
2. **Zelle:**  
   - Correo: Dimellamaite@hotmail.com  
3. **Efectivo/Tarjeta:**  
   - Contactar al WhatsApp: +58 123-456-7890 para confirmar el método de pago.  

**Nota:** La orden se procesará una vez que el pago sea confirmado.
""")

# Sección Datos del Cliente
st.markdown("<div class='section-title'>🚀 Datos del pedido</div>", unsafe_allow_html=True)
customer_name = st.text_input("📝 Nombre Completo")
customer_phone = st.text_input("📞 Teléfono")
customer_address = st.text_area("📍 Dirección")
if st.button("Confirmar Pedido ✅"):
    if customer_name and customer_phone and customer_address:
        st.session_state["order_id"] = generate_order_id()
        send_order_email(
            st.session_state["order_id"],
            st.session_state["quantities"],
            customer_name,
            customer_phone,
            customer_address
        )
        st.success(f"¡Pedido enviado! Orden ID: {st.session_state['order_id']} 🚀. Por favor, compartir comprobante de pago al WhatsApp +58 0424-8943749 o al correo konussfactory@gmail.com. ⚠️ El pedido será enviado una vez que se confirme el pago.")
    else:
        st.error("⚠️ Por favor, completa todos los campos.")
