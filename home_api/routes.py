from flask import jsonify, request
from sqlalchemy.exc import IntegrityError

from home_api import app, db
from home_api.models import HousingAssociation, Building, Apartment, User, UserSchema, HousingAssociationSchema
from home_api.config import Config, DevConfig

# Initialize the Flask-Marshmallow schemas for serializations
all_ha_schema = HousingAssociationSchema(many=True) # Serialize all the results as array
ha_schema = HousingAssociationSchema()

users_schema = UserSchema()
"""
Route abbreviations
ha = Housing Association, refering to the whole housing entity
One housing association might contain multiple building and buildings might contain multiple apartments

"""

@app.route('/ha/get_all', methods=['GET', 'POST'])
def all_ha():
    
    response_object = {'status': 'success'}
    
    if request.method == 'POST':
        try:
            request_data = request.get_json()
            # Create DB model from the received JSON.
            housing_association = ha_schema.load(request_data)
            db.session.add(housing_association)
            db.session.commit()
            # Return the added HA to frontend to be used as current HA
            if request_data['buildings']:
                # If buildings exist loop though them
                for building in request_data['buildings']:
                    # Create DB entry for all buildings in buildings array
                    building_model = Building(
                                        building_name=building['building_name'],
                                        housing_association_id = housing_association.id
                                        )
                    db.session.add(building_model)
                    db.session.commit()
                    # Convert the apartment_count to integer
                    building['apartment_count'] = int(building['apartment_count'])
                    for apartment in range(building['apartment_count']):
                        apartment_number = apartment + 1
                        apartment_model= Apartment(
                                                apartment_number = apartment_number,
                                                building_id = building_model.id
                                            )
                        db.session.add(apartment_model)
                    db.session.commit()
            response_object['data'] = ha_schema.dump(housing_association)
            response_object['message'] = 'Housing association added!'
        except IntegrityError as exception:
            response_object['status'] = 'fail'
            response_object['message'] = 'Something failed when adding housing association to database'
            print(exception)
            db.session.rollback()
    else:
        housing_associations = HousingAssociation.query.all()
        # Serialize the query results to ha_array variable and add the array to response
        ha_array = all_ha_schema.dump(housing_associations)
        response_object['housingAssociations'] = ha_array
    return jsonify(response_object)

@app.route('/ha/<int:ha_id>', methods=['PUT', 'DELETE'])
def delete_ha(ha_id):
    response_object = {'status': 'success'}

    if request.method == 'DELETE':
        housing_association = HousingAssociation.query.get_or_404(ha_id)
        # If housing association is found, delete it's record
        if housing_association:
            db.session.delete(housing_association)
            db.session.commit()
            response_object['message'] = 'Housing association deleted!'
        else:
            response_object['message'] = 'Housing association not found'
    return jsonify(response_object)

@app.route('/users/', methods=['GET', 'POST'])
def users():
    response_object = {'status': 'success'}
    print(request)

    if request.method == 'POST':
        request_data = request.get_json()
        # User Marshmallow to load the JSON directly as User object and commit it to DB.
        user = users_schema.load(request_data)
        db.session.add(user)
        db.session.commit()
        response_object['message'] = 'User added successfully!'
    return jsonify(response_object)
