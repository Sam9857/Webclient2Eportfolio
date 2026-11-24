from flask_sqlalchemy import SQLAlchemy

# SQLAlchemy object
db = SQLAlchemy()


def connect_db(app):

    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:admin123@localhost:2005/postgres'

    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
