from app import create_app
from app import db

from app.models import User

import unittest
import time

class UserModelTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self) -> None:
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_password_setter(self):
        u = User(password='cat')
        with self.assertRaises(AttributeError):
            u.password

    def test_password_verification(self):
        u = User(password='cat')
        self.assertTrue(u.check_password('cat'))
        self.assertFalse(u.check_password('dog'))

    def test_random_password_salt(self):
        u = User(password='cat')
        u2 = User(password='cat')
        self.assertTrue(u.hash_password != u2.hash_password)

    def test_valid_confirmation_token(self):
        u = User(password='cat')
        db.session.add(u)
        db.session.commit()
        token = u.generate_confirmation_token()
        self.assertTrue(u.confirm(token))

    def test_invalid_confirmation_token(self):
        u = User(password='cat')
        u2 = User(password='dog')
        db.session.add_all([u, u2])
        db.session.commit()
        token = u.generate_confirmation_token()
        self.assertFalse(u2.confirm(token))

    def test_expired_confirmation_token(self):
        u = User(password='cat')
        db.session.add(u)
        db.session.commit()
        token = u.generate_confirmation_token(1)
        time.sleep(2)
        self.assertFalse(u.confirm(token))

    def test_valid_reset_password(self):
        u = User(password='cat')
        db.session.add(u)
        db.session.commit()
        token = u.generate_reset_token()
        self.assertTrue(User.reset_password(token, 'dog'))
        self.assertTrue(u.check_password('dog'))

    def test_invalid_reset_password(self):
        u = User(password='cat')
        db.session.add_all([u])
        db.session.commit()
        token = u.generate_reset_token()
        self.assertFalse(User.reset_password(token+'1', 'dog'))
        self.assertTrue(u.check_password('cat'))

    def test_expired_reset_token(self):
        u = User(password='cat')
        db.session.add(u)
        db.session.commit()
        token = u.generate_reset_token(1)
        time.sleep(2)
        self.assertFalse(User.reset_password(token, 'dog'))
        self.assertTrue(u.check_password('cat'))
