# FastAPI Todo Backend

A modern, clean-architecture backend for a Todo application, built as a learning project to master new technologies and backend development best practices.

---

## 🚀 Features
- **User authentication** (JWT, OAuth2)
- **CRUD for todos** (create, read, update, delete)
- **Role-based access** (users can only access their own todos)
- **Caching with Redis** for fast repeated access
- **Async SQLAlchemy** (with PostgreSQL)
- **Alembic migrations**
- **Pydantic validation**
- **Modular project structure** (repository, service, schema, API layers)
- **Pytest** for async testing

---

## 🛠️ Technologies Used

- **Python 3.12**
- **FastAPI** — modern, async web framework
- **SQLAlchemy (async)** — ORM for database access
- **PostgreSQL** — main database
- **Alembic** — database migrations
- **Redis** — caching layer
- **Pydantic** — data validation and serialization
- **Pytest + pytest-asyncio** — testing
- **httpx** — async HTTP client for tests
- **passlib, python-jose** — password hashing & JWT
- **dotenv** — environment variable management

---

## 📁 Project Structure

```
app/
  api/         # FastAPI routers (endpoints)
  core/        # Config, security, redis, dependencies
  database/    # DB config, session, base
  models/      # SQLAlchemy models
  repository/  # DB access logic
  schemas/     # Pydantic schemas
  services/    # Business logic, caching
  migrations/  # Alembic migrations
  tests/       # Pytest tests, fixtures, factories
alembic.ini    # Alembic config
.env.example   # Example environment variables
```

---

## 🧑‍💻 About This Project

This project was created by me as a way to learn and practice modern backend development. My goal was to:
- Explore new technologies (FastAPI, async SQLAlchemy, Redis, Alembic, etc.)
- Understand clean architecture and separation of concerns
- Build a real-world, testable backend from scratch
- Improve my skills as a backend developer

Feel free to use this as a reference or starting point for your own learning!

---

## ⚡ Getting Started

1. **Clone the repo:**
   ```bash
   git clone <your-repo-url>
   cd backend-todo
   ```
2. **Create and activate a virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
4. **Set up environment variables:**
   - Copy `.env.example` to `.env` and fill in your values.
5. **Run migrations:**
   ```bash
   alembic upgrade head
   ```
6. **Start Redis server** (if not running):
   ```bash
   redis-server
   ```
7. **Run the app:**
   ```bash
   uvicorn app.main:app --reload
   ```
8. **Run tests:**
   ```bash
   pytest -v
   ```

---

## 📫 Contact

If you have questions or want to connect, feel free to reach out!
