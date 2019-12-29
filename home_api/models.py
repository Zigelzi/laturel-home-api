from home_api import db, ma
from datetime import datetime

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

    def __repr__(self):
        return f'<HousingAssociation {self.name} | {self.business_id} | {self.street} {self.street_number} | {self.postal_code} {self.city}>'

class HousingAssociationSchema(ma.ModelSchema):
    class Meta:
        model = HousingAssociation