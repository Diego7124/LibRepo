from flask import Blueprint, request, jsonify
from config.db import db
from models.authorModel import Author
from models.bookModel import Book

author_bp = Blueprint('authors',__name__)

@author_bp.route('/authors', methods=['POST'])
def create_author():
    data = request.json
    author = Author(
        FirstName=data['FirstName'],
        LastName=data['LastName'],
        BirthDate=data.get('BirthDate'),
        Nationality=data.get('Nationality')
    )
    db.session.add(author)
    db.session.commit()

    return jsonify({'message': 'Author creado exitosamente'}), 201

@author_bp.route('/authors', methods=['GET'])
def get_authors():
    authors = Author.query.all()
    result = []

    for author in authors:
        result.append({
            'AuthorID': author.AuthorID,
            'FirstName': author.FirstName,
            'LastName': author.LastName,
            'BirthDate': str(author.BirthDate) if author.BirthDate else None,
            'Nationality': author.Nationality
        })

    if not authors:
        return jsonify({'message': 'No se encontraron authors'}), 404

    return jsonify(result), 200


@author_bp.route('/authors/<int:id>', methods=['GET'])
def get_author(id):
    author = db.session.get(Author, id)
    if not author:
        return jsonify({'Message': 'Error, no hay ningun author con ese ID'}), 404

    return jsonify({
        'AuthorID': author.AuthorID,
        'FirstName': author.FirstName,
        'LastName': author.LastName,
        'BirthDate': str(author.BirthDate) if author.BirthDate else None,
        'Nationality': author.Nationality
    }), 200
    
@author_bp.route('/authors/<int:id>', methods = ['PUT'])
def update_author(id):
    author = db.session.get(Author, id)
    if not author:
        return jsonify({"Message":"No hay ningun libro con ese ID"}), 404
    data = request.json

    author.FirstName = data.get('FirstName', author.FirstName)
    author.LastName = data.get('LastName', author.LastName)
    author.BirthDate = data.get('BirthDate', author.BirthDate)
    author.Nationality = data.get('Nationality', author.Nationality)

    db.session.commit()

    return jsonify({
        'FirstName' : author.FirstName,
        'LastName' : author.LastName,
        'BirthDate' : author.BirthDate,
        'Nationality' : author.Nationality  
    }), 200

@author_bp.route('/authors/<int:id>', methods=['DELETE'])
def delete_author(id):
    author = db.session.get(Author, id)
    if not author:
        return jsonify({"Message":"No hay ningun libro con ese ID"}), 404
    
    db.session.delete(author)
    db.session.commit()

    return jsonify({"Message":"Author eliminado exitosamente"}), 200
