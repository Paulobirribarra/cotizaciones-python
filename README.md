# Generador de Cotizaciones en PDF

Esta es una aplicación Flask que genera cotizaciones en formato PDF a partir de un formulario web. Permite ingresar datos del remitente, cliente, productos (con código, nombre, descripción, cantidad y valor), y genera un PDF con un número correlativo y la fecha actual.

## Requisitos previos

- **Python 3.6 o superior**: Asegúrate de tener Python instalado. Puedes descargarlo desde [python.org](https://www.python.org/downloads/).
- **Sistema operativo**: Este proyecto ha sido probado en Windows, pero debería funcionar en Linux y macOS con ajustes mínimos.
- **Dependencias del sistema (para Weasyprint)**:
  - En Windows, instala [GTK3](https://github.com/tschoonj/GTK-for-Windows-Runtime-Environment-Installer) para que Weasyprint funcione correctamente.
  - En Linux, instala las dependencias con:
```
sudo apt-get install libpango-1.0-0 libpangoft2-1.0-0
 ```
## Instalación

### 1. Clonar el repositorio (si está en GitHub)

Si has subido el proyecto a GitHub, clona el repositorio:

```bash
git clone 
cd cotizaciones-python
```
### 2. Crear y activar un entorno virtual  
```
python -m venv .venv
```
### 3. Activa el entorno virtual:
```
.venv\Scripts\activate
```
### 4. Instalar las dependencias
```
pip install flask weasyprint jinja2 python-dotenv bleach
```
Esto instalará:
- flask: Framework web para la aplicación.
- weasyprint: Para generar PDFs a partir de HTML.
- jinja2: Motor de plantillas (ya incluido con Flask).
- python-dotenv: Para manejar variables de entorno.
- bleach: Para sanitizar entradas de usuario.

### 5. Configurar las variables de entorno
Crea un archivo .env en la raíz del proyecto con el siguiente contenido:
```
FLASK_SECRET_KEY=tu_clave_secreta_aqui
OUTPUT_DIR=PDF
STATIC_DIR=static
```

- FLASK_SECRET_KEY: Una clave secreta para Flask (cámbiala por una cadena segura).
- OUTPUT_DIR: Carpeta donde se guardarán los PDFs (por defecto, PDF).
- STATIC_DIR: Carpeta donde se encuentran los archivos estáticos, como el logo (por defecto, static).

### 6. Estructura del proyecto
```
cotizaciones-python/
│
├── .env
├── .gitattributes
├── .gitignore
├── app.py
├── PDF/
│   └── (los PDFs generados se guardarán aquí)
├── static/
│   └── header.png
└── templates/
    ├── cotizacion.html
    └── index.html
```
### 7. Ejecutar la aplicación
Ejecuta el script principal:
```
python app.py
```
Abre tu navegador y ve a http://127.0.0.1:5000/. Deberías ver un formulario para generar cotizaciones.

### 8. Generar una cotización
1. Completa el formulario con los datos del remitente, cliente y productos.
2. Haz clic en "Generar PDF".
3. El PDF se guardará en la carpeta PDF/ (por ejemplo, PDF/cotizacion_1.pdf), y verás un mensaje de confirmación en la página.

### Notas importantes
- Modo debug: La aplicación se ejecuta con debug=True para desarrollo. En producción, cambia app.run(debug=True) a app.run(debug=False) para evitar riesgos de seguridad.
- Permisos: Asegúrate de que tu usuario tenga permisos de escritura en la carpeta PDF/. Si encuentras un error de permisos, verifica que el archivo PDF no esté abierto en otro programa.
- Logo: La imagen logo-cram.png debe estar en la carpeta static/. Si cambias el nombre o la ubicación del archivo, actualiza las rutas en app.py.

### Solución de problemas
- Error de Weasyprint: Si Weasyprint no funciona, verifica que las dependencias del sistema (GTK3, Pango) estén instaladas correctamente.
- Error de permisos: Asegúrate de que la carpeta PDF/ tenga permisos de escritura y que los archivos PDF no estén abiertos en otro programa.
- Logo no se muestra: Verifica que logo-cram.png esté en la carpeta static/ y que el nombre del archivo coincida exactamente.



