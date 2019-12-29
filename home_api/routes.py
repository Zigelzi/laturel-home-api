from flask import jsonify, request

from home_api import app, db
from home_api.models import HousingAssociation, HousingAssociationSchema
from home_api.config import Config, DevConfig

housing_associations = [
    {
        'name': "Hakulinpuisto",
        'businessId': "1234567-8",
        'street': "Hakulintie",
        'streetNumber': 43,
        'postalCode': "08500",
        'city': "Lohja"
    }
]

@app.route('/housing_associations', methods=['GET', 'POST'])
def all_housing_associations():
    
    response_object = {'status': 'success'}
    
    if request.method == 'POST':
        post_data = request.get_json()
        housing_association = HousingAssociation(
            name = post_data.get('name'),
            business_id = post_data.get('businessId'),
            street = post_data.get('street'),
            street_number = post_data.get('streetNumber'),
            postal_code = post_data.get('postalCode'),
            city = post_data.get('city')
        )
        db.session.add(housing_association)
        db.session.commit()
        response_object['message'] = 'Housing association added!'
    else:
        response_object['housingAssociations'] = housing_associations
    return jsonify(response_object)