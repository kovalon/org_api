from app import app, db
from app.models import Employee


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Employee': Employee}


if __name__ == "__main__":
    app.run(ebug=False, host='0.0.0.0')
