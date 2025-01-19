from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import IntegrityError
from db import db
from models import Transaction
from schemas import TransactionSchema

blp = Blueprint("Transactions", "Transactions", url_prefix="/transactions", description="Operations on transactions")


@blp.route("/")
class TransactionList(MethodView):
    @blp.response(200, TransactionSchema(many=True))
    def get(self):
        """List all transaction"""
        return Transaction.query.all()

    @blp.arguments(TransactionSchema)
    @blp.response(201, TransactionSchema)
    def post(self, new_data):
        """Create a new transaction"""
        transaction = Transaction(**new_data)
        db.session.add(transaction)
        db.session.commit()
        return transaction


@blp.route("/<int:transaction_id>")
class TransactionDetail(MethodView):
    @blp.response(200, TransactionSchema)
    def get(self, transaction_id):
        """Get transaction by ID"""
        transaction = Transaction.query.get_or_404(transaction_id)
        return transaction

    @blp.arguments(TransactionSchema)
    @blp.response(200, TransactionSchema)
    def put(self, updated_data, transaction_id):
        """Update an existing transaction"""
        transaction = Transaction.query.get_or_404(transaction_id)
        transaction.sum = updated_data["sum"]
        transaction.commission = updated_data["commission"]
        transaction.status = updated_data.get("status")
        transaction.user_id = updated_data.get("user_id")
        db.session.commit()
        return transaction

    def delete(self, transaction_id):
        """Delete a transaction"""
        transaction = Transaction.query.get_or_404(transaction_id)
        db.session.delete(transaction)
        db.session.commit()
        return {"message": "Транзакция удалена"}, 204
