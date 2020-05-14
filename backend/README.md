# Coffee Shop Backend

## Documentation

- #### Table of Contents
1. [Setup Auth0](#setup-auth0)
2. [Error handlers](#error-handlers)
3. [When are errors expected](#when-are-errors-expected)
4. [Endpoints](#endpoints)
5. [Endpoint description](#endpoint-description)
6. [Testing endpoints](#testing-endpoints)

- #### Setup Auth0

1. Create a new Auth0 Account
2. Select a unique tenant domain
3. Create a new, single page web application
4. Create a new API
    - in API Settings:
        - Enable RBAC
        - Enable Add Permissions in the Access Token
5. Create new API permissions:
    - `get:drinks-detail`
    - `post:drinks`
    - `patch:drinks`
    - `delete:drinks`
6. Create new roles for:
    - Barista
        - can `get:drinks-detail`
    - Manager
        - can perform all actions

##### NOTE: Config variables should be put in file config.properties in the ./backend/ folder and have a form:
```properties
[AUTH_0]
AUTH0_DOMAIN=
ALGORITHMS=['']
API_AUDIENCE=
```

- #### Error handlers
```
1. 400 - Bad Request
2. 401 - Unauthorized
3. 403 - Forbidden
4. 404 - Not Found
5. 422 - Unprocessable Entity
```

- ###### When are errors expected
```
1. 400 - Request body is malformed
2. 401 - JWT cannot be verified or Authorization header is invalid
3. 403 - No permission in JWT to access an endpoint
4. 404 - Requested resource is not found
5. 422 - Request fails to succeed
```

- #### Endpoints
```
1. GET /drinks
2. GET /drinks-detail
3. POST /drinks
4. PATCH /drinks/<drink_id>
5. DELETE /drinks/<drink_id>
```

- ###### Endpoint description
```
1. GET /drinks
    - Fetches all drinks and returns a short long representations of drinks.
    - Request Body: None
    - Request Parameters: None 
    - Identifiers: None
    - Expected Errors: 404
    - Expected Permission: None
    - Return Body: a list of short representations of drinks
    {
      "drinks": [
        {
          "id": 1,
          "recipe": [ {"color": "blue", "parts": 1} ],
          "title": "Water"
        }
      ],
      "success": true
    }    
```

```    
2. GET /drinks-detail
    - Fetches all drinks and returns long representations of drinks.
    - Request Body: None
    - Request Parameters: None 
    - Identifiers: None
    - Expected Errors: 404
    - Required Permission: get:drinks-detail
    - Return Body: a list of long representations of drinks
    {
      "drinks": [
        {
          "id": 1,
          "recipe": [ {"color": "blue", "name":"Water", "parts": 1} ],
          "title": "Water"
        }
      ],
      "success": true
    }
```

```
3. POST /drinks
    - Creates a new drink.
    - Request Parameters: None 
    - Identifiers: None
    - Expected Errors: 400, 422
    - Required Permission: post:drinks
    - Request Body:
    {
	    "title": "Water",
	    "recipe": [ {"color": "blue", "name":"Water", "parts": 1} ]
    }
    - Return Body: a list of long representations of drinks
    {
      "drinks": [
        {
          "id": 1,
          "recipe": [ {"color": "blue", "name":"Water", "parts": 1} ],
          "title": "Water"
        }
      ],
      "success": true
    }
```

```
4. PATCH /drinks/<drink_id>
    - Update one of the requested attributes of a drink.
    - Request Parameters: None 
    - Identifiers: drink_id (int)
    - Expected Errors: 400, 404, 422
    - Required Permission: patch:drinks
    - Request Body (keys are optional):
    {
	    "title": "Water",
	    "recipe": [ {"color": "blue", "name":"Water", "parts": 1} ]
    }
    - Return Body: a list of long representations of drinks, where drinks is an array containing only the updated drink
    {
      "drinks": [
        {
          "id": 1,
          "recipe": [ {"color": "blue", "name":"Water", "parts": 1} ],
          "title": "Water"
        }
      ],
      "success": true,
      "drink_id": drink_id
    }
```
```
5. DELETE /drinks/<drink_id>
    - Remove a drink by a specified ID of a drink.
    - Request Parameters: None 
    - Identifiers: drink_id (int)
    - Expected Errors: 400, 404, 422
    - Required Permission: delete:drinks
    - Request Body: None
    - Return Body: the deleted drink's ID and a success status.
    {
      "success": true,
      "deleted": drink_id
    }
```

- #### Testing endpoints
    - (if not done yet) Install [Postman](https://getpostman.com). 
    - (if not done yet) Register 2 users - assign the Barista role to one and Manager role to the other.
    - Sign into each account and make note of the JWT.
    - Import the postman collection `./starter_code/backend/udacity-fsnd-udaspicelatte.postman_collection.json`
    - Right-clicking the collection folder for barista and manager, navigate to the authorization tab, and including the JWT in the token field (you should have noted these JWTs).
    - Run the collection and correct any errors.
