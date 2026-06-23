# Flask JWT RBAC API

A RESTful API built with Python Flask featuring JWT-based authentication and role-based access control (RBAC). Includes endpoints for user authentication, product management, and user management, each protected according to user roles.

## Features

- **JWT Authentication** — secure login system issuing signed access tokens
- **Role-Based Access Control** — three permission tiers: `user`, `moderator`, `admin`
- **Request Validation** — proper input validation with clear error messages
- **RESTful Design** — clean resource-based routes following REST conventions
- **Proper HTTP Status Codes** — 200, 201, 401, 403, 404, 409, 422 used correctly throughout
- **CORS Enabled** — allows requests from browser-based clients

## Tech Stack

- Python 3
- Flask
- Flask-JWT-Extended
- Flask-CORS

## Project Structure

```
flask-api/
├── run.py                  # Application entry point
├── requirements.txt        # Python dependencies
├── test.html                # Simple browser-based API tester
└── app/
    ├── __init__.py          # App factory, JWT & CORS setup
    ├── models.py            # In-memory data store + RBAC decorator
    └── routes/
        ├── __init__.py
        ├── auth.py           # Login, register, profile endpoints
        ├── products.py       # Product CRUD endpoints
        └── users.py          # User management endpoints
```

## Roles & Permissions

| Role | Products (view) | Products (create/edit) | Products (delete) | Users (view) | Users (manage) |
|------|:---:|:---:|:---:|:---:|:---:|
| user | ✅ | ❌ | ❌ | ❌ | ❌ |
| moderator | ✅ | ✅ | ❌ | ✅ | ❌ |
| admin | ✅ | ✅ | ✅ | ✅ | ✅ |

## Getting Started

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the server

```bash
python run.py
```

The API will be available at `http://localhost:5000`.

### 3. Test it

Open `test.html` in your browser, or use a tool like Postman.

**Test accounts:**

| Email | Password | Role |
|---|---|---|
| admin@example.com | admin123 | admin |
| mod@example.com | mod123 | moderator |
| user@example.com | user123 | user |

## API Endpoints

### Auth
| Method | Endpoint | Auth Required | Description |
|---|---|:---:|---|
| POST | `/api/auth/login` | No | Log in and receive a JWT token |
| POST | `/api/auth/register` | No | Register a new user (default role: user) |
| GET | `/api/auth/me` | Yes | Get current user's profile |

### Products
| Method | Endpoint | Min. Role | Description |
|---|---|---|---|
| GET | `/api/products/` | user | List all products |
| GET | `/api/products/<id>` | user | Get a single product |
| POST | `/api/products/` | moderator | Create a new product |
| PUT | `/api/products/<id>` | moderator | Update a product |
| DELETE | `/api/products/<id>` | admin | Delete a product |

### Users
| Method | Endpoint | Min. Role | Description |
|---|---|---|---|
| GET | `/api/users/` | moderator | List all users |
| GET | `/api/users/<id>` | moderator | Get a single user |
| PATCH | `/api/users/<id>/role` | admin | Update a user's role |
| DELETE | `/api/users/<id>` | admin | Delete a user |

## Example Usage

**Login:**
```bash
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "admin@example.com", "password": "admin123"}'
```

**Authenticated request:**
```bash
curl http://localhost:5000/api/products/ \
  -H "Authorization: Bearer <your_access_token>"
```

## Notes for Production

This project uses an in-memory dictionary as a database for demonstration purposes. For a production deployment, consider:

- Replacing the in-memory store with PostgreSQL/MySQL via SQLAlchemy
- Hashing passwords with `bcrypt` instead of storing them in plain text
- Loading the JWT secret key from an environment variable
- Disabling debug mode and serving via a production WSGI server (e.g. Gunicorn)
- Adding rate limiting (e.g. `flask-limiter`)

## License

This project is open source and available for learning purposes.
