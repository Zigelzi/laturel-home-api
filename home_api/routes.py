from flask import jsonify, request

from home_api import app, db
from home_api.models import HousingAssociation, HousingAssociationSchema
from home_api.config import Config, DevConfig

# Initialize the Flask-Marshmallow schemas for serializations
all_ha_schema = HousingAssociationSchema(many=True) # Serialize all the results as array

@app.route('/housing_associations', methods=['GET', 'POST'])
def all_housing_associations():
    
    response_object = {'status': 'success'}
    
    if request.method == 'POST':
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
    else:
        housing_associations = HousingAssociation.query.all()
        # Serialize the query results to ha_array variable and add the array to response
        ha_array = all_ha_schema.dump(housing_associations)
        response_object['housingAssociations'] = ha_array
    return jsonify(response_object)