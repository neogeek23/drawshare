# drawshare/routing.py
from django.conf.urls import url

from . import consumers

websocket_urlpatterns = [
    url(r'^wss/drawshare/(?P<room_name>[^/]+)/$', consumers.DrawConsumer),
]