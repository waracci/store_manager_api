"""Product endpoints get and post methods"""
from flask_restplus import Namespace, Resource, reqparse
from flask import make_response, jsonify, request
from ..models.Product import Product
from ..models.User import User
from ..utils.validator import ProductDataTransferObject

api = ProductDataTransferObject.product_namespace


product_validator_model = ProductDataTransferObject.product_model
product_validator_response = ProductDataTransferObject.product_response

parser = reqparse.RequestParser()
parser.add_argument('product_name', required=True, help='Product name cannot be blank')
parser.add_argument('product_description', required=True, help='product descipription cannot be blank')
parser.add_argument('product_quantity', required=True, help='product quantity cannot be blank')
parser.add_argument('product_category', required=True, help='product category cannot be blank')
parser.add_argument('product_moq', required=True, help='product moq cannot be blank')


@api.route('')
class ProductEndpoint(Resource):
    """Contains all the endpoints for Product Model"""

    docStr = "Endpoint to post a Product"

    # @api.expect(product_validator_model, validate=True)
    @api.doc(docStr, security='Authentication_token')
    def post(self):
        """Endpoint for adding a product"""

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
            try:
                role = User.get_single_user(user_identity)
                if role['role'] == 'attendant':
                    return make_response(jsonify({'status': 'failed',
                                                'message': 'requires admin'}), 401)
            except Exception:
                return make_response(jsonify({'status': 'failed',
                                                'message': 'requires authorization'}), 401)
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
    #it should work without it
    @api.doc(security='Authentication_token')
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
@api.doc(security='Authentication_token')
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
            if not isinstance(productId, int):
                return make_response(jsonify({'status': 'failed',
                                        'message': 'id requires integer'}), 400)
            single_product = Product.fetch_single_product(productId)
            if single_product == 'not found':
                return make_response(jsonify({'message': 'not found',
                                            'status': 'ok'}), 200)
            return make_response(jsonify({'message': 'success',
                                        'status': 'ok',
                                        'product': single_product}), 200)

    def put(self, productId):
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
            args = parser.parse_args()
            name = args['product_name']
            description = args['product_description']
            quantity = args['product_quantity']
            category = args['product_category']
            moq = args['product_moq']
            existing_product = Product.fetch_single_product(productId)
            if 'not found' in existing_product:
                return dict(message="product not found", status="failed"), 404
            product_update = Product.edit_product(productId, name, description, quantity, category, moq)

            return make_response(jsonify(product_update), 200)

    def delete(self, productId):
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
            deleted_product = Product.delete_product(productId)
            if 'not found' in deleted_product:
                return dict(message="product not found", status="failed"), 404
            return dict(message="product deleted successfully", status="failed"), 200