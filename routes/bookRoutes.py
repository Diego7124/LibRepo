from flask import Blueprint, request, jsonify
from config.db import db
from models.bookModel import Book
from models.authorModel import Author

book_bp = Blueprint('books', __name__)


def parse_int(value, field_name):
    if value is None or value == '':
        return None
    try:
        return int(value)
    except (TypeError, ValueError):
        raise ValueError(f'{field_name} debe ser un numero entero')


def parse_publication_year(value):
    if value is None or value == '':
        return None
    if isinstance(value, str):
        value = value.strip()
        if len(value) >= 4 and value[:4].isdigit():
            return int(value[:4])
    return parse_int(value, 'PublicationYear')

#crud routes

#bookRoutes
@book_bp.route('/books', methods = ['POST'])
def create_book():
    data = request.json
    try:
        author_id = parse_int(data.get('AuthorID'), 'AuthorID')
        publication_year = parse_publication_year(data.get('PublicationYear'))
        available_copies = parse_int(data.get('AvailableCopies', data.get('AvialableCopies', 0)), 'AvailableCopies')
        total_copies = parse_int(data.get('TotalCopies', 0), 'TotalCopies')
    except ValueError as error:
        return jsonify({'error': str(error)}), 400

    author = db.session.get(Author, author_id)
    if not author:
        return jsonify({'Error':'Author no encontrado'}),404
    book = Book(
        ISBN = data['ISBN'],
        Title = data['Title'],
        AuthorID=author_id,
        PublicationYear=publication_year,
        AvailableCopies=available_copies,
        TotalCopies=total_copies
    )

    db.session.add(book)
    db.session.commit()
    return jsonify({'message':'Libro creado exitosamente'}),201

@book_bp.route('/books', methods=['GET'])
def get_books():
    books = Book.query.all()
    result = []
    for book in books:
        result.append({
            'BookID': book.BookID,
            'ISBN': book.ISBN,
            'Title': book.Title,
            'AuthorID': book.AuthorID,
            'PublicationYear': book.PublicationYear,
            'AvailableCopies': book.AvailableCopies,
            'TotalCopies': book.TotalCopies
    })
    
    if not books:
        return jsonify({"message": 'No se pudieron obtener los libros'}),404
        
    return jsonify(result),200

@book_bp.route('/books/<int:id>', methods=['GET'])
def get_book(id):
    book = db.session.get(Book, id)
    if not book:
        return jsonify({'message': 'Libro no encontrado'}), 404
    return jsonify({
        'BookID': book.BookID,
        'ISBN': book.ISBN,
        'Title': book.Title,
        'AuthorID': book.AuthorID,
        'PublicationYear': book.PublicationYear,
        'AvailableCopies': book.AvailableCopies,
        'TotalCopies': book.TotalCopies
    }), 200
    

@book_bp.route('/books/<int:id>', methods=['PUT'])
def update_book(id):
    book = db.session.get(Book,id)
    if not book:
        return jsonify({'message': 'Libro no encontrado'}), 404
    
    data = request.json

    try:
        author_id = parse_int(data['AuthorID'], 'AuthorID') if 'AuthorID' in data else book.AuthorID
        publication_year = parse_publication_year(data['PublicationYear']) if 'PublicationYear' in data else book.PublicationYear
        available_copies = parse_int(data.get('AvailableCopies', data.get('AvialableCopies')), 'AvailableCopies') if ('AvailableCopies' in data or 'AvialableCopies' in data) else book.AvailableCopies
        total_copies = parse_int(data['TotalCopies'], 'TotalCopies') if 'TotalCopies' in data else book.TotalCopies
    except ValueError as error:
        return jsonify({'error': str(error)}), 400

    if 'AuthorID' in data:
        author = db.session.get(Author, author_id)
        if not author:
            return jsonify({'Error': 'Author no encontrado'}), 404
    
    book.ISBN = data.get('ISBN', book.ISBN)
    book.Title = data.get('Title', book.Title)
    book.AuthorID = author_id
    book.PublicationYear = publication_year
    book.AvailableCopies = available_copies
    book.TotalCopies = total_copies

    db.session.commit()

    return jsonify({
        'BookID': book.BookID,
        'ISBN': book.ISBN,
        'Title': book.Title,
        'AuthorID': book.AuthorID,
        'PublicationYear': book.PublicationYear,
        'AvailableCopies': book.AvailableCopies,
        'TotalCopies': book.TotalCopies
    }), 200

        

@book_bp.route('/books/<int:id>', methods=['DELETE'])
def delete_book(id):
    book = db.session.get(Book, id)
    if not book:
        return jsonify({'message': 'No hay ningun libro con ese ID'}), 404
    db.session.delete(book)
    db.session.commit()
    return jsonify({'message': 'Libro eliminado exitosamente'}), 200
