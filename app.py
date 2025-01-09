from flask import Flask, render_template, url_for
from models import User, Transaction, db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///balanse.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# связываем приложение и экземпляр SQLAlchemy
db.init_app(app)


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
