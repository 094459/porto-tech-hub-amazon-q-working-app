import os
from flask import Flask
from flask_login import LoginManager
from models.database import init_db, db
from models import User
from routes import auth_bp, survey_bp, main_bp

def create_app():
    app = Flask(__name__)
    
    # Configuration
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev_key_123')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
        'DATABASE_URL', 'sqlite:///customer_feedback.db'
    )
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize extensions
    init_db(app)
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Register blueprints
    app.register_blueprint(main_bp)
    app.register_blueprint(survey_bp, url_prefix='/survey')
    app.register_blueprint(auth_bp, url_prefix='/auth')
    
    print(app.url_map)
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)