# Product aggregator microservice

This is a microservice application that provides functionality for managing product offers.
Microservice provides API for managing product offers and it includes a background service for periodically updating offer data.  
The API implements CRUD (Create, Read, Update, Delete) structure for product offers. 
The API is read-only to view and retrieve data about offers.

### Getting Started

To run the microservice, follow these steps:

### Installation
1. Clone the repository to your local machine: <br>
git clone https://github.com/nikitach507/product-aggregator-microservice.git
2. Create virtual env with Python 3.10 <br>
python -m venv venv
3. Install the Python dependencies: <br>
pip install -r requirements.txt
4. Create .env file with secret from example.env
5. Add SECRET, REFRESH_TOKEN
6. Starting the Service. To start the microservice, run the following command: <br>
uvicorn microservice.main:app --reload  <br> 

The service will start, and you will see logs indicating.

#### Docker
1. Create .env file with secret from example.env
2. Add SECRET, REFRESH_TOKEN
3. docker-compose up --build

### Using the API
The microservice provides an API for managing product offers. You can access the API at http://localhost:8000.

#### Products Endpoints
GET: /api/v1/products/ - Get a list of all products.<br>
GET: /api/v1/products/{product_id} - Get a product by its ID.<br>
POST: /api/v1/products/ - Create a new product.<br>
PUT: /api/v1/products/{product_id} - Update a product by its ID.<br>
DELETE: /api/v1/products/{product_id} - Delete a product by its ID.<br>

#### Offers Endpoints

GET: /api/v1/offers/ - Get a list of all offers.<br>
GET: /api/v1/offers/{offer_id} - Get an offer by its ID.<br>
GET: /api/v1/offers/products/{product_id} - Get offers by product ID.<br>

#### Price Trend Analysis
GET: /api/v1/price_trend/ - Calculate and retrieve the price trend and percentual rise/fall for a specified product within a given date range. <br>
You can specify the product ID, start date, and end date as query parameters.

### Authentication and Authorization
For added security, this microservice utilizes an authentication mechanism. Users must provide valid access tokens to access certain protected endpoints. This ensures that only authorized users can interact with sensitive data and perform specific operations.

### Background Service
The microservice includes a background service that periodically updates offer data from an external source. The background service runs automatically when the microservice starts.
