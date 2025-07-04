import json
import re
from channels.generic.websocket import AsyncWebsocketConsumer
from django.utils import timezone
from .models import Message
from users.models import User
from asgiref.sync import sync_to_async

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        clean_room_name = re.sub(r'[^a-zA-Z0-9\-_\.]', '_', self.room_name)
        self.room_group_name = f'chat_{clean_room_name}'

        if not clean_room_name or '__' not in clean_room_name:
            print(f"Invalid room name: {self.room_name}")
            await self.close()
            return

        print(f"Connecting to group: {self.room_group_name}")
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        try:
            user = self.scope["user"]
            if user.is_authenticated:
                if user.role == 'manager':
                    print(f"Manager {user.email} joining manager_notifications group")
                    await self.channel_layer.group_add(
                        'manager_notifications',
                        self.channel_name
                    )
                elif user.role == 'employee':
                    print(f"Employee {user.email} going online")
                    await self.channel_layer.group_send(
                        'manager_notifications',
                        {
                            'type': 'user_status',
                            'email': user.email,
                            'status': 'online'
                        }
                    )
        except Exception as e:
            print(f"Error handling user connection: {str(e)}")

        await self.accept()

    async def disconnect(self, close_code):
        if hasattr(self, 'room_group_name'):
            print(f"Disconnecting from group: {self.room_group_name}")
            await self.channel_layer.group_discard(
                self.room_group_name,
                self.channel_name
            )
        try:
            user = self.scope["user"]
            if user.is_authenticated and user.role == 'employee':
                print(f"Employee {user.email} going offline")
                await self.channel_layer.group_send(
                    'manager_notifications',
                    {
                        'type': 'user_status',
                        'email': user.email,
                        'status': 'offline'
                    }
                )
            elif user.is_authenticated and user.role == 'manager':
                print(f"Manager {user.email} leaving manager_notifications group")
                await self.channel_layer.group_discard(
                    'manager_notifications',
                    self.channel_name
                )
        except Exception as e:
            print(f"Error handling user disconnect: {str(e)}")

    async def receive(self, text_data):
        print(f"Received WebSocket data: {text_data}")
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        sender_email = text_data_json['sender']
        receiver_email = text_data_json.get('receiver', None)

        try:
            sender = await sync_to_async(User.objects.get)(email=sender_email)
            receiver = await sync_to_async(User.objects.get)(email=receiver_email) if receiver_email else None
            msg = await sync_to_async(Message.objects.create)(
                sender=sender,
                receiver=receiver,
                content=message
            )
            timestamp = msg.timestamp.strftime("%Y-%m-%d %H:%M:%S")
            print(f"Message saved: {message} from {sender_email} to {receiver_email}")
        except User.DoesNotExist:
            print(f"Error: Invalid sender ({sender_email}) or receiver ({receiver_email})")
            await self.send(text_data=json.dumps({'error': 'Invalid sender or receiver'}))
            return
        except Exception as e:
            print(f"Error saving message: {str(e)}")
            await self.send(text_data=json.dumps({'error': f'Error saving message: {str(e)}'}))
            return

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender': sender_email,
                'timestamp': timestamp,
                'is_read': msg.is_read
            }
        )

        if sender.role == 'employee' and receiver and receiver.role == 'manager':
            print(f"Sending unread_update for {sender_email} to manager_notifications")
            await self.channel_layer.group_send(
                'manager_notifications',
                {
                    'type': 'unread_update',
                    'sender_email': sender_email
                }
            )

    async def chat_message(self, event):
        print(f"Sending chat_message: {event}")
        await self.send(text_data=json.dumps({
            'type': 'chat_message',
            'message': event['message'],
            'sender': event['sender'],
            'timestamp': event['timestamp'],
            'is_read': event['is_read']
        }))

    async def unread_update(self, event):
        print(f"Sending unread_update for {event['sender_email']} to client")
        await self.send(text_data=json.dumps({
            'type': 'unread_update',
            'sender_email': event['sender_email']
        }))

    async def user_status(self, event):
        print(f"Sending user_status: {event['email']} is {event['status']}")
        await self.send(text_data=json.dumps({
            'type': 'user_status',
            'email': event['email'],
            'status': event['status']
        }))