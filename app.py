from flask import Flask, render_template, request, jsonify
import math

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

def fmt(num):
    """
    Formatea el número: 
    - Si es entero (ej: 2.0), devuelve "2"
    - Si tiene decimales (ej: 2.5), devuelve "2.5"
    """
    if num.is_integer():
        return str(int(num))
    return str(round(num, 4))

@app.route('/resolver', methods=['POST'])
def resolver():
    try:
        data = request.get_json()
        
        # 1. Obtener datos y signos
        a_val = float(data['valA'])
        a_sign = int(data['signA'])
        b_val = float(data['valB'])
        b_sign = int(data['signB'])
        c_val = float(data['valC'])
        c_sign = int(data['signC'])

        # Calculamos los valores reales matemáticos
        a = a_val * a_sign
        b = b_val * b_sign
        c = c_val * c_sign

        if a == 0:
            return jsonify({"status": "error", "message": "El coeficiente 'a' no puede ser 0."})

        pasos = []

        # --- GENERACIÓN DE CADENAS PARA MOSTRAR ---
        # Usamos la función fmt() para que no salgan ".0" feos
        
        # Coeficiente A (si es 1 o -1 a veces se omite, pero por claridad lo mostramos numérico si el usuario quiere, 
        # aunque matemáticamente "1m^2" se ve mejor como "m^2". Para simplificar tu código, usaremos el número formateado).
        str_a = fmt(a)
        
        # Para B y C necesitamos manejar el signo visualmente para la ecuación
        # Ejemplo: si b es -3, mostramos "- 3", si es +3, mostramos "+ 3"
        str_b = f"+ {fmt(b)}" if b >= 0 else f"- {fmt(abs(b))}"
        str_c = f"+ {fmt(c)}" if c >= 0 else f"- {fmt(abs(c))}"

        # ECUACIÓN ORIGINAL
        ec_diff = f"{str_a}y'' {str_b}y' {str_c}y = 0"
        
        pasos.append({
            "titulo": "1. Identificación",
            "texto": f"Ecuación a resolver: $${ec_diff}$$"
        })

        # ECUACIÓN CARACTERÍSTICA (Cambio de 'r' a 'm')
        ec_carac = f"{str_a}m^2 {str_b}m {str_c} = 0"
        pasos.append({
            "titulo": "2. Ecuación Característica",
            "texto": f"Sustituimos las derivadas por $m$: $${ec_carac}$$"
        })

        # DISCRIMINANTE
        discriminante = b**2 - 4*a*c
        
        # Texto del cálculo sustituyendo valores limpios
        txt_disc_calc = f"({fmt(b)})^2 - 4({fmt(a)})({fmt(c)})"
        
        pasos.append({
            "titulo": "3. Cálculo del Discriminante",
            "texto": f"Usamos la fórmula general $\\Delta = b^2 - 4ac$: <br> $$\\Delta = {txt_disc_calc} = {fmt(discriminante)}$$"
        })

        sol_general = ""
        raices_txt = ""
        soluciones_lin = ""

        # LÓGICA DE SOLUCIÓN
        if discriminante > 0:
            r1 = (-b + math.sqrt(discriminante)) / (2*a)
            r2 = (-b - math.sqrt(discriminante)) / (2*a)
            
            raices_txt = f"Como $\\Delta > 0$, tenemos dos raíces reales distintas: $$m_1 = {fmt(r1)}, \\quad m_2 = {fmt(r2)}$$"
            soluciones_lin = f"$$y_1 = e^{{{fmt(r1)}x}}, \\quad y_2 = e^{{{fmt(r2)}x}}$$"
            sol_general = f"$$y(x) = C_1 e^{{{fmt(r1)}x}} + C_2 e^{{{fmt(r2)}x}}$$"

        elif discriminante == 0:
            r = -b / (2*a)
            raices_txt = f"Como $\\Delta = 0$, tenemos una raíz real repetida: $$m = {fmt(r)}$$"
            soluciones_lin = f"$$y_1 = e^{{{fmt(r)}x}}, \\quad y_2 = x e^{{{fmt(r)}x}}$$"
            sol_general = f"$$y(x) = C_1 e^{{{fmt(r)}x}} + C_2 x e^{{{fmt(r)}x}}$$"

        else: # Complejos
            parte_real = -b / (2*a)
            parte_imag = math.sqrt(abs(discriminante)) / (2*a)
            
            # Formateamos para que se vea bien
            pr = fmt(parte_real)
            pi = fmt(parte_imag)

            raices_txt = f"Como $\\Delta < 0$, tenemos raíces complejas conjugadas ($ \\alpha \\pm \\beta i $): $$m = {pr} \\pm {pi}i$$"
            soluciones_lin = f"$$y_1 = e^{{{pr}x}} \\cos({pi}x), \\quad y_2 = e^{{{pr}x}} \\sin({pi}x)$$"
            sol_general = f"$$y(x) = e^{{{pr}x}} [C_1 \\cos({pi}x) + C_2 \\sin({pi}x)]$$"

        pasos.append({"titulo": "4. Cálculo de Raíces", "texto": raices_txt})
        pasos.append({"titulo": "5. Soluciones Linealmente Independientes", "texto": soluciones_lin})
        pasos.append({"titulo": "6. Solución General", "texto": sol_general})

        return jsonify({"status": "success", "pasos": pasos})

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

if __name__ == '__main__':
    app.run(debug=True)
