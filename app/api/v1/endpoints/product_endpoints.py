"""Product endpoints get and post methods"""
from flask_restplus import Namespace, Resource, reqparse
from flask import make_response, jsonify
from ..models.Product import Product

api = Namespace('Product_endpoints',
                description='Endpoints for the product includes get and post')

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
        args = parser.parse_args()
        name = args['product_name']
        description = args['product_description']
        quantity = args['product_quantity']
        category = args['product_category']
        moq = args['product_moq']

        new_product = Product(name, description, quantity, category, moq)
        posted_product = new_product.post_product()
        return make_response(jsonify({'status': 'ok',
                                      'message': 'success',
                                      'product': posted_product}), 201)

    # @api.marshal_list_with(product_validator_response, envelope='products')
    def get(self):
        """Retrieve all products"""
        products = Product.fetch_all_products(self)
        return make_response(jsonify({'message': 'success',
                                      'status': 'ok',
                                      'product': products}), 200)


@api.route('/<int:productId>')
class GetSingleProduct(Resource):
    """Get a single Product record"""
    def get(self, productId):
        """Retrieve a single product"""
        single_product = Product.fetch_single_product(productId)
        if single_product == 'not found':
            return make_response(jsonify({'message': 'not found',
                                          'status': 'ok'}), 404)
        return make_response(jsonify({'message': 'success',
                                      'status': 'ok',
                                      'product': single_product}), 200)

    def put(self, productId):
        """Edit a Product record"""
        edit_product = Product.put(self, productId)
        if edit_product == 'not found':
            return make_response(jsonify({'message': 'not found',
                                          'status': 'ok'}), 404)
        return make_response(jsonify({'message': 'success',
                                      'status': 'ok',
                                      'product': edit_product}), 200)
