import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)


@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PATCH,POST,DELETE,OPTIONS')
    # response.headers.add('Access-Control-Allow-Origin', '*')
    return response


db_drop_and_create_all()


@app.route('/drinks', methods=['GET'])
def get_drinks():
    """
        GET /drinks
            it is a public endpoint
            it contains only the short data representation
        returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
            or appropriate status code indicating reason for failure
    """

    response = {
        'drinks': [],
        'success': False
    }

    try:
        drinks = Drink.query.all()
        short_representation = [drink.short() for drink in drinks]
        response['drinks'] = short_representation
        response['success'] = True
    except:
        abort(404)  # not found

    return jsonify(response)


@app.route('/drinks-detail', methods=['GET'])
@requires_auth('get:drinks-detail')
def get_drinks_detail(payload):
    """
        GET /drinks-detail
            it requires the 'get:drinks-detail' permission
            it contains the long data representation
        returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
            or appropriate status code indicating reason for failure
    """
    response = {
        'drinks': [],
        'success': False
    }

    try:
        drinks = Drink.query.all()
        short_representation = [drink.long() for drink in drinks]

        response['drinks'] = short_representation
        response['success'] = True
    except:
        abort(404)  # not found

    return jsonify(response)


@app.route('/drinks', methods=['POST'])
@requires_auth('post:drinks')
def post_drink(payload):
    """
        POST /drinks
            it creates a new row in the drinks table
            it requires the 'post:drinks' permission
            it contains the long data representation
        returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the newly created drink
            or appropriate status code indicating reason for failure
    """
    data = {}
    response = {
        'drinks': [],
        'success': False
    }

    try:
        data = json.loads(request.data)
    except:
        abort(400)  # bad request

    try:
        recipe = data['recipe']  # must be a list od dictionaries
        title = data['title']

        drink = Drink(
            title=title,
            recipe=json.dumps(recipe)
        )
        drink.insert()

        response['drinks'] = drink.long()
        response['success'] = True
        response['drink_id'] = drink.id
    except:
        abort(422)  # unprocessable

    return jsonify(response)


@app.route('/drinks/<drink_id>', methods=['PATCH'])
@requires_auth('patch:drinks')
def update_drink(payload, drink_id):
    """
        PATCH /drinks/<drink_id>
        where <drink_id> is the existing model id
        it responds with a 404 error if <id> is not found
        it updates the corresponding row for <id>
        it requires the 'patch:drinks' permission
        it contains the long data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the updated drink
        or appropriate status code indicating reason for failure
    """
    data = {}
    response = {
        'drinks': [],
        'success': False
    }

    if not drink_id:
        abort(400)  # bad request

    try:
        data = json.loads(request.data)
    except:
        abort(400)  # bad request

    try:
        drink = Drink.query.filter(Drink.id == drink_id).first()
        if not drink:
            abort(404)

        available_colums = Drink.__table__.columns.keys()

        for key, value in data.items():
            if key in available_colums:
                setattr(drink, key, value)

        drink.update()

        response['drinks'].append(drink.long())
        response['success'] = True
        response['drink_id'] = drink.id
    except:
        abort(422)  # unprocessable

    return jsonify(response)


@app.route('/drinks/<drink_id>', methods=['DELETE'])
@requires_auth('delete:drinks')
def delete_drink(payload, drink_id):
    """
        DELETE /drinks/<id>
            where <id> is the existing model id
            it should respond with a 404 error if <id> is not found
            it should delete the corresponding row for <id>
            it should require the 'delete:drinks' permission
        returns status code 200 and json {"success": True, "delete": id} where id is the id of the deleted record
            or appropriate status code indicating reason for failure
    """
    data = {}
    response = {
        'delete': None,
        'success': False
    }

    if not drink_id:
        abort(400)  # bad request

    try:
        drink = Drink.query.filter(Drink.id == drink_id).first()
        if not drink:
            abort(404)
        response['delete'] = drink.id

        drink.delete()

        response['success'] = True
    except:
        abort(422)  # unprocessable

    return jsonify(response)


@app.errorhandler(422)
def unprocessable(error):
    """"
        Unable to process an understood request
    """
    return jsonify({
        "success": False,
        "error": 422,
        "message": str(error)
    }), 422


@app.errorhandler(404)
def not_found(error):
    """"
        Requested element not found
    """
    return jsonify({
        "success": False,
        "error": 404,
        "message": str(error)
    }), 404


@app.errorhandler(400)
def not_found(error):
    """"
        Bad request.
    """
    return jsonify({
        "success": False,
        "error": 400,
        "message": str(error)
    }), 400


@app.errorhandler(401)
def not_found(error):
    """"
        Authorized access.
    """
    return jsonify({
        "success": False,
        "error": 401,
        "message": str(error)
    }), 401


@app.errorhandler(403)
def not_found(error):
    """"
        Forbidden actions.
    """
    return jsonify({
        "success": False,
        "error": 403,
        "message": str(error)
    }), 403
