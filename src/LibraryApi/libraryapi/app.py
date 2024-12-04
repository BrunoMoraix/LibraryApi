from flask import Flask
from libraryapi.extension import db
from libraryapi.routes import initialize_routes
from libraryapi.config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)  # Conecta o banco ao app

    initialize_routes(app)  # Inicializa as rotas
    return app
if __name__ == "__main__":
    app = create_app()
    print("Servidor iniciado em http://127.0.0.1:5000")  # Mensagem de confirmação
    app.run(debug=True)
