# 😼 Spy Cat Agency – Backend API

A API developed in FastAPI for managing the operations of the Spy Cat Agency (SCA), including spy cats, their missions, targets, and notes.

🔗 Related Repository
Frontend (Next.js): [Spy Cat – Frontend](https://github.com/ErickKS/nestjs-spy-cat-agency)

## 🚀 Features

- [X] Spy Cats CRUD: create, update, delete, list, and view cats
    - [X] Breed validation via [TheCatAPI](https://thecatapi.com)
- [X] Spy Cats CRUD: create, update, delete, list, and view cats
  - [X] Create missions
  - [X] Assign cats to missions
  - [X] Mark missions and targets as completed
  - [X] Mark missions and targets as completed
  - [X] Prevent updates to completed missions/targets
- [X] Target Notes: editable until the target is completed

## ⚙️ Project Setup

```bash
# Clone the repo
git clone https://github.com/ErickKS/python-spy-cat-agency
cd python-spy-cat-agency
```

```bash
# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

```bash
# Install dependencies
pip install -r requirements.txt
```

```bash
# Install dependencies
pip install -r requirements.txt
```

```bash
# Run database migrations
alembic upgrade head
```

```bash
# Start the application
uvicorn src.main:app --reload
```

### 🐳 Docker Setup (with PostgreSQL)

```bash
# Copy environment example
cp .env.example .env
```

```bash
# Build and run containers (API + PostgreSQL)
docker-compose up --build -d
```

#### After that, the app should be running at: http://localhost:8000/docs

## ✅ Next Steps

- [ ] Implement tests using `pytest`
- [ ] Create a Dockerfile to containerize the FastAPI app