# Seraphany Archive

A modern full-stack e-commerce platform for archival designer clothing, built with FastAPI and React.

![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)
![React](https://img.shields.io/badge/React-18+-61DAFB.svg)
![TypeScript](https://img.shields.io/badge/TypeScript-5+-3178C6.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)



https://github.com/user-attachments/assets/c3bd0f1f-5bbf-4a27-b25a-306245682745




## ✨ Features

### Customer Features
- 🛍️ **Product Browsing** - Browse products with category filtering and search
- 🖼️ **Image Galleries** - Multiple product images with hover preview
- 🛒 **Shopping Cart** - Persistent cart (survives page refresh)
- 📦 **Order Management** - Place orders, view history, cancel pending orders
- 🔐 **User Authentication** - Secure JWT-based authentication

### Admin Features
- 📝 **Product Management** - Create, edit, delete products
- 🖼️ **Image Upload** - Drag-and-drop multi-image upload
- 👥 **User Management** - View users, manage admin privileges
- 📊 **Order Overview** - View and manage customer orders

### Technical Features
- 🏗️ **Modular Architecture** - Clean separation of concerns with routers
- ✅ **Type Safety** - Full TypeScript frontend, Pydantic validation backend
- 🧪 **Test Coverage** - 39 passing tests for API endpoints
- 🔔 **Toast Notifications** - Professional user feedback system
- 📱 **Responsive Design** - Works on desktop and mobile

## 🛠️ Tech Stack

### Backend
- **Framework:** FastAPI (Python 3.11+)
- **Database:** PostgreSQL with SQLAlchemy ORM
- **Authentication:** JWT tokens with passlib
- **Migrations:** Alembic
- **Validation:** Pydantic v2

### Frontend
- **Framework:** React 18 with TypeScript
- **Routing:** React Router v6
- **State Management:** React Context + React Query
- **Build Tool:** Vite
- **Styling:** CSS Modules

## 📁 Project Structure

```
seraphany_archive/
├── backend/
│   ├── app/
│   │   ├── routers/          # API route handlers
│   │   │   ├── auth.py       # Authentication endpoints
│   │   │   ├── products.py   # Product CRUD
│   │   │   ├── orders.py     # Order management
│   │   │   ├── uploads.py    # Image uploads
│   │   │   └── users.py      # Admin user management
│   │   ├── main.py           # FastAPI app initialization
│   │   ├── schemas.py        # Pydantic models
│   │   ├── models.py         # SQLAlchemy models
│   │   ├── database.py       # Database service
│   │   ├── auth.py           # JWT utilities
│   │   ├── config.py         # App configuration
│   │   └── storage.py        # File upload handling
│   ├── alembic/              # Database migrations
│   ├── tests/                # API tests
│   └── uploads/              # Uploaded images
│
├── frontend/
│   ├── src/
│   │   ├── components/       # Reusable UI components
│   │   ├── pages/            # Page components
│   │   ├── contexts/         # React contexts (Auth, Cart, Toast)
│   │   ├── services/         # API client
│   │   ├── hooks/            # Custom hooks
│   │   ├── types/            # TypeScript definitions
│   │   ├── styles/           # CSS files
│   │   └── config/           # Frontend configuration
│   └── public/               # Static assets
│
└── TODO.md                   # Project roadmap & progress
```

## 🚀 Getting Started

### Prerequisites
- Python 3.11+
- Node.js 18+
- PostgreSQL 14+ (or use SQLite for development)
- Poetry (Python package manager)

### Backend Setup

```bash
# Navigate to backend directory
cd backend

# Install dependencies
poetry install

# Copy environment file and configure
cp .example_env .env
# Edit .env with your database credentials

# Run database migrations
poetry run alembic upgrade head

# Start development server
poetry run uvicorn app.main:app --reload --port 8000
```

### Frontend Setup

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

The frontend will be available at `http://localhost:5173` and the API at `http://localhost:8000`.

## ⚙️ Environment Variables

### Backend (`.env`)

```env
# Database
DATABASE_URL="postgresql://user:password@localhost:5432/vintage_store"

# Security
SECRET_KEY="your-secret-key-change-in-production"

# CORS (comma-separated or JSON array)
CORS_ORIGINS="http://localhost:5173,http://127.0.0.1:5173"

# Debug mode
DEBUG=True
```

### Frontend (`.env`)

```env
VITE_API_BASE_URL=http://localhost:8000
```

## 📚 API Documentation

Once the backend is running, visit:
- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

### Key Endpoints

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| `POST` | `/auth/register` | Register new user | ❌ |
| `POST` | `/auth/login` | Login, get JWT token | ❌ |
| `GET` | `/auth/me` | Get current user | ✅ |
| `GET` | `/products` | List products (with filters) | ❌ |
| `GET` | `/products/{id}` | Get product details | ❌ |
| `POST` | `/products` | Create product | 🔒 Admin |
| `PUT` | `/products/{id}` | Update product | 🔒 Admin |
| `DELETE` | `/products/{id}` | Soft delete product | 🔒 Admin |
| `POST` | `/orders` | Create order | ✅ |
| `GET` | `/orders` | Get user's orders | ✅ |
| `POST` | `/orders/{id}/cancel` | Cancel order | ✅ |
| `POST` | `/upload/product-images` | Upload images | 🔒 Admin |

## 🧪 Testing

```bash
# Run backend tests
cd backend
poetry run pytest -v

# Run with coverage
poetry run pytest --cov=app --cov-report=html
```

Current test status: **39 tests passing** ✅

## 🚢 Deployment

### Backend (Railway/Render)

1. Set environment variables in your hosting platform
2. Ensure `DATABASE_URL` points to your production PostgreSQL
3. Set a secure `SECRET_KEY`
4. Configure `CORS_ORIGINS` for your frontend domain

### Frontend (Netlify/Vercel)

1. Set `VITE_API_BASE_URL` to your production API URL
2. Build with `npm run build`
3. Deploy the `dist` folder

See `TODO.md` for detailed deployment checklist.

## 🏗️ Architecture Decisions

- **Soft Deletes:** Products are marked unavailable instead of deleted (preserves order history)
- **JWT Authentication:** Stateless auth with token refresh support
- **Local Image Storage:** With architecture ready for cloud migration (S3/R2)
- **Cart Persistence:** Uses localStorage for cross-session cart retention
- **Modular Routers:** Each domain (auth, products, orders) has its own router file

## 📝 Development Notes

### Creating an Admin User

```bash
cd backend
poetry run python create_admin.py
```

### Seeding Sample Products

```bash
cd backend
poetry run python seed_products.py
```

### Database Migrations

```bash
# Create new migration
poetry run alembic revision --autogenerate -m "description"

# Apply migrations
poetry run alembic upgrade head

# Rollback
poetry run alembic downgrade -1
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---
