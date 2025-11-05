# BitStore

**BitStore** es un e-commerce de hardware desarrollado como proyecto final de la materia *Programación*.  
Está construido con **Python (Flask)** y **Docker**, e incluye funcionalidades completas de tienda virtual.


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
- **Despliegue:** Fly.io / Render  

---

## 🐳 Ejecución local con Docker

```bash
# Construir la imagen
docker build -t bitstore .

# Ejecutar el contenedor
docker run -p 5000:5000 bitstore