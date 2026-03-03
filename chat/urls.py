from django.urls import path
from .import views

urlpatterns = [
   path('chat-room/<str:username>/', views.ChatView.as_view(), name='chat_room'),
   path('load-messages/<int:chat_room_id>/', views.LoadMessageView.as_view(), name='load_messages'),
]