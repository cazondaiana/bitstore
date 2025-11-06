import os
from flask import Flask, render_template, redirect, url_for, request, flash, session, jsonify
from configuracion import Configuracion
from modelos import bd, Usuario, Producto, Categoria, Pedido, ItemPedido
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
from decimal import Decimal


def crear_aplicacion():
    # Crea y configura Flask
    app = Flask(__name__, static_folder="static", template_folder="plantillas")
    app.config.from_object(Configuracion)

    # Aseguramos que la carpeta 'instance/' exista
    os.makedirs(os.path.join(os.path.dirname(__file__), "instance"), exist_ok=True)

    # Inicializamos base de datos y sistema de login
    bd.init_app(app)
    gestor_login = LoginManager(app)
    # Redirección si un usuario no autenticado intenta acceder
    gestor_login.login_view = "iniciar_sesion"

    @gestor_login.user_loader
    def cargar_usuario(usuario_id):
        """Carga un usuario desde la base de datos según su ID"""
        return Usuario.query.get(int(usuario_id))

    # Rutas principales

    @app.route("/")
    def inicio():
        # Página principal
        busqueda = request.args.get("q", "")
        categoria_id = request.args.get("cat")

        # Muestra catálogo e incluye filtros de búsqueda
        productos = Producto.query
        if busqueda:
            productos = productos.filter(Producto.nombre.ilike(f"%{busqueda}%"))
        if categoria_id:
            productos = productos.filter(Producto.categoria_id == categoria_id)

        productos = productos.limit(50).all()
        categorias = Categoria.query.all()
        return render_template("inicio.html", productos=productos, categorias=categorias, busqueda=busqueda)

    @app.route("/producto/<int:id_producto>")
    def detalle_producto(id_producto):
        """Página de detalle de producto."""
        producto = Producto.query.get_or_404(id_producto)
        return render_template("producto.html", producto=producto)

    # AUTENTICACIÓN 

    @app.route("/registro", methods=["GET", "POST"])
    def registro():
        # Cerramos sesión previa por si acaso
        logout_user()

        """Registro de nuevos usuarios"""
        if request.method == "POST":
            nombre = request.form["nombre"]
            correo = request.form["correo"]
            contraseña = request.form["contraseña"]

            # Verificamos que el usuario o correo no estén repetidos
            if Usuario.query.filter((Usuario.nombre_usuario == nombre) | (Usuario.correo == correo)).first():
                flash("El usuario o correo ya está registrado.", "danger")
                return redirect(url_for("registro"))

            # Guardamos usuario
            usuario = Usuario(nombre_usuario=nombre, correo=correo, contraseña=generate_password_hash(contraseña))
            bd.session.add(usuario)
            bd.session.commit()
            flash("Usuario registrado correctamente. Iniciá sesión.", "success")
            return redirect(url_for("iniciar_sesion"))

        return render_template("registro.html")

    @app.route("/iniciar_sesion", methods=["GET", "POST"])
    def iniciar_sesion():
        """Inicio de sesión de usuarios"""
        if request.method == "POST":
            nombre = request.form["nombre"]
            contraseña = request.form["contraseña"]
            usuario = Usuario.query.filter((Usuario.nombre_usuario == nombre) | (Usuario.correo == nombre)).first()

            if usuario and check_password_hash(usuario.contraseña, contraseña):
                login_user(usuario)
                flash("Sesión iniciada correctamente.", "success")
                return redirect(url_for("inicio"))

            flash("Credenciales inválidas.", "danger")
        return render_template("iniciar_sesion.html")

    @app.route("/cerrar_sesion")
    @login_required
    def cerrar_sesion():
        logout_user()
        flash("Cerraste sesión.", "info")
        return redirect(url_for("inicio"))

    # Carrito

    def obtener_carrito():
        """Obtiene el carrito desde la sesión del usuario"""
        return session.setdefault("carrito", {})

    @app.route("/carrito")
    def ver_carrito():
        # Muestra los productos agregados al carrito
        carrito = obtener_carrito()
        items = []
        total = Decimal('0.0')

        for id_prod, cant in carrito.items():
            p = Producto.query.get(int(id_prod))
            if not p:
                continue

            # Convertimos todos los valores a Decimal
            precio = Decimal(p.precio)
            cantidad = Decimal(cant)
            subtotal = precio * cantidad

            items.append({"producto": p, "cantidad": cant, "subtotal": subtotal})
            total += subtotal

        return render_template("carrito.html", items=items, total=total)

    @app.route("/carrito/agregar/<int:id_producto>", methods=["POST"])
    def agregar_al_carrito(id_producto):
        """ Agrega un producto al carrito """
        cantidad = int(request.form.get("cantidad", 1))
        p = Producto.query.get_or_404(id_producto)
        carrito = obtener_carrito()

        actual = carrito.get(str(id_producto), 0)
        if p.stock < actual + cantidad:
            flash("Stock insuficiente.", "warning")
            return redirect(url_for("detalle_producto", id_producto=id_producto))

        carrito[str(id_producto)] = actual + cantidad
        session.modified = True
        flash("Producto agregado al carrito", "success")
        return redirect(url_for("ver_carrito"))

    @app.route("/carrito/actualizar", methods=["POST"])
    def actualizar_carrito():
        """Actualiza las cantidades de los productos en el carrito"""
        carrito = obtener_carrito()
        for pid, cant in request.form.items():
            if pid.startswith("cantidad_"):
                id_producto = pid.split("_", 1)[1]
                try:
                    q = int(cant)
                except:
                    q = 0
                if q <= 0:
                    carrito.pop(id_producto, None)
                else:
                    prod = Producto.query.get(int(id_producto))
                    if prod and prod.stock < q:
                        flash(f"Stock insuficiente para {prod.nombre}", "warning")
                    else:
                        carrito[id_producto] = q
        session.modified = True
        return redirect(url_for("ver_carrito"))

    @app.route("/carrito/vaciar")
    def vaciar_carrito():
        # Vaciamos el carrito
        session.pop("carrito", None)
        flash("Carrito vaciado.", "info")
        return redirect(url_for("inicio"))

    # Checkout

    @app.route("/confirmar_compra", methods=["GET", "POST"])
    @login_required
    def confirmar_compra():
        """Simula el proceso de compra"""
        carrito = obtener_carrito()
        if not carrito:
            flash("Carrito vacío.", "warning")
            return redirect(url_for("inicio"))

        items = []
        total = Decimal('0.0')

        for pid, cant in carrito.items():
            p = Producto.query.get(int(pid))
            if not p or p.stock < cant:
                flash(f"Stock insuficiente o producto no encontrado: {p.nombre}", "danger")
                return redirect(url_for("ver_carrito"))

            precio = Decimal(p.precio)
            cantidad = Decimal(cant)
            subtotal = precio * cantidad

            items.append((p, cant, subtotal))
            total += subtotal

        if request.method == "POST":
            pedido = Pedido(usuario_id=current_user.id, total=total, estado="Procesando")
            bd.session.add(pedido)

            for p, cant, _ in items:
                p.stock -= cant
                item = ItemPedido(producto_id=p.id, cantidad=cant, precio=p.precio)
                pedido.items.append(item)

            bd.session.commit()
            session.pop("carrito", None)
            flash("Compra completada", "success")
            return redirect(url_for("inicio"))

        return render_template("confirmar_compra.html", items=items, total=total)

    # Panel de administración: simulación

    @app.route("/admin_productos")
    @login_required
    def admin_productos():
        """Vista simple del panel de administración"""
        # Verifica que solo el administrador pueda acceder
        if not current_user.es_admin:
            flash("Acceso denegado. Solo el administrador puede ingresar aquí.", "danger")
            return redirect(url_for("inicio"))

        # Muestra lista de productos
        productos = Producto.query.all()
        return render_template("admin_productos.html", productos=productos)

    return app


if __name__ == "__main__":
    app = crear_aplicacion()
    with app.app_context():
        bd.create_all()
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
