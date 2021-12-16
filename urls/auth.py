from __init__ import *
from flask import Blueprint
from flask.helpers import make_response
from markupsafe import Markup
from models.forms import LoginForm
from models.models import User

from views.module_here import module_common
from models.forms import LoginForm, RegistrationForm

auth = Blueprint('auth', __name__)
common = module_common()

@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    error = ''
    if session.get('login'):
        return redirect(url_for('index'))
    if request.method == 'GET':
        return render_template('UserSystem.html', server_ip=ip, form=LoginForm())
    else:
        next = common.module_login(form)
        print('next: ', next)
        if next or next == []:
            session['login'] = True
            return redirect(url_for('index'))
        else:
            error = "Invalid username or password. Please try again!"
            return render_template('UserSystem.html', server_ip=ip, form=LoginForm(), error=error)


@auth.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    session.clear()
    return redirect(url_for('auth.login'))

