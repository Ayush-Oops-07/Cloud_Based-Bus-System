from flask import Flask, redirect, url_for
from flask_login import LoginManager
from models import db, User
from config import Config

def create_app():
    app = Flask(__name__, template_folder="templates", static_folder="static")
    app.config.from_object(Config)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:4753@localhost:3306/busdb'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Blueprints
    from blueprints.auth import auth_bp
    from blueprints.passenger import passenger_bp
    from blueprints.admin import admin_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(passenger_bp)
    app.register_blueprint(admin_bp, url_prefix="/admin")

    @app.route("/")
    def index():
        return redirect(url_for("passenger.search"))

    with app.app_context():
        db.create_all()

        # Create default admin if not exists
        if not User.query.filter_by(email="admin@bus.com").first():
            admin = User(
                username="Admin",
                email="admin@bus.com",
                # ➡️ Storing password in plain text
                password_hash="admin123",
                role="admin"
            )
            db.session.add(admin)
            db.session.commit()
            print("✅ Default admin created: admin@bus.com / admin123")

    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)