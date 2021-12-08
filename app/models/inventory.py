from flask import current_app as app
import datetime;

#
#
# This file contains all of the SQL queries related to inventory as well as product details.
#
# They are split into three sections:
# 1) Inventory -- listing new products, editing quantity, edit product details, start selling an existing item
# 2) Order Fulfillment -- viewing order history, searching by products or order number, updating shipped/delivered status
# 3) Seller Analytics -- queries for  seller statistics (# orders, # products sold, # items listed, revenue, popular items, loyal buyers)
#
#

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

# Section 1) Inventory-related queries

        @staticmethod
        def add_prod(name, description, price, quantity, seller, url, tag):
            rows = app.db.execute('''
    INSERT INTO Product(name, description, price, available, lister)
    VALUES(:name, :description, :price, true, :id)
    RETURNING id
    ''',
                                  id = seller,
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
            rows = app.db.execute('''
    INSERT INTO ProductTag(tag, product)
    VALUES(:tag, :product)
    RETURNING product
    ''',
                                tag = tag,
                                product = id)
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
            SELECT seller, quantity, firstname, lastname
            FROM ProductInventory, Account
            WHERE product = :pid AND Account.id = ProductInventory.seller''',
            pid=pid)
            return rows

        
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

        @staticmethod
        def get_listed(id):
            rows = app.db.execute('''
            SELECT Product.id, name, description, url
            FROM Product, ProductImage
            WHERE Product.lister = :id
            AND ProductImage.product = Product.id
            ''',
                                  id = id) 
            print(rows)      
            return rows if rows is not None else None
        
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
        def edit_inventory(prod_id, name, description, price, url, tag):
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
                print('updated product in edit_inventory!!')
                rows = app.db.execute('''
                            UPDATE ProductImage
                            SET url = :url
                            WHERE product = :prod_id
                            RETURNING *
                            ''',
                                    prod_id = prod_id, 
                                    url = url)
                rows = app.db.execute('''
                            UPDATE ProductTag(tag, product)
                            SET tag = :tag
                            WHERE product = :prod_id
                            RETURNING product
                            ''',
                                    tag = tag,
                                    prod_id = prod_id)
                print(rows)
            except Exception as err:
                print(err)
            return True

# Section 2) Order fulfillment history-related queries

        @staticmethod
        def get_order_history(id):
            rows = app.db.execute('''
    SELECT AccountOrderProduct.product, quantity, AccountOrderProduct.price, status, 
    placed_at, shipped_at, delivered_at, url, AccountOrder.id, name, AccountOrder.account as customer,
    (quantity * AccountOrderProduct.price) AS cost, Account.address, Account.firstname, Account.lastname 
    FROM AccountOrderProduct, AccountOrder, ProductImage, Product, Account
    WHERE seller = :id
    AND AccountOrder.id = account_order
    AND ProductImage.product = AccountOrderProduct.product
    AND Product.id = AccountOrderProduct.product
    AND AccountOrder.account = Account.id
    ORDER BY placed_at DESC
    ''',
                                  id = id) 
            print(rows)      
            return rows if rows is not None else None

        @staticmethod
        def get_order_history_search(id, prod_name, order_num):
            
            sel = "SELECT AccountOrderProduct.product, quantity, AccountOrderProduct.price, status, placed_at, shipped_at, delivered_at, url, AccountOrder.id, name, AccountOrder.account as customer, (quantity * AccountOrderProduct.price) AS cost, Account.address, Account.firstname, Account.lastname "
            frm = "FROM AccountOrderProduct, AccountOrder, ProductImage, Product, Account"
            where = "WHERE seller = :id AND AccountOrder.id = account_order AND ProductImage.product = AccountOrderProduct.product AND Product.id = AccountOrderProduct.product AND AccountOrder.account = Account.id"
            sby = "ORDER BY placed_at DESC"

            if prod_name:
                where += " AND name = :prod_name"
            if order_num:
                where += " AND AccountOrder.id = :order_num"
            qry = sel + "\n" + frm + "\n" + where + "\n" + sby
            rows = app.db.execute(qry,
                                  id = id,
                                  prod_name = prod_name,
                                  order_num = order_num) 
            print(rows)      
            return rows if rows is not None else None

        @staticmethod
        def update_shipped(account_order, product, seller):
            try:
                rows = app.db.execute('''
                    UPDATE AccountOrderProduct
                    SET shipped_at = :time, status = :status
                    WHERE account_order = :account_order 
                    AND product = :product
                    AND seller = :seller
                    RETURNING *
                ''',
                    time = datetime.datetime.now(),
                    account_order = account_order,
                    product = product,
                    seller = seller,
                    status = 'Shipped'
                    )
                print(rows)
                print("Shipped!")
            except Exception as err:
                print(err)
            return Inventory.get(seller)
    
        @staticmethod
        def update_delivered(account_order, product, seller):
            try:
                rows = app.db.execute('''
                    UPDATE AccountOrderProduct
                    SET delivered_at = :time, status = :status
                    WHERE account_order = :account_order 
                    AND product = :product
                    AND seller = :seller
                    RETURNING *
                ''',
                    time = datetime.datetime.now(),
                    account_order = account_order,
                    product = product,
                    seller = seller,
                    status = 'Delivered'
                    )

                print(rows)
                print("Delivered!")
            except Exception as err:
                print(err)
            return Inventory.get(seller)
            
# Section 3) Seller analytics-related queries

        @staticmethod
        def get_seller_analytics(id):
            rows = app.db.execute( '''
                SELECT count(account_order) as count_order, sum(quantity) as num_items, CAST(SUM(quantity*price) as DECIMAL(14,2)) as total
                FROM AccountOrderProduct
                WHERE seller = :id
            ''',
                id = id)
            print(rows)      
            return rows if rows is not None else None
        
        @staticmethod
        def popular_item(id):
            rows = app.db.execute( '''
                SELECT AccountOrderProduct.product, COUNT(AccountOrderProduct.product) AS value_occurrence, url, name 
                FROM AccountOrderProduct, ProductImage, Product
                WHERE seller = :id
                AND AccountOrderProduct.product = ProductImage.product
                AND AccountOrderProduct.product = Product.id
                GROUP BY AccountOrderProduct.product, url, name
                ORDER BY value_occurrence DESC
                LIMIT 3;
            ''',
                id = id)
            print(rows)      
            return rows if rows is not None else None

        @staticmethod
        def loyal_buyers(id):
            rows = app.db.execute( '''
                SELECT COUNT(AccountOrder.account) AS value_occurrence, Account.firstname, Account.lastname
                FROM (AccountOrderProduct JOIN AccountOrder ON AccountOrderProduct.account_order = AccountOrder.id), Account
                WHERE seller = :id
                AND AccountOrder.account = Account.id
                GROUP BY AccountOrder.account, Account.firstname, Account.lastname
                ORDER BY value_occurrence DESC
                LIMIT 3;
            ''',
                id = id)
            print(rows)      
            return rows if rows is not None else None
        
        @staticmethod
        def remove(uid, pid):
            rows = app.db.execute( '''
                DELETE FROM ProductInventory
                WHERE seller = :uid AND product = :pid
                RETURNING *
            ''',
                uid = uid, pid=pid)
            print(rows)      
            return rows if rows is not None else None

# Method below not used in inventory pages

        @staticmethod
        def get_tags():
            rows = app.db.execute('''
                SELECT id, name
                FROM Tag
        ''')
            print(rows)
            return rows if rows is not None else None
        
        
