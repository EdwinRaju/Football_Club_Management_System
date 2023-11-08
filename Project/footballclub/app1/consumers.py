import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth import get_user_model

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f"chat_{self.room_name}"

        # Join the room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        # Add the player to their individual group based on their role
        user = self.scope["user"]
        if user.role == "player":
            player_group_name = f"player_{user.email}"
            await self.channel_layer.group_add(player_group_name, self.channel_name)

        await self.accept()

    async def disconnect(self, close_code):
        # Leave the room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

        # Remove the player from their individual group based on their role
        user = self.scope["user"]
        if user.role == "player":
            player_group_name = f"player_{user.email}"
            await self.channel_layer.group_discard(player_group_name, self.channel_name)

    # ... (other methods)


    
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        to_player_email = text_data_json.get('to_player_email')
    
        if to_player_email:
            # Determine the WebSocket group for the recipient player
            player_group_name = f"player_{to_player_email}"
    
            # Send the message to the recipient's group
            await self.channel_layer.group_send(
                player_group_name,
                {
                    'type': 'chat.message',
                    'message': message
                }
            )
        else:
            # Broadcast the message to all players
            await self.channel_layer.group_send(
                f"chat_{self.room_name}",  # Use the room group name
                {
                    'type': 'chat.message',
                    'message': message
                }
            )
    

    
    async def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({'message': message}))

    async def send_private_message(self, to_player_email, message):
        # Determine the WebSocket group for the recipient player
        player_group_name = f"player_{to_player_email}"

        # Send the message to the recipient's group
        await self.channel_layer.group_send(
            player_group_name,
            {
                'type': 'chat.message',
                'message': message
            }
        )
