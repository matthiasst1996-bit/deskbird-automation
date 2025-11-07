import subprocess
import sys
import time

print("=" * 60)
print("Starting Deskbird Automation Suite")
print("=" * 60)

print("\n[1/2] Starting Parkplatz booking automation...")
try:
    subprocess.run([sys.executable, "Parkplatz-deskbird_login.py"], check=True)
    print("✓ Parkplatz script completed successfully!")
except Exception as e:
    print(f"✗ Parkplatz script failed: {e}")
    sys.exit(1)

time.sleep(5)

print("\n[2/2] Starting Arbeitsplatz booking automation...")
try:
    subprocess.run([sys.executable, "Arbeitsplatz-deskbird_login.py"], check=True)
    print("✓ Arbeitsplatz script completed successfully!")
except Exception as e:
    print(f"✗ Arbeitsplatz script failed: {e}")
    sys.exit(1)

print("\n" + "=" * 60)
print("✓✓✓ All scripts completed successfully!")
print("=" * 60)
