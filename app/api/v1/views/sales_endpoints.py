"""Sales Endpoints get and post methods"""
from flask_restplus import Namespace, Resource, reqparse
from flask import make_response, jsonify, request

from ..models.Sales import Sales
from ..models.User import User

from ..utils.validator import SalesDataTransferObject
api = SalesDataTransferObject.sales_namespace

sales_validator = SalesDataTransferObject.sales_model

parser = reqparse.RequestParser()
parser.add_argument('made_by')
parser.add_argument('cart')
parser.add_argument('cart_price')


@api.route('')
class SalesEndpoint(Resource):
    """Contains all the endpoints for Sales Model"""

    docstr = "Endpoint to post a sale"

    @api.doc(docstr, security='Authentication_token')
    @api.expect(sales_validator)
    def post(self):
        """Make a Sale"""

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
            made_by = user_identity
            cart = args['cart']
            cart_price = ['cart_price']

            cart_payload = (cart.split(","))
            if len(cart_payload) > 2:
                return make_response(jsonify({'status': 'failed',
                                          'message': 'cart error'}), 400)
            # sold_productId = cart[0]
            # product_quantity = cart[2]

            new_sale = Sales(made_by, cart, cart_price)
            posted_sale = new_sale.post_sales()

            return make_response(jsonify({'status': 'ok',
                                          'message': 'success',
                                          'sales': posted_sale}), 201)

    @api.doc(security='Authentication_token')
    def get(self):
        """Retrieve all sales"""

        # User Authentication
        authentication_header = request.headers.get('Authorization')
        try:
            access_token = authentication_header.split(" ")[1]
            user_identity = User.decode_auth_token(access_token)
            # role = User.get_single_user(user_identity)

            
            if user_identity == 'Invalid token. Please sign in again':
                return make_response(jsonify({'status': 'failed',
                                              'message': 'Invalid token. Please sign in again'}), 401)

            
        except Exception:
            return make_response(jsonify({'status': 'failed',
                                          'message': 'authorization required'}), 401)

        if access_token:
            # role = User.get_single_user(user_identity)
            # if role['role'] == 'attendant':
            #     attendant_sales = Sales.fetch_sales_by_email(user_identity)
            #     if attendant_sales == 'not found':
            #         return make_response(jsonify({'message': 'not found',
            #                                       'status': 'ok'}), 404)
            #     return make_response(jsonify({'message': 'success',
            #                                   'status': 'ok',
            #                                   'product': attendant_sales}), 200)
            sales = Sales.fetch_all_sales(self)
            if len(sales) == 0:
                return make_response(jsonify({'message': 'success',
                                              'status': 'ok',
                                              'product': 'No sales made'}), 200)
            return make_response(jsonify({'status': 'ok',
                                          'message': 'success',
                                          'sales': sales}), 200)

@api.route('/<int:saleId>')
class GetSingleSale(Resource):
    """Gets a single sale record"""
    @api.doc(security='Authentication_token')
    def get(self, saleId):

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
            single_sale = Sales.fetch_single_sale(saleId)
            if single_sale == 'not found':
                return make_response(jsonify({'message': 'not found',
                                              'status': 'ok'}), 404)
            return make_response(jsonify({'message': 'success',
                                          'status': 'ok',
                                          'sales': single_sale}), 200)

        