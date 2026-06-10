# Running Adjective Collector with Docker

This guide converts the project from a local Flask + MariaDB setup into a fully containerised stack using Docker and Docker Compose. Both the app and the database run as containers, so there is no need to install MariaDB or Python on your machine.

---

## Requirements

- [Docker Desktop](https://www.docker.com/products/docker-desktop/) installed and running

---

## 1. Create the Dockerfile

Create a file called `Dockerfile` (no extension) in the project root:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# libmariadb-dev and gcc are required to build the mariadb Python connector
RUN apt-get update && apt-get install -y \
    libmariadb-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["python", "app.py"]
```

---

## 2. Create the database initialisation script

Create `init.sql` in the project root. Docker will run this automatically when the MariaDB container starts for the first time:

```sql
CREATE TABLE IF NOT EXISTS adjectives (
    id        INT          AUTO_INCREMENT PRIMARY KEY,
    adjective VARCHAR(50)  NOT NULL UNIQUE,
    counter   INT          NOT NULL
);
```

---

## 3. Create docker-compose.yml

Create `docker-compose.yml` in the project root:

```yaml
services:

  app:
    build: .
    ports:
      - "5000:5000"
    env_file:
      - .env
    depends_on:
      db:
        condition: service_healthy
    restart: unless-stopped

  db:
    image: mariadb:11
    environment:
      MYSQL_ROOT_PASSWORD: rootpassword
      MYSQL_DATABASE: adjectives
      MYSQL_USER: flaskuser
      MYSQL_PASSWORD: pythonpass
    volumes:
      - db_data:/var/lib/mysql
      - ./init.sql:/docker-entrypoint-initdb.d/init.sql
    healthcheck:
      test: ["CMD", "healthcheck.sh", "--connect", "--innodb_initialized"]
      interval: 10s
      timeout: 5s
      retries: 5
    ports:
      - "3306:3306"

volumes:
  db_data:
```

---

## 4. Update your .env

When running in Docker, the app talks to the `db` container by its service name, not an IP address. Update your `.env`:

```env
DB_HOST=db
DB_PORT=3306
DB_USER=flaskuser
DB_PASSWORD=pythonpass
DB_NAME=adjectives
```

> Keep your original `.env` values backed up if you still want to run the app locally against your UTM VM.

---

## 5. Add a .dockerignore

Create `.dockerignore` in the project root to keep the image small:

```
.env
.venv
__pycache__
*.pyc
*.pyo
.git
```

---

## 6. Build and run

```bash
docker compose up --build
```

The first run will:
1. Build the Flask app image
2. Pull the MariaDB 11 image
3. Start the database, run `init.sql`, and wait until it is healthy
4. Start the Flask app

The app will be available at **http://localhost:5000**

---

## 7. Useful commands

| Task | Command |
|---|---|
| Start in background | `docker compose up -d --build` |
| View logs | `docker compose logs -f` |
| Stop containers | `docker compose down` |
| Stop and delete all data | `docker compose down -v` |
| Open a MariaDB shell | `docker compose exec db mariadb -u flaskuser -ppythonpass adjectives` |
| Rebuild after code change | `docker compose up --build` |

---

## Notes

- Database data is stored in the named volume `db_data`. It persists between restarts. Use `docker compose down -v` only if you want to wipe everything and start fresh.
- The `depends_on: condition: service_healthy` ensures Flask never tries to connect before MariaDB is ready, avoiding startup race conditions.
- Do not commit `.env` to version control. It is already in `.gitignore` but double-check before pushing.
