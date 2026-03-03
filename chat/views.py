from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.http import JsonResponse
from django.contrib.auth import get_user_model
from django.utils.timezone import localtime, now
from .models import ChatRoom, Message
from .utils import get_or_create_chat_room, format_timestamp

User = get_user_model()

class ChatView(LoginRequiredMixin, View):
    
    def get(self, request, username):
        other_user = User.objects.get(username=username)
        chat_room = get_or_create_chat_room(
            request.user, other_user
        )
        queryset = chat_room.messages.order_by('-timestamp')[:20]
        messages = list(reversed(queryset))
        
        chat_room.messages.filter(
            sender=other_user,
            is_read=False
        ).update(is_read=True)
        
        oldest_message_id = messages[0].id if messages else None
        
        return render(request, 'chat.html', {
            'chat_room': chat_room,
            'messages': messages,
            'other_user': other_user,
            'today': localtime(now()).date(),
            'oldest_message_id': oldest_message_id
        })
    
    
class LoadMessageView(LoginRequiredMixin, View):
    
    PAGE_SIZE = 20
    
    def get(self,request, chat_room_id):
        cursor = request.GET.get('cursor')

        chat_room = ChatRoom.objects.get(
            id=chat_room_id,
            chat_users=request.user
        )
        queryset = chat_room.messages.order_by('-timestamp')
        
        if cursor:
            queryset = queryset.filter(id__lt=int(cursor))
        messages = list(queryset[:self.PAGE_SIZE + 1])
        
        has_next = len(messages) > self.PAGE_SIZE
        messages = messages[:self.PAGE_SIZE]
        messages.reverse()
        
        data = [
            {
                'id': msg.id,
                'sender': msg.sender.username,
                'content': msg.content,
                'timestamp': format_timestamp(msg.timestamp),
            }
            for msg in messages
        ]
        next_cursor = messages[0].id if messages else None
        return JsonResponse({
            'messages': data,
            'has_next': has_next,
            'next_cursor': next_cursor
        })
