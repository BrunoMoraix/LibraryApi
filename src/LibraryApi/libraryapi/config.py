import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(BASE_DIR, 'library.db')}"  # Banco SQLite
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Evita warnings desnecessários
