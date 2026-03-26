from models.memberModel import Member
from config.db import db
from flask import Blueprint, request, jsonify

member_bp = Blueprint('members', __name__)

@member_bp.route('/members', methods=['POST'])
def create_member():
    data = request.json
    member = Member(
        StudentID = data['StudentID'],
        FirstName = data['FirstName'],
        LastName = data['LastName'],
        Email = data['Email'],
        PhoneNumber = data['PhoneNumber'], 
    )
    if db.session.get(Member, member.StudentID):
        return jsonify({'message': 'Member con ese StudentID ya existe'}), 400
    
    db.session.add(member)
    db.session.commit()

    return jsonify({'message': 'Member creado exitosamente'}), 201


@member_bp.route('/members', methods = ['GET'])
def get_members():
    members = Member.query.all()
    result = []

    if not members:
        return jsonify({'Message':'No hay ningun Miembro para Mostrar'})

    for member in members:
        result.append({
        'MemberID': member.MemberID,
        'StudentID': member.StudentID,
        'FirstName': member.FirstName,
        'LastName': member.LastName,  
        'Email': member.Email,
        "PhoneNumber": member.PhoneNumber
        })

    return jsonify(result),200

@member_bp.route('/members/<int:id>', methods = ['GET'])
def get_member(id):
    member = db.session.get(Member, id)
    if not member:
        return jsonify({'Message':'No hay ningun Miembro con ese ID'})
    
    return jsonify({
        'MemberID': member.MemberID,
        'StudentID': member.StudentID,
        'FirstName': member.FirstName,
        'LastName': member.LastName,  
        'Email': member.Email,
        "PhoneNumber": member.PhoneNumber
    }), 200

@member_bp.route('/members/<int:id>', methods = ['PUT'])
def update_member(id):
    member = db.session.get(Member,id) 
    if not member:
        return jsonify({"Message":"No hay ningun Miembro con ese ID"}),404
    
    data = request.json

    member.FirstName = data.get('FirstName', member.FirstName)
    member.LastName = data.get('LastName', member.LastName)
    member.Email = data.get('Email', member.Email)
    member.PhoneNumber = data.get('PhoneNumber', member.PhoneNumber)

    db.session.commit()

    return jsonify({
        "Message": "Usuario actualizado correctamente",
        'FirstName': member.FirstName,
        'LastName': member.LastName,
        'Email': member.Email,
        'PhoneNumber': member.PhoneNumber
    }),200
    

@member_bp.route('/members/<int:id>', methods=['DELETE'])
def delete_member(id):
    
    member = db.session.get(Member,id)

    if not member:
        return jsonify({'Message': 'No se encontro ningun Miembro'}),404
    
    db.session.delete(member)
    db.session.commit()

    return jsonify({'Message': 'Se elimino correctamente el miembro'}),200
        