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
    response.headers.add('Access-Control-Allow-Origin', '*')
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
        abort(404)

    return jsonify(response)


'''
    GET /drinks-detail
        it requires the 'get:drinks-detail' permission
        it contains the long data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''


@app.route('/drinks-detail', methods=['GET'])
def get_drinks_detail():
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
        abort(404)

    return jsonify(response)


'''
@TODO implement endpoint
    POST /drinks
        it should create a new row in the drinks table
        it should require the 'post:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the newly created drink
        or appropriate status code indicating reason for failure
'''

'''
@TODO implement endpoint
    PATCH /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should update the corresponding row for <id>
        it should require the 'patch:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the updated drink
        or appropriate status code indicating reason for failure
'''

'''
@TODO implement endpoint
    DELETE /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should delete the corresponding row for <id>
        it should require the 'delete:drinks' permission
    returns status code 200 and json {"success": True, "delete": id} where id is the id of the deleted record
        or appropriate status code indicating reason for failure
'''


@app.errorhandler(422)
def unprocessable(error):
    """"
        Unable to process an understood request
    """
    return jsonify({
        "success": False,
        "error": 422,
        "message": "Unprocessable"
    }), 422


@app.errorhandler(404)
def not_found(error):
    """"
        Requested element not found
    """
    return jsonify({
        "success": False,
        "error": 404,
        "message": "Not Found"
    }), 404


'''
@TODO implement error handlers using the @app.errorhandler(error) decorator
    each error handler should return (with approprate messages):
             jsonify({
                    "success": False, 
                    "error": 404,
                    "message": "resource not found"
                    }), 404

'''

'''
@TODO implement error handler for 404
    error handler should conform to general task above 
'''

'''
@TODO implement error handler for AuthError
    error handler should conform to general task above 
'''
