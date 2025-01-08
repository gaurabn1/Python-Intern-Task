from flask import Flask
from extensions import db, bcrypt, jwt, session
from config import Config
from blog.routes import blog_blueprint
from auth.routes import auth_blueprint
import blocklist


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    session.init_app(app)
    jwt.init_app(app)
    bcrypt.init_app(app)

    # Register Blueprints
    app.register_blueprint(auth_blueprint, url_prefix="/auth")
    app.register_blueprint(blog_blueprint, url_prefix="/blog")

    return app


app = create_app()

with app.app_context():
    from models import User, Blog  
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)
