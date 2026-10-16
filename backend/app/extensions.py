"""extensions.py: Instancias globales de extensiones para evitar importaciones circulares."""
from celery import Celery

# Inicializar Celery e indicar explícitamente qué módulos contienen las tareas
celery_app = Celery(
    'genetic_scheduler',
    include=['app.tasks.ga_tasks']
)