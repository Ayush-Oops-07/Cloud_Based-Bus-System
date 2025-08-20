from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()

# ----------------- User -----------------
class User(db.Model, UserMixin):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    phone = db.Column(db.String(20), nullable=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), default="passenger")

    bookings = db.relationship("Booking", back_populates="user", lazy=True)

# ----------------- City -----------------
class City(db.Model):
    __tablename__ = "cities"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)

# ----------------- Bus -----------------
class Bus(db.Model):
    __tablename__ = "bus"
    id = db.Column(db.Integer, primary_key=True)
    bus_name = db.Column(db.String(100), nullable=False)
    bus_type = db.Column(db.String(120), nullable=False)
    total_seats = db.Column(db.Integer, nullable=False)
    bus_number = db.Column(db.String(50), unique=True, nullable=False)

    routes = db.relationship("Route", back_populates="bus", lazy=True)
    seats = db.relationship("Seat", back_populates="bus", lazy=True)

# ----------------- Route -----------------
class Route(db.Model):
    __tablename__ = "routes"
    id = db.Column(db.Integer, primary_key=True)
    source_id = db.Column(db.Integer, db.ForeignKey("cities.id"), nullable=False)
    destination_id = db.Column(db.Integer, db.ForeignKey("cities.id"), nullable=False)
    bus_id = db.Column(db.Integer, db.ForeignKey("bus.id"), nullable=False)

    source = db.relationship("City", foreign_keys=[source_id])
    destination = db.relationship("City", foreign_keys=[destination_id])
    bus = db.relationship("Bus", back_populates="routes")

    schedules = db.relationship("Schedule", back_populates="route", lazy=True)

# ----------------- Schedule -----------------
class Schedule(db.Model):
    __tablename__ = "schedule"
    id = db.Column(db.Integer, primary_key=True)
    route_id = db.Column(db.Integer, db.ForeignKey("routes.id"), nullable=False)
    travel_date = db.Column(db.Date, nullable=False)
    departure_time = db.Column(db.DateTime, nullable=False)
    arrival_time = db.Column(db.DateTime, nullable=False)
    price = db.Column(db.Float, nullable=False)

    route = db.relationship("Route", back_populates="schedules")
    bookings = db.relationship("Booking", back_populates="schedule", lazy=True)

# ----------------- Seat -----------------
class Seat(db.Model):
    __tablename__ = "seat"
    id = db.Column(db.Integer, primary_key=True)
    bus_id = db.Column(db.Integer, db.ForeignKey("bus.id"), nullable=False)
    seat_number = db.Column(db.String(10), nullable=False)
    is_booked = db.Column(db.Boolean, default=False)

    bus = db.relationship("Bus", back_populates="seats")
    bookings = db.relationship("Booking", back_populates="seat", uselist=False)

# ----------------- Booking -----------------
class Booking(db.Model):
    __tablename__ = "bookings"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    seat_id = db.Column(db.Integer, db.ForeignKey("seat.id"), nullable=False)
    schedule_id = db.Column(db.Integer, db.ForeignKey("schedule.id"), nullable=False)
    seat_number = db.Column(db.String(10), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    pnr = db.Column(db.String(20), unique=True, nullable=True)
    status = db.Column(db.String(20), default="initiated", nullable=False)

    user = db.relationship("User", back_populates="bookings")
    seat = db.relationship("Seat", back_populates="bookings")
    schedule = db.relationship("Schedule", back_populates="bookings")
    payment = db.relationship("Payment", back_populates="booking", uselist=False)

# ----------------- Payment -----------------
class Payment(db.Model):
    __tablename__ = "payments"
    id = db.Column(db.Integer, primary_key=True)
    booking_id = db.Column(db.Integer, db.ForeignKey("bookings.id"), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), default="pending")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    booking = db.relationship("Booking", back_populates="payment")