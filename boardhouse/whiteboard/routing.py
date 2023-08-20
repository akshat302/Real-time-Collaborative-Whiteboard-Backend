# routing.py
from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r'^whiteboard/(?P<board_id>[0-9a-f\-]{32,})$', consumers.WhiteBoardConsumer.as_asgi()),
]