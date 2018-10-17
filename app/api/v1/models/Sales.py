"""Sale Model and Data storage functions"""
from datetime import datetime



class Sales():
    """This class defines the Sales Model and
        the various methods of manipulating the Sales data"""

    sale_id = 1
    salesList = []

    def __init__(self, made_by, cart, cart_price):
        """Initialize the Sales Model with constructor"""

        self.id = len(Sales.salesList) + 1
        self.cart = cart
        self.made_by = made_by
        self.cart_price = cart_price
        self.date_created = datetime.now()
        self.date_modified = datetime.now()

    def post_sales(self):
        """Sale method to make a sale record"""

        sale_item = dict(
            id=self.id,
            cart=self.cart,
            made_by=self.made_by,
            cart_price=self.cart_price,
            date_created=self.date_created,
            date_modified=self.date_modified
        )
        Sales.salesList.append(sale_item)
        return sale_item

    def fetch_all_sales(self):
        """Sale method to fetch all sales"""
        return Sales.salesList

    @staticmethod
    def fetch_single_sale(saleId):
        """Sale method to fetch a single sale record"""
        sale_record = [sale for sale in Sales.salesList if sale['id'] == saleId]
        if sale_record:
            return sale_record
        return 'not found'