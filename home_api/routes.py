from flask import jsonify, request, make_response
from sqlalchemy.exc import IntegrityError

from home_api import app, db
from home_api.models import HousingAssociation, Building, Apartment, User, UserSchema, HousingAssociationSchema
from home_api.config import Config, DevConfig

# Initialize the Flask-Marshmallow schemas for serializations
all_ha_schema = HousingAssociationSchema(many=True) # Serialize all the results as array
ha_schema = HousingAssociationSchema()

many_users_schema = UserSchema(many=True) # Serialize all the results as array
users_schema = UserSchema()

# Status message descriptions
status_msg_fail = 'fail'
status_msg_success = 'success'

"""
Route abbreviations
ha = Housing Association, refering to the whole housing entity
One housing association might contain multiple building and buildings might contain multiple apartments
"""

@app.route('/ha/get_all', methods=['GET'])
def get_all_ha():
    response_object = {'status': status_msg_success}
    housing_associations = HousingAssociation.query.all()
    # Serialize the query results to ha_array variable and add the array to response
    ha_array = all_ha_schema.dump(housing_associations)
    response_object['housingAssociations'] = ha_array
    return jsonify(response_object)

@app.route('/ha/add', methods=['POST'])
def add_ha():
    response_object = {'status': status_msg_success}

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
        return make_response(jsonify(response_object), 201)
    except IntegrityError as exception:
        response_object['status'] = status_msg_fail
        response_object['message'] = 'Something failed when adding housing association to database'
        print(exception)
        db.session.rollback()
        return make_response(jsonify(response_object, 400))

@app.route('/ha/<int:ha_id>', methods=['DELETE'])
def delete_ha(ha_id):
    response_object = {'status': status_msg_success}
    housing_association = HousingAssociation.query.get_or_404(ha_id)
    # If housing association is found, delete it's record
    if housing_association:
        db.session.delete(housing_association)
        db.session.commit()
        response_object['message'] = 'Housing association deleted!'
        return jsonify(response_object)
    else:
        response_object['status'] = status_msg_fail
        response_object['message'] = 'Housing association not found'
        return make_response(jsonify(response_object), 404)

@app.route('/users/', methods=['GET'])
def get_all_users():
    response_object = {'status': status_msg_success}
    users = User.query.all()
    users_array = many_users_schema.dump(users)
    response_object['users'] = users_array
    return jsonify(response_object)

@app.route('/users/', methods=['POST'])
def add_user():
    response_object = {'status': status_msg_success}
    request_data = request.get_json()
    print(request_data)
    user = User.query.filter_by(email=request_data.get('email')).first()
    if not user:
        # Check that user doesn't exist in the database and add him/her to the DB
        try:
            # User Marshmallow to load the JSON directly as User object and commit it to DB.
            # Generate hashed password for the user
            user = User(
                name=request_data.get('name'),
                email=request_data.get('email')
                )
            print(f'User: {user}')
            user.set_password(request_data.get('password'))
            db.session.add(user)
            db.session.commit()
            # Generate JWT for the user
            auth_token = user.encode_auth_token(user.id)
            response_object['message'] = 'User added successfully!'
            response_object['auth_token'] = auth_token.decode()
            return make_response(jsonify(response_object), 201)
        except Exception as e:
            print(f'Exception: {e}')
            response_object['status'] = status_msg_fail
            response_object['message'] = 'Error occurred when adding user to database. Please try again.'
            return make_response(jsonify(response_object), 401)
    else:
        response_object['status'] = status_msg_fail
        response_object['message'] = 'User already exists. Please log in or try another email'
        return make_response(jsonify(response_object), 202)

@app.route('/auth/login', methods=['POST'])
def login():
    response_object = {'status': status_msg_success}
    request_data = request.get_json()
    try:
        user = User.query.filter_by(email=request_data.get('email')).first()
        if user and user.check_password(request_data['password']):
            auth_token = user.encode_auth_token(user.id)
            if auth_token:
                response_object['message'] = 'Succesfully logged in'
                response_object['auth_token'] = auth_token.decode()
                return make_response(jsonify(response_object), 200)
        else:
            response_object['status'] = status_msg_fail
            response_object['message'] = 'Login information incorrect. Please try again.'
            return make_response(jsonify(response_object), 401)
    except Exception as e:
        print(f'Execption: {e}')
        response_object['status'] = status_msg_fail
        response_object['message'] = 'Login failed. Please try again'
        return make_response(jsonify(response_object), 500)
