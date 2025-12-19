from flask import Flask
from app.watchlist_db import init_db

def create_app() -> Flask:
    app = Flask(__name__)
    app.secret_key = "dev-secret"  # ok for class project

    init_db()

    from web_app.routes.home_routes import home_bp
    from web_app.routes.stocks_routes import stocks_bp
    from web_app.routes.watchlist_routes import watchlist_bp

    app.register_blueprint(home_bp)
    app.register_blueprint(stocks_bp)
    app.register_blueprint(watchlist_bp)

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
