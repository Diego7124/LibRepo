import os
from urllib.parse import quote_plus
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def init_db(app):
    server = os.environ.get('DB_SERVER')
    database = os.environ.get('DB_NAME')
    driver = os.environ.get('DB_DRIVER')

    connection_string = f"DRIVER={{{driver}}};SERVER={server};DATABASE={database};Trusted_Connection=yes;"
    app.config['SQLALCHEMY_DATABASE_URI'] = f"mssql+pyodbc:///?odbc_connect={quote_plus(connection_string)}"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    with app.app_context():
        db.create_all()
