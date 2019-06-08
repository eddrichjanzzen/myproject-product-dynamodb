from flask import Flask
from flask_cors import CORS

# Add new blueprints here
from product_routes import product_module

# Initialize the flask application
app = Flask(__name__)
CORS(app)

# Add a blueprint for the products module
app.register_blueprint(product_module)

# Run the application
app.run(host="0.0.0.0", port=5000, debug=True)