from django.db import models

from utils.models import CUDate

SIDE_BUY = 'Buy'
SIDE_SELL = 'Sell'

SIDE_CHOICES = (
    (SIDE_BUY, 'Buy'),
    (SIDE_SELL, 'Sell'),
)

STATUS_OPEN = 'open'
STATUS_CANCELED = 'canceled'
STATUS_FAILED = 'failed'
STATUS_CLOSED = 'closed'

STATUS_CHOICES = (
    (STATUS_OPEN, 'Open'),
    (STATUS_CANCELED, 'Canceled'),
    (STATUS_FAILED, 'Failed'),
    (STATUS_CLOSED, 'Closed'),
)


class Order(CUDate):
    order_id = models.CharField(max_length=50, unique=True)
    symbol = models.CharField(max_length=10)
    volume = models.IntegerField()
    timestamp = models.DateTimeField()
    side = models.CharField(max_length=5, choices=SIDE_CHOICES)
    price = models.FloatField()
    account = models.ForeignKey('accounts.Account', on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=STATUS_OPEN, blank=True)
