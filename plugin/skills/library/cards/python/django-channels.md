---
name: django-channels
title: Django Channels
area: python
tags: [python, django, channels, websocket, asgi, realtime]
detect: [dep:channels, dep:channels-redis, dep:daphne]
related: [django, asyncio, pytest-asyncio, celery]
---
Django Channels: ASGI consumers, channel layers and groups for WebSockets and background workers.

## Verify
- `python manage.py check`: `ASGI_APPLICATION` and `CHANNEL_LAYERS` settings are valid.
- `python -c "import config.asgi"` (your asgi module): the ProtocolTypeRouter and URL routes import cleanly.
- `pytest -q`: consumer tests with `channels.testing.WebsocketCommunicator`.
- `daphne -b 127.0.0.1 -p 8000 config.asgi:application`: serves WebSockets locally.

## Test first
```python
import pytest
from channels.testing import WebsocketCommunicator
from config.asgi import application

@pytest.mark.asyncio
@pytest.mark.django_db(transaction=True)
async def test_anonymous_rejected():
    comm = WebsocketCommunicator(application, "/ws/chat/room1/")
    connected, _ = await comm.connect()
    assert not connected
```
Use `transaction=True` because consumers run DB code in threads. Set `CHANNEL_LAYERS` to `channels.layers.InMemoryChannelLayer` in test settings.

## Do
- Subclass `AsyncJsonWebsocketConsumer`. Join groups in `connect()` with `await self.channel_layer.group_add(group, self.channel_name)` and leave in `disconnect()`.
- Wrap the router: `AuthMiddlewareStack(URLRouter(...))` inside `AllowedHostsOriginValidator`.
- Reject unauthenticated users in `connect()` with `await self.close()` before `accept()`.
- Broadcast with `group_send(group, {"type": "chat.message", ...})`: the dotted type maps to the handler `chat_message`.
- Use Redis (`channels_redis.core.RedisChannelLayer`) in production, with `hosts` in `CONFIG`.
- Wrap ORM access in `database_sync_to_async`.
- Send from sync code with `async_to_sync(channel_layer.group_send)(...)`.

## Avoid
- Calling the ORM directly in an async consumer: `SynchronousOnlyOperation`. Wrap with `database_sync_to_async`.
- `InMemoryChannelLayer` in multi-process production: groups do not span processes. Use Redis.
- Skipping the origin validator: cross-site WebSocket hijacking. Wrap with `AllowedHostsOriginValidator`.
- A `type` with no matching handler method: the message is dropped with an error. Name the handler `type.replace(".", "_")`.
- Trusting client JSON: validate the payload and permissions on every receive, not only at connect.
- Blocking calls in async consumers: they stall every socket on the worker.

## Review
- [ ] Connect checks auth and permission for the specific room or object.
- [ ] Origin validation wraps the WebSocket router.
- [ ] Production channel layer is Redis, with `group_expiry` and capacity set deliberately.
- [ ] Every `group_add` has a matching `group_discard` in `disconnect`.
- [ ] Tests cover connect rejection, one message round trip and disconnect.
