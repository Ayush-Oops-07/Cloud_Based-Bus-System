from flask import Flask
from datetime import date, timedelta, datetime
from werkzeug.security import generate_password_hash
from models import db, User, Bus, Route, Schedule, Seat, City

# Create a minimal Flask app context
app = Flask(__name__)
# Configure the database URI for the app
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:4753@localhost/busdb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

with app.app_context():
    # Drop and re-create fresh tables
    db.drop_all()
    db.create_all()

    # ---------------- Cities ----------------
    city_names = [
        "Delhi", "Mumbai", "Chennai", "Kolkata", "Bengaluru",
        "Hyderabad", "Pune", "Jaipur", "Agra", "Lucknow",
        "Bhopal", "Indore", "Ahmedabad", "Surat", "Patna"
    ]
    cities = [City(name=name) for name in city_names]
    db.session.add_all(cities)
    db.session.commit()
    print("✅ Cities inserted")

    city_map = {c.name: c.id for c in City.query.all()}

    # ---------------- Buses ----------------
    buses = [
        Bus(bus_name="Volvo Express", bus_type="AC", total_seats=40, bus_number="DL-01-A-1234"),
        Bus(bus_name="Shatabdi Travels", bus_type="Non-AC", total_seats=45, bus_number="MH-02-B-5678"),
        Bus(bus_name="Night Rider", bus_type="Sleeper", total_seats=30, bus_number="TN-03-C-9012"),
        Bus(bus_name="Rajdhani Deluxe", bus_type="AC", total_seats=50, bus_number="WB-04-D-3456"),
        Bus(bus_name="CityLink", bus_type="Non-AC", total_seats=35, bus_number="KA-05-E-7890"),
    ]
    db.session.add_all(buses)
    db.session.commit()
    print("✅ Buses inserted")

    # ---------------- Routes ----------------
    routes = [
        Route(source_id=city_map["Delhi"], destination_id=city_map["Agra"], bus_id=buses[0].id),
        Route(source_id=city_map["Delhi"], destination_id=city_map["Jaipur"], bus_id=buses[1].id),
        Route(source_id=city_map["Mumbai"], destination_id=city_map["Pune"], bus_id=buses[2].id),
        Route(source_id=city_map["Chennai"], destination_id=city_map["Bengaluru"], bus_id=buses[3].id),
        Route(source_id=city_map["Hyderabad"], destination_id=city_map["Bhopal"], bus_id=buses[4].id),
    ]
    db.session.add_all(routes)
    db.session.commit()
    print("✅ Routes inserted")

    # ---------------- Schedules ----------------
    schedules = []
    for r in routes:
        for i in range(1, 6):
            travel_date = date.today() + timedelta(days=i)
            # You need to define dummy arrival and departure times
            # A datetime object is required for the columns
            departure_time = datetime.combine(travel_date, datetime.min.time())
            arrival_time = departure_time + timedelta(hours=5)
            s = Schedule(
                route_id=r.id,
                travel_date=travel_date,
                departure_time=departure_time,
                arrival_time=arrival_time,
                price=500.00
            )
            schedules.append(s)
    db.session.add_all(schedules)
    db.session.commit()
    print("✅ Schedules inserted")

    # ---------------- Seats ----------------
    for s in Schedule.query.all():
        bus = Bus.query.get(s.route.bus_id)
        if bus:
            for i in range(1, bus.total_seats + 1):
                seat = Seat(bus_id=bus.id, seat_number=str(i))
                db.session.add(seat)
    db.session.commit()
    print("✅ Seats inserted")

    # ---------------- Admin User ----------------
    admin = User(
        username="admin",
        email="admin@bus.com",
        password_hash=generate_password_hash("admin123"),
        role="admin"
    )
    db.session.add(admin)
    db.session.commit()
    print("✅ Admin user created: admin@bus.com / admin123")

    print("🎉 Database seeded successfully!")