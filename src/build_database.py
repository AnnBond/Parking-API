import os
from config import db
from models import Driver, Vehicle
from datetime import datetime

# Data to initialize database with
DRIVER = [
    {
        "first_name": "Admin",
        "last_name": "Admin",
    },
    {
        "first_name": "Mark",
        "last_name": "Lewis",
    },
    {
        "first_name": "Joel",
        "last_name": "Valentine",
    },
    {
        "first_name": "Ioan",
        "last_name": "Oberon",
    },
    {
        "first_name": "Layton",
        "last_name": "Henry",
    },
]

VEHICLE = [
    {
        "driver_id": 3,
        "make": "Vehicle 1",
        "model": "Ford Galaxy",
        "plate_number": "AA 1111 BB",
        "created_at": "2021-12-10 23:08:54",
        "updated_at": "2021-12-10 23:08:54",
    },
    {
        "driver_id": 2,
        "make": "Vehicle 2",
        "model": "Nissan Altima",
        "plate_number": "AA 2222 BB",
        "created_at": "2021-12-10 23:09:54",
        "updated_at": "2021-12-10 23:09:54",
    },
    {
        "driver_id": 1,
        "make": "Vehicle 4",
        "model": "Cadillac CTS",
        "plate_number": "AA 3333 BB",
        "created_at": "2021-12-10 23:10:54",
        "updated_at": "2021-12-10 23:10:54",
    },
    {
        "driver_id": 1,
        "make": "Vehicle 4",
        "model": "Mazda CX-5",
        "plate_number": "AA 4444 BB",
        "created_at": "2021-12-10 23:11:54",
        "updated_at": "2021-12-10 23:11:54",
    },
]

# Delete database file if it exists currently
if os.path.exists("../parking.db"):
    os.remove("../parking.db")

# Create the database
db.create_all()

# iterate over the DRIVER structure and populate the database
for driver in DRIVER:
    data = Driver(last_name=driver.get("last_name"),
                  first_name=driver.get("first_name"),
                  created_at=datetime.now(),
                  updated_at=datetime.now())
    db.session.add(data)

# iterate over the VEHICLE structure and populate the database
for vehicle in VEHICLE:
    driver_id, make, model, plate_number, created_at, updated_at = vehicle
    data = Vehicle(
        driver_id=vehicle.get("driver_id"),
        make=vehicle.get("make"),
        model=vehicle.get("model"),
        plate_number=vehicle.get("plate_number"),
        created_at=datetime.strptime(vehicle.get("created_at"), "%Y-%m-%d %H:%M:%S"),
        updated_at=datetime.strptime(vehicle.get("updated_at"), "%Y-%m-%d %H:%M:%S"),
    )
    db.session.add(data)

db.session.commit()
