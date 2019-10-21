import unittest

from app import create_app
from app import db
from app.models import Role
from app.models import Shop
from app.models import User


class ShopModelTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        Role.insert_roles()
        a = User(name='admin', email='sorvihead1@gmail.com', password='123')
        u1 = User(name='1', email='1', password='123')
        u2 = User(name='2', email='2', password='123')
        u3 = User(name='3', email='3', password='123')
        s = Shop(name='afi', shop_code='9066')
        u1.shop = s
        db.session.add_all([a, u1, u2, u3, s])
        db.session.commit()

    def tearDown(self) -> None:
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_shop_right_create(self):
        s = Shop.query.filter_by(name='afi').first()
        self.assertIsNotNone(s)
        self.assertEqual(s.shop_code, '9066')

    def test_admin_in_shop(self):
        a = User.query.filter_by(name='admin').first()
        s = Shop.query.filter_by(name='afi').first()
        self.assertTrue(a in s.users)
        self.assertTrue(a.shop == s)

    def test_add_user(self):
        s = Shop.query.filter_by(name='afi').first()
        users = User.query.all()
        for u in users:
            s.add_user(u)
        db.session.add(s)
        db.session.commit()
        for u in users:
            self.assertTrue(u in s.users)
            self.assertTrue(u.shop == s)

    def test_remove_user(self):
        s = Shop.query.filter_by(name='afi').first()
        users = User.query.all()
        for u in users:
            s.remove_user(u)
        db.session.add(s)
        db.session.commit()
        for u in users:
            self.assertFalse(u in s.users)
            self.assertFalse(u.shop == s)

    def test_has_user(self):
        s = Shop.query.filter_by(name='afi').first()
        u1 = User(name='4', email='4', password='4')
        u2 = User(name='5', email='5', password='4')
        users = [u1, u2]
        db.session.add_all(users)
        db.session.commit()
        for u in users:
            s.add_user(u)
        db.session.add(s)
        db.session.commit()
        for u in users:
            self.assertTrue(s.has_user(u))

        s.remove_user(users[1])
        db.session.add(s)
        db.session.commit()
        self.assertTrue(s.has_user(users[0]))
        self.assertFalse(s.has_user(users[1]))
