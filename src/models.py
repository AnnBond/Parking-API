from datetime import datetime

from config import db
from marshmallow import fields

from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field


class Driver(db.Model):
    __tablename__ = "driver"
    driver_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(32))
    last_name = db.Column(db.String(32))
    created_at = db.Column(
        db.DateTime, default=datetime.now()
    )
    updated_at = db.Column(
        db.DateTime, onupdate=datetime.now()
    )

    vehicle = db.relationship('Vehicle', backref='driver')

    def __repr__(self) -> str:
        return 'Driver>>> {self.first_name}'


class Vehicle(db.Model):
    __tablename__ = 'vehicle'
    vehicle_id = db.Column(db.Integer, primary_key=True)
    driver_id = db.Column(db.Integer, db.ForeignKey('driver.driver_id'))
    make = db.Column(db.String, nullable=False)
    model = db.Column(db.String, nullable=False)
    plate_number = db.Column(db.String, nullable=False)
    created_at = db.Column(
        db.DateTime, default=datetime.now()
    )
    updated_at = db.Column(
        db.DateTime, onupdate=datetime.now()
    )

    def __repr__(self) -> str:
        return 'Vehicle>>> {self.vehicle_id}'


class DriverSchema(SQLAlchemyAutoSchema):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    class Meta:
        fields = ('driver_id', 'first_name', 'last_name', 'created_at', 'updated_at', 'vehicle')
        model = Driver
        include_relationships = True
        load_instance = True
        sqla_session = db.session

    vehicle = fields.Nested("DriverVehicleSchema", default=[], many=True)


class VehicleSchema(SQLAlchemyAutoSchema):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    class Meta:
        model = Vehicle
        include_relationships = True
        load_instance = True
        include_fk = True
        sqla_session = db.session
        vehicle_id = auto_field()
        created_at = auto_field(dump_only=True)

    if Vehicle.driver_id is not None:
        driver = fields.Nested("VehicleDriverSchema", default=[])


class DriverVehicleSchema(SQLAlchemyAutoSchema):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    vehicle_id = fields.Int()
    driver_id = fields.Int()
    make = fields.Str()
    model = fields.Str()
    plate_number = fields.Str()
    created_at = fields.Str()
    updated_at = fields.Str()


class VehicleDriverSchema(SQLAlchemyAutoSchema):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    driver_id = fields.Int()
    last_name = fields.Str()
    first_name = fields.Str()
    created_at = fields.Str()
    updated_at = fields.Str()
