from app import app, db
from app.models import Employee
import daemon


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Employee': Employee}


with daemon.DaemonContext():
    if __name__ == "__main__":
        app.run(debug=False, host='0.0.0.0')
