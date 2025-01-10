from flask import Flask
from models import User, Transaction, db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///balanse.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()

        # Создаем Пользователей
        user1 = User(name='ООО.Полет', username= 'admin', password='7777777', email='andreilkt@yandex.ru', balance='1000', commission_rate='10', URL_webhook='Сообщение с сервера1')
        user2 = User(name='ООО.Airplane', username= 'admin1', password='7777777', email='andreylkt@yandex.ru', balance='500', commission_rate='10', URL_webhook='Сообщение с сервера2')
        user3 = User(name='ООО.Кайт', username= 'admin2', password='7777777', email='andreilkt@mail.ru', balance='700', commission_rate='10', URL_webhook='Сообщение с сервера3')
        user4 = User(name='Fly_paraplan', username= 'admin3', password='7777777', email='andreylkt@mail.ru', balance='800', commission_rate='10', URL_webhook='Сообщение с сервера4')
        db.session.add_all([user1, user2, user3, user4])
        db.session.commit()

        # создаем транзакции
        transaction1 = Transaction(sum='10000', commission='100', status='Ожидание', user=user1)
        transaction2 = Transaction(sum='100000', commission='100', status='Подтверждена', user=user2)
        transaction3 = Transaction(sum='1000000', commission='100', status='Истекла', user=user3)
        transaction4 = Transaction(sum='100000', commission='100', status='отменена', user=user4)
        db.session.add_all([transaction1, transaction2, transaction3, transaction4])
        db.session.commit()
