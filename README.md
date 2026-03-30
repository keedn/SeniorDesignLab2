# Electric Eye Safety Beam System

A frequency-selective **electric eye** safety system built with an **Arduino receiver**, a **Python serial bridge**, and **SendGrid email alerts**. The project detects when a light beam is interrupted, reports the event over serial, and sends an email notification when the beam changes from clear to blocked.

## Overview

This repo implements a light beam interrupter safety system similar to the Lab 02 objective: design a frequency-selective filter that passes the desired optical signal while rejecting interference, then use that filtered signal to detect when the beam is blocked. The uploaded lab description frames the project as an “electric eye” system where a transmitter shines a beam at a receiver, and an obstruction triggers a warning condition.

In this implementation:

- The **Arduino** samples the photodetector input and runs a **7th-order digital frequency-selective filter**.
- The filtered output is rectified and thresholded with a short hysteresis window.
- The Arduino sends either `ALERT` or `CLEAR` over the serial port once per second.
- A **Python bridge** listens on the serial port and sends an email when the system transitions from `CLEAR` to `ALERT`.

## How It Works

### 1. Signal detection on the Arduino
The Arduino sketch reads the analog input from the receiver, scales it, and applies a digital filter using the numerator and denominator coefficients defined in the sketch. It then computes a rectified signal and checks the maximum over a hysteresis window before deciding whether the beam is blocked. The sketch drives an LED indicator and prints `ALERT` or `CLEAR` to serial at 1200 baud. 
### 2. Serial monitoring on the computer
`bridge.py` opens the configured serial port, continuously reads the Arduino output, and watches for a state transition. When it sees `ALERT` after a previous `CLEAR`, it triggers the email alert function. This prevents repeated emails from being sent every loop while the beam remains blocked. 

### 3. Email notification
`alert.py` builds a timestamped SendGrid message with the subject **"Electric Eye Interruption"** and sends it using the API key stored in `CONFIG.py`. It also includes debug output to help troubleshoot failed sends.

## Repository Structure

```text
.
├── Final Arduino.cpp      # Main Arduino implementation used for the project
├── lab2_filter_sketch.ino # Earlier/reference lab sketch
├── bridge.py              # Reads serial messages and triggers alerts
├── alert.py               # Sends email notifications using SendGrid
├── CONFIG.py              # Local config file for secrets (not committed)
└── README.md
```

## Hardware / Software Requirements

### Hardware
- Arduino board
- Light transmitter / receiver pair for the optical beam
- Photodetector wired to an analog input
- Indicator LED on digital pin 12
- USB connection from Arduino to computer

### Software
- Arduino IDE
- Python 3.x
- Python packages:
  - `pyserial`
  - `sendgrid`

Install Python dependencies with:

```bash
pip install pyserial sendgrid
```

## Arduino Configuration

The primary Arduino file uses:

- `analogPin = A1`
- `LED = 12`
- `BAUD_RATE = 1200`
- `threshold_val = 0.02`
- sample period `Ts = 333` microseconds (3000 Hz)

These settings are defined directly in the sketch. The code updates the detection result once per second and prints serial messages that the Python bridge depends on.

### Notes
- Make sure your receiver hardware is actually connected to **A1** if you are using `Final Arduino.cpp`. The reference lab sketch uses **A0**, so keep the code and wiring consistent. 
- Tune `threshold_val` for your specific room lighting, sensor placement, and transmitter strength.
- The LED turns on when the beam is treated as blocked in the final Arduino implementation. 

## Python Configuration

### 1. Create `CONFIG.py`
Create a local file named `CONFIG.py` in the same directory as `alert.py`:

```python
SENDGRID_API_KEY = "your_sendgrid_api_key_here"
```

### 2. Update sender and recipient emails
In `alert.py`, replace:

- `FROM_EMAIL = "from_email"`
- `to_emails="to_email"`

with real email addresses.

Important: the sender must be a verified sender identity in SendGrid, as noted in the code comments.

### 3. Set the correct serial port
In `bridge.py`, update:

```python
SERIAL_PORT = 'COM5'
```

to match your machine.

Examples:
- Windows: `COM3`, `COM4`, `COM5`
- macOS/Linux: `/dev/ttyUSB0`, `/dev/ttyACM0`, or similar

The bridge expects the Arduino to be running at **1200 baud**. 

## Running the Project

### Step 1: Upload the Arduino sketch
Open `Final Arduino.cpp` in the Arduino IDE (or copy it into an `.ino` file if needed), select the correct board and port, and upload it to the Arduino.

### Step 2: Start the Python bridge
From the project folder, run:

```bash
python bridge.py
```

If the serial connection succeeds, you should see:

```text
Connected to COM5. Monitoring Safety Beam...
```

(or the port you configured). fileciteturn0file1

### Step 3: Break the beam
When the beam is interrupted and the Arduino reports `ALERT`, the Python bridge will print a warning and call the email sender. When the beam is restored, it prints a reset message and continues monitoring. 

## Example Runtime Flow

```text
Arduino detects low filtered signal
-> Arduino prints ALERT
-> bridge.py reads ALERT
-> if previous state was CLEAR, call send_emergency_email()
-> SendGrid sends "Electric Eye Interruption" email
-> when beam is restored, Arduino prints CLEAR
-> bridge.py resets monitoring state
```

## Troubleshooting

### Serial port will not open
If you see:

```text
Error: Could not open COM5. Check your connection.
```

check that:
- the Arduino is plugged in
- the correct serial port is selected
- the Arduino Serial Monitor is closed
- the baud rate matches the sketch (`1200`) 

### No email is sent
Check the following:
- `CONFIG.py` exists and contains a valid `SENDGRID_API_KEY`
- the sender email is verified in SendGrid
- the recipient email is correct
- your network allows the outbound API request

`alert.py` includes debug prints for API-key loading, status codes, and error details to help diagnose SendGrid issues. 

### Repeated or missing alerts
The bridge only sends an email when the state changes from `CLEAR` to `ALERT`. If you want repeated alerts while the beam stays blocked, you would need to change the transition logic in `bridge.py`. As written, it is intentionally edge-triggered. 

### Detection is unreliable
Try:
- adjusting `threshold_val`
- reducing ambient light interference
- improving beam alignment
- confirming the receiver is wired to the analog pin used in the code
- checking the filter coefficients and sample timing against your design assumptions 

## Security Notes

Do **not** commit `CONFIG.py` or any real API keys to GitHub. This project depends on a secret SendGrid API key, and exposing that key can allow unauthorized use of your account. The repo should keep secrets in ignored local config or environment variables.

## Future Improvements

- Move secrets from `CONFIG.py` to environment variables
- Add a buzzer in addition to the LED/email alert
- Log beam events to a file with timestamps
- Add debounce or longer persistence checks before alerting
- Add support for SMS or push notifications
- Make the serial port and email addresses configurable from the command line

## Acknowledgment

This project builds on the Lab 02 electric-eye filtering concept and a reference digital filter sketch provided for the lab. The current repo extends that base by adding serial monitoring and automated email notification. 
