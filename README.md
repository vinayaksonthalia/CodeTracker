# CodeTracker API

A clean, single-file FastAPI backend application for tracking and logging coding problems (e.g., LeetCode, HackerRank).

## Features

- **Create, Read, Delete** problem logs via REST API endpoints.
- Stores detailed problem attributes: title, difficulty, pattern, language, and custom notes.
- Built-in **SQLite** database for zero-config, file-based data storage.
- Powered by **SQLAlchemy** for ORM interactions.
- Data validation enforced automatically by **Pydantic**.
- Pre-configured **CORS** middleware so your future frontend can connect instantly.

## Setup Instructions

### 1. Prerequisites
Ensure you have Python 3.8+ installed on your system.

### 2. Install Dependencies
It's recommended to use a virtual environment to keep your project isolated.

```bash
# Create and activate a virtual environment (optional but recommended)
python3 -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate

# Install the required packages
pip install fastapi uvicorn sqlalchemy pydantic
```

### 3. Run the Application
You can run the FastAPI server locally using `uvicorn`. The `--reload` flag makes the server automatically restart when you save changes to your code.

```bash
uvicorn main:app --reload
```

### 4. Explore Interactive Documentation
FastAPI automatically generates beautiful interactive API documentation based on your code schemas.
Once the server is running, visit:
- **Swagger UI**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) (Great for testing API endpoints from your browser)
- **ReDoc**: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/problems` | Add a new problem |
| `GET` | `/problems` | Retrieve all problems |
| `GET` | `/problems/{id}` | Retrieve a specific problem by ID |
| `DELETE`| `/problems/{id}` | Delete a specific problem by ID |

## File Structure

Everything is neatly organized within `main.py` to make it easy for beginners to understand the flow:
1. **Database Configuration:** Setup for SQLite.
2. **SQLAlchemy Models:** Database table schemas.
3. **Pydantic Schemas:** Request/Response validation.
4. **FastAPI Initialization:** App setup and CORS middleware.
5. **API Routes:** The endpoints for interacting with the data.

When you first run the app, the SQLite database will be automatically created as a file named `codetracker.db` in the same directory.
