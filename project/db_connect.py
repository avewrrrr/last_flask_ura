from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def connect_db(app):
    app.config['SQLALCHEMY_DATABASE_URI'] = ( 'postgresql://postgres:admin@localhost:4444/db_oris_lastproject' )
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
