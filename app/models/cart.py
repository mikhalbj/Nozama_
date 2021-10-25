class Cart:
    def __init__(self, account_id, product_id, quantity):
        self.account_id = account_id
        self.product_id = product_id
        self.quantity = quantity
    
    @staticmethod
    def get_all(account_id):
        rows = app.db.execute('''
SELECT *
FROM CartProduct
WHERE account_id = :account_id
''',
                              account_id=account_id)
        return [CartProduct(*row) for row in rows]

    @staticmethod
    def cart_total(account_id):
        cost = app.db.execute('''
SELECT SUM(price)
FROM CartProduct, Product
WHERE CartProduct.product_id = Product.id AND account_id = :account_id
''',
                              order_id=order_id)
        return cost[0][0] if cost else 0.0
   