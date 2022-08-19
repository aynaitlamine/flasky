from flask import render_template
from flask_login import login_required
from . import main
from ..decorators import admin_required, permission_required
from ..models import Permission


@main.route("/", methods=["GET"])
def index():
    return render_template('pages/index.html')


    
@main.route('/admin')
@login_required
@admin_required
def for_admins_only():
    return "For administrators!"

@main.route('/moderate')
@login_required
@permission_required(Permission.MODERATE)
def for_moderators_only():
    return "For comment moderators!"
