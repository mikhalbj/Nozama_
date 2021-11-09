from flask import current_app as app

class OrderProduct:
    def __init__(self, order_id, product_id, quantity, price, status, shipped_at, delivered_at):
        self.order_id = order_id
        self.product_id = product_id
        self.quantity = quantity
        self.price = price
        self.status = status
        self.shipped_at = shipped_at
        self.delivered_at = delivered_at

    @staticmethod
    def get_all(order_id):
        rows = app.db.execute('''
SELECT *
FROM AccountOrderProduct
WHERE account_order = :order_id
''',
                              order_id=order_id)
        return [OrderProduct(*row) for row in rows]

    @staticmethod
    def order_cost(order_id):
        cost = app.db.execute('''
SELECT SUM(price)
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
    def get_all(account_id, limit=20):
        rows = app.db.execute('''
SELECT id, account, placed_at
FROM AccountOrder
WHERE account = :account_id
''',
                              account_id=account_id)
        return [Order(*row, OrderProduct.order_cost(row[0]), OrderProduct.get_all(row[0])) for row in rows]