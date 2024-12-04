from libraryapi.extension import db
from libraryapi.models import Book, User, Loan
from libraryapi.app import create_app

app = create_app()

with app.app_context():
    db.drop_all()  # Apaga todas as tabelas existentes (cuidado com isso em produção!)
    db.create_all()  # Cria todas as tabelas novamente
    print("Tabelas recriadas com sucesso!")
