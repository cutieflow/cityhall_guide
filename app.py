from flask import Flask, render_template, g, request, redirect, url_for
from flask_login import LoginManager, login_user, logout_user, login_required, UserMixin, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # セキュアなキーを設定

DATABASE = 'cityhall.db'

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

class User(UserMixin):
    def __init__(self, id):
        self.id = id

@login_manager.user_loader
def load_user(user_id):
    db = get_db()
    user = db.execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()
    if user:
        return User(user['id'])
    return None

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route('/')
def index():
    db = get_db()
    floors = db.execute('SELECT * FROM floors ORDER BY id DESC').fetchall()
    return render_template('index.html', floors=floors)

@app.route('/floor/<int:floor_id>')
def floor_detail(floor_id):
    db = get_db()
    floor = db.execute('SELECT * FROM floors WHERE id = ?', (floor_id,)).fetchone()
    return render_template('floor_detail.html', floor=floor)

@app.route('/admin', methods=['GET', 'POST'])
@login_required
def admin():
    db = get_db()
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        db.execute('INSERT INTO floors (name, description) VALUES (?, ?)', (name, description))
        db.commit()
        return redirect(url_for('admin'))
    floors = db.execute('SELECT * FROM floors ORDER BY id DESC').fetchall()
    return render_template('admin.html', floors=floors)

@app.route('/admin/edit/<int:floor_id>', methods=['GET', 'POST'])
@login_required
def edit_floor(floor_id):
    db = get_db()
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        db.execute('UPDATE floors SET name = ?, description = ? WHERE id = ?', (name, description, floor_id))
        db.commit()
        return redirect(url_for('admin'))
    floor = db.execute('SELECT * FROM floors WHERE id = ?', (floor_id,)).fetchone()
    return render_template('edit_floor.html', floor=floor)

@app.route('/admin/delete/<int:floor_id>', methods=['POST'])
@login_required
def delete_floor(floor_id):
    db = get_db()
    db.execute('DELETE FROM floors WHERE id = ?', (floor_id,))
    db.commit()
    return redirect(url_for('admin'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        db = get_db()
        username = request.form['username']
        password = request.form['password']
        user = db.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
        if user and check_password_hash(user['password'], password):
            login_user(User(user['id']))
            return redirect(url_for('admin'))
        else:
            return render_template('login.html', error="ログインに失敗しました")
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
