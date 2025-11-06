# BitStore

**BitStore** es un e-commerce de hardware desarrollado por el grupo BitLegion de la cohorte 2024, como proyecto final de la materia Programación IV de la Tecnicatura Universitaria en Programación, dictada en la Universidad Nacional Tecnológica con sede en San Rafael.  


## Funcionalidades principales

- Registro e inicio de sesión de usuarios
- Base de datos SQLite integrada
- Catálogo de productos con imágenes, precios y stock
- Filtro por categorías
- Carrito de compras
- Confirmación de compra simulada
- Base de datos SQLite integrada

---

## Tecnologías utilizadas

- **Backend:** Flask + SQLAlchemy  
- **Frontend:** HTML, CSS, Jinja2  
- **Base de datos:** SQLite  
- **Servidor:** Gunicorn (en contenedor Docker)  
- **Deploy:** Render  

---

## Ejecución local

Recomendamos clonar el repositorio, y luego crear el entorno virtual con los requisitos de requirements.txt para lograr una ejecución exitosa del e-commerce


python -m venv venv
venv\Scripts\activate  # En Windows
# o
source venv/bin/activate  # En Linux/Mac
