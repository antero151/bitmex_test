from rest_framework import serializers

from accounts.models import Account
from orders.models import Order, SIDE_CHOICES
from utils.bitmex import BitMexClient


class OrderSerializer(serializers.ModelSerializer):
    account = serializers.PrimaryKeyRelatedField(queryset=Account.objects.all(), required=False)

    class Meta:
        model = Order
        fields = ('id', 'order_id', 'symbol', 'volume', 'timestamp', 'side', 'price', 'account')

    def validate(self, attrs):
        account = self.context.get('account')
        if account:
            attrs['account_id'] = account.id
        else:
            raise serializers.ValidationError('account name is not valid')
        return attrs


class CreateOrderSerializer(serializers.Serializer):
    symbol = serializers.CharField()
    side = serializers.ChoiceField(choices=SIDE_CHOICES)
    orderQty = serializers.FloatField()
    price = serializers.FloatField()

    def save(self, **kwargs):
        account = self.context.get('account')
        bitmex_client = BitMexClient(account)
        result, status = bitmex_client.new_order(**self.validated_data)
        if status == 200:
            order_data = {
                'order_id': result.get('orderID'),
                'symbol': result.get('symbol'),
                'side': result.get('side'),
                'volume': result.get('orderQty'),
                'timestamp': result.get('timestamp'),
                'price': result.get('price'),
                'account': account,
            }
            order = Order.objects.create(**order_data)
            return order
        else:
            raise serializers.ValidationError(result)
