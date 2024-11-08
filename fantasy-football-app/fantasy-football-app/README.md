# Fantasy Football League Web App

## Setup

1. Clone the repository
2. Install backend dependencies:
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: .\venv\Scripts\activate
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
