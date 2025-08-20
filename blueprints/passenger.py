from datetime import datetime
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from models import db, Bus, Route, Schedule, Booking, Payment, User, City , Seat
from helpers import seat_map, generate_pnr

passenger_bp = Blueprint("passenger", __name__, template_folder="../templates/passenger")

@passenger_bp.route("/search", methods=["GET", "POST"])
@login_required
def search():
    # ➡️ Query City model for city names
    cities = City.query.order_by(City.name).all()

    results = []
    if request.method == "POST":
        src_id = request.form.get("source")
        dest_id = request.form.get("destination")
        date = request.form.get("date")
        bus_type = request.form.get("bus_type")

        # ➡️ Filter by foreign keys (source_id and destination_id)
        q = Schedule.query.join(Route).join(Bus).filter(
            Route.source_id == src_id,
            Route.destination_id == dest_id
        )

        if date:
            try:
                travel_date = datetime.strptime(date, "%Y-%m-%d").date()
                q = q.filter(Schedule.travel_date == travel_date)
            except ValueError:
                flash("Invalid date format", "danger")
                return redirect(url_for("passenger.search"))

        if bus_type and bus_type != "Any":
            q = q.filter(Bus.bus_type == bus_type)

        results = q.all()

    return render_template(
        "passenger/search.html",
        cities=cities,  # ➡️ Pass the City objects to the template
        results=results
    )

@passenger_bp.route("/schedule/<int:schedule_id>/seats", methods=["GET", "POST"])
@login_required
def seats(schedule_id):
    sched = Schedule.query.get_or_404(schedule_id)
    bus = sched.route.bus
    booked = set(b.seat_number for b in Booking.query.filter_by(schedule_id=schedule_id, status="booked").all())
    seats = seat_map(bus.total_seats)

    if request.method == "POST":
        seat_number = request.form.get("seat")
        if seat_number in booked:
            flash("Seat already booked, choose another.", "danger")
            return redirect(url_for("passenger.seats", schedule_id=schedule_id))
        # ➡️ Find the seat_id based on bus_id and seat_number
        seat = Seat.query.filter_by(bus_id=bus.id, seat_number=seat_number).first()
        if not seat:
            flash("Invalid seat selected.", "danger")
            return redirect(url_for("passenger.seats", schedule_id=schedule_id))


        booking = Booking(user_id=current_user.id,
                          schedule_id=schedule_id,
                          seat_id=seat.id,
                          seat_number=seat_number,
                          status="initiated")
        db.session.add(booking)
        db.session.commit()
        return redirect(url_for("passenger.payment", booking_id=booking.id))

    return render_template("passenger/seat_selection.html",
                           sched=sched, bus=bus, seats=seats, booked=booked)

@passenger_bp.route("/payment/<int:booking_id>", methods=["GET", "POST"])
@login_required
def payment(booking_id):
    booking = Booking.query.get_or_404(booking_id)
    sched = booking.schedule
    if request.method == "POST":
        # Fake payment always success
        amount = sched.price
        pay = Payment(booking_id=booking.id, amount=amount, status="success")
        booking.status = "booked"
        if not booking.pnr:
            booking.pnr = generate_pnr()
        db.session.add(pay)
        db.session.commit()
        return redirect(url_for("passenger.confirmation", booking_id=booking.id))
    return render_template("passenger/payment.html", booking=booking, sched=sched)

@passenger_bp.route("/confirmation/<int:booking_id>")
@login_required
def confirmation(booking_id):
    booking = Booking.query.get_or_404(booking_id)
    return render_template("passenger/confirmation.html", booking=booking)

@passenger_bp.route("/bookings")
@login_required
def my_bookings():
    bookings = Booking.query.filter_by(user_id=current_user.id).order_by(Booking.created_at.desc()).all()
    return render_template("passenger/history.html", bookings=bookings)

@passenger_bp.route("/cancel/<int:booking_id>", methods=["POST"])
@login_required
def cancel(booking_id):
    booking = Booking.query.get_or_404(booking_id)
    if booking.user_id != current_user.id:
        flash("Not allowed.", "danger")
        return redirect(url_for("passenger.my_bookings"))
    if booking.status != "booked":
        flash("Only booked tickets can be cancelled.", "warning")
        return redirect(url_for("passenger.my_bookings"))

    booking.status = "cancelled"
    db.session.commit()
    flash("Booking cancelled.", "success")
    return redirect(url_for("passenger.my_bookings"))