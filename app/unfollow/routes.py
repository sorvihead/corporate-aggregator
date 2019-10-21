from flask import redirect
from flask import render_template
from flask import url_for
from flask_login import current_user
from flask_login import login_required

from app import db
from app.models import Permission
from app.unfollow import bp
from app.unfollow.forms import ChoiceForm
from app.unfollow.forms import EditForm


@bp.route('/edit', methods=['GET', 'POST'])
@login_required
def first_edit_profile():
    if current_user.can(Permission.WRITE):
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
    return render_template('unfollow/edit.html', form=form, name=current_user.username)


@bp.route('/choice', methods=['GET', 'POST'])
@login_required
def first_choice():
    if current_user.can(Permission.WRITE):
        return redirect(url_for('main.index'))
    if not current_user.name:
        return redirect(url_for('unfollow.first_edit_profile'))
    form = ChoiceForm()
    if form.validate_on_submit():
        return redirect(url_for('unfollow.wait'))  # TODO create request
    return render_template('unfollow/choice.html', form=form, name=current_user.name)


@bp.route('/wait')
@login_required
def wait():
    if current_user.can(Permission.WRITE):
        return redirect(url_for('main.index'))
    if not current_user.name:
        return redirect(url_for('unfollow.first_edit_profile'))
    # TODO if current_user.shop -> redirect
    return render_template('unfollow/wait.html')