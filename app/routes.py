from jsonschema import validate, Draft7Validator

from app import app
from flask import jsonify
from flask import abort
from flask import make_response
from flask import request
from . import schemas

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


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not Found'}), 404)


@app.errorhandler(405)
def not_found(error):
    return make_response(jsonify({'error': 'Method Not Allowed'}), 405)


@app.route('/organization/api/v1.0/employees', methods=['GET'])
def get_employees():
    return jsonify({'employees': employees})


@app.route('/organization/api/v1.0/employees/<int:employee_id>', methods=['GET'])
def get_employee(employee_id):
    employee = list(filter(lambda t: t['id'] == employee_id, employees))
    return jsonify({'employee': employee[0]}) if len(employee) > 0 else abort(404)


@app.route('/organization/api/v1.0/employees/', methods=['POST'])
def create_employee():
    if not request.json:
        abort(400)
    v = Draft7Validator(schemas.employee_schema)
    errors = sorted(v.iter_errors(request.json), key=lambda e: e.path)
    if len(errors) > 0:
        error_response = [error.message for error in errors]
        return make_response(jsonify({'errors': error_response}), 400)
    employee = {
        'id': employees[-1]['id'] + 1,
        'surname': request.json['surname'],
        'name': request.json['name'],
        'patronymic': request.json['patronymic'],
        'position': request.json['position'],
        'number': request.json['number']
    }
    employees.append(employee)
    return jsonify({'employees': employees}), 201


@app.route('/organization/api/v1.0/employees/<int:employee_id>', methods=['PUT'])
def put_employee(employee_id):
    employee = list(filter(lambda t: t['id'] == employee_id, employees))
    if not request.json:
        abort(400)
    v = Draft7Validator(schemas.employee_schema)
    errors = sorted(v.iter_errors(request.json), key=lambda e: e.path)
    if len(errors) > 0:
        error_response = [error.message for error in errors]
        return make_response(jsonify({'errors': error_response}), 400)
    employee[0]['surname'] = request.json.get('surname', employee[0]['surname'])
    employee[0]['name'] = request.json.get('name', employee[0]['name'])
    employee[0]['patronymic'] = request.json.get('patronymic', employee[0]['patronymic'])
    employee[0]['position'] = request.json.get('position', employee[0]['position'])
    employee[0]['number'] = request.json.get('number', employee[0]['number'])
    return jsonify({'employee': employee[0]}), 200


@app.route('/organization/api/v1.0/employees/<int:employee_id>', methods=['DELETE'])
def delete_employee(employee_id):
    employee = list(filter(lambda t: t['id'] == employee_id, employees))
    if len(employee) == 0:
        abort(404)
    employees.remove(employee[0])
    return jsonify({'result': True})
