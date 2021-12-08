from logging import info
from flask import render_template, redirect, url_for, flash, request
from werkzeug.urls import url_parse

from flask import current_app as app
from flask_login import current_user

import json

from .models.user import User
from .models.order import Order
from .models.account import Account


from flask import Blueprint
bp = Blueprint('api', __name__)

'''
Return the number of account orders placed in every month
'''
@bp.route('/api/purchases/dates', methods=['GET'])
def purchase_dates():
    if not current_user.is_authenticated:
        return json.dumps('[]')
    
    class Res:
        def __init__(self, month, count):
            self.month = month
            self.count = count

        def serialize(self):
            return {
                'month': str(self.month),
                'count': str(self.count)
            }

    rows = app.db.execute('''
            SELECT date_trunc('month', ao.placed_at) as month, COUNT(op.product)
            FROM AccountOrder as ao, AccountOrderProduct as op
            WHERE account = :account_id AND ao.id = op.account_order
            GROUP BY month
            ''',
            account_id=current_user.id)

    results = [Res(*row).serialize() for row in rows]

    
    return json.dumps(results)

'''
Return the amount spent in every month
'''
@bp.route('/api/purchases/spending', methods=['GET'])
def purchase_spending():
    if not current_user.is_authenticated:
        return json.dumps('[]')
    
    class Res:
        def __init__(self, month, spending):
            self.month = month
            self.spending = spending

        def serialize(self):
            return {
                'month': str(self.month),
                'spending': str(self.spending)
            }

    rows = app.db.execute('''
            SELECT date_trunc('month', ao.placed_at) as month, SUM(op.quantity * op.price)
            FROM AccountOrder as ao, AccountOrderProduct as op
            WHERE account = :account_id AND ao.id = op.account_order
            GROUP BY month
            ''',
            account_id=current_user.id)

    results = [Res(*row).serialize() for row in rows]

    
    return json.dumps(results)

'''
Return the number of purchases and the total spent per category each month
'''
@bp.route('/api/purchases/categories', methods=['GET'])
def purchase_categories():
    if not current_user.is_authenticated:
        return json.dumps('[]')
    
    class Res:
        def __init__(self, category, count, amount):
            self.category = category
            self.count = count
            self.amount = amount

        def serialize(self):
            return {
                'category': str(self.category),
                'count': str(self.count),
                'amount': str(self.amount)
            }

    rows = app.db.execute('''
            SELECT t.name, COUNT(op.product), SUM(op.price * quantity)
            FROM AccountOrder as ao, AccountOrderProduct as op, ProductTag as pt, Tag as t
            WHERE account = :account_id AND ao.id = op.account_order AND pt.tag = t.id AND pt.product = op.product
            GROUP BY t.name
            ''',
            account_id=current_user.id)

    results = [Res(*row).serialize() for row in rows]

    
    return json.dumps(results)

@bp.route('/api/seller/sales', methods=['GET'])
def seller_sales():
    if not current_user.is_authenticated:
        return json.dumps('[]')

    return 'Not implemented'

    
