## TinyPulse - Downtime tracking & monitoring service.

This small project can be deployed and run via docker containers, that will allow you to enter and track whether a repository is up & running or if it has encountered some error and is unreachable. 

In addition to an on-demand service check, this will give you an option to enable background tracking which will be executed via celery in order to track the status of the services while you sleep.

Configuration options such as Email when a service is down or recently recovered from a downtime is something which is a part of this project. Additionally, graphs & charts to provide a dynamic & interactive report is a small feature as well.

## Tech Stack 

1. Backend  - Python,FastAPI, Celery
2. Frontend - ReactJS
3. Database - PostgreSQL, Redis
4. Deploy   - Docker, Caddy RP
5. Other    - Alembic, Plotly


## Running the Backend 

### Install UV 

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Install the packages

```bash
cd tiny-pulse-backend
uv sync
```

### Run the backend server 
```bash
uv run fastapi dev src/main.py
```
