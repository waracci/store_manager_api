from flask_restplus import fields

from ..endpoints.product_endpoints import api as product_namespace
from ..endpoints.sales_endpoints import api as sales_endpoints

class ProductDataTransferObject():
    product_ns = product_namespace

    product_model = product_ns.model('product model', {
        'product_name': fields.String(description='product name'),
        'product_description': fields.String(description='product description'),
        'product_quantity': fields.Integer(description='product stock quantity'),
        'product_category': fields.String(description='product category'),
        'product_moq': fields.Integer(description='product minimum order quantity')
    })

    product_response = product_ns.model('Product response for any get method', {
        'product_id': fields.String(description='Unique Id for every product'),
        'product_name': fields.String(description='product name'),
        'product_description': fields.String(description='product description'),
        'product_quantity': fields.String(description='product quantity'),
        'product_category': fields.String(description='product category'),
        'product_moq': fields.String(description='Minimum order quantity'),
        'product_quantity_store': fields.String(description='stock level'),
        'date_created': fields.String(description='date product was added to inventory'),
        'date_modified': fields.String(description='date product details were modified')
    })

class SalesDataTransferObject():
    pass

class LoginDataTransferObject():
    pass

class RegisterDataTransferObject():
    pass