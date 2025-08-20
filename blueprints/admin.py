from datetime import datetime
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from models import db, Bus, Route, Schedule, Booking, Payment, User

admin_bp = Blueprint("admin", __name__, template_folder="../templates/admin")

def is_admin():
    return current_user.is_authenticated and getattr(current_user, 'role', None) == 'admin'

def admin_guard():
    if not is_admin():
        flash("Admin access only.", "danger")
        return redirect(url_for("auth.login"))


@admin_bp.route("/")
@login_required
def dashboard():
    if not is_admin():
        return admin_guard()
    counts = {
        "buses": Bus.query.count(),
        "routes": Route.query.count(),
        "schedules": Schedule.query.count(),
        "bookings": Booking.query.count(),
        "payments": Payment.query.count(),
    }
    latest = Booking.query.order_by(Booking.created_at.desc()).limit(10).all()
    return render_template("admin/dashboard.html", counts=counts, latest=latest)

@admin_bp.route("/buses", methods=["GET","POST"])
@login_required
def buses():
    if not is_admin():
        return admin_guard()
    if request.method == "POST":
        bus = Bus(
            bus_name=request.form.get("bus_name"),
            bus_type=request.form.get("bus_type") or "AC",
            total_seats=int(request.form.get("total_seats") or 40)
        )
        db.session.add(bus)
        db.session.commit()
        flash("Bus saved.", "success")
    buses = Bus.query.all()
    return render_template("admin/buses.html", buses=buses)

@admin_bp.route("/routes", methods=["GET","POST"])
@login_required
def routes():
    if not is_admin():
        return admin_guard()
    buses = Bus.query.all()
    if request.method == "POST":
        r = Route(
            source=request.form.get("source"),
            destination=request.form.get("destination"),
            bus_id=int(request.form.get("bus_id"))
        )
        db.session.add(r)
        db.session.commit()
        flash("Route saved.", "success")
    routes = Route.query.all()
    return render_template("admin/routes.html", buses=buses, routes=routes)

@admin_bp.route("/schedules", methods=["GET","POST"])
@login_required
def schedules():
    if not is_admin():
        return admin_guard()
    routes_list = Route.query.all()
    if request.method == "POST":
        route_id = int(request.form.get("route_id"))
        date_str = request.form.get("date")
        time_str = request.form.get("time")
        price = float(request.form.get("price"))
        s = Schedule(
            route_id=route_id,
            travel_date=datetime.strptime(date_str, "%Y-%m-%d").date(),
            depart_time=time_str,
            price=price
        )
        db.session.add(s)
        db.session.commit()
        flash("Schedule saved.", "success")
    schedules = Schedule.query.all()
    return render_template("admin/schedules.html", routes=routes_list, schedules=schedules)

@admin_bp.route("/reports")
@login_required
def reports():
    if not is_admin():
        return admin_guard()
    payments = Payment.query.order_by(Payment.created_at.desc()).all()
    total = sum(p.amount for p in payments)
    return render_template("admin/reports.html", payments=payments, total=total)
