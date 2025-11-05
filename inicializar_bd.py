from tienda import crear_aplicacion
from modelos import bd, Usuario, Categoria, Producto
from werkzeug.security import generate_password_hash

# Inicializar la base de datos 
app = crear_aplicacion()
with app.app_context():
    bd.create_all()

    # Creamos el usuario administrador para que siempre haya un usuario en la base de datos
    if not Usuario.query.filter_by(nombre_usuario="admin").first():
        admin = Usuario(
            nombre_usuario="admin",
            correo="admin@tienda.local",
            contraseña=generate_password_hash("admin123"),
            es_admin=True  # Diferenciamos otros usuarios del admin
        )
        bd.session.add(admin)


    # Crear categorías
    nombres_categorias = [
        "Placas de video", "Placas madre", "Procesadores",
        "Memoria RAM", "Almacenamiento", "Periféricos"
    ]
    categorias = []
    for nombre in nombres_categorias:
        c = Categoria.query.filter_by(nombre=nombre).first()
        if not c:
            c = Categoria(nombre=nombre)
            bd.session.add(c)
        categorias.append(c)
    bd.session.commit()

    # Cargamos los productos de la tienda y clasificamos según categoría
    productos = [
    {"codigo": "GPU-RTX3060", "nombre": "NVIDIA RTX 3060 12GB", 
     "descripcion": "Tarjeta gráfica potente", "precio": 547099, "stock": 8, 
     "categoria": categorias[0], "imagen": "img/gpu_rtx3060.jpg"},
    {"codigo": "MB-ASUS-B550M", "nombre": "ASUS TUF B550M", 
     "descripcion": "Placa madre AMD", "precio": 274999, "stock": 8, 
     "categoria": categorias[1], "imagen": "img/mb_asus_tuf.jpg"},
    {"codigo": "CPU-R5600X", "nombre": "AMD Ryzen 5 5600X", 
     "descripcion": "Procesador 6 núcleos", "precio": 361724, "stock": 10, 
     "categoria": categorias[2], "imagen": "img/cpu_ryzen5600x.jpg"},
    {"codigo": "RAM-16GB-3200", "nombre": "Kingston 16GB DDR4 3200", 
     "descripcion": "Memoria RAM de alto rendimiento", "precio": 125000, "stock": 12, 
     "categoria": categorias[3], "imagen": "img/ram_16gb_3200.jpg"},
    {"codigo": "SSD-1TB", "nombre": "Samsung SSD 1TB", 
     "descripcion": "Unidad de estado sólido 1TB", "precio": 228000, "stock": 7, 
     "categoria": categorias[4], "imagen": "img/ssd_1tb.jpg"},
    {"codigo": "KB-MECH", "nombre": "Teclado Mecánico RGB", 
     "descripcion": "Periférico gamer retroiluminado", "precio": 84999, "stock": 15, 
     "categoria": categorias[5], "imagen": "img/kb_mech.jpg"}
    ]


    # Insertar productos si no existen
    for prod in productos:
        if not Producto.query.filter_by(codigo=prod["codigo"]).first():
            p = Producto(
                codigo=prod["codigo"], nombre=prod["nombre"], descripcion=prod["descripcion"],
                precio=prod["precio"], stock=prod["stock"], imagen=prod["imagen"], categoria=prod["categoria"]
            )
            bd.session.add(p)

    bd.session.commit()
    print("Base de datos inicializada")
