from flask import flash
from flask import redirect
from flask import render_template
from flask import url_for
from flask_login import current_user
from flask_login import login_required

from app import db
from app.models import Department
from app.models import Permission
from app.models import Request
from app.models import Shop
from app.unfollow import bp
from app.unfollow.forms import ChoiceForm
from app.unfollow.forms import CreateShopForm
from app.unfollow.forms import EditForm


@bp.route('/edit', methods=['GET', 'POST'])
@login_required
def first_edit_profile():
    if current_user.can(Permission.WRITE):
        flash("Вы уже состоите в магазине")
        return redirect(url_for('main.index'))
    form = EditForm()
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.surname = form.surname.data
        current_user.about_me = form.about_me.data
        current_user.position = form.position.data
        db.session.add(current_user)
        db.session.commit()
        return redirect(url_for('unfollow.first_choice'))
    form.name.data = current_user.name
    form.surname.data = current_user.surname
    form.about_me.data = current_user.about_me
    form.position.data = current_user.position
    return render_template('unfollow/edit.html', form=form, name=current_user.username)


@bp.route('/choice', methods=['GET', 'POST'])
@login_required
def first_choice():
    if current_user.can(Permission.WRITE):
        flash("Вы уже состоите в магазине")
        return redirect(url_for('main.index'))
    if not current_user.name or not current_user.surname or not current_user.position:
        return redirect(url_for('unfollow.first_edit_profile'))
    form = ChoiceForm()
    if form.validate_on_submit():
        shop = Shop.query.filter(Shop.name == form.shop.data or Shop.shop_code == form.shop.data).first()
        department = Department.query.filter_by(name=form.department.data).first()
        r = Request(user=current_user, shop=shop, department=department)
        db.session.add(r)
        db.session.commit()
        flash("Ваша заявка сформирована")
        return redirect(url_for('unfollow.wait', shop=form.shop.data))  # TODO create request
    return render_template('unfollow/choice.html', form=form, name=current_user.name)


@bp.route('/wait/<shop>/<department>')
@login_required
def wait(shop, department):
    if current_user.can(Permission.WRITE):
        flash("Вы уже состоите в магазине")
        return redirect(url_for('main.index'))
    if not current_user.name or not current_user.surname or not current_user.position:
        flash("Не хватает ваших данных")
        return redirect(url_for('unfollow.first_edit_profile'))
    shop_instance = Shop.query.filter(Shop.name == shop or Shop.shop_code == shop).first()
    department_instance = Department.query.filter_by(name=department).first()
    request = Request.query.filter_by(user=current_user,
                                      shop=shop_instance,
                                      department=department_instance).first()
    if not request:
        flash("Заявка не сформирована")
        return redirect(url_for('unfollow.first_choice'))
    return render_template('unfollow/wait.html')


@bp.route('/create', methods=['POST', 'GET'])
@login_required
def create_shop():
    if current_user.can(Permission.WRITE):
        flash("Вы уже состоите в магазине")
        return redirect(url_for('main.index'))
    if not current_user.name or not current_user.surname or not current_user.position:
        flash("Не хватает ваших данных")
        return redirect(url_for('unfollow.first_edit_profile'))
    form = CreateShopForm()
    if form.validate_on_submit():
        shop_name = form.name.data
        shop_code = form.shop_code.data
        Shop.create_shop(current_user, shop_name, shop_code)
        db.session.commit()
        flash("Магазин создан")
        return redirect(url_for('main.index'))  # TODO на страницу магазина
    return render_template('unfollow/create.html', form=form)