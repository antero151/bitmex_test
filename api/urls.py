from rest_framework.routers import DefaultRouter

from accounts.views import AccountsViewSet
from orders.views import OrdersViewSet

router = DefaultRouter()

router.register(r'accounts', AccountsViewSet, basename='accounts')
router.register(r'(?P<account_name>[\w-]+)/orders', OrdersViewSet, basename='orders')
urlpatterns = router.urls
