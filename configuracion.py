import os
BASE_DIR = os.path.abspath(os.path.dirname(__file__))


# Configuración general de flask
class Configuracion:
    SECRET_KEY = "clave_super_secreta_para_la_tienda"
    SQLALCHEMY_DATABASE_URI = "sqlite:///tienda_virtual.sqlite"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
