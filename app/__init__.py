from flask import Flask, jsonify
from config import Config
#-------------
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from celery import Celery

#----------------------------
celery = Celery(__name__,
                broker='redis://localhost:6379/0',
                backend='redis://localhost:6379/0')

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    #------------------------------------
    celery.conf.update(app.config)

    #-------------------------------------
    REDIS_URI = "redis://localhost:6379/1"

    limiter = Limiter(
        app=app,
        key_func=get_remote_address,
        storage_uri=REDIS_URI,
        default_limits=["100 per day", "10 per hour"]

    )

    app.limiter = limiter

    @app.errorhandler(429)
    def ratelimit_handler(e):
        return jsonify({
            "error": "Límite de solicitudes excedido",
            "message": "Has superado el límite de peticiones permitido. "
        }), 429

    #-------------------------------------



    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    return app