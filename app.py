from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, current_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash
from models import User, Transaction, db
from flask_smorest import Api
from db import db
import models
from resources import blp as transactionBlueprint
import yaml

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///balanse.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'paraplan'

app.config["API_TITLE"] = "Transaction API"
app.config["API_VERSION"] = "v0.0.1"
app.config["OPENAPI_VERSION"] = "3.1.0"
app.config["OPENAPI_URL_PREFIX"] = "/"
app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
# app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database-file.db"

db.init_app(app)
api = Api(app)
api.register_blueprint(transactionBlueprint)

# Add server information to the OpenAPI spec
api.spec.options["servers"] = [
    {
        "url": "http://127.0.0.1:8000",
        "description": "Local development server"
    }
]


# Serve OpenAPI spec document endpoint for download
@app.route("/openapi.yaml")
def openapi_yaml():
    spec = api.spec.to_dict()
    return app.response_class(
        yaml.dump(spec, default_flow_style=False),
        mimetype="application/x-yaml"
    )


@app.route('/')
def main():
    main_list = User.query.all()
    return render_template('index.html', main=main_list, name='main')


@app.route('/balanse')
def users():
    user_list = User.query.all()
    return render_template('balanse.html', users=user_list, name='users')


@app.route('/transaction')
def transactions():
    transaction_list = Transaction.query.all()
    return render_template('transaction.html', transactions=transaction_list)


# if __name__ == '__main__':
#     app.run(debug=True)


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('profile'))
    else:
        return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('profile'))
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('profile'))
        else:
            flash('Неверно введены данные')
    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('profile'))
    if request.method == 'POST':
        name = request.form['name']
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        balance = request.form['balance']
        commission_rate = request.form['commission_rate']
        URL_webhook = request.form['URL_webhook']
        user = User.query.filter_by(username=username).first()
        # email = User.query.filter_by(email=email).first()
        if user:
            flash('Имя пользователя уже занято')
        # elif email:
        #     flash('email уже занят')
        else:
            hashed_password = generate_password_hash(password)
            new_user = User(name=name, username=username, password=hashed_password, email=email, balance=balance,
                            commission_rate=commission_rate, URL_webhook=URL_webhook)
            db.session.add(new_user)
            db.session.commit()
            flash('Аккаунт успешно создан')
            return redirect(url_for('login'))
    return render_template('register.html')


@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_user(id):
    user = User.query.get_or_404(id)
    if request.method == 'POST':
        user.name = request.form['name']
        user.username = request.form['username']
        user.password = generate_password_hash(request.form['password'])
        user.email = request.form['email']
        user.balance = request.form['balance']
        user.commission_rate = request.form['commission_rate']
        user.URL_webhook = request.form['URL_webhook']
        db.session.commit()

        return redirect(url_for('profile'))
    return render_template('edit.html', user=user)


@app.route('/delete/<int:id>', methods=['POST'])
def delete_user(id):
    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('profile'))


@app.route('/profile')
def profile():
    if current_user.is_authenticated:
        return render_template('profile.html', user=current_user)
    else:
        return redirect(url_for('login'))


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
