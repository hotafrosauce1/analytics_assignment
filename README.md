
## **1. Design Explanation**
My design consists of a FastAPI backend exposing a REST API for data ingestion and analytics.  For POST requests, the data ingestion task is asynchronously offloaded to 
a Redis message queue where it can be picked up by a Celery worker, enabling a queue-based event-driven data ingestion.  For GET requests, 
a SQL query is made to the Postgres database and the result is returned to the client as a JSON document.  The query computes aggregated metrics for a given user_id, start_date, and end_date. The Postgres 
database contains a single table named health_metrics with the columns:

- `user_id` (INTEGER)
- `timestamp` (TIMESTAMP WITH TIME ZONE)
- `heart_rate` (INTEGER)
- `steps` (INTEGER)
- `calories` (FLOAT)

With the primary key being `(user_id, timestamp)`

---

## **2. Running the Application with Docker**

Build and start the services using:

```bash
   docker-compose up --build -d
```
This will spin up:
- **FastAPI** (`fastapi_app`) - REST API server
- **PostgreSQL** (`postgres_db`) - Database
- **Redis** (`redis`) - Celery message broker
---

## **3. Testing the API Endpoints**
Below are **sample requests** for testing the API manually.

### **Ingest Sample Data (POST `/ingest`)**
Use the following command to send **a new health data entry**:
```bash
   curl -X POST "http://localhost:8000/ingest" \
        -H "Content-Type: application/json" \
        -d '{"user_id": 303, "timestamp": "2025-02-01T14:00:00Z", "heart_rate": 88, "steps": 400, "calories": 15.2}'
```
**Expected Response:**
```json
{"message": "Data received"}
```

---

### **Retrieve Aggregated Data (GET `/metrics`)**
Retrieve **aggregated health statistics** for `user_id = 303` over a time range:
```bash
   curl "http://localhost:8000/metrics?user_id=303&start_date=2025-02-01T13:00:00Z&end_date=2025-02-01T15:00:00Z"
```
**Expected Response:**
```json
{
  "avg_heart_rate": 88.0,
  "total_steps": 400,
  "total_calories": 15.2
}
```

---

## **4. Running Tests**
Run the following command to run the small suite of tests in **tests/test_main.py**:
```bash
   docker exec -it fastapi_app python tests/test_main.py
```

**Expected Output:**
```
Sending POST request with data: {'user_id': 101, 'timestamp': '2025-01-01T09:45:00Z', 'heart_rate': 82, 'steps': 300, 'calories': 13}

Sending POST request with data: {'user_id': 202, 'timestamp': '2025-01-01T10:00:00Z', 'heart_rate': 90, 'steps': 500, 'calories': 22.5}

Sending POST request with data: {'user_id': 101, 'timestamp': '2025-01-01T10:15:00Z', 'heart_rate': 85, 'steps': 200, 'calories': 9.1}

Sending POST request with data: {'user_id': 101, 'timestamp': '2025-01-01T09:30:00Z', 'heart_rate': 78, 'steps': 150, 'calories': 6.5}

All POST requests sent!

Sending GET request to the server for user_id 101 between 2025-01-01T09:00:00Z and 2025-01-01T11:00:00Z

Sending GET request to the server for user_id 101 between 2025-01-01T12:00:00Z and 2025-01-01T13:00:00Z

Sending GET request to the server for invalid user_id 999 between 2025-01-01T09:00:00Z and 2025-01-01T11:00:00Z

Sending GET request to the server with invalid argument types

Sending GET request to the server with missing arguments

Sending POST request to the server with invalid argument types

Sending POST request to the server with missing arguments

All tests passed!
```

---

## **5. Stopping the Application**
```bash
   docker-compose down
```

---
