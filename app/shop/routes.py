from flask_login import current_user
from flask_login import login_required

from app.decorators import permission_required
from app.decorators import shop_required
from app.models import Permission
from app.shop import bp


@bp.route('/<shop_code>')
@login_required
@permission_required(Permission.WRITE)
@shop_required(current_user.shop)
def shop(shop_code):
    return ''


@bp.route('/<shop_code>/requests')
@login_required
@permission_required(Permission.MODERATE)
@shop_required(current_user.shop)
def requests(shop_code):
    return ''


@bp.route('/departments')
@login_required
@permission_required(Permission.WRITE)
@shop_required(current_user.shop)
def departments(shop_code):
    return ''


@bp.route('/<shop_code>/users')
@login_required
@permission_required(Permission.WRITE)
@shop_required(current_user.shop)
def users(shop_code):
    return ''


@bp.route('/<shop_code>/timetable')
@login_required
@permission_required(Permission.WRITE)
@shop_required(current_user.shop)
def timetable(shop_code):
    return ''


@bp.route('/<shop_code>/furniture')
@login_required
@permission_required(Permission.WRITE)
@shop_required(current_user.shop)
def furniture(shop_code):
    return ''