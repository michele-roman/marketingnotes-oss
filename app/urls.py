from django.urls import path
from app.views import (
    home, 
    ChatListView, 
    ChatDetailView, 
    ChatCreateView, 
    ChatUpdateView,
    send_message,
    select_ai_response,
    add_text_to_custom,
    update_custom_response,
    APIKeysView
)

urlpatterns = [
    path("", home, name="home"),
    path("chat/", ChatListView.as_view(), name="chat-list"),
    path("chat/new/", ChatCreateView.as_view(), name="chat-create"),
    path("chat/<int:pk>/", ChatDetailView.as_view(), name="chat-detail"),
    path("chat/<int:pk>/edit/", ChatUpdateView.as_view(), name="chat-update"),
    path("chat/<int:chat_id>/send/", send_message, name="send-message"),
    path("chat/<int:chat_id>/select-response/", select_ai_response, name="select-ai-response"),
    path("chat/<int:chat_id>/add-to-custom/", add_text_to_custom, name="add-to-custom"),
    path("chat/<int:chat_id>/update-custom/", update_custom_response, name="update-custom-response"),
    path("api-keys/", APIKeysView.as_view(), name="api-keys"),
]
