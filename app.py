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
if "delivery_cost" not in st.session_state:
    st.session_state["delivery_cost"] = 0.0

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

# Opciones de delivery
st.markdown("<div class='section-title'>🚚 Delivery</div>", unsafe_allow_html=True)
delivery_option = st.selectbox(
    "Seleccione la ubicación para el delivery:",
    ["Lechería (Gratis)", "Puerto La Cruz ($0.5)", "Barcelona ($2.0)"]
)

# Determinar el costo del delivery
if delivery_option == "Puerto La Cruz ($0.5)":
    st.session_state["delivery_cost"] = 0.5
elif delivery_option == "Barcelona ($2.0)":
    st.session_state["delivery_cost"] = 2.0
else:
    st.session_state["delivery_cost"] = 0.0

# Función para enviar el pedido por correo
def send_order_email(order_id, cart, customer_name, customer_phone, customer_address, payment_reference, delivery_option, delivery_cost):
    subject = f"Nuevo Pedido - {order_id}"
    body = f"""
    Nuevo Pedido Realizado:

    Orden ID: {order_id}
    Cliente: {customer_name}
    Teléfono: {customer_phone}
    Dirección: {customer_address}
    Referencia: {payment_reference}

    Delivery: {delivery_option} (${delivery_cost:.2f})

    Detalles del Pedido:
    """
    total = delivery_cost
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

st.markdown("""
<style>
/* Fondo general */
.stApp {
    background: linear-gradient(to bottom, #fdf5f5, #ffffff); /* Fondo suave */
    font-family: 'Poppins', sans-serif;
    color: #000000 !important; /* Texto negro predeterminado */
    padding: 10px;
}

/* Texto general */
body, div, p, span, label, h1, h2, h3, h4, h5, h6, textarea, input, button {
    color: #000000 !important; /* Texto negro forzado */
    background-color: transparent !important; /* Fondo transparente por defecto */
    margin: 0;
}

/* Títulos principales */
h1, h2, h3 {
    color: #e63946 !important; /* Títulos en rojo elegante */
    text-align: center;
    text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.1); /* Sombras suaves */
    margin-bottom: 20px;
}

/* Separadores de sección */
.section-title {
    background: #e63946 !important; /* Fondo rojo intenso */
    color: #ffffff !important; /* Texto blanco */
    font-size: 20px !important; /* Tamaño de fuente */
    font-weight: bold !important; /* Negrita */
    text-align: center !important; /* Centrado */
    padding: 12px !important; /* Espaciado interno */
    border-radius: 10px !important; /* Bordes redondeados */
    box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.15) !important; /* Sombra */
    margin-bottom: 20px !important; /* Margen inferior */
    text-transform: uppercase !important; /* Texto en mayúsculas */
}

/* Campos de entrada */
input, textarea {
    background-color: #ffffff !important; /* Fondo blanco asegurado */
    color: #000000 !important; /* Texto negro garantizado */
    border: 2px solid #e63946 !important; /* Borde rojo */
    border-radius: 8px;
    padding: 12px;
    font-size: 16px;
    box-sizing: border-box;
    margin-bottom: 15px;
    transition: border 0.3s ease, box-shadow 0.3s ease;
}
input:focus, textarea:focus {
    outline: none !important;
    border: 2px solid #c22834 !important;
    box-shadow: 0px 0px 5px rgba(226, 57, 70, 0.5);
}
</style>
""", unsafe_allow_html=True)

# Encabezado
st.markdown("<h1 class='header'>🍕 Konuss -¡Ahora la pizza se come en cono!🎉</h1>", unsafe_allow_html=True)
# Sección Menú
st.markdown("<div class='section-title'>📋 Menú</div>", unsafe_allow_html=True)
for product in products:
    col1, col2 = st.columns([4, 1])  # División de columnas: producto y botón
    with col1:
        st.write(f"**{product['name']}** - ${product['price']:.2f}")
        st.write(f"{product['description']}")
    with col2:
        if st.button("Añadir", key=f"add_{product['name']}"):
            st.session_state["quantities"][product["name"]] += 1
            st.success(f"🎉 ¡{product['name']} añadido al carrito!")

# Sección Carrito
st.markdown("<div class='section-title'>🛒 Tu carrito</div>", unsafe_allow_html=True)
if any(quantity > 0 for quantity in st.session_state["quantities"].values()):
    st.session_state["total"] = st.session_state["delivery_cost"]  # Inicia con el costo del delivery
    st.write(f"**Delivery: {delivery_option} - ${st.session_state['delivery_cost']:.2f}**")

    for product_name, quantity in st.session_state["quantities"].items():
        if quantity > 0:
            product = next((p for p in products if p["name"] == product_name), None)
            if product:
                subtotal = product["price"] * quantity
                st.session_state["total"] += subtotal
                st.write(f"- {product_name}: {quantity} x ${product['price']:.2f} = ${subtotal:.2f}")

    st.write(f"### Total: ${st.session_state['total']:.2f} 💵")
else:
    st.write("¡Tu carrito está vacío! 😥")

# Métodos de Pago
st.markdown("""
### Métodos de Pago 💳
1. **PagoMovil:**  
   - C.I: 8.342.252  
   - Teléfono: 0424-8943749  
   - Banco: Banesco  
2. **Zelle:**  
   - Correo: Dimellamaite@hotmail.com  
3. **Efectivo/Tarjeta:**  
   - Contactar al WhatsApp: +58 0424-8943749 para confirmar el método de pago.  

**⚠️Nota: La orden será procesada una vez el pago haya sido confirmado ⚠️**
""")

# Sección Datos del Cliente
st.markdown("<div class='section-title'>🚀 Datos del pedido</div>", unsafe_allow_html=True)
customer_name = st.text_input("🖍 Nombre Completo")
customer_phone = st.text_input("📞 Teléfono")
customer_address = st.text_area("📍 Dirección")
payment_reference = st.text_input("💳 Últimos 6 dígitos de referencia bancaria del pago")

if st.button("Confirmar Pedido ✅"):
    if customer_name and customer_phone and customer_address and payment_reference:
        st.session_state["order_id"] = generate_order_id()
        send_order_email(
            st.session_state["order_id"],
            st.session_state["quantities"],
            customer_name,
            customer_phone,
            customer_address,
            payment_reference,
            delivery_option,
            st.session_state["delivery_cost"]
        )
        st.success(
            f"🎉 Tu pedido ha sido realizado exitosamente. Tu número de orden es {st.session_state['order_id']}. "
            f"Por favor, comparte el comprobante de pago con el número de referencia **{payment_reference}** "
            f"al Whatsapp +58 0424-8943749 o al e-mail konussfactory@gmail.com. **⚠️ El pedido será enviado una vez confirmado el pago. ⚠️**"
        )
    else:
        st.error("⚠️ Por favor, completa todos los campos.")
