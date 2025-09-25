import streamlit as st

# --- FUNCIONES LÓGICAS (Sin cambios) ---
def is_prime(n):
    if n <= 1: return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0: return False
    return True

def get_divisors(n):
    return [i for i in range(1, n + 1) if n % i == 0]

# --- FUNCIÓN DE DIBUJO SVG (Sin cambios) ---
def generate_svg_visualization(number, group_size):
    ball_radius, padding, balls_per_row = 15, 10, 10
    canvas_width, max_y = 800, 0
    svg_elements = []
    x_start, y_start = 40, 40
    x, y = x_start, y_start
    balls_drawn = 0

    while balls_drawn < number:
        is_complete = (number - balls_drawn >= group_size)
        outline_color = "green" if is_complete else "red"
        coords, group_x_start, group_y_start = [], x, y
        
        for i in range(group_size):
            cx, cy = x, y
            if balls_drawn < number:
                svg_elements.append(f'<circle cx="{cx}" cy="{cy}" r="{ball_radius}" fill="skyblue" stroke="blue" stroke-width="2" />')
                balls_drawn += 1
            else:
                svg_elements.append(f'<circle cx="{cx}" cy="{cy}" r="{ball_radius}" fill="none" stroke="lightgrey" stroke-width="2" stroke-dasharray="4" />')
            
            coords.append((cx - ball_radius, cy - ball_radius, cx + ball_radius, cy + ball_radius))
            
            if (i + 1) % balls_per_row == 0:
                x, y = group_x_start, y + ball_radius * 2 + padding
            else:
                x += ball_radius * 2 + padding

        if coords:
            min_x, min_y = min(c[0] for c in coords) - padding, min(c[1] for c in coords) - padding
            max_x, max_y = max(c[2] for c in coords) + padding, max(c[3] for c in coords) + padding
            svg_elements.append(f'<rect x="{min_x}" y="{min_y}" width="{max_x - min_x}" height="{max_y - min_y}" fill="none" stroke="{outline_color}" stroke-width="3" />')
        
        y = group_y_start
        x = max_x + padding * 2
        
        if x > canvas_width - (balls_per_row * (ball_radius * 2 + padding)):
            x, y = x_start, max_y + padding * 2
    
    canvas_height = max_y + padding * 4
    svg_header = f'<svg width="{canvas_width}" height="{canvas_height}" xmlns="http://www.w3.org/2000/svg">'
    return svg_header + "".join(svg_elements) + '</svg>'

# --- INTERFAZ DE LA APLICACIÓN WEB ---

st.set_page_config(layout="wide")

st.title("🔢 Visualizador Interactivo de Divisibilidad")
st.markdown("Una herramienta para explorar los divisores, los números primos y compuestos de forma visual.")

# --- Inicializar el estado de la sesión ---
# Esto es clave: se asegura de que las variables persistan entre recargas.
if 'visualize' not in st.session_state:
    st.session_state.visualize = False
    st.session_state.number = 12
    st.session_state.group_size = 3

# --- Entradas de usuario ---
col1, col2 = st.columns(2)
with col1:
    number_input = st.number_input("Ingresa un número (1-100):", min_value=1, max_value=100, value=st.session_state.number, step=1)
with col2:
    group_size_input = st.number_input("Agrupar en grupos de:", min_value=1, max_value=100, value=st.session_state.group_size, step=1)

# --- Botón para visualizar ---
if st.button("Visualizar Agrupación", type="primary"):
    # Al hacer clic, activamos la visualización y guardamos los números.
    st.session_state.visualize = True
    st.session_state.number = number_input
    st.session_state.group_size = group_size_input

# --- Bloque de visualización ---
# Este bloque ahora se ejecuta si 'visualize' es True, independientemente de la última acción.
if st.session_state.visualize:
    
    # Usamos los números guardados en el estado de la sesión
    num = st.session_state.number
    group = st.session_state.group_size
    
    is_divisible = (num % group == 0)
    if is_divisible:
        st.success(f"¡División Exacta! {num} es divisible por {group}.")
    else:
        st.error(f"División No Exacta. {num} no es divisible por {group}.")
    
    # Mostrar la visualización SVG
    svg_image = generate_svg_visualization(num, group)
    st.markdown(svg_image, unsafe_allow_html=True)
    
    st.markdown("---") # Separador visual
    
    # El resumen ahora no hará que todo lo demás desaparezca
    if st.checkbox("Mostrar Resumen (¿Es primo o compuesto?)"):
        divisors = get_divisors(num)
        is_num_prime = is_prime(num)
        
        if is_num_prime:
            st.info(f"**{num} es un número PRIMO**")
        else:
            st.warning(f"**{num} es un número COMPUESTO**")
        
        st.write(f"**Divisores de {num}:** {', '.join(map(str, divisors))}")