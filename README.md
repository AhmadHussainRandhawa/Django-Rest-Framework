<div align="center">

# DRF E-Commerce API

**A production-patterned e-commerce backend built with Django REST Framework** — JWT auth, filtering & search, pagination, Redis caching, and auto-generated OpenAPI docs.

[![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=flat&logo=python&logoColor=white)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-5.2-092E20?style=flat&logo=django&logoColor=white)](https://www.djangoproject.com/)
[![DRF](https://img.shields.io/badge/DRF-3.16-A30000?style=flat&logo=django&logoColor=white)](https://www.django-rest-framework.org/)
[![Redis](https://img.shields.io/badge/Redis-Caching-DC382D?style=flat&logo=redis&logoColor=white)](https://redis.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

[Features](#-features) · [Tech Stack](#-tech-stack) · [API Reference](#-api-reference) · [Getting Started](#-getting-started) · [Authentication](#-authentication) · [Acknowledgments](#-acknowledgments)

</div>

---

## 📖 About

This repository is a hands-on implementation of a **RESTful e-commerce API** — covering products, orders, users, authentication, filtering, caching, and API documentation the way a real backend team would build it.

It was built while working through **[Django REST Framework Course for Beginners](https://www.youtube.com/watch?v=6AEvlNgRPNc&list=PL-2EBeDYMIbTLulc9FSoAXhbmXpLq2l5t)** by **[BugBytes](https://www.youtube.com/@bugbytes3923)** — widely regarded as one of the best free DRF courses available. Every commit in this repo's history tracks a concept as it was learned and applied, so the commit log itself doubles as a study trail through DRF's core patterns: generic views, viewsets & routers, serializers (including nested read/write serializers), permissions, filtering, pagination, JWT auth, caching, and schema generation.

> This is a learning project with production-grade patterns — not a toy CRUD demo. It's meant to demonstrate a working understanding of how real Django APIs are structured.

---

## ✨ Features

**Core API**
- Full CRUD for `Product`, with search, filtering, and ordering
- `Order` / `OrderItem` model with a many-to-many-through relationship, computed subtotals, and total price aggregation
- Custom `User` model (`AbstractUser`) with per-user order scoping
- Class-based generic views **and** a `ModelViewSet` + `DefaultRouter`, showing both approaches deliberately

**Auth & Permissions**
- JWT authentication via `djangorestframework-simplejwt` (access + refresh tokens)
- Endpoint-level permission logic — e.g. `AllowAny` for reads, `IsAdminUser` for writes, `IsAuthenticated` for order access
- Staff users see all orders; regular users only see their own (enforced at the queryset level, not just the view)

**Filtering, Search & Pagination**
- `django-filter` FilterSets for `Product` (name, price ranges) and `Order` (user, status, date)
- Custom `InStockFilterBackend` to exclude out-of-stock products
- DRF `SearchFilter` and `OrderingFilter`
- Configurable `PageNumberPagination` (custom page size params, max page size)

**Performance**
- Redis-backed response caching on the product list endpoint
- Cache invalidation via Django **signals** (`post_save` / `post_delete`) — cache is cleared automatically when product data changes, not left stale
- `django-silk` integrated for request/query profiling during development

**Documentation & Tooling**
- Auto-generated OpenAPI schema via `drf-spectacular`, with Swagger UI and Redoc
- ER diagram generation via `django-extensions` (`models.dot`)
- `populate_db` management command to seed realistic sample data in one step
- `.http` request collection (`api.http`) for manual endpoint testing in-editor

---

## 🛠 Tech Stack

| Layer | Technology |
|---|---|
| Language | Python 3.12 |
| Framework | Django 5.2 |
| API Layer | Django REST Framework 3.16 |
| Auth | djangorestframework-simplejwt (JWT) |
| Filtering | django-filter |
| Caching | Redis (`django-redis`) |
| API Docs | drf-spectacular (OpenAPI 3, Swagger UI, Redoc) |
| Profiling | django-silk |
| Config | django-environ (`.env`-based settings) |
| Database | SQLite (dev) — swappable via `DATABASE_URL` |

---

## 🧩 Architecture

```
drf-ecommerce-api/
├── api/                      # Core application
│   ├── models.py             # User, Product, Order, OrderItem
│   ├── serializers.py        # Read/write serializers, nested & computed fields
│   ├── views.py              # Generic views + ModelViewSet
│   ├── filters.py            # FilterSets + custom filter backend
│   ├── admin.py              # Admin panel config (inline OrderItems)
│   ├── signals.py            # Cache invalidation on Product save/delete
│   └── management/commands/  # populate_db — seeds sample data
├── drf_course/               # Project config
│   ├── settings.py           # Env-based settings, DRF config, JWT, caching
│   └── urls.py               # Routes: API, JWT, schema, silk
├── api.http                  # Manual request collection
├── models.dot                # ER diagram source (django-extensions)
└── requirements.txt
```

**Data model at a glance:**

```
User ──< Order >──< OrderItem >── Product
```

An `Order` belongs to a `User` and holds many `Product`s through `OrderItem`, which tracks quantity and derives a per-line subtotal. `Order.total_price` is computed server-side from its items — never trusted from client input.

---

## 📡 API Reference

Base URL (local): `http://127.0.0.1:8000/`

| Method | Endpoint | Description | Auth |
|---|---|---|---|
| `GET` | `/products/` | List products (paginated, filterable, searchable) | Public |
| `POST` | `/products/` | Create a product | Admin |
| `GET` | `/products/<id>` | Retrieve a single product | Public |
| `PUT` / `PATCH` | `/products/<id>` | Update a product | Admin |
| `DELETE` | `/products/<id>` | Delete a product | Admin |
| `GET` | `/products/info` | Aggregate stats — count, max price | Public |
| `GET` | `/orders/` | List orders (own orders, or all if staff) | Authenticated |
| `POST` | `/orders/` | Create an order with line items | Authenticated |
| `PUT` / `PATCH` | `/orders/<order_id>/` | Update an order and its items | Authenticated |
| `DELETE` | `/orders/<order_id>/` | Delete an order | Authenticated |
| `GET` | `/users/` | List users | Authenticated |
| `POST` | `/api/token/` | Obtain JWT access + refresh token pair | Public |
| `POST` | `/api/token/refresh/` | Refresh an access token | Public |
| `GET` | `/api/schema/swagger-ui/` | Interactive Swagger UI | Public |
| `GET` | `/api/schema/redoc/` | Redoc API documentation | Public |

**Filtering examples:**

```
GET /products/?price__gt=50&price__lt=200
GET /products/?search=camera
GET /products/?ordering=-price
GET /orders/?status=Pending&created_at__gt=2026-01-01
```

---

## 🚀 Getting Started

### Prerequisites
- Python 3.12+
- Redis (running locally, default `redis://127.0.0.1:6379`)

### Installation

```bash
# 1. Clone the repository
git clone git@github.com:AhmadHussainRandhawa/drf-ecommerce-api.git
cd drf-ecommerce-api

# 2. Create and activate a virtual environment
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment variables
cp .env.example .env          # then edit .env — see table below

# 5. Apply migrations
python manage.py migrate

# 6. Seed sample data (creates an admin user + demo products/orders)
python manage.py populate_db

# 7. Run the development server
python manage.py runserver
```

The API is now live at `http://127.0.0.1:8000/`, with interactive docs at `/api/schema/swagger-ui/`.

### Environment Variables

Create a `.env` file in the project root:

| Variable | Description | Example |
|---|---|---|
| `SECRET_KEY` | Django secret key | `django-insecure-...` |
| `DEBUG` | Debug mode toggle | `True` |
| `ALLOWED_HOSTS` | Comma-separated allowed hosts | `localhost,127.0.0.1` |
| `DATABASE_URL` | Database connection string | `sqlite:///db.sqlite3` |

---

## 🔐 Authentication

This API uses **JWT** (JSON Web Tokens). Obtain a token pair, then pass the access token as a `Bearer` token on protected routes.

```http
POST /api/token/
Content-Type: application/json

{
    "username": "admin",
    "password": "test"
}
```

Response:

```json
{
    "access": "<access-token>",
    "refresh": "<refresh-token>"
}
```

Then, on protected endpoints:

```http
GET /orders/
Authorization: Bearer <access-token>
```

Access tokens are short-lived (5 minutes); use `/api/token/refresh/` with the refresh token to obtain a new one.

---

## 🧪 Testing

```bash
python manage.py test
```

Tests cover order-scoping behavior — confirming that authenticated users only ever see their own orders, and that unauthenticated requests are correctly rejected.

---

## 🗺 Roadmap

- [ ] Add DRF throttling for public endpoints
- [ ] Add product image upload with validation
- [ ] Dockerize the project (app + Postgres + Redis)
- [ ] Add CI (GitHub Actions) running tests on every push
- [ ] Expand test coverage to products and filtering

---

## 🙌 Acknowledgments

This project was built by following **[Django REST Framework Course for Beginners](https://www.youtube.com/watch?v=6AEvlNgRPNc&list=PL-2EBeDYMIbTLulc9FSoAXhbmXpLq2l5t)**, a free playlist by **[BugBytes](https://www.youtube.com/@bugbytes3923)** — highly recommended for anyone learning DRF from the ground up. All implementation, structuring, and commit history in this repo reflect independent, hands-on practice while following the course.

---

## 📄 License

This project is licensed under the **MIT License** — see [LICENSE](LICENSE) for details.

---

<div align="center">

Built by **[Ahmad Hussain](https://github.com/AhmadHussainRandhawa)**

</div>
