# Main application file: app.py
from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.exc import IntegrityError

app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    role = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password_hash = db.Column(db.String(128), nullable=False)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        role = request.form['role']
        password = request.form['password']
        password_hash = generate_password_hash(password)

        new_user = User(username=username, email=email, role=role, password_hash=password_hash)
        try:
            db.session.add(new_user)
            db.session.commit()
        except IntegrityError:
            flash('Error: Username or email already exists.', 'danger')
            return redirect(url_for('register'))
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password_hash, password):
            session['user_id'] = user.id
            session['username'] = user.username
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password.', 'danger')

    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        flash('Please log in to access the dashboard.', 'warning')
        return redirect(url_for('login'))

    users = User.query.all()
    return render_template('dashboard.html', users=users)

@app.route('/add', methods=['GET', 'POST'])
def add_user():
    if 'user_id' not in session:
        flash('Please log in to add users.', 'warning')
        return redirect(url_for('login'))

    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        role = request.form['role']
        password = request.form['password']
        password_hash = generate_password_hash(password)

        new_user = User(username=username, email=email, role=role, password_hash=password_hash)
        try:
            db.session.add(new_user)
            db.session.commit()
        except IntegrityError:
            flash('Error: Username or email already exists.', 'danger')
            return redirect(url_for('add_user'))
        flash('User added successfully!', 'success')
        return redirect(url_for('dashboard'))

    return render_template('add_user.html')

@app.route('/edit/<int:user_id>', methods=['GET', 'POST'])
def edit_user(user_id):
    if 'user_id' not in session:
        flash('Please log in to edit users.', 'warning')
        return redirect(url_for('login'))

    user = User.query.get_or_404(user_id)
    if request.method == 'POST':
        user.username = request.form['username']
        user.email = request.form['email']
        user.role = request.form['role']
        if request.form['password']:
            user.password_hash = generate_password_hash(request.form['password'])

        try:
            db.session.commit()
            flash('User updated successfully!', 'success')
            return redirect(url_for('dashboard'))
        except:
            flash('Error updating user.', 'danger')

    return render_template('edit_user.html', user=user)

@app.route('/delete/<int:user_id>', methods=['POST'])
def delete_user(user_id):
    if 'user_id' not in session:
        flash('Please log in to delete users.', 'warning')
        return redirect(url_for('login'))

    user = User.query.get_or_404(user_id)
    try:
        db.session.delete(user)
        db.session.commit()
        flash('User deleted successfully!', 'success')
    except:
        flash('Error deleting user.', 'danger')

    return redirect(url_for('dashboard'))

@app.route('/logout')
def logout():
    session.clear()
    flash('Logged out successfully.', 'info')
    return redirect(url_for('login'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)