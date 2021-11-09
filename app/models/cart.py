from flask import current_app as app

class Cart:
    def __init__(self, account_id, total):
        self.account_id = account_id
        self.total = total
    
    @staticmethod
    def get_all(account_id):
        rows = app.db.execute('''
            SELECT Product.id, Product.name, CartProduct.quantity, Product.Price*CartProduct.quantity AS "totalPrice"
            FROM CartProduct, Product
            WHERE cartProduct.account = :account_id AND Product.id = CartProduct.produc
            ''',
            account_id=account_id)
        return [CartProduct(*row) for row in rows]

    @staticmethod
    def cart_total(account_id):
        cost = app.db.execute('''
            SELECT SUM(Product.Price*CartProduct.quantity)
            FROM CartProduct, Product
            WHERE CartProduct.product = Product.id AND cartProduct.account = :account_id
            ''',
            account_id=account_id)
        return cost[0][0] if cost else 0.0
   



    @staticmethod
    def get(account_id):
        total = Cart.cart_total(account_id)
        return Cart(account_id, total)


