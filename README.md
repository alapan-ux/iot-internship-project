# Week 3: Simulating IoT Communication Protocols

## Project title
MQTT-Style Communication Simulation for Three IoT Sensor Nodes

## Overview
This project models three IoT sensor nodes publishing readings to a central broker. A monitoring dashboard subscribes to each sensor topic. The simulation records message delivery, simulated network latency, and message failures.

## Important scope note
This is a self-contained Python simulation of MQTT-style publish/subscribe behaviour. It does **not** connect to a live MQTT broker or implement the full MQTT wire protocol. This distinction is stated so the submission accurately describes what was tested.

## Requirements
- Python 3.8 or later
- No third-party Python packages required

## Run
```bash
python iot_mqtt_simulation.py
```

The program creates:
- `simulation_results.csv` — one row per published message
- `simulation_summary.txt` — delivery and latency summary

## Simulated configuration
- Protocol model: MQTT-style publish/subscribe
- Nodes: Node-1 (temperature), Node-2 (humidity), Node-3 (light)
- Broker: one central in-program broker
- Subscriber: Monitoring-Dashboard
- Messages per node: 10 (30 total)
- Simulated latency range: 20–120 ms
- Simulated message failure probability: 8%
- Random seed: 21 for repeatable results

## Topics
- `home/sensor/temperature`
- `home/sensor/humidity`
- `home/sensor/light`

## Error handling and evaluation
Each publish operation is marked delivered or failed. The CSV stores the simulated latency and delivery state. The summary reports delivery rate and latency statistics. Re-run with a different random seed or failure rate to explore other network conditions.

## Limitations and future work
This simplified model does not perform real Wi-Fi transmission, broker authentication, QoS handshakes, retained messages, or packet-level network emulation. A future extension can connect Python Paho-MQTT clients to Mosquitto, or use Node-RED/Cisco Packet Tracer where available.
