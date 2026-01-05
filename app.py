from flask import Flask, render_template, request, jsonify
import math

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

def formatear_signo(val):
    """Ayuda a mostrar bonito el signo en la ecuación textual"""
    if val < 0:
        return f"- {abs(val)}"
    return f"+ {val}"

@app.route('/resolver', methods=['POST'])
def resolver():
    try:
        data = request.get_json()
        
        # Recibimos el valor absoluto y el signo por separado
        a_val = float(data['valA'])
        a_sign = int(data['signA']) # 1 o -1
        
        b_val = float(data['valB'])
        b_sign = int(data['signB'])
        
        c_val = float(data['valC'])
        c_sign = int(data['signC'])

        # Calculamos los coeficientes reales para la matemática
        a = a_val * a_sign
        b = b_val * b_sign
        c = c_val * c_sign

        if a == 0:
            return jsonify({"status": "error", "message": "El coeficiente 'a' no puede ser 0 en 2do orden."})

        pasos = []

        # Paso 1: Identificación (Formateo visual mejorado)
        # Primer término
        str_a = f"{a}" if a_sign > 0 else f"-{abs(a)}"
        # Segundos términos (gestionando espacios y signos)
        str_b = f"+ {b}" if b >= 0 else f"- {abs(b)}"
        str_c = f"+ {c}" if c >= 0 else f"- {abs(c)}"

        ec_diff = f"{str_a}y'' {str_b}y' {str_c}y = 0"
        
        pasos.append({
            "titulo": "1. Identificación",
            "texto": f"Ecuación a resolver: $${ec_diff}$$"
        })

        # Paso 2: Ecuación Característica
        ec_carac = f"{str_a}r^2 {str_b}r {str_c} = 0"
        pasos.append({
            "titulo": "2. Ecuación Característica",
            "texto": f"Sustituimos derivadas por $r$: $${ec_carac}$$"
        })

        # Paso 3: Discriminante
        discriminante = b**2 - 4*a*c
        pasos.append({
            "titulo": "3. Cálculo del Discriminante",
            "texto": f"$\\Delta = b^2 - 4ac$. <br> $\\Delta = ({b})^2 - 4({a})({c}) = {discriminante}$"
        })

        # Paso 4, 5, 6: Lógica matemática (Igual que antes)
        sol_general = ""
        raices_txt = ""
        soluciones_lin = ""

        if discriminante > 0:
            r1 = round((-b + math.sqrt(discriminante)) / (2*a), 4)
            r2 = round((-b - math.sqrt(discriminante)) / (2*a), 4)
            raices_txt = f"$\\Delta > 0$, dos raíces reales distintas: $$r_1 = {r1}, \quad r_2 = {r2}$$"
            soluciones_lin = f"$$y_1 = e^{{{r1}x}}, \quad y_2 = e^{{{r2}x}}$$"
            sol_general = f"$$y(x) = C_1 e^{{{r1}x}} + C_2 e^{{{r2}x}}$$"

        elif discriminante == 0:
            r = round(-b / (2*a), 4)
            raices_txt = f"$\\Delta = 0$, raíz real repetida: $$r = {r}$$"
            soluciones_lin = f"$$y_1 = e^{{{r}x}}, \quad y_2 = x e^{{{r}x}}$$"
            sol_general = f"$$y(x) = C_1 e^{{{r}x}} + C_2 x e^{{{r}x}}$$"

        else: # Complejos
            parte_real = round(-b / (2*a), 4)
            parte_imag = round(math.sqrt(abs(discriminante)) / (2*a), 4)
            raices_txt = f"$\\Delta < 0$, raíces complejas: $$r = {parte_real} \pm {parte_imag}i$$"
            soluciones_lin = f"$$y_1 = e^{{{parte_real}x}} \cos({parte_imag}x), \quad y_2 = e^{{{parte_real}x}} \sin({parte_imag}x)$$"
            sol_general = f"$$y(x) = e^{{{parte_real}x}} [C_1 \cos({parte_imag}x) + C_2 \sin({parte_imag}x)]$$"

        pasos.append({"titulo": "4. Cálculo de Raíces", "texto": raices_txt})
        pasos.append({"titulo": "5. Soluciones Linealmente Independientes", "texto": soluciones_lin})
        pasos.append({"titulo": "6. Solución General", "texto": sol_general})

        return jsonify({"status": "success", "pasos": pasos})

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

if __name__ == '__main__':
    app.run(debug=True)
