"""
Week 3 - Simulating IoT Communication Protocols
A dependency-free MQTT-style communication simulation.

Scenario:
- Three IoT sensor nodes publish readings to a central broker.
- A monitoring client subscribes to the sensor topic.
- The broker forwards messages to the subscriber.
- Simulated latency and occasional message delivery failures are recorded.
This is a protocol-behaviour simulation, not a live MQTT broker connection.
"""

import random
import time
import csv
import statistics
from dataclasses import dataclass, asdict
from pathlib import Path

RANDOM_SEED = 21
TOTAL_MESSAGES_PER_DEVICE = 10
LATENCY_MIN_MS = 20
LATENCY_MAX_MS = 120
FAILURE_RATE = 0.08
OUTPUT_DIR = Path(__file__).resolve().parent

@dataclass
class Message:
    device_id: str
    topic: str
    payload: str
    sequence: int
    timestamp_s: float

class IoTDevice:
    def __init__(self, device_id, sensor_type, topic):
        self.device_id = device_id
        self.sensor_type = sensor_type
        self.topic = topic

    def create_message(self, sequence, rng):
        if self.sensor_type == "temperature":
            value = round(rng.uniform(22.0, 34.0), 2)
            unit = "C"
        elif self.sensor_type == "humidity":
            value = round(rng.uniform(35.0, 80.0), 2)
            unit = "%"
        else:
            value = round(rng.uniform(100.0, 900.0), 2)
            unit = "lux"
        return Message(
            self.device_id, self.topic,
            f"{self.sensor_type}={value}{unit}",
            sequence, time.time()
        )

class Broker:
    def __init__(self, rng):
        self.rng = rng
        self.subscribers = {}
        self.records = []

    def subscribe(self, topic, client_name):
        self.subscribers.setdefault(topic, []).append(client_name)

    def publish(self, message):
        latency = self.rng.uniform(LATENCY_MIN_MS, LATENCY_MAX_MS)
        delivered = self.rng.random() >= FAILURE_RATE
        subscribers = self.subscribers.get(message.topic, [])
        record = {
            "device_id": message.device_id,
            "topic": message.topic,
            "sequence": message.sequence,
            "payload": message.payload,
            "latency_ms": round(latency, 2),
            "delivered": delivered,
            "subscriber_count": len(subscribers),
        }
        self.records.append(record)
        return record

def run_simulation():
    rng = random.Random(RANDOM_SEED)
    devices = [
        IoTDevice("Node-1", "temperature", "home/sensor/temperature"),
        IoTDevice("Node-2", "humidity", "home/sensor/humidity"),
        IoTDevice("Node-3", "light", "home/sensor/light"),
    ]
    broker = Broker(rng)
    for device in devices:
        broker.subscribe(device.topic, "Monitoring-Dashboard")

    for device in devices:
        for sequence in range(1, TOTAL_MESSAGES_PER_DEVICE + 1):
            message = device.create_message(sequence, rng)
            broker.publish(message)

    records = broker.records
    delivered = [r for r in records if r["delivered"]]
    failed = len(records) - len(delivered)
    latencies = [r["latency_ms"] for r in records]
    average_latency = statistics.mean(latencies) if latencies else 0
    min_latency = min(latencies) if latencies else 0
    max_latency = max(latencies) if latencies else 0
    delivery_rate = (len(delivered) / len(records) * 100) if records else 0

    csv_path = OUTPUT_DIR / "simulation_results.csv"
    with csv_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(records[0].keys()))
        writer.writeheader()
        writer.writerows(records)

    summary = {
        "total_messages": len(records),
        "delivered_messages": len(delivered),
        "failed_messages": failed,
        "delivery_rate_percent": round(delivery_rate, 2),
        "average_latency_ms": round(average_latency, 2),
        "minimum_latency_ms": round(min_latency, 2),
        "maximum_latency_ms": round(max_latency, 2),
        "configured_failure_rate_percent": FAILURE_RATE * 100,
        "random_seed": RANDOM_SEED,
    }
    summary_path = OUTPUT_DIR / "simulation_summary.txt"
    with summary_path.open("w", encoding="utf-8") as f:
        for key, value in summary.items():
            f.write(f"{key}: {value}\n")

    print("WEEK 3 MQTT-STYLE SIMULATION COMPLETE")
    for key, value in summary.items():
        print(f"{key}: {value}")
    print(f"Detailed results: {csv_path.name}")
    print(f"Summary: {summary_path.name}")

if __name__ == "__main__":
    run_simulation()
