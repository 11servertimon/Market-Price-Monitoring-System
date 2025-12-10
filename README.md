# Market Price Monitoring System

Market Price Monitoring System is a backend API built with **Django** and **Django REST Framework** designed for tracking, storing, and analysing product prices across multiple stores over time.

The project demonstrates a real-world backend architecture featuring:

- relational data modelling  
- historical data tracking  
- analytical endpoints  
- role-based write permissions  
- fully documented REST API (Swagger / ReDoc)  
- Dockerized production-style deployment  

---

## Features

### Core domain

- **Stores**
  - Represents online and physical shops
  - Metadata: name, website, is_online flag

- **Products**
  - Central product catalog
  - Fields: name, SKU (unique), category

- **Price Records**
  - Historical pricing snapshots per product and store
  - Fields: price, currency, captured_at timestamp

---

## CRUD API

All entities expose full CRUD capabilities via Django REST Framework viewsets:

- `Store`  
- `Product`  
- `PriceRecord`

Base API prefix:

```

/api/v1/

```

Read operations are publicly accessible.  
Write operations require authentication.

---

## Analytics Endpoints

The system includes custom analytical endpoints for price insights:

---

### 📊 Product Statistics

```

GET /api/v1/products/{id}/statistics/?from=YYYY-MM-DD&to=YYYY-MM-DD

````

Returns aggregated price data for a given product, optionally filtered by date range:

```json
{
  "min_price": "19.99",
  "max_price": "25.50",
  "avg_price": "22.74",
  "latest_price": "20.99",
  "currency": "USD",
  "num_records": 14
}
````

---

### 📈 Product Price History

```
GET /api/v1/products/{id}/price-history/
```

Returns a chronological list of all price records for a product:

```json
[
  {
    "store_id": 3,
    "store_name": "Shop A",
    "price": "19.99",
    "currency": "USD",
    "captured_at": "2024-01-10T08:00:00Z"
  },
  {
    "store_id": 4,
    "store_name": "Shop B",
    "price": "21.50",
    "currency": "USD",
    "captured_at": "2024-01-12T08:00:00Z"
  }
]
```

---

### 🏪 Store Comparison

```
GET /api/v1/products/{id}/store-comparison/
```

Displays the latest price per store for the selected product and highlights best and worst offers:

```json
{
  "stores": [
    {
      "store_id": 3,
      "store_name": "Shop A",
      "price": "19.99",
      "currency": "USD",
      "captured_at": "2024-01-12T08:00:00Z"
    },
    {
      "store_id": 4,
      "store_name": "Shop B",
      "price": "22.49",
      "currency": "USD",
      "captured_at": "2024-01-11T08:00:00Z"
    }
  ],
  "cheapest_store": {
    "store_id": 3,
    "store_name": "Shop A",
    "price": "19.99",
    "currency": "USD",
    "captured_at": "2024-01-12T08:00:00Z"
  },
  "most_expensive_store": {
    "store_id": 4,
    "store_name": "Shop B",
    "price": "22.49",
    "currency": "USD",
    "captured_at": "2024-01-11T08:00:00Z"
  }
}
```

---

## Tech Stack

* **Backend:** Python, Django
* **API:** Django REST Framework
* **Database:** PostgreSQL
* **API Documentation:** drf-spectacular (Swagger / ReDoc / OpenAPI)
* **Auth:** Session authentication & Basic authentication
* **Permissions:** `IsAuthenticatedOrReadOnly`
* **Containerization:** Docker & docker-compose

---

## API Documentation

Once the server is running:

* Swagger UI

  ```
  http://localhost:8000/api/docs/
  ```

* ReDoc

  ```
  http://localhost:8000/api/redoc/
  ```

* Raw OpenAPI schema

  ```
  http://localhost:8000/api/schema/
  ```

---

## Authentication & Permissions

* **Anonymous users**

  * Can perform all **GET (read)** requests including analytics endpoints

* **Authenticated users**

  * Required for **write operations**:

    * POST
    * PUT
    * PATCH
    * DELETE

You can create an admin account with:

```bash
python manage.py createsuperuser
```

and log in via:

```
http://localhost:8000/admin/
```

Authentication methods:

* Session Authentication (via browser admin login)
* Basic Authentication (via API clients such as Postman)

---

## Local Development Setup (without Docker)

### 1. Clone the repository

```bash
git clone <repository-url>
cd Market-Price-Monitoring-System
```

---

### 2. Create and activate a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
```

---

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

### 4. Configure environment variables

Create a `.env` file in the project root (use `.env.example` as template):

```env
DB_NAME=market_price_monitor
DB_USER=postgres
DB_PASSWORD=your_password_here
DB_HOST=localhost
DB_PORT=5432
```

---

### 5. Apply migrations and create admin user

```bash
cd backend
python manage.py migrate
python manage.py createsuperuser
```

---

### 6. Run development server

```bash
python manage.py runserver
```

Access the API at:

```
http://127.0.0.1:8000/api/v1/
```

---

## Docker Setup

This project includes a fully containerized development environment.

### 1. Copy environment template

```bash
cp .env.example .env
```

Adjust database credentials if needed.

---

### 2. Start services

```bash
docker compose up --build
```

This will:

* Start PostgreSQL (`db` container)
* Build and start Django backend (`web` container)
* Automatically apply all migrations

---

### 3. Access services

* API root

  ```
  http://localhost:8000/api/v1/
  ```

* Swagger UI

  ```
  http://localhost:8000/api/docs/
  ```

* ReDoc

  ```
  http://localhost:8000/api/redoc/
  ```

Stop containers:

```bash
docker compose down
```

---

## Example Workflow

1. Create stores and products (via API or Django admin).
2. Insert multiple `PriceRecord` entries for various stores.
3. Call analytics endpoints:

   * `/statistics/`
   * `/price-history/`
   * `/store-comparison/`

to analyse market pricing trends and store competitiveness.

---

## Possible Future Extensions

* External price import or scraping automation
* Currency conversion support
* User roles and organization-based access
* Automated testing & CI pipeline
* Frontend dashboard consuming this API

```
