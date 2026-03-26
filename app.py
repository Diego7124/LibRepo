from flask import Flask
from dotenv import load_dotenv
from config.db import init_db
from routes.bookRoutes import book_bp
from routes.authorRoutes import author_bp
from routes.memberRoutes import member_bp

load_dotenv()

app = Flask(__name__)
init_db(app)
app.register_blueprint(book_bp)
app.register_blueprint(author_bp)
app.register_blueprint(member_bp)
@app.route('/')
def index():
    return {'message': 'API funcionando'}




if __name__ == '__main__':
    app.run()
