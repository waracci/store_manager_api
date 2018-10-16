from flask_restplus import Api
from flask import Blueprint

# Import all endpoints for all models
from .endpoints import product_endpoints

version1 = Blueprint('api version 1', __name__, url_prefix='/api/v1')

api = Api(version1, 
                title='Store manager API',
                version='1.0',
                description='An application that helps store owners manage sales and product inventory records')
api.add_namespace(product_endpoints, path='/products')