from flask import Flask, render_template, request

app = Flask(__name__)


def calcular_promedio_y_estado(
    nota1: float, nota2: float, nota3: float, asistencia: float
) -> tuple[float, str]:
    """Calcula el promedio de 3 notas y determina si el estudiante aprueba."""
    promedio = round((nota1 + nota2 + nota3) / 3, 1)
    estado = "APROBADO" if promedio >= 40 and asistencia >= 75 else "REPROBADO"
    return promedio, estado


def obtener_nombre_mas_largo(nombres: list[str]) -> tuple[str, int]:
    """Retorna el nombre con mayor cantidad de caracteres y su longitud."""
    nombre_mayor = max(nombres, key=len)
    return nombre_mayor, len(nombre_mayor)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/ejercicio1", methods=["GET", "POST"])
def ejercicio1():
    promedio = None
    estado = None
    error = None
    valores = {"nota1": "", "nota2": "", "nota3": "", "asistencia": ""}

    if request.method == "POST":
        for campo in valores:
            valores[campo] = request.form.get(campo, "").strip()

        try:
            nota1 = float(valores["nota1"])
            nota2 = float(valores["nota2"])
            nota3 = float(valores["nota3"])
            asistencia = float(valores["asistencia"])
        except ValueError:
            error = "Por favor, ingresa valores numéricos válidos en todos los campos."
        else:
            if not all(10 <= n <= 70 for n in (nota1, nota2, nota3)):
                error = "Cada nota debe estar entre 10 y 70."
            elif not (0 <= asistencia <= 100):
                error = "La asistencia debe estar entre 0 y 100."
            else:
                promedio, estado = calcular_promedio_y_estado(
                    nota1, nota2, nota3, asistencia
                )

    return render_template(
        "ejercicio1.html",
        promedio=promedio,
        estado=estado,
        error=error,
        valores=valores,
    )


@app.route("/ejercicio2", methods=["GET", "POST"])
def ejercicio2():
    nombre_mayor = None
    cantidad_caracteres = None
    error = None
    valores = {"nombre1": "", "nombre2": "", "nombre3": ""}

    if request.method == "POST":
        for campo in valores:
            valores[campo] = request.form.get(campo, "").strip()

        nombres = [valores["nombre1"], valores["nombre2"], valores["nombre3"]]
        if not all(nombres):
            error = "Por favor, completa los 3 nombres."
        else:
            nombre_mayor, cantidad_caracteres = obtener_nombre_mas_largo(nombres)

    return render_template(
        "ejercicio2.html",
        nombre_mayor=nombre_mayor,
        cantidad_caracteres=cantidad_caracteres,
        error=error,
        valores=valores,
    )


if __name__ == "__main__":
    app.run(debug=True)
