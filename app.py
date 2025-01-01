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

st.markdown("""
<style>
/* Fondo general */
.stApp {
     background: linear-gradient(to bottom, #ffe5e5, #ffcccc)); /* Fondo suave */
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
/* Separadores de sección con prioridad */
.section-title {
    background: #e63946 !important; /* Fondo rojo intenso */
    color: #ffffff !important; /* Texto negro forzado */
    font-size: 20px !important; /* Tamaño de fuente */
    font-weight: bold !important; /* Negrita */
    text-align: center !important; /* Centrado */
    padding: 12px !important; /* Espaciado interno */
    border-radius: 10px !important; /* Bordes redondeados */
    box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.15) !important; /* Sombra */
    margin-bottom: 20px !important; /* Margen inferior */
    text-transform: uppercase !important; /* Texto en mayúsculas */
}

/* Reseteo de colores heredados */
body, div, p, span, label, h1, h2, h3, h4, h5, h6 {
    color: inherit !important; /* Hereda el color correctamente */
}

/* Forzar texto negro global */
* {
    color: #000000 !important; /* Asegurar texto negro en cualquier elemento */
}

/* Fondo blanco para cualquier interferencia */
.section-title * {
    background-color: transparent !important; /* Fondo transparente dentro de la sección */
}


/* Entradas de texto y áreas */
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

/* Botones */
.stButton>button {
    background-color: #e63946 !important; /* Fondo rojo */
    color: white !important; /* Texto blanco */
    border-radius: 8px;
    padding: 10px 15px;
    font-size: 16px;
    border: none;
    box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
    transition: transform 0.2s ease, box-shadow 0.2s ease;
    cursor: pointer;
    margin-top: 5px;
    width: 100%;
}
.stButton>button:hover {
    background-color: #c22834 !important; /* Fondo rojo más oscuro */
    transform: scale(1.05); /* Efecto de zoom */
    box-shadow: 0px 6px 8px rgba(0, 0, 0, 0.2);
}

/* Tarjetas de productos */
.stColumn > div {
    background-color: #ffffff; /* Fondo blanco */
    color: #000000 !important; /* Texto negro */
    border-radius: 10px;
    box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
    padding: 15px;
    margin-bottom: 20px;
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}
.stColumn > div:hover {
    transform: scale(1.03);
    box-shadow: 0px 6px 10px rgba(0, 0, 0, 0.2);
}

/* Mensajes de éxito */
.stSuccess {
    background-color: #d4edda !important; /* Verde claro */
    border-left: 5px solid #28a745 !important;
    color: #155724 !important; /* Texto verde oscuro */
    padding: 10px;
    margin-bottom: 10px;
    border-radius: 5px;
}

/* Ocultar header y footer innecesarios */
header, footer {
    visibility: hidden;
}

/* Responsividad */
@media only screen and (max-width: 768px) {
    .section-title {
        font-size: 18px;
        padding: 10px;
    }
    input, textarea {
        font-size: 14px;
        padding: 10px;
    }
    .stButton>button {
        font-size: 14px;
        padding: 8px;
    }
}

            /* Alinear los elementos de los productos horizontalmente */
.product-container {
    display: flex; /* Disposición en fila */
    align-items: center; /* Centrado vertical */
    justify-content: space-between; /* Espaciado entre texto y botón */
    background-color: #ffffff; /* Fondo blanco */
    color: #000000; /* Texto negro */
    border-radius: 10px; /* Bordes redondeados */
    box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1); /* Sombra */
    padding: 10px; /* Espaciado interno */
    margin-bottom: 15px; /* Espaciado entre productos */
}

/* Ajustar el texto del producto */
.product-info {
    flex: 3; /* Toma el 70% del espacio horizontal */
    text-align: left; /* Alineación a la izquierda */
}

/* Botón "Añadir" */
.add-button {
    flex: 1; /* Toma el 30% del espacio horizontal */
    background-color: #e63946; /* Fondo rojo */
    color: white; /* Texto blanco */
    border: none;
    border-radius: 8px; /* Bordes redondeados */
    padding: 8px 10px; /* Espaciado interno */
    font-size: 14px; /* Texto tamaño medio */
    text-align: center;
    cursor: pointer;
    box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1); /* Sombra */
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}
.add-button:hover {
    background-color: #c22834; /* Fondo rojo oscuro */
    transform: scale(1.05); /* Zoom ligero al pasar */
}

/* Ajuste responsivo para móviles */
@media only screen and (max-width: 768px) {
    .product-container {
        flex-direction: row; /* Mantener disposición horizontal */
        padding: 8px; /* Reducir el espaciado interno */
    }
    .product-info {
        font-size: 14px; /* Texto más pequeño */
    }
    .add-button {
        font-size: 12px; /* Botón más pequeño */
        padding: 6px; /* Espaciado menor */
    }
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
   - C.I: 8.342.252  
   - Teléfono: 0424-8943749  
   - Banco: Banesco  
2. **Zelle:**  
   - Correo: Dimellamaite@hotmail.com  
3. **Efectivo/Tarjeta:**  
   - Contactar al WhatsApp: +58 0424-8943749 para confirmar el método de pago.  

**Nota: La orden se procesará una vez que el pago sea confirmado.**
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
        st.success(f"¡Pedido enviado! Orden ID: {st.session_state['order_id']} 🚀. Por favor, compartir comprobante de pago al WhatsApp +58 0424-8943749 o al correo konussfactory@gmail.com. **⚠️ El pedido será enviado una vez que se confirme el pago.**")
    else:
        st.error("⚠️ Por favor, completa todos los campos.")
