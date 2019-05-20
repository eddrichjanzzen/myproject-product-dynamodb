from flask import Blueprint
from flask import Flask, json, Response, request
from products import product_table_client
from custom_logger import setup_logger

# Set up the custom logger and the Blueprint
logger = setup_logger(__name__)
product_module = Blueprint('products', __name__)

# Allow the default route to return a health check
@product_module.route('/')
def health_check():
    return "This a health check. Product Management Service is up and running."

    
@product_module.route('/products')
def get_all_products():

    #returns all the products coming from dynamodb
    serviceResponse = product_table_client.getAllProducts()
    
    resp = Response(serviceResponse)
    resp.headers["Content-Type"] = "application/json"
    
    return resp
    
@product_module.route("/products/<product_id>", methods=['GET'])
def get_product(product_id):

    #returns a product given its id
    serviceResponse = product_table_client.getProduct(product_id)

    resp = Response(serviceResponse)
    resp.headers["Content-Type"] = "application/json"

    return resp

@product_module.route("/products", methods=['POST'])
def create_product():

    #creates a new product. The product id is automatically generated.
    product_dict = json.loads(request.data)
    serviceResponse = product_table_client.createProduct(product_dict)

    resp = Response(serviceResponse)
    resp.headers["Content-Type"] = "application/json"

    return resp


@product_module.route("/products/<product_id>", methods=['PUT'])
def update_product(product_id):
    
    #updates a product given its id.
    product_dict = json.loads(request.data)
    serviceResponse = product_table_client.updateProduct(product_id, product_dict)

    resp = Response(serviceResponse)
    resp.headers["Content-Type"] = "application/json"

    return resp

@product_module.route("/products/<product_id>", methods=['DELETE'])
def delete_product(product_id):
    
    #deletes a product given its id.
    serviceResponse = product_table_client.deleteProduct(product_id)

    resp = Response(serviceResponse)
    resp.headers["Content-Type"] = "application/json"

    return resp

