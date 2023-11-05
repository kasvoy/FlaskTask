from flask import Blueprint, render_template, flash, redirect, url_for
from .forms import RegistrationForm, LoginForm

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():

    form = RegistrationForm()
    
    if form.validate_on_submit():
        flash(f"Account created for {form.username.data}.", 'success')
        return redirect(url_for('tasks.tasks_page'))
    
    return render_template('auth/register.html', form=form)

@auth_bp.route('/login')
def login():
    login_form = LoginForm()


    return render_template('auth/login.html')
