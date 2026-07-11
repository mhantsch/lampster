#!/usr/bin/env python3
import subprocess
import sys
import threading

# Configuration: What you want to automate
LOCK_CMD = "sleep 15; lampster off" # Replace with your script
UNLOCK_CMD = "lampster on" # Replace with your script

def process_log_stream():
    # We monitor the live journal for cosmic-greeter and gkr-pam
    cmd = [
        'journalctl', '-t', 'cosmic-greeter', '-f', '-n', '0'
    ]

    print("Monitoring COSMIC logs... (Ctrl+C to stop)")

    try:
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
        
        for line in iter(process.stdout.readline, b''):
            decoded_line = line.decode('utf-8').strip()
            
            if not decoded_line:
                continue

#            print(f"[LINE] {decoded_line}")

            # Detect LOCK (BackgroundImage filter input is logged when the screen locks)
            if "cosmic-greeter" in decoded_line and "BackgroundImage" in decoded_line:
                print(f"[LOCK] Detected: {decoded_line}")
                # Run your lock automation here
                subprocess.run(LOCK_CMD, shell=True)

            # Detect UNLOCK (gkr-pam logs 'unlocked login keyring' on success)
            elif "gkr-pam" in decoded_line and \
                 ( \
                       ("unlocked login keyring" in decoded_line) \
                    or ("no password is available for user" in decoded_line) \
                 ):
                print(f"[UNLOCK] Detected: {decoded_line}")
                # Run your unlock automation here
                subprocess.run(UNLOCK_CMD, shell=True)

    except KeyboardInterrupt:
        pass
    finally:
        process.kill()

if __name__ == "__main__":
    process_log_stream()
