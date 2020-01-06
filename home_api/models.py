from home_api import db, ma
from datetime import datetime
from marshmallow import EXCLUDE
from marshmallow_sqlalchemy.fields import Nested

'''
Database model for the application.
Migrations are handled by Flask-Migrate

Commands
Create the migration: flask db migrate
Migrate the changes to the models: flask db upgrade
Revert the changes created by migration: flask db downgrade
'''

class HousingAssociation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True)
    business_id = db.Column(db.String(10), unique=True)
    street = db.Column(db.String(100))
    street_number = db.Column(db.Integer)
    postal_code = db.Column(db.String(15))
    city = db.Column(db.String(100))
    created = db.Column(db.DateTime, default=datetime.utcnow)

    # Foreign keys and relationships
    buildings = db.relationship('Building', backref='housing_association', lazy='dynamic')

    def __repr__(self):
        return f'<HousingAssociation {self.name} | {self.business_id} | {self.street} {self.street_number} | {self.postal_code} {self.city}>'

class Building(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    building_name = db.Column(db.String(10)) # Building name, usually letter
    
    # Foreign keys and relationships
    housing_association_id = db.Column(db.Integer, db.ForeignKey('housing_association.id'))
    apartments = db.relationship('Apartment', backref='building', lazy='dynamic')
    # TODO: Add repairs relationship

    def __repr__(self):
        return f'<Building {self.building_name}>'

class Apartment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    apartment_number = db.Column(db.Integer)

    # Foreign keys
    building_id = db.Column(db.Integer, db.ForeignKey('building.id'))

    def __repr__(self):
        return f'<Apartment {self.apartment_number}>'

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    email = db.Column(db.String(255), unique=True)

# Marshmallow serialization schemas

class BuildingSchema(ma.ModelSchema):
    apartments = Nested(lambda: ApartmentSchema, many=True, dump_only=True, exclude=['building'])
    class Meta:
        model = Building

class HousingAssociationSchema(ma.ModelSchema):
    # Override the buildings attribute as Nested field.
    buildings = Nested(BuildingSchema, many=True, dump_only=True, exclude=['housing_association'])
    class Meta:
        model = HousingAssociation
        unknown = EXCLUDE


class ApartmentSchema(ma.ModelSchema):
    class Meta:
        model = Apartment

class UserSchema(ma.ModelSchema):
    class Meta:
        model = User
