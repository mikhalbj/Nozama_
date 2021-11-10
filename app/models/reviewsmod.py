from flask import current_app as app


class Review:
    def __init__(self, id, title, description=None, rating=None, time, edited=False):
        self.id = id
        self.name = name
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
SELECT id, title, author, description
FROM Review
WHERE id = :id
''',
                              id=id)
        return rows[0] if rows is not None else None