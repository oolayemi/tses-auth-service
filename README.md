# Auth API Microservice

**Olayemi Olaomo** (<olayemiolaomo5@gmail.com>)  
January 15, 2026

---

## Clone Repository

Clone the repo:

```bash
git clone https://github.com/capitalsagetechnology/py-api-template.git
cd py-api-template
```

Create your `.env` from the `.env.sample`.

---

## Setup Local Development Environment

Setup your virtual environment using **venv** and **uv**  
> Your local `.venv` setup may be slightly different depending on your operating system.

We use **uv** as the package manager for this project.  
Install guide: https://docs.astral.sh/uv/

```bash
uv python install 3.13
uv python list
uv venv
source .venv/bin/activate
uv sync

---

## Run Code Locally

Ensure that the latest version of **Docker Desktop** is installed.  
Docker Compose is installed automatically with Docker Desktop.

Installation guide:  
https://docs.docker.com/desktop/install/mac-install

Run the following command from the root of the application:

```bash
docker compose up --build
```

Access the API documentation:
- http://localhost:58001/api/v1/doc

---

## Manage Migrations

Whenever you make changes to models, generate migrations **before pushing your code**.

Run the following commands in another terminal while the app is running:

```bash
docker compose exec api python manage.py makemigrations
docker compose exec api python manage.py migrate
```

## Contributors

| Name            | Role | Email                     |
|-----------------|------|---------------------------|
| Olayemi Olaomo  | SA   | olayemiolaomo5@gmail.com  |

---

