import datetime;
from flask import current_app as app

class Cart:
    def __init__(self, account_id, total):
        self.account_id = account_id
        self.total = total
    
    @staticmethod
    def get_all(account_id):
        rows = app.db.execute('''
            SELECT Product.id, Product.name, CartProduct.quantity, CAST(Product.Price*CartProduct.quantity AS DECIMAL(10,2)) AS "totalPrice"
            FROM CartProduct, Product
            WHERE cartProduct.account = :account_id AND Product.id = CartProduct.product
            ''',
            account_id=account_id)     
        return rows if rows is not None else None


    @staticmethod
    def place_order(account_id, time):

        balance = Cart.get_balance(account_id)
        total = Cart.cart_total(account_id)

        rows = app.db.execute('''
        UPDATE Balance
        SET balance = balance - :total
        WHERE id = :account_id
        RETURNING *
        ''',
        total = total,
        account_id = account_id
        )

        rows = app.db.execute('''
        INSERT INTO AccountOrder(account, placed_at)
        VALUES(:account_id, :time)
        RETURNING id
        ''',
        account_id = account_id,
        time = time)
        id = rows[0][0]

        orderid = Cart.getoid(account_id, time)
        index = 0
        cart_prods = Cart.getcp(account_id)
        for x in cart_prods:
            product = cart_prods[index][0]
            price = cart_prods[index][1]
            quant = cart_prods[index][2]
            Cart.edit_inventory(account_id, product, quant, orderid, price, time)
            index += 1

        rows = app.db.execute('''
        DELETE FROM CartProduct WHERE account = :account_id RETURNING account
        ''',
        account_id = account_id
        )

        return rows if rows is not None else None
    
    @staticmethod
    def check_inventory(account_id, time):
        orderid = Cart.getoid(account_id, time)
        cart_prods = Cart.getcp(account_id)
        index = 0
        for x in cart_prods:
            product = cart_prods[index][0]
            total = Cart.inventory_total(product)
            quant = cart_prods[index][2]
            if quant > total:
                return False
        return True


    @staticmethod
    def edit_inventory(account_id, prodid, quant, orderid, price, time):
        sellers = Cart.getsellers(prodid)
        index = 0
        while quant > 0:
            amount = min(quant, sellers[index][1])
            s = sellers[index][0]
            q = sellers[index][1]
            cost = price*amount
            Cart.updateaop(orderid, prodid, s, amount, price)
            Cart.editseller(prodid, q, amount, s, cost)
            quant -= amount
            index += 1
        return True

    @staticmethod
    def add_cart(account_id, quantity, id):
        rows = app.db.execute('''
        INSERT INTO CartProduct(account, product, quantity)
        VALUES(:account_id, :prod_id, :quantity)
        RETURNING account
        ''',
            account_id = account_id,
            prod_id = id,
            quantity = quantity)
        return True
    
    @staticmethod
    def cart_total(account_id):
        rows = app.db.execute('''
            SELECT SUM(Product.Price*CartProduct.quantity)
            FROM CartProduct, Product
            WHERE CartProduct.product = Product.id AND cartProduct.account = :account_id
            ''',
            account_id=account_id)
        return rows[0][0] if rows else 0.0

    @staticmethod
    def inventory_total(product):
        rows = app.db.execute('''
            SELECT SUM(Quantity)
            FROM ProductInventory 
            WHERE product = :product
            ''',
            product=product)
        return rows[0][0] if rows else 0.0

    @staticmethod
    def getoid(account_id, time):
        rows = app.db.execute('''
           SELECT id FROM AccountOrder 
           WHERE account = :account_id AND placed_at = :time
            ''',
            account_id=account_id,
            time=time)
        return rows[0][0] if rows else 0.0

    @staticmethod
    def getcp(account_id):
        rows = app.db.execute('''
           SELECT product, price, quantity 
           FROM CartProduct, Product 
           WHERE CartProduct.product = Product.id AND CartProduct.account = :account_id
            ''',
            account_id=account_id)
        return rows if rows else 0.0

    @staticmethod
    def getsellers(prodid):
        rows = app.db.execute('''
           SELECT Seller, Quantity 
           FROM ProductInventory 
           WHERE product = :prodid
            ''',
            prodid=prodid)
        return rows if rows else 0.0

    @staticmethod
    def updateaop(orderid, prodid, seller, amount, price):
        status = 'Order Placed'
        rows = app.db.execute('''
           INSERT INTO AccountOrderProduct(account_order, product, seller, quantity, price, status, shipped_at, delivered_at)
           VALUES(:orderid, :prodid, :seller, :amount, :price, :status, NULL, NULL)
           RETURNING account_order
            ''',
            orderid=orderid,
            prodid=prodid,
            seller=seller,
            amount=amount,
            price=price,
            status=status)
        return True

    @staticmethod
    def saved(account_id):
        rows = app.db.execute('''
            SELECT Product.id, Product.name
            FROM SavedProduct, Product
            WHERE SavedProduct.account = :account_id AND Product.id = SavedProduct.product
            ''',
            account_id=account_id)     
        return rows if rows is not None else None
    
    @staticmethod
    def save(account_id, pid):
        rows = app.db.execute('''
            INSERT INTO SavedProduct(account, product)
            VALUES(:account_id, :prod_id)
            RETURNING account
            ''',
            account_id = account_id,
            prod_id = pid)
        return rows if rows is not None else None
    
    @staticmethod
    def can_save(account_id, pid):
        rows = app.db.execute('''
            SELECT product
            FROM SavedProduct
            WHERE account = :account_id AND product = :prod_id
            ''',
            account_id = account_id,
            prod_id = pid)
        return False if rows else True

    @staticmethod
    def removeProduct(account_id, product):
        rows = app.db.execute('''
            DELETE FROM CartProduct WHERE account = :account_id AND product = :product RETURNING account
            ''',
            account_id = account_id,
            product = product
            )
        return rows if rows is not None else None
    
    @staticmethod
    def removeSaved(account_id, product):
        rows = app.db.execute('''
            DELETE FROM SavedProduct WHERE account = :account_id AND product = :product RETURNING account
            ''',
            account_id = account_id,
            product = product
            )
        return rows if rows is not None else None

    @staticmethod
    def editseller(prod_id, quantity, amount, seller, cost): 
        rows = app.db.execute('''
            UPDATE ProductInventory
            SET quantity = :quantity - :amount
            WHERE product = :prod_id AND seller = :seller
            RETURNING *
            ''',
            prod_id = prod_id,
            quantity = quantity,
            amount = amount,
            seller = seller
            )
        
        rows = app.db.execute('''
            UPDATE Balance
            SET balance = balance + :cost
            WHERE id = :seller
            RETURNING *
            ''',
            cost = cost,
            seller = seller
            )

        return rows if rows is not None else None

    @staticmethod
    def get_balance(id):
        rows = app.db.execute('''
            SELECT balance
            FROM Balance
            WHERE id = :id
            ''',
            id = id)
        return rows[0][0] if rows else 0.0

    @staticmethod
    def editQuantity(account, product, quantity):
        rows = app.db.execute('''
            UPDATE CartProduct
            SET quantity = :quantity
            WHERE product = :product AND account = :account
            RETURNING *
            ''',
            quantity = quantity,
            product = product,
            account = account
            )
        return rows if rows is not None else None