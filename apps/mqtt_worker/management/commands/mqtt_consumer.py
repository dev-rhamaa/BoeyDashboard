"""Django management command to run an MQTT consumer that stores sensor data.

Run with:

    python manage.py mqtt_consumer

Environment variables (can be placed in .env):
    MQTT_BROKER       - Hostname of the MQTT broker (default: broker.emqx.io)
    MQTT_PORT         - Port (int, default: 1883)
    MQTT_TOPIC        - Topic to subscribe to (supports wildcards)
"""

import json
import logging
import os
from datetime import datetime

import paho.mqtt.client as mqtt
from django.core.management.base import BaseCommand
from django.utils import timezone

from apps.boey.models import SensorReading

logger = logging.getLogger(__name__)

BROKER = os.getenv("MQTT_BROKER", "broker.emqx.io")
PORT = int(os.getenv("MQTT_PORT", 1883))
TOPIC = os.getenv("MQTT_TOPIC", "boey2025-kirei/#")
CLIENT_ID = os.getenv("MQTT_CLIENT_ID", "django-mqtt-consumer")


class Command(BaseCommand):
    help = "Starts an MQTT client to consume sensor data and store it in the database."

    def handle(self, *args, **options):
        self.stdout.write(
            self.style.SUCCESS(
                f"Connecting to MQTT broker {BROKER}:{PORT} and subscribing to {TOPIC}"
            )
        )

        client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1, CLIENT_ID)
        client.on_connect = self.on_connect
        client.on_message = self.on_message
        client.on_disconnect = self.on_disconnect

        # Stash client on self so callbacks can access DB
        self.client = client

        try:
            client.connect(BROKER, PORT, 60)
        except Exception as exc:
            self.stderr.write(self.style.ERROR(f"MQTT connection failed: {exc}"))
            return

        client.loop_forever()

    # Callback methods -----------------------------------------------------

    def on_connect(self, client, userdata, flags, rc):  # noqa: N802
        if rc == 0:
            logger.info("Connected to MQTT broker")
            client.subscribe(TOPIC)
        else:
            logger.error("Failed to connect, return code %s", rc)

    def on_disconnect(self, client, userdata, rc):  # noqa: N802
        logger.warning("Disconnected from MQTT broker with rc=%s", rc)

    def on_message(self, client, userdata, msg):  # noqa: N802
        payload = msg.payload.decode()
        logger.debug("Received message on %s: %s", msg.topic, payload)

        try:
            data = json.loads(payload)
        except json.JSONDecodeError:
            logger.error("Invalid JSON payload: %s", payload)
            return

        try:
            timestamp = datetime.strptime(data["timestamp"], "%Y-%m-%d %H:%M:%S")
            timestamp = timezone.make_aware(timestamp)
        except (KeyError, ValueError):
            timestamp = timezone.now()

        try:
            latitude, longitude = data.get("geolocation", [0, 0])

            SensorReading.objects.create(
                timestamp=timestamp,
                sensor_id=data.get("sensor_id", "unknown"),
                ph=data.get("ph"),
                turbidity_ntu=data.get("turbidity_ntu"),
                do_mg_l=data.get("do_mg_l"),
                ec_us_cm=data.get("ec_us_cm"),
                temperature_c=data.get("temperature_c"),
                latitude=latitude,
                longitude=longitude,
            )
            logger.info("Stored sensor reading from %s", data.get("sensor_id"))
        except Exception as exc:  # pylint: disable=broad-except
            logger.exception("Failed to save sensor reading: %s", exc)
