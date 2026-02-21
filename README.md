# 🏪 POS Retail Shop — Django + MySQL

## Project Structure
```
pos_project/
├── manage.py
├── requirements.txt
├── .env.example
├── pos_project/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── shop/
    ├── models.py          # Product, Sale, SaleItem
    ├── views.py           # POS, Dashboard, API views
    ├── urls.py
    ├── admin.py
    ├── templates/shop/
    │   ├── base.html
    │   ├── pos.html       # Main POS Interface
    │   ├── dashboard.html # Dashboard + Charts
    │   └── products.html  # Product Management
    └── static/shop/
        ├── css/style.css
        └── js/pos.js
```

## Setup Instructions

### 1. Install Requirements
```bash
pip install -r requirements.txt
```

### 2. Configure MySQL
Create `.env` file from `.env.example` and fill in your MySQL credentials.

### 3. Run Migrations
```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py seed_products   # Load sample products
```

### 4. Run Server
```bash
python manage.py runserver
```

### 5. Access
- POS Interface: http://localhost:8000/
- Dashboard: http://localhost:8000/dashboard/
- Admin: http://localhost:8000/admin/

## Features
- ✅ POS Interface (MMK / THB currency)
- ✅ Product Management (Add/Edit/Delete)
- ✅ Sales Overview & History
- ✅ Stock Alert (Low stock notifications)
- ✅ Daily/Monthly Report Charts
- ✅ Receipt Print
- ✅ MySQL Database
