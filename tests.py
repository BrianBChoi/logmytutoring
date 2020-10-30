from datetime import datetime, timedelta
import unittest
from app import app, db
from app.models import User, Session

class UserModelCase(unittest.TestCase):
    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://' # temp database
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_password_hashing(self):
        u = User(username='susan')
        u.set_password('cat')
        self.assertFalse(u.check_password('dog'))
        self.assertTrue(u.check_password('cat'))

    def test_avatar(self):
        u = User(username='john', email='john@example.com')
        self.assertEqual(u.avatar(128), ('https://www.gravatar.com/avatar/'
                                         'd4c74594d841139328695756648b6bd6'
                                         '?d=identicon&s=128'))

    def test_new_sessions(self):
        # create a user
        u = User(username='john')
        db.session.add(u)
        db.session.commit()
        self.assertEqual(u.sessions.all(), [])

        # create three sessions
        s1 = Session(notes='session1', tutor=u,
                     date=datetime.utcnow() + timedelta(seconds=1))
        s2 = Session(notes='session2', tutor=u,
                     date=datetime.utcnow() + timedelta(seconds=2))
        s3 = Session(notes='session3', tutor=u,
                     date=datetime.utcnow() + timedelta(seconds=3))
        db.session.add_all([s1, s2, s3])
        db.session.commit()

        # check all sessions are showing up
        all_sessions = u.sessions.all()
        self.assertEqual(all_sessions, [s1, s2, s3])

        # check descending order of new_sessions()
        new_sessions = u.new_sessions().all()
        self.assertEqual(new_sessions, [s3, s2, s1])

if __name__ == '__main__':
    unittest.main(verbosity=2)
