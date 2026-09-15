
import os
from netmiko import ConnectHandler


devices = [
    {
        "device_type": "cisco_ios",
        "host": os.getenv("CISCO_HOST"),
        "username": os.getenv("CISCO_USERNAME"),
        "password": os.getenv("CISCO_PASSWORD"),
        "commands": [
            "show ip interface brief",
            "show version",
            "show ip route"
        ]
    },
    {
        "device_type": "linux",
        "host": os.getenv("LINUX_HOST"),
        "username": os.getenv("LINUX_USERNAME"),
        "password": os.getenv("LINUX_PASSWORD"),
        "commands": [
            "ip --br addr",
            "uname -a",
            "ip route",
            "df -h"
        ]
    }
]


for device in devices:
    commands = device.pop("commands")

    print(f"\nConnecting to {device['host']}...")

    try:
        connection = ConnectHandler(**device)

        for command in commands:
            print(f"\n--- {command} ---")
            output = connection.send_command(command)
            print(output)

        connection.disconnect()

    except Exception as e:
        print(f"Connection failed: {e}")