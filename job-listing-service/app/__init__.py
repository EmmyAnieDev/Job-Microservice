from flask import Flask, jsonify
from flask_cors import CORS

from app.api.db import db
from config import Config, config
from app.extensions import mail, ma, migrate

from app.api.v1.routes import jobs

def create_app():
    app = Flask(__name__)
    app.config.from_object(config)
    app.config.from_object(Config)

    # Initialize CORS
    CORS(app, resources={r"/*": {"origins": "*"}})

    # Initialize extensions
    db.init_app(app)
    mail.init_app(app)
    ma.init_app(app)
    migrate.init_app(app, db)

    # Register Flask blueprints
    app.register_blueprint(jobs.bp)

    # Health check endpoint
    @app.route('/api', methods=['GET'])
    def api_check():
        return jsonify({
            'message': 'API is running...',
            'version': '1.0.0',
            'status': 'healthy'
        }), 200

    return app