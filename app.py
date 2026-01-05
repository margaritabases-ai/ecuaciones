from flask import Flask, render_template, request, jsonify
import math

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/resolver', methods=['POST'])
def resolver():
    try:
        data = request.get_json()
        # Obtenemos coeficientes (convertimos a float)
        a = float(data['a'])
        b = float(data['b'])
        c = float(data['c'])

        pasos = []

        # Paso 1: Identificar la ecuación
        ec_diff = f"{a}y'' + {b}y' + {c}y = 0"
        pasos.append({
            "titulo": "1. Identificación",
            "texto": f"Tenemos una Ecuación Diferencial Lineal Homogénea de coeficientes constantes: $${ec_diff}$$"
        })

        # Paso 2: Ecuación Característica
        ec_carac = f"{a}r^2 + {b}r + {c} = 0"
        pasos.append({
            "titulo": "2. Ecuación Característica",
            "texto": f"Sustituimos las derivadas por potencias de r: $${ec_carac}$$"
        })

        # Paso 3: Calcular Discriminante
        discriminante = b**2 - 4*a*c
        pasos.append({
            "titulo": "3. Cálculo del Discriminante",
            "texto": f"Usamos la fórmula general. El discriminante es $\Delta = b^2 - 4ac$. <br> Calculamos: $({b})^2 - 4({a})({c}) = {discriminante}$"
        })

        sol_general = ""
        raices_txt = ""
        soluciones_lin = ""

        # Paso 4 y 5: Raíces y Solución
        if discriminante > 0:
            r1 = round((-b + math.sqrt(discriminante)) / (2*a), 4)
            r2 = round((-b - math.sqrt(discriminante)) / (2*a), 4)
            raices_txt = f"Como $\Delta > 0$, tenemos dos raíces reales distintas: $$r_1 = {r1}, \quad r_2 = {r2}$$"
            soluciones_lin = f"$$y_1 = e^{{{r1}x}}, \quad y_2 = e^{{{r2}x}}$$"
            sol_general = f"$$y(x) = C_1 e^{{{r1}x}} + C_2 e^{{{r2}x}}$$"

        elif discriminante == 0:
            r = round(-b / (2*a), 4)
            raices_txt = f"Como $\Delta = 0$, tenemos una raíz real repetida: $$r = {r}$$"
            soluciones_lin = f"$$y_1 = e^{{{r}x}}, \quad y_2 = x e^{{{r}x}}$$"
            sol_general = f"$$y(x) = C_1 e^{{{r}x}} + C_2 x e^{{{r}x}}$$"

        else: # Discriminante negativo (Complejos)
            parte_real = round(-b / (2*a), 4)
            parte_imag = round(math.sqrt(abs(discriminante)) / (2*a), 4)
            raices_txt = f"Como $\Delta < 0$, tenemos raíces complejas conjugadas ($ \\alpha \pm \\beta i $): $$r = {parte_real} \pm {parte_imag}i$$"
            soluciones_lin = f"$$y_1 = e^{{{parte_real}x}} \cos({parte_imag}x), \quad y_2 = e^{{{parte_real}x}} \sin({parte_imag}x)$$"
            sol_general = f"$$y(x) = e^{{{parte_real}x}} (C_1 \cos({parte_imag}x) + C_2 \sin({parte_imag}x))$$"

        pasos.append({"titulo": "4. Cálculo de Raíces", "texto": raices_txt})
        pasos.append({"titulo": "5. Soluciones Linealmente Independientes", "texto": soluciones_lin})
        pasos.append({"titulo": "6. Solución General", "texto": sol_general})

        return jsonify({"status": "success", "pasos": pasos})

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

if __name__ == '__main__':
    app.run(debug=True)
