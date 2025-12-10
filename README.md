# Market Price Monitoring System

This repository contains the backend for the Market Price Monitoring System built with Django and Django REST Framework.

## Getting started

1. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Provide PostgreSQL connection details via environment variables:
   ```bash
   export DB_NAME=market_price_db
   export DB_USER=postgres
   export DB_PASSWORD=postgres
   export DB_HOST=localhost
   export DB_PORT=5432
   ```
4. Apply migrations and start the development server:
   ```bash
   cd backend
   python manage.py migrate
   python manage.py runserver
   ```

API endpoints are exposed under `/api/v1/`.

## API documentation

Interactive API documentation is available once the development server is running:

- Raw OpenAPI schema: `http://localhost:8000/api/schema/`
- Swagger UI: `http://localhost:8000/api/docs/`
- ReDoc: `http://localhost:8000/api/redoc/`

All CRUD and analytics endpoints are included in the generated schema.

## Authentication

- Write operations (POST, PUT, PATCH, DELETE) require authentication.
- You can create an admin user with `python manage.py createsuperuser` and sign in via `/admin/` to use the browsable API with your session.
- Anonymous users can perform read-only requests (GET), including the analytics endpoints.

## Analytics endpoints

### Product statistics
`GET /api/v1/products/{id}/statistics/?from=YYYY-MM-DD&to=YYYY-MM-DD`

Returns aggregate data for a product's price records (optionally filtered by capture date):

```json
{
  "min_price": "19.99",
  "max_price": "25.50",
  "avg_price": "22.74",
  "latest_price": "20.99",
  "currency": "USD",
  "num_records": 14
}
```

### Product price history
`GET /api/v1/products/{id}/price-history/`

Returns a chronological list of all captured prices for the product:

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

### Store comparison
`GET /api/v1/products/{id}/store-comparison/`

Shows the latest captured price per store for the product and highlights the cheapest and most expensive stores:

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
