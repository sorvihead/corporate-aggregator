from functools import wraps

from flask import abort
from flask import flash
from flask import redirect
from flask import url_for
from flask_login import current_user

from app.models import Permission
from app.models import Shop


def permission_required(permission):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if current_user.role.name == 'Unfollow':
                return redirect(url_for('unfollow.first_edit_profile'))
            if not current_user.can(permission):
                abort(403)
            return f(*args, **kwargs)

        return decorated_function

    return decorator


def admin_required(f):
    return permission_required(Permission.ADMIN)(f)


def shop_required():
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            requested_shop = args[0] if args else kwargs.get('shop_code')
            shop_instance = Shop.query.filter_by(shop_code=requested_shop).first()
            current_shop = current_user.shop if current_user else None
            if not current_shop:
                flash('Вы не состоите в магазине')
                return redirect(url_for('main.index'))
            if not shop_instance:
                flash('Такого магазина не существует')
                return redirect(url_for('main.index'))
            if current_shop is not shop_instance:
                flash('Вы не состоите в данном магазине')
                return redirect(url_for('main.index'))
            return f(*args, **kwargs)
        return decorated_function
    return decorator


# TODO сделать shop_required, для того чтобы юзер не мог смотреть в другие магазины.
#  (Видимо придется делать проверку в каждой вьюхе)
