import os
from urllib.parse import quote_plus
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def init_db(app):
    database_url = os.environ.get('DATABASE_URL')
    if not database_url:
        raise RuntimeError('DATABASE_URL environment variable not set')
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    with app.app_context():
        db.create_all()
