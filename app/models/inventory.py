# Creating the inventory page based on a typed-in seller

from flask import current_app as app

class Inventory:
        def __init__(self, id, prod_id, name, available):
            self.id = id
            self.prod_id = prod_id
            self.name = name
            self.available = available

        @staticmethod
        def get(id):
            rows = app.db.execute('''
    SELECT Product.id, name, quantity, seller, description
    FROM Product, ProductInventory
    WHERE Product.id = ProductInventory.product
        AND ProductInventory.seller = :id
    ''',
                                  id = id) 
            print(rows)      
            return rows if rows is not None else None

        @staticmethod
        def add_prod(name, description, price, quantity, seller, url):
            rows = app.db.execute('''
    INSERT INTO Product(name, description, price, available)
    VALUES(:name, :description, :price, true)
    RETURNING id
    ''',
                                  name=name,
                                  description=description,
                                  price=price)
            id = rows[0][0]
            rows = app.db.execute('''
    INSERT INTO ProductInventory(product, seller, quantity)
    VALUES(:id, :seller, :quantity)
    RETURNING product
    ''',
                                  id = id, 
                                  seller = seller,
                                  quantity = quantity)
            print('It was added!')
            rows = app.db.execute('''
    INSERT INTO ProductImage(product, url)
    VALUES(:id, :url)
    RETURNING product
    ''',
                                  id = id, 
                                  url = url)
            return Inventory.get(seller)
        
        @staticmethod
        def sells(uid, pid):
            rows = app.db.execute('''
            SELECT seller
            FROM ProductInventory
            WHERE seller = :uid AND product = :pid''',
            uid=uid, pid=pid)
            return True if len(rows) != 0 else False
        
        @staticmethod
        def all_sellers(pid):
            rows = app.db.execute('''
            SELECT seller, quantity
            FROM ProductInventory
            WHERE product = :pid''',
            pid=pid)
            return rows
        
        @staticmethod
        def start_selling(uid, q, pid):
            rows = app.db.execute('''
            INSERT INTO ProductInventory(product, seller, quantity)
            VALUES (:pid, :uid, :q)
            RETURNING product''',
            uid=uid, pid=pid, q=q)
            print("USERS NOW SELLING THIS PRODUCT")

        @staticmethod
        def edit_quantity(prod_id, quantity, seller):
            try: 
                rows = app.db.execute('''
                UPDATE ProductInventory
                SET quantity = :quantity
                WHERE product = :prod_id AND seller = :seller
                RETURNING *
                ''',
                                        prod_id = prod_id,
                                        quantity = quantity,
                                        seller = seller
                )
                print(rows)
            except Exception as err:
                print(err)
            return Inventory.get(seller)

        @staticmethod
        def edit_inventory(prod_id, name, description, price, quantity, url, seller):
            try:
                rows = app.db.execute('''
        UPDATE Product
        SET name= :name, description= :description, price=:price
        WHERE id = :prod_id
        RETURNING *
        ''',
                                    prod_id = prod_id,
                                    name=name,
                                    description=description,
                                    price=price)
                print('updated!')
                rows = app.db.execute('''
        UPDATE ProductInventory
        SET quantity = :quantity
        WHERE product = :prod_id AND seller = :seller
        RETURNING *
        ''',
                                    prod_id = prod_id, 
                                    quantity = quantity,
                                    seller = seller)
                rows = app.db.execute('''
        UPDATE ProductImage
        SET url =:url
        WHERE product = :prod_id
        RETURNING *
        ''',
                                    prod_id = prod_id, 
                                    url = url)
                print(rows)
            except Exception as err:
                print(err)
            return Inventory.get(seller)

        @staticmethod
        def get_order_history(id):
            rows = app.db.execute('''
    SELECT AccountOrderProduct.product, quantity, price, status, placed_at, shipped_at, delivered_at, url
    FROM AccountOrderProduct, AccountOrder, ProductImage
    WHERE seller = '07aab60d-7991-4ec4-b1ca-3c8489e30e4d'
    AND AccountOrder.id = account_order
    AND ProductImage.product = AccountOrderProduct.product
    ORDER BY placed_at DESC
    ''',
                                  id = id) 
            print(rows)      
            return rows if rows is not None else None

        @staticmethod
        def is_lister(id):
            rows = app.db.execute('''
    SELECT id
    FROM Seller, Product
    WHERE Seller.id = :id AND Product.lister = :id
    ''',
                                  id=id) 
            print(rows)
            return True if len(rows) != 0 else False