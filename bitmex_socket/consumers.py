import asyncio

from channels.db import database_sync_to_async
from channels.exceptions import DenyConnection, StopConsumer
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from django.core.exceptions import ValidationError

from accounts.models import Account
from utils.bitmex_ws import BitmexWS


class BitmexConsumer(AsyncJsonWebsocketConsumer):
    bitmex_instrument_group = 'bitmex-instrument'
    instrument_task = None
    connections = []

    async def connect(self):
        BitmexConsumer.connections.append(self.channel_name)
        await self.check_run_instrument_socket()
        await self.accept()

    async def websocket_disconnect(self, close_code):
        BitmexConsumer.connections.remove(self.channel_name)
        if len(self.connections) == 0:
            BitmexConsumer.instrument_task.cancel()
            BitmexConsumer.instrument_task = None
        await self.channel_layer.group_discard(
            self.bitmex_instrument_group,
            self.channel_name
        )
        raise StopConsumer()

    async def receive_json(self, content, **kwargs):
        # Send message to room group
        action = content.get('action')
        account_name = content.get('account')
        await self.check_user_data(account_name)
        if action == 'subscribe':
            await self.action_subscribe()
        elif action == 'unsubscribe':
            await self.action_unsubscribe()
        else:
            raise DenyConnection("wrong action")

    async def action_subscribe(self):
        await self.channel_layer.group_add(
            self.bitmex_instrument_group,
            self.channel_name
        )

    async def action_unsubscribe(self):
        await self.channel_layer.group_discard(
            self.bitmex_instrument_group,
            self.channel_name
        )

    async def check_run_instrument_socket(self):
        if not BitmexConsumer.instrument_task:
            BitmexConsumer.instrument_task = asyncio.create_task(self.run_instrument_output())

    async def run_instrument_output(self):
        ws = BitmexWS()
        ws.subscribe_topic('instrument')
        while True:
            message = ws.receive()
            if message:
                await self.channel_layer.group_send(
                    self.bitmex_instrument_group,
                    {
                        'type': 'instrument_message',
                        'message': message
                    }
                )
            await asyncio.sleep(0.1)

    async def instrument_message(self, event):
        message = event['message']

        await self.send_json({
            'message': message
        })

    async def check_user_data(self, account_name):
        if not account_name:
            await self.send_json({'message': "account name is required"})
            await self.close()
        self.account = await self.get_account(account_name)
        if not self.account:
            await self.send_json({'message': "account does not exist"})
            await self.close()

    @database_sync_to_async
    def get_account(self, account_name):
        account = None
        try:
            account = Account.objects.filter(
                name=account_name
            ).values('name', 'api_key', 'api_secret').first()
        except ValidationError:
            pass
        return account
