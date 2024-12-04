from flask import request, jsonify
from libraryapi.models import db, Book, User, Loan
from datetime import datetime



def initialize_routes(app):
    @app.route('/books', methods=['GET', 'POST'])
    def manage_books():
       
        if request.method == 'POST':
            data = request.json  
            new_book = Book(
                title=data['title'],
                author=data['author'],
                genre=data['genre'],
                year=data['year']
                
            )
            db.session.add(new_book)  
            db.session.commit() 
            return jsonify({"message": "Livro adicionado com sucesso!"}), 201

        
        books = Book.query.all()  
        if books:
            return jsonify([{
                "id": book.id,
                "title": book.title,
                "author": book.author,
                "genre": book.genre,
                "year": book.year,
                
            } for book in books])
        else:
            return jsonify({"message": "No books found"}), 404
        
    @app.route('/books/<int:id>', methods=['GET', 'PUT', 'DELETE'])
    def manage_single_book(id):
        
        if request.method == 'GET':
            book = Book.query.get(id)
            if book is None:
                return jsonify({"message": "Livro nao encontrado"}), 404
            return jsonify({
                "id": book.id,
                "title": book.title,
                "author": book.author,
                "genre": book.genre,
                "year": book.year
            })

        
        if request.method == 'PUT':
            book = Book.query.get(id)
            if book is None:
                return jsonify({"message": "Livro nao encontrado"}), 404

            data = request.json
            book.title = data['title']
            book.author = data['author']
            book.genre = data['genre']
            book.year = data['year']
            
            db.session.commit()
            return jsonify({"message": "Livro atualizado com sucesso!"})

        
        if request.method == 'DELETE':
            book = Book.query.get(id)
            if book is None:
                return jsonify({"message": "Book not found"}), 404

            db.session.delete(book)
            db.session.commit()
            return jsonify({"message": "Livro deletado com sucesso!"}), 200
        




        #---------------------------------------------------------------------------------------------------------------------------------------------------------------------
        
    

 
    @app.route('/user', methods=['GET', 'POST'])
    def manage_users():
        
        if request.method == 'POST':
            data = request.json
            new_user = User(
                name=data['name'],
                address=data['address'],
                email=data['email'],
                phone=data['phone']
            )
            db.session.add(new_user) 
            db.session.commit()  
            return jsonify({"message": "Usuário adicionado com sucesso!"}), 201

        
        users = User.query.all() 
        if users:
            return jsonify([{
                "id": user.id,
                "name": user.name,
                "address": user.address,
                "email": user.email,
                "phone": user.phone
            } for user in users])
        else:
            return jsonify({"message": "Nenhum usuário encontrado"}), 404
        
    @app.route('/user/<int:id>', methods=['GET', 'PUT', 'DELETE'])
    def manage_single_user(id):
        
        if request.method == 'GET':
            user = User.query.get(id)
            if user is None:
                return jsonify({"message": "Usuário não encontrado"}), 404
            return jsonify({
                "id": user.id,
                "name": user.name,
                "address": user.address,
                "email": user.email,
                "phone": user.phone
            })

        
        if request.method == 'PUT':
            user = User.query.get(id)
            if user is None:
                return jsonify({"message": "Usuário não encontrado"}), 404

            data = request.json
            user.name = data['name']
            user.address = data['address']
            user.email = data['email']
            user.phone = data['phone']
            
            db.session.commit()  
            return jsonify({"message": "Usuário atualizado com sucesso!"})

       
        if request.method == 'DELETE':
            user = User.query.get(id)
            if user is None:
                return jsonify({"message": "Usuário não encontrado"}), 404

            db.session.delete(user)  
            db.session.commit()  
            return jsonify({"message": "Usuário deletado com sucesso!"}), 200
        
        #---------------------------------------------------------------------------------------------------------------------------------------------------------------------

    MAX_LOANS = 3  

    # registrar e listar empréstimos
    @app.route('/loans', methods=['GET', 'POST'])
    def manage_loans():
        
        if request.method == 'POST':
            data = request.json
            user_id = data['user_id']
            book_id = data['book_id']
            
           
            book = Book.query.get(book_id)
            if book is None:
                return jsonify({"message": "Livro não encontrado"}), 404

           
            user = User.query.get(user_id)
            if user is None:
                return jsonify({"message": "Usuário não encontrado"}), 404

           
            user_loans_count = Loan.query.filter_by(user_id=user_id, return_date=None).count()
            if user_loans_count >= MAX_LOANS:
                return jsonify({"message": "Limite de empréstimos alcançado"}), 400

            # Registrar o empréstimo
            new_loan = Loan(
                user_id=user_id,
                book_id=book_id,
                loan_date=datetime.utcnow()
            )
            db.session.add(new_loan)
            db.session.commit()
            return jsonify({"message": "Empréstimo registrado com sucesso!"}), 201

        
        loans = Loan.query.all()
        if loans:
            return jsonify([{
                "id": loan.id,
                "user_id": loan.user_id,
                "book_id": loan.book_id,
                "loan_date": loan.loan_date,
                "return_date": loan.return_date
            } for loan in loans])
        else:
            return jsonify({"message": "Nenhum empréstimo encontrado"}), 404
        
    # devolver livros 
    @app.route('/loans/<int:id>/return', methods=['PUT'])
    def return_loan(id):
        loan = Loan.query.get(id)
        if loan is None:
            return jsonify({"message": "Empréstimo não encontrado"}), 404
        
        
        loan.return_date = datetime.utcnow()
        db.session.commit()
        return jsonify({"message": "Livro devolvido com sucesso!"})

    # excluir um empréstimo
    @app.route('/loans/<int:id>', methods=['DELETE'])
    def delete_loan(id):
        loan = Loan.query.get(id)
        if loan is None:
            return jsonify({"message": "Empréstimo não encontrado"}), 404

        db.session.delete(loan)
        db.session.commit()
        return jsonify({"message": "Empréstimo excluído com sucesso!"}), 200
    
    #------------------------------------------------------------------------------------------------------------------------

    @app.route('/reports/maisempretimo', methods=['GET'])
    def most_borrowed_books():
    
        result = db.session.query(Loan.book_id, db.func.count(Loan.book_id).label('count')) \
            .group_by(Loan.book_id) \
            .order_by(db.func.count(Loan.book_id).desc()) \
            .limit(5).all()

   
        books = []
        for book_id, count in result:
            book = Book.query.get(book_id)
            if book:
                books.append({
                    "title": book.title,
                    "author": book.author,
                    "genre": book.genre,
                    "year": book.year,
                    "borrow_count": count
            })

        return jsonify(books)

# usuários com empréstimos pendentes
    @app.route('/reports/pendentes', methods=['GET'])
    def pendentes():
    
        result = db.session.query(Loan.user_id, db.func.count(Loan.id).label('pending_loans')) \
            .filter(Loan.return_date == None) \
            .group_by(Loan.user_id) \
            .all()

   
        users = []
        for user_id, pending_loans in result:
            user = User.query.get(user_id)
            if user:
                users.append({
                    "name": user.name,
                    "email": user.email,
                    "pending_loans": pending_loans
            })

        return jsonify(users)