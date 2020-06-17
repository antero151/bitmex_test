from rest_framework import viewsets

from accounts.models import Account
from accounts.serializers import AccountSerializer


class AccountsViewSet(viewsets.ModelViewSet):
    serializer_class = AccountSerializer
    queryset = Account.objects.all()
