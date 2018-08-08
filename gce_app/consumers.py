from channels.generic.websocket import AsyncJsonWebsocketConsumer

class MainConsumer(AsyncJsonWebsocketConsumer):

    async def connect(self):
        if self.scope['user'].is_anonymous:
            self.close()
        else:
            await self.channel_layer.group_add(self.scope['user'].username, self.channel_name)
            await self.channel_layer.group_add('connected_users', self.channel_name)
            await self.accept()
            # print('connected')

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard('connected_users',self.channel_name)
        # print('disconnected')
        


    async def receive_json(self, content, **kwargs):
        # print('received')
        print(content['text'])
        # await self.channel_layer.group_send(
        #     'connected_users', {
        #         'type': 'user.notify',
        #         'content': 'this is for all connected users'
        #     })

        # await self.channel_layer.group_send(
        #     self.scope['user'].username, {
        #         'type': 'user.notify',
        #         'content': 'this is for the one making the call'
        #     })

    async def user_notify(self, event):
        await self.send_json({
                'data': event['content']
            })
