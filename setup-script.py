# setup_project.py
import os
import subprocess
from pathlib import Path

def create_file(path: Path, content: str = ""):
    """Create a file with optional content"""
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

def setup_project():
    # Project root
    root = Path("fantasy-football-app")
    root.mkdir(exist_ok=True)

    # Backend structure
    backend = root / "backend"
    backend.mkdir(exist_ok=True)

    # Create Python files with basic content
    create_file(backend / "app" / "__init__.py")
    create_file(backend / "app" / "main.py", """from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Fantasy Football League API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/v1/health-check")
async def health_check():
    return {"status": "healthy"}
""")

    # Create backend directories
    dirs = [
        "alembic/versions",
        "app/models",
        "app/schemas",
        "app/api/v1/endpoints",
        "app/core",
        "app/services",
        "tests/api",
    ]
    
    for dir_path in dirs:
        (backend / dir_path).mkdir(parents=True, exist_ok=True)
        create_file(backend / dir_path / "__init__.py")

    # Create requirements.txt
    requirements = """fastapi==0.104.1
uvicorn==0.24.0
sqlalchemy==2.0.23
alembic==1.12.1
psycopg2-binary==2.9.9
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
python-multipart==0.0.6
requests==2.31.0
"""
    create_file(backend / "requirements.txt", requirements)

    # Frontend structure using Vite
    print("Setting up frontend with Vite...")
    os.chdir(root)
    subprocess.run(["npm", "create", "vite@latest", "frontend", "--", "--template", "react-ts"], check=True)
    
    # Frontend additional directories
    frontend = root / "frontend" / "src"
    frontend_dirs = [
        "components/common",
        "components/stats",
        "components/posts",
        "pages",
        "hooks",
        "api",
        "types",
        "utils",
        "context",
        "styles",
    ]
    
    for dir_path in frontend_dirs:
        (frontend / dir_path).mkdir(parents=True, exist_ok=True)

    # Create docker files
    docker = root / "docker"
    docker.mkdir(exist_ok=True)
    
    # Backend Dockerfile
    create_file(docker / "backend.Dockerfile", """FROM python:3.11-slim

WORKDIR /app
COPY ./backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY ./backend .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
""")

    # Frontend Dockerfile
    create_file(docker / "frontend.Dockerfile", """FROM node:18-alpine

WORKDIR /app
COPY ./frontend/package*.json ./
RUN npm install
COPY ./frontend .

CMD ["npm", "run", "dev"]
""")

    # Docker Compose
    create_file(root / "docker-compose.yml", """version: '3.8'
services:
  backend:
    build:
      context: .
      dockerfile: docker/backend.Dockerfile
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://postgres:postgres@db:5432/fantasy_football
    depends_on:
      - db

  frontend:
    build:
      context: .
      dockerfile: docker/frontend.Dockerfile
    ports:
      - "5173:5173"
    volumes:
      - ./frontend:/app
      - /app/node_modules
    environment:
      - VITE_API_URL=http://localhost:8000

  db:
    image: postgres:15
    environment:
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=postgres
      - POSTGRES_DB=fantasy_football
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
""")

    # Create README
    create_file(root / "README.md", """# Fantasy Football League Web App

## Setup

1. Clone the repository
2. Install backend dependencies:
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: .\\venv\\Scripts\\activate
   pip install -r requirements.txt
   ```

3. Install frontend dependencies:
   ```bash
   cd frontend
   npm install
   ```

## Development

### Backend
```bash
cd backend
uvicorn app.main:app --reload
```

### Frontend
```bash
cd frontend
npm run dev
```

## Docker
To run the entire stack:
```bash
docker-compose up --build
```
""")

    print("Project structure created successfully!")
    print("\nNext steps:")
    print("1. cd fantasy-football-app")
    print("2. cd frontend && npm install")
    print("3. cd ../backend")
    print("4. python -m venv venv")
    print("5. source venv/bin/activate  # On Windows: .\\venv\\Scripts\\activate")
    print("6. pip install -r requirements.txt")

if __name__ == "__main__":
    setup_project()