"""
This is the people module and supports all the REST actions for the
vehicle data
"""
import re
from flask import make_response, abort, request
from config import db
from models import Driver, Vehicle, VehicleSchema


def read_all():
    """
    This function responds to a request for /api/vehicles/vehicle
    with the complete list of vehicles
    :return:                json list of all vehicles for all drivers
    """

    with_drivers = request.args.get('with_drivers')

    if with_drivers:
        vehicles = Vehicle.query.filter(Vehicle.driver).order_by(
            db.desc(Vehicle.created_at)).all() if with_drivers == 'yes' else Vehicle.query.filter(
            Vehicle.driver_id.is_(None)).all()
    else:
        vehicles = Vehicle.query.all()

    vehicle_schema = VehicleSchema(many=True)

    return vehicle_schema.dump(vehicles)


def read_one(vehicle_id):
    """
    This function responds to a request for
    /api/vehicles/vehicle/{vehicle_id}
    with one matching vehicle
    :param vehicle_id:       id of the vehicle
    :return:                json string of vehicle contents
    """

    vehicle = Vehicle.query \
        .filter(Vehicle.vehicle_id == vehicle_id) \
        .one_or_none()

    if vehicle is not None:

        vehicle_schema = VehicleSchema()
        return vehicle_schema.dump(vehicle)
    else:
        abort(404, 'Vehicle not found for Id: {id}'.format(id=vehicle_id))


def create(vehicle):
    """
    This function creates a new vehicle.
    :param vehicle:     The JSON containing the vehicle data
    :return:            201 on success
    """

    plate_number = vehicle.get('plate_number')

    regexp = re.compile('[A-Z]{2} [0-9]{4} [A-Z]{2}')
    if regexp.match(plate_number) is None:
        abort(
            409,
            "Plate number {plate_number} doesn't match a format [AA 1111 AA]".format(
                plate_number=plate_number
            ),
        )

    make = vehicle.get('make')
    model = vehicle.get('model')

    existing_vehicle = (
        Vehicle.query.filter(Vehicle.make == make).filter(Vehicle.model == model).filter(
            Vehicle.plate_number == plate_number).one_or_none()
    )

    if existing_vehicle is None:
        schema = VehicleSchema()
        new_vehicle = schema.load(vehicle, session=db.session)

        db.session.add(new_vehicle)
        db.session.commit()

        return schema.dump(new_vehicle), 200
    else:
        abort(
            409,
            "Vehicle {model} {make} {plate_number} exists already".format(
                model=model, make=make, plate_number=plate_number
            ),
        )


def update(vehicle_id, vehicle):
    """
    This function updates an existing vehicle.
    :param vehicle_id:       Id of the vehicle
    :param vehicle:          The JSON containing the vehicle data
    :return:                 200 on success
    """

    update_vehicle = Vehicle.query.filter(
        Vehicle.vehicle_id == vehicle_id
    ).one_or_none()

    plate_number = vehicle.get("plate_number")

    regexp = re.compile('[A-Z]{2} [0-9]{4} [A-Z]{2}')
    if regexp.match(plate_number) is None:
        abort(
            409,
            "Plate number {plate_number} doesn't match a format [AA 1111 AA]".format(
                plate_number=plate_number
            ),
        )

    make = vehicle.get("make")
    model = vehicle.get("model")

    existing_vehicle = (
        Vehicle.query.filter(Vehicle.make == make).filter(Vehicle.model == model).filter(
            Vehicle.plate_number == plate_number).one_or_none()
    )

    if update_vehicle is None:
        abort(
            404,
            "Vehicle not found for Id: {vehicle_id}".format(vehicle_id=vehicle_id),
        )
    elif (
            existing_vehicle is not None and existing_vehicle.vehicle_id != vehicle_id
    ):
        abort(
            409,
            "Vehicle {make} {model} {plate_number} exists already".format(
                make=make, model=model, plate_number=plate_number
            ),
        )
    else:
        schema = VehicleSchema()
        update = schema.load(vehicle, session=db.session)
        update.vehicle_id = update_vehicle.vehicle_id

        db.session.merge(update)
        db.session.commit()

        return schema.dump(update_vehicle), 200


def set_driver(vehicle_id, driver):
    """
    This function updates an existing vehicle.
    :param vehicle_id:       Id of the vehicle
    :param driver:           The JSON containing the vehicle data
    :return:                 200 on success
    """

    driver_id = driver.get("driver_id")

    update_vehicle = Vehicle.query.filter(
        Vehicle.vehicle_id == vehicle_id
    ).one_or_none()

    update_driver = Driver.query.filter(
        Driver.driver_id == driver_id
    ).outerjoin(Vehicle).one_or_none()

    if update_vehicle is None:
        abort(
            404,
            "Vehicle not found for Id: {vehicle_id}".format(vehicle_id=vehicle_id),
        )
    elif (
            update_driver is None
    ):
        abort(
            404,
            "Driver id not found for Id: {driver_id}".format(driver_id=driver_id),
        )
    else:
        schema = VehicleSchema()

        update_vehicle.driver_id = 1 if update_vehicle.driver_id == driver_id else driver_id

        db.session.merge(update_vehicle)
        db.session.commit()

        return schema.dump(update_vehicle), 200


def delete(vehicle_id):
    """
    This function deletes a vehicle
    :param vehicle_id:   Id of vehicle to delete
    :return:             200 on successful delete, 404 if not found
    """

    vehicle = Vehicle.query.filter(Vehicle.vehicle_id == vehicle_id).one_or_none()

    if vehicle is not None:
        db.session.delete(vehicle)
        db.session.commit()
        return make_response(
            "Vehicle {vehicle_id} deleted".format(vehicle_id=vehicle_id), 200
        )
    else:
        abort(
            404,
            "Vehicle not found for Id: {vehicle_id}".format(vehicle_id=vehicle_id),
        )
