"""Product endpoints get and post methods"""
from flask_restplus import Namespace, Resource, reqparse
from flask import make_response, jsonify, request
from ..models.Product import Product
from ..models.User import User

api = Namespace('Product_endpoints',
                description='Product endpoints')

from ..utils.validator import ProductDataTransferObject

product_validator_model = ProductDataTransferObject.product_model
product_validator_response = ProductDataTransferObject.product_response

parser = reqparse.RequestParser()
parser.add_argument('product_name')
parser.add_argument('product_description')
parser.add_argument('product_quantity')
parser.add_argument('product_category')
parser.add_argument('product_moq')


@api.route('')
class ProductEndpoint(Resource):
    """Contains all the endpoints for Product Model"""

    docStr = "Endpoint to post a Product"

    # @api.expect(product_validator_model, validate=True)
    @api.doc(docStr)
    def post(self):
        """add product"""

        # User Authentication
        authentication_header = request.headers.get('Authorization')
        try:
            access_token = authentication_header.split(" ")[1]
            user_identity = User.decode_auth_token(access_token)
            if user_identity == 'Invalid token. Please sign in again':
                return make_response(jsonify({'status': 'failed',
                                              'message': 'Invalid token. Please sign in again'}), 401)
            
        except Exception:
            return make_response(jsonify({'status': 'failed',
                                          'message': 'authorization required'}), 401)
        
        if access_token:
            role = User.get_single_user(user_identity)
            print(role['role'])
            if role['role'] == 'attendant':
                return make_response(jsonify({'status': 'failed',
                                            'message': 'requires admin'}), 401)
            args = parser.parse_args()
            name = args['product_name']
            description = args['product_description']
            quantity = args['product_quantity']
            category = args['product_category']
            moq = args['product_moq']

            new_product = Product(name, description, quantity, category, moq)
            new_product.added_by = user_identity
            posted_product = new_product.post_product()
            return make_response(jsonify({'status': 'ok',
                                        'message': 'success',
                                        'product': posted_product}), 201)
        
        return make_response(jsonify({'status': 'failed',
                                        'message': 'authorization required'}), 401)

    # @api.marshal_list_with(product_validator_response, envelope='products')
    def get(self):
        """Retrieve all products"""
        # User Authentication
        authentication_header = request.headers.get('Authorization')
        try:
            access_token = authentication_header.split(" ")[1]
            user_identity = User.decode_auth_token(access_token)
            
            if user_identity == 'Invalid token. Please sign in again':
                return make_response(jsonify({'status': 'failed',
                                        'message': 'Invalid token. Please sign in again'}), 401)
        except Exception:
            return make_response(jsonify({'status': 'failed',
                                        'message': 'authorization required'}), 401)

        if access_token:
            products = Product.fetch_all_products(self)
            if len(products) == 0:
                return make_response(jsonify({'message': 'success',
                                      'status': 'ok',
                                      'product': 'No products added to inventory'}), 200)
            return make_response(jsonify({'message': 'success',
                                      'status': 'ok',
                                      'product': products}), 200)


@api.route('/<int:productId>')
class GetSingleProduct(Resource):
    """Get a single Product record"""
    def get(self, productId):
        """Retrieve a single product"""
        # User Authentication
        authentication_header = request.headers.get('Authorization')
        try:
            access_token = authentication_header.split(" ")[1]
            user_identity = User.decode_auth_token(access_token)
            
            if user_identity == 'Invalid token. Please sign in again':
                return make_response(jsonify({'status': 'failed',
                                        'message': 'Invalid token. Please sign in again'}), 401)
        except Exception:
            return make_response(jsonify({'status': 'failed',
                                        'message': 'authorization required'}), 401)

        if access_token:
            single_product = Product.fetch_single_product(productId)
            if single_product == 'not found':
                return make_response(jsonify({'message': 'not found',
                                            'status': 'ok'}), 404)
            return make_response(jsonify({'message': 'success',
                                        'status': 'ok',
                                        'product': single_product}), 200)
