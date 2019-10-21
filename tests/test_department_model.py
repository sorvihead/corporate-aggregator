import unittest

from app import create_app
from app import db
from app.models import Role
from app.models import Department
from app.models import User


class DepartmentModelTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        Role.insert_roles()
        a = User(name='admin', email='sorvihead1@gmail.com', password='123')
        u1 = User(name='10', email='10', password='123')
        u2 = User(name='20', email='20', password='123')
        u3 = User(name='30', email='30', password='123')
        d = Department(name='kids')
        u1.department = d
        db.session.add_all([a, u1, u2, u3, d])
        db.session.commit()

    def tearDown(self) -> None:
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_department_right_create(self):
        d = Department.query.filter_by(name='kids').first()
        self.assertIsNotNone(d)

    def test_admin_in_department(self):
        a = User.query.filter_by(name='admin').first()
        d = Department.query.filter_by(name='kids').first()
        self.assertTrue(a in d.users)
        self.assertTrue(a.department == d)

    def test_add_user(self):
        d = Department.query.filter_by(name='kids').first()
        users = User.query.all()
        for u in users:
            d.add_user(u)
        db.session.add(d)
        db.session.commit()
        for u in users:
            self.assertTrue(u in d.users)
            self.assertTrue(u.department == d)

    def test_remove_user(self):
        d = Department.query.filter_by(name='kids').first()
        users = User.query.all()
        for u in users:
            d.remove_user(u)
        db.session.add(d)
        db.session.commit()
        for u in users:
            self.assertFalse(u in d.users)
            self.assertFalse(u.department == d)

    def test_has_user(self):
        d = Department.query.filter_by(name='kids').first()
        u1 = User(name='40', email='40', password='4')
        u2 = User(name='50', email='50', password='4')
        users = [u1, u2]
        db.session.add_all(users)
        db.session.commit()
        for u in users:
            d.add_user(u)
        db.session.add(d)
        db.session.commit()
        for u in users:
            self.assertTrue(d.has_user(u))

        d.remove_user(users[1])
        db.session.add(d)
        db.session.commit()
        self.assertTrue(d.has_user(users[0]))
        self.assertFalse(d.has_user(users[1]))
