from app import app, db
from app.models import User, Student, Session

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Session': Session, 'Student', Student}
