from db_connect import db

class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(55), unique=True, nullable=False)
    password = db.Column(db.String(100), unique=False, nullable=False)

    # указание на отношение (один u - один p)
    profile = db.relationship(
        'Profile',
        uselist=False,
        back_populates='user'
    )

    # указание на отношение (один u - много n)
    notes = db.relationship(
        'Notes',
        back_populates='user'
    )


class Profile(db.Model):
    __tablename__ = 'profile'

    id = db.Column(db.Integer, primary_key=True)
    bio = db.Column(db.String(100), nullable=False)
    ava = db.Column(db.String(555), nullable=True)

    # указание на отношение (один u - один p)
    user = db.relationship(
        'User',
        back_populates='profile'
    )

    # зависимая таблица из 1 к 1 с внешним ключом (указание на владельца user)
    user_id = db.Column(
        db.Integer,
        db.ForeignKey('user.id'),
        unique=True
    )

class Notes(db.Model):
    __tablename__ = 'notes'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(55), nullable=False)
    text_in_note = db.Column(db.Text, nullable=False)

    tags = db.relationship('Tags', secondary='notes_tags', back_populates='notes')

    user_id = db.Column(
        db.Integer,
        db.ForeignKey('user.id')
    )

    # указание на отношение (один u - много n)
    user = db.relationship(
        'User',
        back_populates='notes'
    )

class Tags(db.Model):
    __tablename__ = 'tags'
    id = db.Column(db.Integer, primary_key=True)
    name_title = db.Column(db.String(55), nullable=False)

    notes = db.relationship('Notes', secondary='notes_tags', back_populates='tags')

# many to many
notes_tags = db.Table(
    'notes_tags',
    db.Column('notes_id', db.Integer, db.ForeignKey('notes.id')),
    db.Column('tags_id', db.Integer, db.ForeignKey('tags.id'))
)

