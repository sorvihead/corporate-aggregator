from functools import wraps

from flask import abort
from flask import redirect
from flask import url_for
from flask_login import current_user

from app.models import Permission


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

# TODO сделать shop_required, для того чтобы юзер не мог смотреть в другие магазины
