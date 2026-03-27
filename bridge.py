import serial
import time
import alert 

SERIAL_PORT = 'COM5' # Adjust to your actual COM port
BAUD_RATE = 1200

last_status = "CLEAR"

# This variable tracks the LAST known state of the beam
# We start assuming it is CLEAR (False means not blocked)
is_currently_blocked = False

try:
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
    print(f"Connected to {SERIAL_PORT}. Monitoring Safety Beam...")
except:
    print(f"Error: Could not open {SERIAL_PORT}. Check your connection.")
    exit()

while True:
    if ser.in_waiting > 0:
        line = ser.readline().decode('utf-8').strip()
        
        # Scenario: Beam becomes BLOCKED
        if line == "ALERT" and last_status == "CLEAR":
            print("!!! BEAM BROKEN: Sending Email Alert !!!")
            alert.send_emergency_email()
            
        # Scenario: Beam becomes CLEAR again
        elif line == "CLEAR":
            print("--- Beam Restored: System Reset ---")
            # is_currently_blocked = False # Reset state so the next block triggers an email
            
        if line in ["ALERT", "CLEAR"]:
            last_status = line
            
        # Optional: Print status to console without sending email
        print(f"Current Status: {line}")