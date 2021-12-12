"""
This is the driver module and supports all the REST actions
"""

# System modules
from datetime import datetime

# 3rd party modules
from flask import make_response, abort, request

from config import db
from models import (
    Driver,
    DriverSchema, Vehicle,
)


def read_all():
    """
    This function responds to a request for /api/drivers
    with the complete lists of drivers
    :return:        json string of list of drivers
    """
    after_date = request.args.get('created_at__gte')
    before_date = request.args.get('created_at__lte')

    drivers = Driver.query

    if after_date:
        drivers = drivers.filter(Driver.created_at > datetime.strptime(after_date, "%d-%m-%Y"))
    if before_date:
        drivers = drivers.filter(Driver.created_at <= datetime.strptime(before_date, "%d-%m-%Y"))

    drivers = drivers.all()
    drivers_schema = DriverSchema(many=True)

    return drivers_schema.dump(drivers)


def read_one(driver_id):
    """
    This function responds to a request for /api/drivers/driver/{driver_id}
    with one matching driver from drivers
    :param driver_id:      id of driver to find
    :return:               driver matching last name
    """

    driver = (
        Driver.query.filter(Driver.driver_id == driver_id).outerjoin(
            Vehicle).one_or_none()
    )

    if driver is not None:
        driver_schema = DriverSchema()
        return driver_schema.dump(driver)
    else:
        abort(404, 'Driver not found for Id: {driver_id}'.format(driver_id=driver_id))


def create(driver):
    """
    This function creates a new driver in the drivers structure
    based on the passed in driver data
    :param driver:  driver to create in drivers structure
    :return:        201 on success, 406 on driver exists
    """
    first_name = driver.get('first_name')
    last_name = driver.get('last_name')

    existing_driver = (
        Driver.query.filter(Driver.first_name == first_name).filter(
            Driver.last_name == last_name).one_or_none()
    )

    if existing_driver is None:
        schema = DriverSchema()
        new_driver = schema.load(driver, session=db.session)

        db.session.add(new_driver)
        db.session.commit()

        return schema.dump(new_driver), 201
    else:
        abort(
            409,
            "Driver {first_name} {last_name} exists already".format(
                first_name=first_name, last_name=last_name
            ),
        )


def update(driver_id, driver):
    """
    This function updates an existing driver in the drivers structure
    :param driver_id:   last name of driver to update in the drivers structure
    :param driver:      driver to update
    :return:            updated driver structure
    """

    update_driver = Driver.query.filter(
        Driver.driver_id == driver_id
    ).one_or_none()

    first_name = driver.get("first_name")
    last_name = driver.get("last_name")

    existing_driver = (
        Driver.query.filter(Driver.first_name == first_name).filter(
            Driver.last_name == last_name).one_or_none()
    )

    if update_driver is None:
        abort(
            404,
            "Driver not found for Id: {driver_id}".format(driver_id=driver_id),
        )
    elif (
            existing_driver is not None
    ):
        abort(
            409,
            "Driver {first_name} {last_name} exists already".format(
                first_name=first_name, last_name=last_name
            ),
        )
    else:
        schema = DriverSchema()
        update_driver = schema.load(driver, session=db.session)

        # Set the id to the driver we want to update
        update.driver_id = update_driver.driver_id

        db.session.merge(update)
        db.session.commit()

        return schema.dump(update_driver), 200


def delete(driver_id):
    """
    This function deletes a driver from the drivers structure
    :param driver_id:   last name of driver to delete
    :return:            200 on successful delete, 404 if not found
    """

    driver = Driver.query.filter(Driver.driver_id == driver_id).one_or_none()

    if driver is not None:
        db.session.delete(driver)
        db.session.commit()
        return make_response(
            "Driver {driver_id} deleted".format(driver_id=driver_id), 200
        )

    else:
        abort(
            404,
            "Driver not found for Id: {driver_id}".format(driver_id=driver_id),
        )
