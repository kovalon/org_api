from jsonschema import validate

employee_schema = {
    "type": "object",
    "properties": {
        "surname": {"type": "string"},
        "name": {"type": "string"},
        "patronymic": {"type": "string"},
        "position": {"type": "string"},
        "number": {"type": "integer"}
    },
    "required": [
            "surname",
            "name",
            "patronymic",
            "position",
            "number"
        ]
}
