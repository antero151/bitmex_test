from rest_framework import mixins, viewsets

from accounts.models import Account
from django.core.exceptions import ValidationError


class MultiSerializerViewSet(mixins.ListModelMixin,
                             mixins.RetrieveModelMixin,
                             mixins.CreateModelMixin,
                             mixins.DestroyModelMixin,
                             viewsets.GenericViewSet):
    serializers = {
        'default': None,
    }

    def get_serializer_class(self):
        return self.serializers.get(self.action, self.serializers['default'])


def get_account_by_name(account_name):
    try:
        account = Account.objects.get(name=account_name)
        return account
    except (Account.DoesNotExist, ValidationError):
        return None
