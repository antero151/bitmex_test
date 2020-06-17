from rest_framework import status
from rest_framework.response import Response

from orders.models import Order, STATUS_CANCELED, STATUS_OPEN, STATUS_CLOSED
from orders.serializers import OrderSerializer, CreateOrderSerializer
from utils.bitmex import BitMexClient
from utils.views import get_account_by_name, MultiSerializerViewSet


class OrdersViewSet(MultiSerializerViewSet):
    serializers = {
        'default': OrderSerializer,
        'create': CreateOrderSerializer
    }

    def dispatch(self, request, *args, **kwargs):
        self.account = get_account_by_name(self.kwargs.get('account_name', None))
        return super(OrdersViewSet, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        if self.account:
            return Order.objects.filter(account_id=self.account.id, status=STATUS_OPEN)
        else:
            return []

    def get_serializer_context(self):
        context = super(OrdersViewSet, self).get_serializer_context()
        context['account'] = self.account
        return context

    def list(self, request, *args, **kwargs):

        queryset = self.filter_queryset(self.get_queryset())
        bitmex_client = BitMexClient(self.account)
        result, status = bitmex_client.get_orders()
        if result:
            order_ids = [order['orderID'] for order in result]
            queryset = queryset.filter(order_id__in=order_ids)
        else:
            queryset = []

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        bitmex_client = BitMexClient(self.account)
        instance = self.get_object()

        result, _status = bitmex_client.cancel_order(instance.order_id)
        if _status == 200:
            instance.status = STATUS_CANCELED
        else:
            instance.status = STATUS_CLOSED
        instance.save()

        print(instance, _status)
        return Response(status=status.HTTP_204_NO_CONTENT)



