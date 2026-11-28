# Week 4 – IoT Device Integration and Interoperability Testing

## Project
**IoT-Based Smart Home Automation**

This project simulates multiple IoT devices communicating through a common MQTT-style topic/message layer. A temperature sensor controls a fan, while a motion sensor controls a light.

## Devices
- Temperature sensor (`temp-01`): publishes temperature in degrees Celsius.
- Motion sensor (`motion-01`): publishes a Boolean motion status.
- Smart fan actuator (`fan`): switches ON at 28°C or above; otherwise OFF.
- Smart light actuator (`light`): switches ON when motion is detected; otherwise OFF.
- In-memory broker/gateway: routes messages by topic.
- Logger: records timestamps, source, topic, payload and result.

## Files
- `Week4_Device_Integration_Report.docx` – complete report.
- `iot_device_simulation.py` – runnable Python simulation.
- `architecture.png` – system architecture diagram.
- `simulation_log.csv` and `test_summary.txt` – generated after running the simulation.

## Requirements
- Python 3.8 or newer
- No third-party Python packages required

## Run
```bash
python iot_device_simulation.py
```
The script creates `simulation_log.csv` and `test_summary.txt` in the current folder.

## Interoperability checks
1. Topic compatibility: each sensor publishes to its documented topic.
2. Payload compatibility: temperature must be numeric and use unit `C`; motion must be Boolean.
3. Command routing: valid sensor messages trigger the corresponding actuator command.
4. Error handling: malformed payloads are rejected and logged.
5. Repeatability: the same input sequence should produce the same device states.

## Important scope note
This is a software simulation of MQTT-style communication. It does not connect to a real MQTT broker, Wi-Fi network, sensor, fan, or light. Do not describe simulated results as physical hardware measurements.
