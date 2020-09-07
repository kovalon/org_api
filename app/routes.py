import uuid
from flask_restplus import Resource
from app import db, api
from flask import jsonify
from flask_restplus import abort
from flask import make_response
from flask import request
from .models import Employee
from .serializers import employee_post, employee_put

ns = api.namespace('organization/api/v1.0/employees', description='Операции, связанные с реестром работников')


# Класс, описывающий методы get и post объекта Employee
@ns.route('/')
@api.response(400, 'Введены неверные данные')
@api.response(500, 'Ошибка сервера')
class EmployeeCollection(Resource):
    @api.response(200, 'Выдача реестра сотрудников')
    def get(self):
        """Возращает список работников"""
        employees = Employee.query.all()
        return jsonify({'employees': [employee.to_dict() for employee in employees]})

    @api.response(201, 'Сотрудник успешно создан')
    @api.expect(employee_post)
    def post(self):
        """Создает нового работника в реестре Employee"""
        try:
            employee = Employee(id=str(uuid.uuid4()),
                                surname=request.json['surname'],
                                name=request.json['name'],
                                patronymic=request.json['patronymic'],
                                position=request.json['position'],
                                number=int(request.json['number']))
            db.session.add(employee)
            db.session.commit()
        except Exception as e:
            return make_response(jsonify({'errors': str(e)}), 400)
        result = {
            'id': str(employee.id),
            'surname': employee.surname,
            'name': employee.name,
            'patronymic': employee.patronymic,
            'position': employee.position,
            'number': employee.number,
        }
        return {'employee': result}, 201


# Класс, описывающий методы get, put и delete объекта Employee с использование id в качестве path параметра
@ns.route('/<string:id>')
@api.response(404, 'Работник не найден')
@api.response(400, 'Введены неверные данные')
@api.response(500, 'Ошибка сервера')
class EmployeeItem(Resource):
    @api.response(200, 'Выдается сотрудник по переданному в запросе id')
    def get(self, id):
        """Возращает данные о сотруднике по его id"""
        employee = Employee.query.get(id)
        return jsonify({'employee': employee.to_dict()}) if employee else abort(404)

    @api.response(200, 'Данные сотрудника успешно обновлены')
    @api.expect(employee_put)
    def put(self, id):
        """Обновляет данные о сотруднике в реестре Employee"""
        employee = Employee.query.get(id)
        try:
            employee.surname = request.json.get('surname', employee.surname)
            employee.name = request.json.get('name', employee.name)
            employee.patronymic = request.json.get('patronymic', employee.patronymic)
            employee.position = request.json.get('position', employee.position)
            employee.number = request.json.get('number', employee.number)
            db.session.commit()
        except Exception as e:
            return make_response(jsonify({'errors': str(e)}), 400)
        result = {
            'id': str(employee.id),
            'surname': employee.surname,
            'name': employee.name,
            'patronymic': employee.patronymic,
            'position': employee.position,
            'number': employee.number,
        }
        return {'employee': result}, 200

    @api.response(200, 'Сотрудник успешно удален')
    def delete(self, id):
        """Удаляет сотрудника из реесра Employee"""
        employee = Employee.query.get(id)
        if not employee:
            abort(404, 'Not found')
        db.session.delete(employee)
        db.session.commit()
        return jsonify({'result': True})
