from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from app.config import config

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message_category = 'info'
migrate = Migrate()

def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)

    from app import models

    # Register Blueprints
    from app.routes.auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)
    
    from app.routes.dashboard import dashboard as dashboard_blueprint
    app.register_blueprint(dashboard_blueprint)
    
    from app.routes.income import income_bp
    app.register_blueprint(income_bp)
    
    from app.routes.expenses import expenses_bp
    app.register_blueprint(expenses_bp)
    
    from app.routes.budgets import budgets_bp
    app.register_blueprint(budgets_bp)
    
    from app.routes.goals import goals_bp
    app.register_blueprint(goals_bp)
    
    from app.routes.ai import ai_bp
    app.register_blueprint(ai_bp)
    
    from app.routes.reports import reports_bp
    app.register_blueprint(reports_bp)

    return app
