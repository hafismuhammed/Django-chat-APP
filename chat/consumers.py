import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from django.contrib.auth import get_user_model
from django.utils.timezone import localtime, now
from .models import ChatRoom, Message
from .utils import get_or_create_chat_room, format_timestamp

User = get_user_model()

#temporary in-memory store
online_users = set()

class ChatConsumer(AsyncWebsocketConsumer):
    """
    Chat consumer for handling WebSocket connections.
    """
    
    async def connect(self):
       print("CONNECTED:", self.scope["user"])
       self.user = self.scope['user']

       if not self.user.is_authenticated:
           await self.close()
           return
       
       self.other_username = self.scope['url_route']['kwargs']['username']
       
       self.room_name = self.get_room_name(self.user.username, self.other_username)
       self.room_group_name = f"chat_{self.room_name}"

       await self.channel_layer.group_add(
           self.room_group_name,
           self.channel_name
       )
       
       online_users.add(self.user.username)

       await self.accept()
       
       #online status notify
       await self.channel_layer.group_send(
           self.room_group_name,
           {
               'type': 'user_status',
               'username': self.user.username,
               'status': 'online'
           }
       )
       
    async def disconnect(self, code):
        online_users.discard(self.user.username)
        
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        
        #offline status notify
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'user_status',
                'username': self.user.username,
                'status': 'offline'
            }
        )
        
        
    def get_room_name(self, user1, user2):
        return '_'.join(sorted([user1, user2]))
    
    
    async def receive(self, text_data):
        """
         Function to handle incoming WebSocket messages
        """
        print("RECEIVED:", text_data)
        data = json.loads(text_data)
        message = data.get('message')
        event_type = data.get('type', 'message')
        
        if event_type == 'typing':
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'typing_indicator',
                    'username': self.user.username
                }
            )
            return
        
        if event_type == "read_message":
            message_id = data.get("message_id")

            await sync_to_async(
                Message.objects.filter(id=message_id).update
            )(is_read=True)

            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": "message_read",
                    "message_id": message_id,
                    "reader": self.user.username
                }
            )
            return
        
        receiver = await sync_to_async(User.objects.get)(
            username=self.other_username
        )
        # get or create chat room
        chat_room = await sync_to_async(get_or_create_chat_room)(
            self.user,
            receiver
        )
        
        # Save messages
        message_obj = await sync_to_async(Message.objects.create)(
            chat_room=chat_room,
            sender=self.user,
            content=message
        )
        
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender': self.user.username,
                'timestamp': format_timestamp(message_obj.timestamp),
                'message_id': message_obj.id,
                'is_read': False
            }
        )
        
    async def chat_message(self, event):
        """
        Function to handle chat messages
        """
        await self.send(text_data=json.dumps({
            'type': 'message',
            'message': event['message'],
            'sender': event['sender'],
            'message_id': event.get('message_id'),
            'timestamp': event['timestamp'],
            'is_read': event.get('is_read')
        }))
        
    async def typing_indicator(self, event):
        """
        Function to handle typing indicators
        """
        await self.send(text_data=json.dumps({
            'type': 'typing',
            'username': event['username']
        }))
        
    async def user_status(self, event):
        await self.send(text_data=json.dumps({
            'type': 'user_status',
            'username': event['username'],
            'status': event['status']
        }))
        
    async def message_read(self, event):
        await self.send(text_data=json.dumps({
            "type": "message_read",
            "message_id": event["message_id"],
            "reader": event["reader"]
        }))
        
        
        
        
    
    
