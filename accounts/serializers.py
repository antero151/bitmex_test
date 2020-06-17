from rest_framework import serializers
from accounts.models import Account


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ('name', 'api_key', 'api_secret')
