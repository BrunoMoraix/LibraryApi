from libraryapi.app import create_app
from libraryapi.extension import db
from libraryapi.models import Book

# Criar o app
app = create_app()

with app.app_context():
    # Verifique se a tabela Book existe e está vazia
    books = Book.query.all()
    print(f"Livros no banco de dados: {len(books)}")

    # Se não houver livros, insira um livro de teste
    if len(books) == 0:
        book = Book(
            title="O Senhor dos Anéis",
            author="J.R.R. Tolkien",
            genre="Fantasia",
            year=1954
        )
        db.session.add(book)
        db.session.commit()
        print("Livro adicionado com sucesso!")
