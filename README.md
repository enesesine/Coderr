# Coderr Backend

This is the backend implementation for the **Coderr** platform, developed using **Django** and **Django REST Framework**.  
It provides a fully functional RESTful API for a freelance marketplace with user roles, offers, orders, reviews, and more.

---

## 🚀 Features

### 🔐 Authentication & Users
- **Registration & Login** (via Token or JWT)
- **Custom User Model** with profile fields
- Role system: `customer` vs `business`
- Separate API endpoints to list `business` and `customer` profiles

### 📄 Profile Management
- View and update your own profile
- Search and filter other profiles based on roles

### 🛍️ Offers
- Business users can:
  - Create offers with multiple offer details (basic / standard / premium)
  - Edit or delete their own offers
- All users can:
  - View offers (with pagination, search, filters)

### 📦 Orders
- Customers can:
  - Place orders based on offer details
- Business users can:
  - Update order status (e.g., mark as completed)
- Admins can:
  - Delete orders
- Additional endpoints:
  - Count active and completed orders for a business user

### 🌟 Reviews
- Customers can:
  - Submit one review per business
  - Update or delete their own reviews
- All users can:
  - View reviews with filters and ordering

### 📊 Base Info
- Public endpoint to fetch general stats about the platform:
  - Total reviews
  - Average rating
  - Number of business profiles
  - Number of offers

---

## 📦 Requirements

Install dependencies with:

```bash
pip install -r requirements.txt
