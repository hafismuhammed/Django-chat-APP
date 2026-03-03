from django.db.models import Count
from .models import ChatRoom
from django.utils.timezone import localtime, now


def get_or_create_chat_room(user1, user2):
    """
    Function to get or create a chat room between two users.

    Args:
        user1 (obj): User object represents the first user
        user2 (obj): User object represents the second user

    Returns:
        obj: ChatRoom object
    """
    
    chat_rooms = ChatRoom.objects.annotate(
        num_users=Count('chat_users')
    ).filter(
        num_users=2,
        chat_users=user1
        ).filter(
            chat_users=user2
        )
        
    if chat_rooms.exists():
        return chat_rooms.first()
    
    chat_room = ChatRoom.objects.create()
    chat_room.chat_users.add(user1, user2)
    return chat_room

def format_timestamp(timestamp):
    """
    Function to format timestamps for display.

    Args:
        timestamp (datetime): The timestamp to format.

    Returns:
        str: The formatted timestamp.
    """
    timestamp = localtime(timestamp)

    if timestamp.date() == now().date():
        formatted_time = timestamp.strftime("%I:%M %p")
    else:
        formatted_time = timestamp.strftime("%d %b %Y, %I:%M %p")

    return formatted_time