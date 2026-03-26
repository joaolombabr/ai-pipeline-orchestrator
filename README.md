# 🚀 AI Pipeline Orchestrator

> Plataforma de orquestração de pipelines de dados com processamento assíncrono, containerizada com Docker.

![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.111-green?logo=fastapi)
![Docker](https://img.shields.io/badge/Docker-Compose-blue?logo=docker)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-blue?logo=postgresql)
![Celery](https://img.shields.io/badge/Celery-5.3-green?logo=celery)
![Redis](https://img.shields.io/badge/Redis-7-red?logo=redis)

---

## 🏗️ Arquitetura

```
┌─────────────┐     ┌──────────────┐     ┌─────────────────┐
│    Nginx    │────▶│  FastAPI API │────▶│   PostgreSQL    │
│ (Port 80)  │     │  (Port 8000) │     │   (Port 5432)   │
└─────────────┘     └──────┬───────┘     └─────────────────┘
                           │
                    ┌──────▼───────┐
                    │    Redis     │
                    │  (Port 6379) │
                    └──────┬───────┘
                           │
              ┌────────────┴────────────┐
              │                         │
       ┌──────▼──────┐          ┌───────▼──────┐
       │  Celery     │          │  Celery Beat │
       │  Worker     │          │  (Scheduler) │
       └─────────────┘          └──────────────┘
                    ┌─────────────────┐
                    │     Flower      │
                    │  (Port 5555)    │
                    └─────────────────┘
```

## ✨ Funcionalidades

- **REST API** completa com FastAPI e documentação automática (Swagger/ReDoc)
- **Processamento assíncrono** de pipelines ETL com Celery
- **Agendamento automático** de tarefas via Celery Beat (cron)
- **Monitoramento em tempo real** com Flower dashboard
- **Banco de dados relacional** PostgreSQL com SQLAlchemy async
- **Cache e message broker** com Redis
- **Reverse proxy** com Nginx + rate limiting
- **Healthcheck** de todos os serviços
- **Docker Compose** com 6 containers orquestrados

## 🚀 Como rodar

### Pré-requisitos
- Docker >= 24
- Docker Compose >= 2.20

### 1. Clone o projeto
```bash
git clone https://github.com/joaolombabr/ai-pipeline-orchestrator
cd ai-pipeline-orchestrator
```

### 2. Configure o ambiente
```bash
cp .env.example .env
# Edite o .env com suas configurações se necessário
```

### 3. Suba os containers
```bash
make up
# ou: docker compose up -d --build
```

### 4. Acesse os serviços

| Serviço | URL | Descrição |
|---------|-----|-----------|
| API Docs | http://localhost/docs | Swagger UI |
| ReDoc | http://localhost/redoc | Documentação alternativa |
| Health | http://localhost/health | Status dos serviços |
| Flower | http://localhost:5555 | Monitor de tarefas Celery |

---

## 📡 Endpoints da API

### Pipelines
| Método | Endpoint | Descrição |
|--------|----------|-----------|
| GET | `/api/v1/pipelines/` | Lista todos os pipelines |
| POST | `/api/v1/pipelines/` | Cria novo pipeline |
| GET | `/api/v1/pipelines/{id}` | Busca pipeline por ID |
| POST | `/api/v1/pipelines/{id}/run` | Dispara execução |
| GET | `/api/v1/pipelines/{id}/runs` | Lista execuções |
| DELETE | `/api/v1/pipelines/{id}` | Remove pipeline |

### Tasks
| Método | Endpoint | Descrição |
|--------|----------|-----------|
| GET | `/api/v1/tasks/{task_id}` | Status de uma tarefa |
| DELETE | `/api/v1/tasks/{task_id}` | Cancela uma tarefa |

---

## 🛠️ Comandos úteis

```bash
make up           # Sobe todos os containers
make down         # Derruba os containers
make logs         # Logs em tempo real
make logs-api     # Logs apenas da API
make logs-worker  # Logs apenas do worker
make shell        # Shell dentro da API
make db           # Acessa o PostgreSQL
make reset        # Reset total (remove volumes)
```

## 🧪 Testando a API

```bash
# Criar um pipeline
curl -X POST http://localhost/api/v1/pipelines/ \
  -H "Content-Type: application/json" \
  -d '{"name": "Meu ETL", "description": "Pipeline de teste", "config": {"source": "api"}}'

# Disparar execução
curl -X POST http://localhost/api/v1/pipelines/{id}/run

# Verificar status da tarefa
curl http://localhost/api/v1/tasks/{task_id}
```

---

## 🗂️ Estrutura do projeto

```
ai-pipeline-orchestrator/
├── docker-compose.yml
├── .env.example
├── Makefile
├── api/
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── main.py
│   ├── core/
│   │   ├── config.py       # Configurações (Pydantic Settings)
│   │   ├── database.py     # SQLAlchemy async
│   │   └── celery_app.py   # Celery + Beat schedule
│   ├── models/
│   │   └── pipeline.py     # Modelos do banco
│   ├── routers/
│   │   ├── pipelines.py    # CRUD de pipelines
│   │   ├── tasks.py        # Status de tarefas
│   │   └── health.py       # Healthcheck
│   └── worker/
│       └── tasks.py        # Tarefas Celery (ETL)
├── postgres/
│   └── init.sql            # Setup inicial do banco
└── nginx/
    └── nginx.conf          # Reverse proxy + rate limit
```

---

## 👨‍💻 Autor

**João Paulo** — Dev Full Stack & IA  
[![LinkedIn](https://img.shields.io/badge/LinkedIn-joaolombadev-blue?logo=linkedin)](https://www.linkedin.com/in/joaolombadev)
[![GitHub](https://img.shields.io/badge/GitHub-joaolombabr-black?logo=github)](https://github.com/joaolombabr)
[![X](https://img.shields.io/badge/X-outlastgoat2-black?logo=x)](https://x.com/outlastgoat2)
