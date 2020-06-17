import bitmex
from rest_framework.exceptions import APIException


class BitMexClient:
    def __init__(self, account):
        try:
            self.client = bitmex.bitmex(api_key=account.api_key, api_secret=account.api_secret)
        except Exception as e:
            print(e)
            raise APIException(detail='bitmex api not available')

    def get_orders(self):
        result = self.make_request(self.client.Order.Order_getOrders(filter='{"ordStatus":"New"}'))
        return result

    def new_order(self, **kwargs):
        result = self.make_request(self.client.Order.Order_new(**kwargs))
        return result

    def cancel_order(self, order_id):
        result = self.make_request(self.client.Order.Order_cancel(orderID=order_id))
        return result

    @staticmethod
    def make_request(resource):
        try:
            result, status = resource.result()
            return result, status.status_code
        except Exception as e:
            return e.swagger_result, e.status_code
