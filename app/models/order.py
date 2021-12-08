import json
from flask import current_app as app

class OrderProduct:
    def __init__(self, account_id, order_id, product, quantity, price, status, shipped_at, delivered_at, name, totalPrice):
        self.account_id = account_id
        self.order_id = order_id
        self.product = product
        self.quantity = quantity
        self.price = price
        self.status = status
        self.shipped_at = shipped_at
        self.delivered_at = delivered_at
        self.name = name
        self.totalPrice = totalPrice


    def toJSON(self):
        return json.dumps({
            'order_id': self.order_id,
            'product_id': self.product_id,
            'quantity': self.quantity,
            'price': self.price,
            'status': self.status,
            'shipped_at': self.shipped_at,
            'delivered_at': self.delivered_at,
            'name': self.name,
            #'url': self.url
        }, default=lambda o: str(o))
        # return json.dumps('{{order_id: {}, product_id: {}, quantity: {}, price: {}, status: {}, shipped_at: {}, delivered_at: {}, name: {}, url: {}}}'.format(self.order_id, self.product_id, self.quantity, self.price, self.status, self.shipped_at, self.delivered_at, self.name, self.url))

    @staticmethod
    def get_all(order_id):
        rows = app.db.execute('''
SELECT OP.account_order, OP.quantity, OP.price, OP.status, OP.shipped_at, OP.delivered_at, P.name, PI.url, CAST(OP.price*OP.quantity AS DECIMAL(10,2)) AS "totalPrice", P.id
FROM AccountOrderProduct AS OP, ProductImage AS PI, Product AS P
WHERE OP.account_order = :order_id AND OP.product = PI.product AND P.id = OP.product
''',
                              order_id=order_id)
        return rows if rows is not None else None

    @staticmethod
    def order_cost(order_id):
        cost = app.db.execute('''
SELECT SUM(CAST(price*quantity AS DECIMAL(10,2)))
FROM AccountOrderProduct
WHERE account_order = :order_id
''',
                              order_id=order_id)
        return cost[0][0] if cost else 0.0

class Order:
    def __init__(self, id, account_id, placed_at, cost, products):
        self.id = id
        self.account_id = account_id
        self.placed_at = placed_at
        self.cost = cost
        self.products = products
    
    def toJSON(self):
        products_json = [OrderProduct.toJSON(prod) for prod in self.products]

        return json.dumps({
            'id': str(self.id),
            'account_id': str(self.account_id),
            'placed_at': self.placed_at,
            'cost': self.cost,
            'products': products_json
        }, default=lambda o: str(o))
        # return json.dumps('{{id: {}, account_id: {}, placed_at: {}, cost: {}, products: {} }}'.format(self.id, self.account_id, self.placed_at, self.cost, products_json))

    @staticmethod
    def get(id):
        rows = app.db.execute('''
SELECT id, account, placed_at
FROM AccountOrder
WHERE id = :id
''',
                              id=id)
        return Order(*(rows[0]), OrderProduct.order_cost(id), OrderProduct.get_all(id)) if rows is not None else None


    @staticmethod
    def get_all(account_id):
        rows = app.db.execute('''
SELECT id, account, placed_at
FROM AccountOrder
WHERE account = :account_id
''',
                              account_id=account_id)
        return [Order(*row, OrderProduct.order_cost(row[0]), OrderProduct.get_all(row[0])) for row in rows]

    @staticmethod
    def get_paginated(account_id, limit=10, offset=0):
        rows = app.db.execute('''
SELECT id, account, placed_at
FROM AccountOrder
WHERE account = :account_id
ORDER BY placed_at DESC
LIMIT :limit
OFFSET :offset
''',
                              account_id=account_id, limit=limit, offset=offset)
        return [Order(*row, OrderProduct.order_cost(row[0]), OrderProduct.get_all(row[0])) for row in rows]