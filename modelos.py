from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

# Inicializamos la base de datos
bd = SQLAlchemy()

# Modelos de bases de datos

class Usuario(UserMixin, bd.Model):
    """Usuarios registrados en la tienda (clientes y administradores)."""
    __tablename__ = "usuarios"
    id = bd.Column(bd.Integer, primary_key=True)
    nombre_usuario = bd.Column(bd.String(80), unique=True, nullable=False)
    correo = bd.Column(bd.String(200), unique=True, nullable=False)
    contraseña = bd.Column(bd.String(200), nullable=False)
    es_admin = bd.Column(bd.Boolean, default=False)  # Define si el usuario es administrador

    pedidos = bd.relationship("Pedido", back_populates="usuario")


class Categoria(bd.Model):
    """Categorías de productos (por ejemplo: Placas, Memorias, etc.)."""
    __tablename__ = "categorias"
    id = bd.Column(bd.Integer, primary_key=True)
    nombre = bd.Column(bd.String(100), nullable=False, unique=True)
    productos = bd.relationship("Producto", back_populates="categoria")


class Producto(bd.Model):
    """Productos individuales del catálogo."""
    __tablename__ = "productos"
    id = bd.Column(bd.Integer, primary_key=True)
    codigo = bd.Column(bd.String(50), unique=True, nullable=False)
    nombre = bd.Column(bd.String(200), nullable=False)
    descripcion = bd.Column(bd.Text)
    precio = bd.Column(bd.Numeric(precision=10, scale=2), nullable=False)
    stock = bd.Column(bd.Integer, nullable=False, default=0)
    imagen = bd.Column(bd.String(300))
    categoria_id = bd.Column(bd.Integer, bd.ForeignKey("categorias.id"))

    categoria = bd.relationship("Categoria", back_populates="productos")


class Pedido(bd.Model):
    """Pedido o compra realizada por un usuario."""
    __tablename__ = "pedidos"
    id = bd.Column(bd.Integer, primary_key=True)
    fecha_creacion = bd.Column(bd.DateTime, default=datetime.utcnow)
    estado = bd.Column(bd.String(50), default="Pendiente")
    total = bd.Column(bd.Float, nullable=False)

    # Usuario que realizó la compra
    usuario_id = bd.Column(bd.Integer, bd.ForeignKey("usuarios.id"))
    usuario = bd.relationship("Usuario", back_populates="pedidos")

    # Relación con los productos comprados
    items = bd.relationship("ItemPedido", back_populates="pedido", cascade="all, delete-orphan")


class ItemPedido(bd.Model):
    """Ítem individual dentro de un pedido."""
    __tablename__ = "items_pedido"
    id = bd.Column(bd.Integer, primary_key=True)
    producto_id = bd.Column(bd.Integer, bd.ForeignKey("productos.id"))
    pedido_id = bd.Column(bd.Integer, bd.ForeignKey("pedidos.id"))
    cantidad = bd.Column(bd.Integer, nullable=False)
    precio = bd.Column(bd.Float, nullable=False)

    producto = bd.relationship("Producto")
    pedido = bd.relationship("Pedido", back_populates="items")
