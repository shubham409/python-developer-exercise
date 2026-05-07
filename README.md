# Network Route Optimization API

A Django REST Framework based backend service for network route optimization using Dijkstra’s shortest path algorithm.

The system allows:

- Creating network nodes
- Creating directional network edges with latency
- Finding shortest latency path between nodes
- Storing route history
- Filtering historical route queries

---

# Tech Stack

- Python 3.11.7
- Django
- Django REST Framework
- PostgreSQL
- Dijkstra's Algorithm

---

# Features

- Node management APIs
- Edge management APIs
- Shortest path computation
- Route history tracking
- Admin panel support
- API test coverage
- PostgreSQL support

---

# Project Setup

## 1. Clone Repository

```bash
git clone <repository-url>
cd network-route-optimization
```

---

# 2. Create Virtual Environment

## Windows

```bash
python -m venv venv
venv\Scripts\activate
```

## Linux/Mac

```bash
python3 -m venv venv
source venv/bin/activate
```

---

# 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

# 4. Configure PostgreSQL

Update database configuration in:

```text
core/settings.py
```

Example:

```python
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "network_db",
        "USER": "postgres",
        "PASSWORD": "your_password",
        "HOST": "localhost",
        "PORT": "5432",
    }
}
```

Create PostgreSQL database before running migrations.

Example:

```sql
CREATE DATABASE network_db;
```

---

# 5. Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

---

# 6. Create Admin User

```bash
python manage.py createsuperuser
```

---

# 7. Run Server

```bash
python manage.py runserver
```

Application will start at:

```text
http://127.0.0.1:8000
```

---

# Admin Panel

```text
http://127.0.0.1:8000/admin
```

---

# Run Tests

```bash
python manage.py test
```

---

# API Base URL

```text
http://127.0.0.1:8000/solution1
```

---

# Available APIs

| Method | Endpoint | Description |
|---|---|---|
| POST | `/solution1/nodes` | Create node |
| GET | `/solution1/nodes/list` | List nodes |
| DELETE | `/solution1/nodes/{id}` | Delete node |
| POST | `/solution1/edges` | Create edge |
| GET | `/solution1/edges/list` | List edges |
| DELETE | `/solution1/edges/{id}` | Delete edge |
| POST | `/solution1/routes/shortest` | Find shortest route |
| GET | `/solution1/routes/history` | Fetch route history |

---

# Example Shortest Route Request

## Request

```json
{
  "source": "ServerA",
  "destination": "ServerD"
}
```

## Response

```json
{
  "total_latency": 23.4,
  "path": [
    "ServerA",
    "ServerB",
    "ServerD"
  ]
}
```

---

# Algorithm Used

The shortest route is computed using:

```text
Dijkstra's Algorithm
```

The network is modeled as a directed weighted graph where:

- Nodes represent servers
- Edges represent directional network connections
- Latency acts as edge weight

Time Complexity:

```text
O((V + E) log V)
```

using a priority queue(min heap).

---

# Design Notes

- Graph is treated as directional
- Route history is persisted for auditing
- PostgreSQL JSONField used for path storage
- select_related used to optimize DB queries
- API validations included for edge cases

---

# Future Improvements

Possible production-scale enhancements:

- Redis graph caching
- pgRouting integration
- Neo4j graph database
- Bidirectional routing support
- Async route computation
- Route caching

---

# Author

Shubham Kumar Mishra
