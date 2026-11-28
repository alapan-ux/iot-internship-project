"""
Week 4: Device Integration and Interoperability Testing
IoT Smart Home simulation (software-only; no physical hardware required).

Run:
    python iot_device_simulation.py

Outputs:
    simulation_log.csv
    test_summary.txt
"""
import csv
import time
from dataclasses import dataclass
from datetime import datetime

@dataclass
class Message:
    topic: str
    payload: dict
    timestamp: str
    source: str

class Device:
    def __init__(self, device_id):
        self.device_id = device_id

    def publish(self, topic, payload):
        return Message(topic, payload, datetime.now().isoformat(timespec="seconds"), self.device_id)

class TemperatureSensor(Device):
    def read(self, value_c):
        return self.publish("home/sensor/temperature", {"value": value_c, "unit": "C"})

class MotionSensor(Device):
    def read(self, detected):
        return self.publish("home/sensor/motion", {"detected": bool(detected)})

class Actuator(Device):
    def __init__(self, device_id):
        super().__init__(device_id)
        self.state = "OFF"

    def command(self, state):
        self.state = state
        return self.publish(f"home/actuator/{self.device_id}/command", {"state": state})

class MQTTStyleBroker:
    """Small in-memory broker demonstrating topic-based message routing."""
    def __init__(self):
        self.subscribers = {}
        self.messages = []

    def subscribe(self, topic, callback):
        self.subscribers.setdefault(topic, []).append(callback)

    def publish(self, message):
        self.messages.append(message)
        for topic, callbacks in self.subscribers.items():
            if topic == message.topic:
                for callback in callbacks:
                    callback(message)

def main():
    broker = MQTTStyleBroker()
    fan = Actuator("fan")
    light = Actuator("light")
    events = []

    def log_event(message, result):
        events.append({
            "timestamp": message.timestamp,
            "source": message.source,
            "topic": message.topic,
            "payload": str(message.payload),
            "result": result
        })

    def on_temperature(message):
        value = message.payload.get("value")
        if isinstance(value, (int, float)) and message.payload.get("unit") == "C":
            state = "ON" if value >= 28 else "OFF"
            command = fan.command(state)
            log_event(message, f"VALID; fan={state}")
            log_event(command, f"COMMAND; fan={state}")
        else:
            log_event(message, "ERROR; invalid temperature format")

    def on_motion(message):
        detected = message.payload.get("detected")
        if isinstance(detected, bool):
            state = "ON" if detected else "OFF"
            command = light.command(state)
            log_event(message, f"VALID; light={state}")
            log_event(command, f"COMMAND; light={state}")
        else:
            log_event(message, "ERROR; invalid motion format")

    broker.subscribe("home/sensor/temperature", on_temperature)
    broker.subscribe("home/sensor/motion", on_motion)

    temperature = TemperatureSensor("temp-01")
    motion = MotionSensor("motion-01")

    # Test scenarios: normal values, threshold boundary, and malformed payload.
    test_messages = [
        temperature.read(31.5),   # fan ON
        temperature.read(24.0),   # fan OFF
        motion.read(True),        # light ON
        motion.read(False),       # light OFF
        temperature.publish("home/sensor/temperature", {"value": "hot", "unit": "C"}),
        motion.publish("home/sensor/motion", {"detected": "yes"}),
    ]

    for message in test_messages:
        broker.publish(message)

    # CSV evidence log
    with open("simulation_log.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["timestamp", "source", "topic", "payload", "result"])
        writer.writeheader()
        writer.writerows(events)

    passed = sum(1 for e in events if e["result"].startswith(("VALID", "COMMAND")))
    errors = sum(1 for e in events if e["result"].startswith("ERROR"))
    summary = (
        "WEEK 4 SIMULATION SUMMARY\n"
        f"Sensor input messages: {len(test_messages)}\n"
        f"Logged events (including actuator commands): {len(events)}\n"
        f"Valid processing / command events: {passed}\n"
        f"Rejected malformed messages: {errors}\n"
        f"Final fan state: {fan.state}\n"
        f"Final light state: {light.state}\n"
        "Note: Results are from a local software simulation, not physical hardware testing.\n"
    )
    with open("test_summary.txt", "w", encoding="utf-8") as f:
        f.write(summary)
    print(summary)

if __name__ == "__main__":
    main()
