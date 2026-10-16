"""__init__.py: Flask App Factory."""
from flask import Flask
from flask_cors import CORS
from mongoengine import connect
from app.config import Config
from app.extensions import celery_app

def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Habilitar CORS para el Frontend (React)
    CORS(app)
    
    # Conectar a MongoDB
    connect(host=app.config["MONGO_URI"])
    
    # Configurar Celery
    celery_app.conf.update(
        broker_url=app.config["CELERY_BROKER_URL"],
        result_backend=app.config["CELERY_RESULT_BACKEND"],
        # CLAVE: Indicar a Celery qué módulos contienen las tareas
        include=['app.tasks.ga_tasks'] 
    )
    
    class ContextTask(celery_app.Task):
        """Permite que las tareas de Celery accedan al contexto de Flask si es necesario."""
        abstract = True
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)
    celery_app.Task = ContextTask

    # Registrar Blueprints (Controladores)
    from app.controllers.scenario_controller import scenario_bp
    from app.controllers.execution_controller import execution_bp
    from app.controllers.report_controller import report_bp
    
    app.register_blueprint(scenario_bp, url_prefix="/api/v1/scenarios")
    app.register_blueprint(execution_bp, url_prefix="/api/v1/executions")
    app.register_blueprint(report_bp, url_prefix="/api/v1/reports")

    return app