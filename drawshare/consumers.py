# drawshare/consumers.py
from channels.generic.websocket import AsyncWebsocketConsumer
import json


class DrawConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'drawshare_%s' % self.room_name

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        color = text_data_json['color']
        x1 = text_data_json['x1']
        y1 = text_data_json['y1']
        x2 = text_data_json['x2']
        y2 = text_data_json['y2']

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'drawshare_message',
                'color': color,
                'x1': x1,
                'y1': y1,
                'x2': x2,
                'y2': y2
            }
        )

    async def drawshare_message(self, event):
        color = event['color']
        x1 = event['x1']
        y1 = event['y1']
        x2 = event['x2']
        y2 = event['y2']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'color': color,
            'x1': x1,
            'y1': y1,
            'x2': x2,
            'y2': y2,
        }))
