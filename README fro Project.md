# Bus Ticketing & Payment System (Flask + MySQL + JWT)

Simple, easy-to-run demo for bus reservations, fake payments, and admin management.

## Features
- Register/Login with JWT cookies
- Search buses by route/date/bus type
- Seat selection with booked seats disabled
- Booking + PNR generation
- Fake payment (always success)
- Booking history + cancellation
- Admin: buses, routes, schedules, payment reports

## Tech
- Flask, SQLAlchemy
- MySQL (PyMySQL driver) or SQLite fallback
- JWT via cookies (Flask-JWT-Extended)
- Bootstrap for UI

## Quickstart

1. **Clone & Install**
```bash
python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

2. **Create DB**
- Create a MySQL database named `busdb` (or change the name in `.env`).
```sql
CREATE DATABASE busdb CHARACTER SET utf8mb4;
```
- Copy `.env.example` to `.env` and update credentials.

3. **Run App**
```bash
export FLASK_APP=app.py
flask --app app.py run
# or first-time table creation:
flask --app app.py init-db
```

4. **Create Admin User** (via /register then update role in DB or quick SQL)
```sql
UPDATE users SET role='admin' WHERE email='your-admin-email@example.com';
```

5. **Add data**
- Login as admin → Add buses/routes/schedules
- Logout → Login as normal user → Search, book, pay (fake), view/cancel

## Deploy (AWS EC2 sketch)
- Install Python 3.x, MySQL client, and `pip install -r requirements.txt`
- Set environment variables (`SECRET_KEY`, `JWT_SECRET_KEY`, `DATABASE_URL`)
- Run with `gunicorn -w 2 -b 0.0.0.0:8000 app:app` behind Nginx

## Notes
- JWT is stored in cookies (simpler for server-rendered pages).
- **Fake payments only**, for demo purpose.
- For production: enable HTTPS, set `JWT_COOKIE_SECURE=True`, add CSRF, and use Alembic migrations.
