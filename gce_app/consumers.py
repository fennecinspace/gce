from channels.generic.websocket import AsyncJsonWebsocketConsumer

class MainConsumer(AsyncJsonWebsocketConsumer):

    async def connect(self):
        await self.channel_layer.group_add('connectedUsers', self.channel_name)
        await self.accept()

        print('connected')

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard('connectedUsers',self.channel_name)
        print('disconnected')
        


    async def receive_json(self, content, **kwargs):
        print('received')
        await self.channel_layer.group_send(
            'connectedUsers', {
                'type': 'connectedUsers.notify',
                'content': 'this is a group message'
            })

        await self.send_json({
                'content': 'this is a message for the one making the call'
            })

    async def connectedUsers_notify(self, event):
        print(event)
        await self.send_json({
                'content': event['content']
            })
        # await self.send({
        #     'type': 'connectedUsers_notify',
        #     'text': event['text']
        # })
