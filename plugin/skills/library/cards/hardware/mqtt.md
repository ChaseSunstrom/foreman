---
name: mqtt
title: MQTT
area: hardware
tags: [mqtt, iot, broker, messaging, mosquitto, pubsub]
detect: [dep:paho-mqtt, dep:aiomqtt, dep:mqtt, dep:rumqttc, dep:mqtt.js, dep:MQTTnet, file:mosquitto.conf]
related: [home-assistant, raspberry-pi, python]
---
MQTT publish/subscribe: topic design, QoS, retained messages, last will, and Mosquitto for local testing.

## Verify
- `mosquitto -c mosquitto.conf -v`: the broker config parses and the broker starts (stop with Ctrl-C).
- `mosquitto_sub -h localhost -t 'app/#' -v -C 1 -W 10`: one message arrives on the topic tree within 10 seconds.
- `mosquitto_pub -h localhost -t app/test -m ping -q 1`: a QoS 1 publish is accepted.
- `mosquitto_sub -h localhost -t 'app/+/status' -v`: retained status messages show immediately on subscribe.

## Test first
Run a throwaway local broker for tests and assert a round trip through it. Fail first on the missing publish.
```python
import paho.mqtt.client as mqtt, queue

def test_device_publishes_status(broker_port):
    q = queue.Queue()
    c = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    c.on_message = lambda cl, ud, m: q.put(m)
    c.connect("localhost", broker_port)
    c.subscribe("app/dev1/status", qos=1)
    c.loop_start()
    start_device("dev1", broker_port)
    assert q.get(timeout=5).payload == b"online"
    c.loop_stop()
```
Start `mosquitto` on a random port in a fixture (or a container). Keep topic building and payload parsing in pure functions with their own unit tests.

## Do
- Design topics hierarchically and lowercase: `site/device/measurement`; no leading slash, no spaces; use `+` and `#` only when subscribing.
- Pick QoS per message: 0 for lossy telemetry, 1 for commands (handle duplicates idempotently), 2 only when needed.
- Publish device presence with a last will (`will_set`) and a retained `online` message on connect.
- Retain state topics, not events; clear a retained message by publishing an empty payload with retain.
- Use unique client IDs per process; reconnect with backoff and resubscribe in `on_connect`.
- Enable TLS and authentication on any broker beyond localhost; restrict topics with an ACL file.
- Use a payload schema (JSON with a version field, or protobuf) and validate on receipt.
- Keep message handlers fast; hand work to a queue.

## Avoid
- paho-mqtt 1.x call style in 2.x: `mqtt.Client()` without a `CallbackAPIVersion` raises. Pass `mqtt.CallbackAPIVersion.VERSION2` and use the new callback signatures.
- Two clients with the same client ID: the broker disconnects the first and they flap. Make IDs unique.
- Subscribing in code before the connection is up or only once: subscriptions are lost on reconnect with a clean session. Subscribe in `on_connect`.
- Calling `loop_forever` and blocking the thread you need: use `loop_start` or an async client.
- `allow_anonymous true` on an exposed Mosquitto listener: open broker. Require passwords or certs.
- Publishing large payloads or per-sample bursts at QoS 2: throughput collapses. Batch and lower QoS.
- Topic names that embed unbounded values (timestamps, UUIDs per message): the topic tree grows without bound.

## Review
- [ ] Topic names follow one documented hierarchy with no wildcards in publishes.
- [ ] QoS, retain and last will are chosen on purpose for each topic.
- [ ] Reconnect resubscribes and handlers are idempotent.
- [ ] Credentials, TLS and ACLs exist for non-local brokers; no secrets in code.
- [ ] A broker-backed test covers publish and receive.
