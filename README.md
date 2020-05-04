# Coffee Shop for Jessica W.

## The story and requirements

A person, let's call her Jessica W., has decided to open a new digitally enabled cafe for students to order drinks, socialize, and study hard. 
But they need help setting up their menu experience.

According to her budget, she decided to hire a developer and requested the following functionaries:

1) Display graphics representing the ratios of ingredients in each drink.
2) Allow public users to view drink names and graphics.
3) Allow the shop baristas to see the recipe information.
4) Allow the shop managers to create new drinks and edit existing drinks.

Jessica's notes:
- Functionality is more important
- Customers won't see the menu, so the look should be simple.

## Logic and Views
For detailed documentations, setup and requirements refer to (server and client are separate):

1. [`./backend/`](./backend/README.md)
2. [`./frontend/`](./frontend/README.md)

## About the Stack

### Backend

The `./backend` directory contains a  Flask server with a SQLAlchemy model called Drink. 

The endpoints are completed and restricted to satisfy Jessica's requirements.

[View the README.md within ./backend for more details.](./backend/README.md)

### Frontend

The `./frontend` directory contains a complete Ionic frontend to consume the data from the Flask server. 

As per Jessica's requirements, the frontend was completed with the main focus on interaction with the backend.

[View the README.md within ./frontend for more details.](./frontend/README.md)
