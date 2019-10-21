from datetime import datetime
from hashlib import md5

from flask import current_app
from flask_login import AnonymousUserMixin
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash

from app import db
from app import login


class Permission:
    FOLLOW = 1
    WRITE = 2
    MODERATE = 4
    ADMIN = 8


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), index=True)
    surname = db.Column(db.String(50), index=True)
    username = db.Column(db.String(20), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    hash_password = db.Column(db.String(128))
    about_me = db.Column(db.Text())
    position = db.Column(db.String(128), index=True)
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    confirmed = db.Column(db.Boolean, default=False)
    requests = db.relationship('Request', backref='user', lazy='dynamic')
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))
    shop_id = db.Column(db.Integer, db.ForeignKey('shop.id'))
    department_id = db.Column(db.Integer, db.ForeignKey('department.id'))

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if not self.role:
            if self.email in current_app.config['ADMINS']:
                self.role = Role.query.filter_by(name='Administrator').first()
            else:
                self.role = Role.query.filter_by(default=True).first()

    def __repr__(self):
        return f'<User -> name: {self.name},' \
               f' role: {self.role},' \
               f' confirmed: {self.confirmed}>'

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.hash_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hash_password, password)

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return f'https://www.gravatar.com/avatar/{digest}?d=identicon&s={size}'

    def generate_reset_token(self, expires_in=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expires_in)
        return s.dumps({'reset': self.id}).decode('utf-8')

    @staticmethod
    def reset_password(token, new_password):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token.encode('UTF-8'))
        except:
            return False
        user = User.query.get(data.get('reset'))
        if not user:
            return False
        user.password = new_password
        db.session.add(user)
        return True

    def generate_confirmation_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm': self.id}).decode('utf-8')

    def confirm(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token.encode('utf-8'))
        except:
            return False

        if data.get('confirm') != self.id:
            return False
        self.confirmed = True
        db.session.add(self)
        return True

    def can(self, perm):
        return self.role and self.role.has_permission(perm)

    def is_administrator(self):
        return self.can(Permission.ADMIN)

    def ping(self):
        self.last_seen = datetime.utcnow()
        db.session.add(self)
        db.session.commit()

    def accept_request(self, request):
        if self.can(Permission.MODERATE) or self.is_administrator():
            request.approved = True
            db.session.add(request)
            return request
        else:
            raise PermissionError

    def reject_request(self, request, message=None):
        if self.can(Permission.MODERATE) or self.is_administrator():
            request.approved = False
            request.message = message
            db.session.add(request)
            return request
        else:
            raise PermissionError

    def elevate(self, user, role=None):
        if self.can(Permission.MODERATE) or self.is_administrator():
            if not role:
                role = Role.query.filter_by(name='User').first()
                user.role = role
                db.session.add(user)
            else:
                user.role = role
                db.session.add(user)
        else:
            raise PermissionError

    def add_to_shop(self, user, shop):
        if self.can(Permission.MODERATE) or self.is_administrator():
            shop.add_user(user)
        else:
            raise PermissionError

    def add_to_department(self, user, department):
        if self.can(Permission.MODERATE) or self.is_administrator():
            department.add_user(user)
        else:
            raise PermissionError

    def remove_from_shop(self, user, shop):
        if self.can(Permission.MODERATE) or self.is_administrator():
            shop.remove_user(user)
        else:
            raise PermissionError

    def remove_from_department(self, user, department):
        if self.can(Permission.MODERATE) or self.is_administrator():
            department.remove_user(user)
        else:
            raise PermissionError


class AnonymousUser(AnonymousUserMixin):
    def can(self, permissions):
        return False

    def is_administrator(self):
        return False


login.anonymous_user = AnonymousUser


class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    default = db.Column(db.Boolean, default=False, index=True)
    permissions = db.Column(db.Integer)
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __init__(self, **kwargs):
        super(Role, self).__init__(**kwargs)
        if not self.permissions:
            self.permissions = 0

    def add_permission(self, perm):
        if not self.has_permission(perm):
            self.permissions += perm

    def remove_permission(self, perm):
        if self.has_permission(perm):
            self.permissions -= perm

    def reset_permissions(self):
        self.permissions = 0

    def has_permission(self, perm):
        return self.permissions & perm == perm

    @staticmethod
    def insert_roles():
        roles = {
            'Unfollow': [Permission.FOLLOW],
            'User': [Permission.FOLLOW, Permission.WRITE],
            'Moderator': [Permission.FOLLOW, Permission.WRITE, Permission.MODERATE],
            'Administrator': [Permission.FOLLOW, Permission.WRITE, Permission.MODERATE, Permission.ADMIN]
        }
        default_role = 'Unfollow'
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if not role:
                role = Role(name=r)
            role.reset_permissions()
            for perm in roles[r]:
                role.add_permission(perm)
            role.default = (role.name == default_role)
            db.session.add(role)

        db.session.commit()

    def __repr__(self):
        return f'<Role -> name: {self.name},' \
               f' default: {self.default},' \
               f' permissions: {self.permissions}>'


class Shop(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, index=True)
    shop_code = db.Column(db.String(8), unique=True, index=True)
    users = db.relationship('User', backref='shop', lazy='dynamic')
    departments = db.relationship('Department', backref='shop', lazy='dynamic')  # TODO
    requests = db.relationship('Request', backref='shop', lazy='dynamic')  # TODO

    def __init__(self, **kwargs):
        super(Shop, self).__init__(**kwargs)
        role = Role.query.filter_by(name='Administrator').first()
        admin = User.query.filter_by(role=role).first()
        self.users.append(admin)

    def add_user(self, user):
        if not self.has_user(user):
            self.users.append(user)

    def remove_user(self, user):
        if self.has_user(user):
            self.users.remove(user)
            if user.department:
                department = Department.query.filter(Department.users.contains(user)).first()
                if department.has_user(user):
                    department.remove_user(user)

    def has_user(self, user):
        return user in self.users


class Department(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), index=True)
    users = db.relationship('User', backref='department', lazy='dynamic')
    requests = db.relationship('Request', backref='department', lazy='dynamic')
    shop_id = db.Column(db.Integer, db.ForeignKey('shop.id'))

    def __init__(self, **kwargs):
        super(Department, self).__init__(**kwargs)
        role = Role.query.filter_by(name='Administrator').first()
        admin = User.query.filter_by(role=role).first()
        self.users.append(admin)

    def add_user(self, user):
        if not self.has_user(user) and user.shop == self.shop:
            self.users.append(user)

    def remove_user(self, user):
        if self.has_user(user) and user.shop == self.shop:
            self.users.remove(user)

    def has_user(self, user):
        return user in self.users


class Request(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    department_id = db.Column(db.Integer, db.ForeignKey('department.id'))
    shop_id = db.Column(db.Integer, db.ForeignKey('shop.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    description = db.Column(db.Text)
    message = db.Column(db.Text)
    approved = db.Column(db.Boolean, index=True, default=False)

    def __init__(self, **kwargs):
        super(Request, self).__init__(**kwargs)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))
