import sqlalchemy
from jsonschema import Draft7Validator
from app import app, db
from flask import jsonify, json
from flask import abort
from flask import make_response
from flask import request
from . import schemas
from .models import Employee

employees = [
    {
        'id': 1,
        'surname': 'Kovalchuk',
        'name': 'Ivan',
        'patronymic': 'Kirillovich',
        'position': 'programmer',
        'number': '1'
    },
    {
        'id': 2,
        'surname': 'Likhachev',
        'name': 'Mikhail',
        'patronymic': 'Petrovich',
        'position': 'SoftWare Architect',
        'number': '2'
    }
]


@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'error': 'Bad request'}))


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not Found'}), 404)


@app.errorhandler(405)
def not_found(error):
    return make_response(jsonify({'error': 'Method Not Allowed'}), 405)


@app.errorhandler(500)
def not_found(error):
    return make_response(jsonify({'error': 'Internal Server Error'}), 500)


@app.route('/organization/api/v1.0/employees', methods=['GET'])
def get_employees():
    employees = Employee.query.all()
    return jsonify({'employees': [employee.to_dict() for employee in employees]})


@app.route('/organization/api/v1.0/employees/<string:employee_id>', methods=['GET'])
def get_employee(employee_id):
    employee = Employee.query.get(employee_id)
    return jsonify({'employee': employee.to_dict()}) if employee else abort(404)


@app.route('/organization/api/v1.0/employees/', methods=['POST'])
def create_employee():
    if not request.json:
        abort(400)
    v = Draft7Validator(schemas.employee_schema)
    errors = sorted(v.iter_errors(request.json), key=lambda e: e.path)
    if len(errors) > 0:
        error_response = [error.message for error in errors]
        return make_response(jsonify({'errors': error_response}), 400)
    try:
        employee = Employee(surname=request.json['surname'],
                            name=request.json['name'],
                            patronymic=request.json['patronymic'],
                            position=request.json['position'],
                            number=int(request.json['number']))

        db.session.add(employee)
        db.session.commit()
    except Exception as e:
        return make_response(jsonify({'errors': str(e)}), 400)

    employee = {
        'id': employee.id,
        'surname': employee.surname,
        'name': employee.name,
        'patronymic': employee.patronymic,
        'position': employee.position,
        'number': employee.number
    }
    # employees.append(employee)
    return jsonify({'employee': employee}), 201


@app.route('/organization/api/v1.0/employees/<string:employee_id>', methods=['PUT'])
def put_employee(employee_id):
    employee = Employee.query.get(employee_id)
    if not employee:
        abort(400)
    if not request.json:
        abort(400)
    v = Draft7Validator(schemas.employee_schema)
    errors = sorted(v.iter_errors(request.json), key=lambda e: e.path)
    if len(errors) > 0:
        error_response = [error.message for error in errors]
        return make_response(jsonify({'errors': error_response}), 400)
    try:
        employee.surname = request.json.get('surname', employee.surname)
        employee.name = request.json.get('name', employee.name)
        employee.patronymic = request.json.get('patronymic', employee.patronymic)
        employee.position = request.json.get('position', employee.position)
        employee.number = request.json.get('number', employee.number)
        db.session.commit()
    except Exception as e:
        return make_response(jsonify({'errors': str(e)}), 400)
    return jsonify({'employee': employee.to_dict()}), 200


@app.route('/organization/api/v1.0/employees/<string:employee_id>', methods=['DELETE'])
def delete_employee(employee_id):
    employee = Employee.query.get(employee_id)
    if not employee:
        abort(404)
    db.session.delete(employee)
    db.session.commit()
    return jsonify({'result': True})
