Flask-Mongo JWT Authentication API
This repository contains a RESTful API built with Flask, using MongoDB as the database through the mongoengine package. The API features JWT-based authentication to ensure resource security.

API Features
User Registration
User Login - Returns a JWT token upon successful authentication
Template CRUD operations:
Create a new template
Read all templates
Read a single template by ID
Update a template by ID
Delete a template by ID
Live Demo
Hosted on Render(https://spiceblue-project.onrender.com)

Endpoints & Methods
User Registration
URL: /register
Method: POST
User Login
URL: /login
Method: POST
Template CRUD
Insert New Template

URL: /template
Method: POST
Get All Templates

URL: /template
Method: GET
Get Single Template

URL: /template/<template_id>
Method: GET
Update Single Template

URL: /template/<template_id>
Method: PUT
Delete Single Template

URL: /template/<template_id>
Method: DELETE
Setup & Installation
Clone the repository:

Use Postman or a similar tool to test the API. Ensure to use the appropriate headers and request bodies as mentioned in the API documentation.