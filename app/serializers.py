from flask_restplus import fields
from app import api


employee_post = api.model('Данные о сотруднике', {
    'surname': fields.String(description='Фамилия', required=True),
    'name': fields.String(description='Имя', required=True),
    'patronymic': fields.String(description='Отчество', required=True),
    'position': fields.String(description='Должность в организации'),
    'number': fields.Integer(description='Табельный номер'),
})

employee_put = api.model('Данные о сотруднике', {
    'surname': fields.String(description='Фамилия'),
    'name': fields.String(description='Имя'),
    'patronymic': fields.String(description='Отчество'),
    'position': fields.String(description='Должность в организации'),
    'number': fields.Integer(description='Табельный номер'),
})
