from flask import current_app as app


class Review:
    def __init__(self, id, title, author, time, description=None, rating=None, edited=False):
        self.id = id
        self.name = name
        self.author = author
        self.price = price
        self.time = time
        if description:
            self.description = description
        if rating:
            self.rating = rating
        if edited:
            self.edited = edited

#get all reviews for given product
    @staticmethod
    def getProdRev(id):
        rows = app.db.execute('''
        SELECT id, title, author, description, written_at, edited_at, rating
        FROM Review, ProductReview
        WHERE ProductReview.product = :id AND ProductReview.review = Review.id
        ORDER BY rating
        ''', id=id)
        return rows if rows is not None else None

#get all reviews for given seller
    @staticmethod
    def getSellRev(id):
        rows = app.db.execute('''
        SELECT id, title, author, description, written_at, edited_at, rating
        FROM Review, SellerReview
        WHERE SellerReview.seller = :id AND SellerReview.review = Review.id
        ORDER BY rating
        ''', id=id)
        return rows if rows is not None else None

#add a PRODUCT review
    @staticmethod
    def add_prodrev(title, author, description, written_at, rating): #I dont think that I need author here but will need to autoppopulate some how on entry
        rows = app.db.execute('''
    INSERT INTO Review(title, author, description, written_at, edited_at, rating)
    VALUES(:title, :author, :description, :written_at, none, :rating)
    RETURNING id
    ''',
            title=title,
            author=author,
            description=description,
            written_at=written_at,
            rating=rating)
        id = rows[0][0]
        rows = app.db.execute('''
    INSERT INTO ProductReview(review, product)
    VALUES(:review, :product)
    RETURNING review
    ''',
                                  review=review, 
                                  product=product)

        return




#edit an existing review
    @staticmethod
    def edit_review(review_id, title, description, edited_at):
        try:
                rows = app.db.execute('''
        UPDATE Review
        SET title= :title, description= :description, edited_at=:edited_at
        WHERE id = :review_id
        RETURNING *
        ''',
                                    review_id = review_id,
                                    title=title,
                                    description=description,
                                    edited_at=edited_at)
                print('updated')
        except Exception as err:
            print(err)
        return Review.get(author)


#get all reviews written by one user
    @staticmethod
    def review_history(id):
            rows = app.db.execute('''
    SELECT ProductReview.product, author, description, written_at, edited_at, rating
    FROM ProductReview, Review
    WHERE author = :id
    AND ProductReview.review = Review.id
    ORDER BY rating
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