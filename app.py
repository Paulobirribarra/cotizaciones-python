import os
import base64
import secrets
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash
from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML
from dotenv import load_dotenv
import bleach

# Cargar variables de entorno desde el archivo .env
load_dotenv()

app = Flask(__name__)

# Configurar la clave secreta de Flask
secret_key = os.getenv("FLASK_SECRET_KEY")
if not secret_key:
    secret_key = secrets.token_hex(16)
    print(f"FLASK_SECRET_KEY no encontrada en .env. Se generó una nueva clave: {secret_key}")
app.secret_key = secret_key

# Configuración de las carpetas usando variables de entorno
OUTPUT_DIR = os.getenv("OUTPUT_DIR")
STATIC_DIR = os.getenv("STATIC_DIR")

# Crear la carpeta de salida si no existe
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

# Función para convertir la imagen a base64
def get_logo_base64():
    image_path = os.path.join(STATIC_DIR, "header.png")
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode("utf-8")
        return f"data:image/png;base64,{encoded_string}"

# Determinar el número correlativo para los PDFs
def get_next_correlative():
    existing_files = [
        f for f in os.listdir(OUTPUT_DIR)
        if f.startswith("cotizacion_") and f.endswith(".pdf")
    ]
    if not existing_files:
        return 1
    last_file = sorted(existing_files)[-1]
    last_number = int(last_file.replace("cotizacion_", "").replace(".pdf", ""))
    return last_number + 1

# Filtro personalizado para formatear números con separadores de miles
def format_number(value):
    return "{:,.0f}".format(value).replace(",", ".")

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Obtener datos del formulario y sanitizarlos
        nombre_remitente = bleach.clean(request.form["nombre_remitente"])
        cargo_remitente = bleach.clean(request.form["cargo_remitente"])
        rut_remitente = bleach.clean(request.form["rut_remitente"])
        correo_remitente = bleach.clean(request.form["correo_remitente"])
        cliente = bleach.clean(request.form["cliente"])
        especificaciones = bleach.clean(request.form["especificaciones"])
        garantia = bleach.clean(request.form["garantia"])
        tiempo_entrega = bleach.clean(request.form["tiempo_entrega"])

        # Obtener lista de productos y sanitizarlos
        nombres = request.form.getlist("nombre_producto[]")
        codigos = request.form.getlist("codigo[]")
        descripciones = request.form.getlist("descripcion[]")
        cantidades = request.form.getlist("cantidad[]")
        valores_con_iva = request.form.getlist("valor_con_iva[]")

        productos = []
        total_con_iva = 0
        # Iterar sobre los nombres (campo obligatorio) para procesar los productos
        for i in range(len(nombres)):
            nombre = bleach.clean(nombres[i])
            # Acceder a los otros campos de manera segura
            codigo = bleach.clean(codigos[i] if i < len(codigos) else "")
            descripcion = bleach.clean(descripciones[i] if i < len(descripciones) else "")
            try:
                cantidad = int(cantidades[i] if i < len(cantidades) else 0)
                valor_con_iva = float(valores_con_iva[i] if i < len(valores_con_iva) else 0)
            except (ValueError, IndexError) as e:
                flash("Error: La cantidad y el valor unitario deben ser números válidos.", "error")
                return redirect(url_for("index"))

            # Calcular valor neto (sin IVA) a partir del valor con IVA
            valor_neto = valor_con_iva / 1.19  # IVA 19%
            valor_total_neto = valor_neto * cantidad
            valor_total_con_iva = valor_con_iva * cantidad

            productos.append({
                "nombre": nombre,
                "codigo": codigo,
                "descripcion": descripcion,
                "cantidad": cantidad,
                "valor_neto": valor_neto,
                "valor_total_neto": valor_total_neto,
                "valor_con_iva": valor_con_iva,
                "valor_total_con_iva": valor_total_con_iva
            })
            total_con_iva += valor_total_con_iva

        # Calcular total neto e IVA
        total_neto = total_con_iva / 1.19
        iva = total_con_iva - total_neto

        # Configurar Jinja2
        env = Environment(loader=FileSystemLoader("templates"))
        env.filters["format_number"] = format_number
        template = env.get_template("cotizacion.html")

        # Obtener el número correlativo
        correlative = get_next_correlative()
        correlative_str = f"{correlative:06d}"

        # Obtener la fecha actual en formato DD/MM/YYYY
        fecha_actual = datetime.now().strftime("%d/%m/%Y")

        # Obtener la imagen en base64
        logo_base64 = get_logo_base64()

        # Rellenar la plantilla con los datos
        html_content = template.render(
            nombre_remitente=nombre_remitente,
            cargo_remitente=cargo_remitente,
            rut_remitente=rut_remitente,
            correo_remitente=correo_remitente,
            cliente=cliente,
            productos=productos,
            total_neto=total_neto,
            iva=iva,
            total_con_iva=total_con_iva,
            especificaciones=especificaciones,
            garantia=garantia,
            tiempo_entrega=tiempo_entrega,
            correlative=correlative_str,
            logo_base64=logo_base64,
            fecha_actual=fecha_actual
        )

        # Generar el nombre del archivo con número correlativo
        pdf_filename = f"cotizacion_{correlative}.pdf"
        pdf_path = os.path.join(OUTPUT_DIR, pdf_filename)

        # Si el archivo ya existe, intentar eliminarlo
        if os.path.exists(pdf_path):
            try:
                os.remove(pdf_path)
            except Exception as e:
                flash(f"No se pudo eliminar el archivo existente {pdf_path}: {str(e)}", "error")
                return redirect(url_for("index"))

        # Convertir HTML a PDF y guardar en la carpeta PDF
        try:
            HTML(string=html_content, base_url=STATIC_DIR).write_pdf(pdf_path)
            flash(f"PDF generado correctamente: {pdf_filename}", "success")
        except Exception as e:
            flash(f"Error al generar el PDF: {str(e)}", "error")

        # Redirigir al usuario a la página principal con un mensaje
        return redirect(url_for("index"))

    # Valores predefinidos para el formulario (anonimizados)
    valores_predefinidos = {
        "cliente": "Nombre del Cliente",
        "rut_remitente": "XX.XXX.XXX-X",
        "garantia": "Garantía Legal 12 meses entregada por la marca.",
        "tiempo_entrega": "Tiempo de entrega inmediata. Producto en stock."
    }
    return render_template("index.html", **valores_predefinidos)

if __name__ == "__main__":
    # Nota: debug=True solo debe usarse en desarrollo. En producción, usar debug=False.
    app.run(debug=True)