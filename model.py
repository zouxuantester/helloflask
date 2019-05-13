__author__ = 'zouxuan'
__date__ = '2019/5/10 11:15 AM'


from flask_app import db
from datetime import datetime


class Note(db.Model):
    __tablename__ = 'note'
    id = db.Column(db.INTEGER, primary_key=True)
    body = db.Column(db.TEXT)
    create_time = db.Column(db.DateTime, default=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

    def __repr__(self):
        return self.body
    pass


class Author(db.Model):
    id = db.Column(db.INTEGER, primary_key=True)
    name = db.Column(db.String(50))
    phone = db.Column(db.String(20), unique=True)
    articles = db.relationship('Article')


class Article(db.Model):
    id = db.Column(db.INTEGER, primary_key=True)
    title = db.Column(db.String(100))
    body = db.Column(db.TEXT)
    create_time = db.Column(db.DateTime, default=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    author_id = db.Column(db.INTEGER, db.ForeignKey('author.id'))

    def __repr__(self):
        return 'Title: %s, body: %s' % (self.title, self.body)


class Writer(db.Model):
    id = db.Column(db.INTEGER, primary_key=True)
    name = db.Column(db.String(20))
    books = db.relationship('Book', back_populates='writer')

    def __repr__(self):
        return self.name


class Book(db.Model):
    id = db.Column(db.INTEGER, primary_key=True)
    title = db.Column(db.String(100))
    body = db.Column(db.Text)
    writer_id = db.Column(db.INTEGER, db.ForeignKey('writer.id'))
    writer = db.relationship('Writer', back_populates='books')

    def __repr__(self):
        return self.title
