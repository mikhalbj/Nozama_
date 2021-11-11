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

    @staticmethod
    def get(id):
        rows = app.db.execute('''
        SELECT id, title, author, description, written_at, edited_at, rating
        FROM Review, ProductReview
        WHERE ProductReview.product = :id AND ProductReview.review = Review.id
        ''', id=id)
        return rows if rows is not None else None