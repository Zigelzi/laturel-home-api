from flask import jsonify, request
from sqlalchemy import exc

from home_api import app, db
from home_api.models import HousingAssociation, HousingAssociationSchema
from home_api.config import Config, DevConfig

# Initialize the Flask-Marshmallow schemas for serializations
all_ha_schema = HousingAssociationSchema(many=True) # Serialize all the results as array

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
            post_data = request.get_json()
            # Create DB model from the received JSON.
            housing_association = HousingAssociation(
                name = post_data.get('name'),
                business_id = post_data.get('businessId'),
                street = post_data.get('street'),
                street_number = int(post_data.get('streetNumber')),
                postal_code = post_data.get('postalCode'),
                city = post_data.get('city')
            )
            db.session.add(housing_association)
            db.session.commit()
            response_object['message'] = 'Housing association added!'
        except exc.IntegrityError:
            response_object['status'] = 'fail'
            response_object['message'] = 'Unable to add housing association, unique database constraint violated'
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
        housing_association = HousingAssociation.query.get(ha_id)
        # If housing association is found, delete it's record
        if housing_association:
            db.session.delete(housing_association)
            db.session.commit()
            response_object['message'] = 'Housing association deleted!'
        else:
            response_object['message'] = 'Housing association not found'
    return jsonify(response_object)
