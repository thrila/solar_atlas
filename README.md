
# Running Frontend & Backend

This repo has two apps:

- **Frontend** → Vite + React (`/frontend`)
- **Backend** → FastAPI (`/backend`)

---

## 1. Install Dependencies

### Frontend
```bash
cd frontend
npm install
````

### Backend

```bash
cd backend
pip install -r requirements.txt
```

---

## 2. Run the Apps

### Frontend (Vite Dev Server)

```bash
cd frontend
npm run dev
```

* Default: [http://localhost:5173](http://localhost:5173)

### Backend (FastAPI with Uvicorn)

```bash
cd backend
uvicorn app:app --reload
```

* Default: [http://localhost:8000](http://localhost:8000)
* Docs: [http://localhost:8000/docs](http://localhost:8000/docs)

