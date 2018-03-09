from emile_server import app
from backend import db


def create_app():
     db.init_app(app)
     with app.app_context():
         db.create_all()
     return True


if __name__=='__main__':
    create_app()
