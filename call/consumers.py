import json

from channels.generic.websocket import AsyncWebsocketConsumer


class VideoCallConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']

        await self.channel_layer.group_add(
            self.room_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, code):
        await self.channel_layer.group_discard(
            self.room_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        print(text_data_json) # TODO: print 지우기
        event_type = text_data_json['type']

        if event_type == 'offer':
            await self.channel_layer.group_send(
                self.room_name,
                {
                    'type': 'call_received',
                    'data': text_data_json['offer']
                }
                )

            await self.channel_layer.send(self.room_name, {'data': text_data_json['offer']})
                
        if event_type == 'answer':
            await self.channel_layer.group_send(
                self.room_name,
                {
                    'type': 'call_answered',
                    'data': text_data_json['data']
                }
            )

        if event_type == 'ICEcandidate':
            await self.channel_layer.group_send(
                self.room_name,
                {
                    'type': 'ICEcandidate',
                    'data': text_data_json['data']
                }
            )

    async def call_received(self, event):
            await self.send(text_data=json.dumps(
                    {
                        'type': 'call_received',
                        'data': event['data']
                    }
                )
            )

    async def call_answered(self, event):
            await self.send(text_data=json.dumps(
                    {
                        'type' : 'call_answered',
                        'data' : event['data'],
                        'offer': await self.channel_layer.receive(self.room_name) 
                    }
                )
            )

    async def ICEcandidate(self, event):
            await self.send(text_data=json.dumps(
                    {
                        'type': 'ICEcandidate',
                        'data': event['data']
                    }
                )
            )