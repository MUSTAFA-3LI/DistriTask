# chat/urls.py
from django.urls import path

from chat import consumers
from . import views

app_name = "chat"

urlpatterns = [
    path('chat/', views.chat_page, name='chat_page'),
    path('employee/', views.employee_chat_page, name='employee_chat'),
    path('private/<str:email>/', views.manager_private_chat, name='manager_private_chat'),
    path('messages/', views.message_list, name='chat_messages'),  # إضافة هذا المسار
    path('unread_counts/', views.unread_counts, name='unread_counts'),
    path('mark_read/', views.mark_read, name='mark_read'),    
]
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.urls import re_path

websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<room_name>\w+)/$', consumers.ChatConsumer.as_asgi()),
]

# التأكد من أن التوجيه يشمل WebSocket
application = ProtocolTypeRouter({
    'websocket': AuthMiddlewareStack(
        URLRouter(
            websocket_urlpatterns
        )
    ),
})