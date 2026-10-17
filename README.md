# Genetic Task Scheduler

Platform for modeling, executing, and visualizing task scheduling problems using a genetic algorithm. The project combines a Flask backend, MongoDB storage, asynchronous processing with Celery + Redis, and a React web interface for analyzing results, convergence, and Gantt-style schedules.

## What does it solve?

The system allows you to:

- Create job and operation scheduling scenarios.
- Run optimizations based on a genetic algorithm.
- Save results and execution parameters.
- Generate statistical reports from multiple runs.
- Visualize fitness evolution and the suggested final schedule.

## Tech stack

- Backend: Python, Flask, MongoEngine, NumPy, Celery
- Database: MongoDB
- Task queue: Redis
- Frontend: React + Vite + TypeScript
- Visualization: D3
- Infrastructure: Docker Compose

## Project structure

```text
.
├── backend/                 # REST API + genetic algorithm logic
│   ├── app/                 # Flask app, controllers, services, models
│   ├── docker-compose.yml   # MongoDB, Redis, API, and Celery worker
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── run.py
│   └── test_backend.py
├── frontend/                # React application for visual interaction
│   ├── src/
│   ├── package.json
│   └── vite.config.ts
├── example_scenarios/       # Example JSON scenarios
├── setup_and_run.sh         # Quick start on Linux/macOS
├── setup_and_run.ps1        # Quick start on Windows
├── LICENSE
├── Code_of_Conduct.md
└── README.md
```

## Prerequisites

For the recommended containerized setup, you need:

- Docker
- Docker Compose
- Node.js 18+
- npm
- Python 3 (optional, mainly for local testing and scripts)

> Docker startup is intended to make the full API, MongoDB, and Redis environment easier to set up.

### Docker permission issue on Linux

If Docker is installed but the user cannot run it, the project script will detect this and print a clear message with the usual fix:

```bash
sudo groupadd -f docker
sudo usermod -aG docker "$USER"
newgrp docker
sudo systemctl enable --now docker
```

This is a host-level permission problem, not a project bug. The script validates `docker info` before trying to start the containers.

## Quick start

### Option 1: Automated script

#### Linux/macOS

```bash
chmod +x setup_and_run.sh
./setup_and_run.sh
```

If the system is missing dependencies, you can use:

```bash
./setup_and_run.sh --install-deps
```

This mode detects the Linux distribution and tries to install the required packages automatically (Docker, Docker Compose, Node.js, npm, Python, etc.).

#### Windows (PowerShell)

```powershell
powershell -ExecutionPolicy Bypass -File .\setup_and_run.ps1
```

These scripts validate dependencies, create the `.env` file if it does not exist, check Docker permissions, start Docker, and launch the frontend.

### Option 2: Manual installation

1. Configure backend environment variables:

```bash
cd backend
cp .env.example .env
```

2. Start infrastructure services:

```bash
docker compose up --build -d
```

3. Install frontend dependencies:

```bash
cd ../frontend
npm install
npm run dev
```

### Docker troubleshooting

If the command fails with a permissions error, run:

```bash
sudo groupadd -f docker
sudo usermod -aG docker "$USER"
newgrp docker
```

Then restart the terminal or log out/in again.

## Default URLs

- Frontend: http://localhost:5173
- Flask API: http://localhost:5000
- MongoDB: mongodb://localhost:27017
- Redis: redis://localhost:6379

## Scenario model

The API accepts scenarios with this general structure:

```json
{
  "name": "Scenario 1",
  "jobs": [
    {
      "job_id": 1,
      "operations": [
        {
          "op_id": 1,
          "times": {
            "M1": 3.5,
            "M2": 6.7,
            "M3": 2.5,
            "M4": 8.2
          }
        }
      ]
    }
  ]
}
```

Actual examples are in the `example_scenarios/` folder.

## REST API

### Scenarios

| Method | Route | Description |
|---|---|---|
| POST | `/api/v1/scenarios` | Create a scenario |
| GET | `/api/v1/scenarios` | List saved scenarios |

### Executions

| Method | Route | Description |
|---|---|---|
| POST | `/api/v1/executions` | Trigger an asynchronous execution of the algorithm |
| GET | `/api/v1/executions/<execution_id>` | Check the status and result of an execution |

### Reports

| Method | Route | Description |
|---|---|---|
| POST | `/api/v1/reports` | Generate a statistical report |
| GET | `/api/v1/reports/<report_id>` | Check the status of the report |

## How the algorithm works

The backend rebuilds each scenario as a job scheduling problem structure and runs a genetic algorithm with:

- random initial population,
- makespan evaluation,
- load-balanced selection and mutation,
- best chromosome calculation,
- generation of data for schedule and convergence.

Results are serialized so the frontend can display them in charts and tables.

## Development and testing

To run backend tests:

```bash
cd backend
pytest
```

To build the frontend application:

```bash
cd frontend
npm run build
```

## Usage notes

- The backend uses Celery so the interface is not blocked while optimization runs.
- MongoDB stores scenarios, executions, and reports.
- Redis acts as the broker and result backend for Celery.
- The frontend connects to the REST API to load scenarios and check results in real time.

## License

This project is distributed under the license indicated in [LICENSE](LICENSE).

## Contributing

If you want to contribute, you can:

1. Clone the repository.
2. Create a working branch.
3. Make changes and test the functionality.
4. Open a pull request with a clear description of the improvement.

---

Developed as a task scheduling solution focused on optimization with evolutionary algorithms.