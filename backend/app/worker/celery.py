"""
Módulo de configuração do worker Celery para o Sistema de Gestão de Licitações Governamentais.
Este módulo configura o Celery para processamento de tarefas em background.
"""

import os
from celery import Celery

from app.core.config import settings

# Configuração do Celery com Redis como broker
celery_app = Celery(
    "worker",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_BROKER_URL
)

# Configurações do Celery
celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="America/Sao_Paulo",
    enable_utc=True,
    task_track_started=True,
    worker_max_tasks_per_child=1000,
    task_acks_late=True,
    task_reject_on_worker_lost=True,
    task_time_limit=3600,  # 1 hora
    task_soft_time_limit=3540,  # 59 minutos
)

# Inclui tarefas do módulo tasks
celery_app.autodiscover_tasks(["app.worker.tasks"])
