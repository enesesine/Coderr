# 🛠️ Coderr Backend

This is the backend API for **Coderr**, a service marketplace platform connecting customers with business users.
Built with **Django** and **Django REST Framework**, it supports role-based registration, offer management, orders, reviews, and more.

---

## 🚀 Features

- ✅ Role-based user registration (`customer` / `business`)
- ✅ JWT token-based authentication (login/refresh)
- ✅ Profile management per user type
- ✅ Offer creation with tiered pricing (`basic`, `standard`, `premium`)
- ✅ Order creation and tracking
- ✅ Review system with rating/comments
- ✅ Statistics endpoint for public insights
- ✅ Admin panel support

---

## 🛠️ Tech Stack

- **Python** 3.12+
- **Django** 5.x
- **Django REST Framework**
- **SQLite** for local development
- **Simple JWT** for authentication
- **CORS** support for frontend access

---

## 📦 Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/your-username/coderr-backend.git
cd coderr-backend
```

### 2. Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate      # On Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Apply migrations

```bash
python manage.py migrate
```

### 5. Run development server

```bash
python manage.py runserver
```

---

## 🔐 Authentication (JWT)

### 1. Obtain token

`POST /api/token/`
```json
{
  "username": "your_username",
  "password": "your_password"
}
```
Response:
```json
{
  "access": "...",
  "refresh": "..."
}
```

### 2. Use token in requests
```
Authorization: Bearer <access_token>
```

---

## 📬 API Overview

### 🔐 Auth
- `POST /api/registration/` – Register new user
- `POST /api/login/` – Login and receive token

### 👤 Profiles
- `GET /api/profiles/business/` – List business users
- `GET /api/profiles/customer/` – List customer users
- `GET/PUT /api/profile/<id>/` – View or update your profile

### 📦 Offers
- `GET/POST /api/offers/` – List or create offers
- `GET/PATCH/DELETE /api/offers/<id>/` – Manage specific offer
- `GET /api/offerdetails/<id>/` – Retrieve detailed offer tier

### 📄 Orders
- `GET/POST /api/orders/` – List/create orders
- `PATCH /api/orders/<id>/` – Update order status
- `DELETE /api/orders/<id>/delete/` – Admin-only delete
- `GET /api/completed-order-count/<business_user_id>/` – Business order stats

### ⭐ Reviews
- `GET /api/reviews/` – List all reviews
- `POST /api/reviews/create/` – Create new review
- `PATCH /api/reviews/<id>/` – Update own review
- `DELETE /api/reviews/<id>/delete/` – Delete own review

### 📊 Base Info
- `GET /api/base-info/` – General stats (reviews, offers, business users...)

---

## 🧪 Testing

- Tested via Postman collections
- Verified permissions per role
- Status codes handled for 401/403/404/400 errors

---

## 📁 Folder Structure

```
coderr-backend/
│
├── auth_app/         # Custom user model + auth views
├── profiles_app/     # Profile view + filtering by role
├── offers_app/       # Offer creation and tiered pricing
├── orders_app/       # Order management
├── reviews_app/      # Ratings and feedback system
├── base_info_app/    # Stats endpoint
├── core/             # Django project settings
├── requirements.txt
└── README.md
```

---

## 👤 Author

**Enes**  
📧 eneslucker@gmail.com

---

## 📌 License

This project is built for educational purposes. Not intended for production use.
