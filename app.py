from flask import Flask
from flask_cors import CORS
import os
from dotenv import load_dotenv
from config.db import init_db
from routes.bookRoutes import book_bp
from routes.authorRoutes import author_bp
from routes.memberRoutes import member_bp


load_dotenv()

app = Flask(__name__)
# Lee los orígenes permitidos desde la variable de entorno ALLOWED_ORIGINS
allowed_origins = os.getenv("ALLOWED_ORIGINS", "*")
if "," in allowed_origins:
    allowed_origins = [origin.strip() for origin in allowed_origins.split(",")]
CORS(app, origins=allowed_origins)
init_db(app)
app.register_blueprint(book_bp)
app.register_blueprint(author_bp)
app.register_blueprint(member_bp)
@app.route('/')
def index():
    return {'message': 'API funcionando'}




if __name__ == '__main__':
    app.run()
