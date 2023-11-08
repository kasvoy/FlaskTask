from flask import Blueprint, render_template, flash, redirect, url_for, request
from .forms import RegistrationForm, LoginForm
from .models import User, db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, current_user, logout_user, login_required


auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():

    form = RegistrationForm()
    
    if form.validate_on_submit():

        user = User(username=form.username.data, email=form.email.data,
                     password=generate_password_hash(form.password.data))

        db.session.add(user)
        db.session.commit()

        flash(f"Account created for {form.username.data}.", 'success')
        return redirect(url_for('tasks.tasks_page'))
    
    return render_template('auth/register.html', form=form)



@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email_attempting = form.email.data

        user = db.session.scalars(db.select(User).where(User.email == email_attempting)).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember_me.data)
  
            flash(f"{user.username} logged in!", 'success')
            if request.args.get('next'):
                return redirect(request.args.get('next'))
            else:
                return redirect(url_for('tasks.tasks_page'))
        else:
            flash(f"Wrong email or password", 'danger')
        
    return render_template('auth/login.html', form=form)


@auth_bp.route('/logout')
def logout():
    logout_user()
    flash('Sucessfully logged out', 'info')

    return redirect(url_for('tasks.tasks_page'))

@auth_bp.route('/account')
@login_required
def account():
    return render_template('auth/account.html')

@auth_bp.route('/users')
def users_query():
    users = db.session.execute(db.select(User))
    print(db.session.scalars(db.Select(User).where(User.id == int(6))).all())
    

    return render_template('auth/query.html', users=users)
    