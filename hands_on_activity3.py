import os

from netmiko import ConnectHandler
from netmiko.exceptions import (
    NetmikoAuthenticationException,
    NetmikoTimeoutException,
)

from inventory import get_device
# system={
#     "name": "FONI-Router-01",
#     "device_type": "cisco_ios",
#     "role": "router",
#     "password_env": "CISCO_PASSWORD",
#     "username_env": "CISCO_USERNAME",
#     "host":"54.90.112.247"
# }



def connect_to_system(system):
    """Connect to a device using credentials stored in environment variables."""
    username = os.getenv(system["username_env"])
    password = os.getenv(system["password_env"])

    if not username or not password:
        raise ValueError(
            f"Credentials are not set for {system['name']}. "
            f"Check {system['username_env']} and {system['password_env']}."
        )

    connection_info = {
        "device_type": system["type"],
        "host": system["host"],
        "username": username,
        "password": password,
    }

    print(connection_info)

    return ConnectHandler(**connection_info)


def create_cisco_loopback(connection):
    """Create Loopback300 on the Cisco router."""
    commands = [
        "interface Loopback300",
        "description FONI Training Loopback",
        "ip address 192.0.2.100 255.255.255.255",
    ]
    return connection.send_config_set(commands)



def read_cisco_loopback(connection):
    """Display the current configuration of Loopback100."""
    return connection.send_command(
        "show running-config interface Loopback300"
    )


def remove_cisco_loopback(connection):
    """Remove Loopback100 from the Cisco router."""
    return connection.send_config_set([
        "no interface Loopback300"
    ])


def run_cisco_lifecycle(system):
    """Run the create, read, remove, and final-read lifecycle."""
    connection = None

    try:
        connection = connect_to_system(system)

        print("CREATE")
        print(create_cisco_loopback(connection))

        print("\nREAD AFTER CREATE")
        print(read_cisco_loopback(connection))

        print("\nREMOVE")
        print(remove_cisco_loopback(connection))

        print("\nREAD AFTER REMOVE")
        print(read_cisco_loopback(connection))

    except NetmikoAuthenticationException:
        print(f"{system['name']} -> FAILED: AUTHENTICATION")

    except NetmikoTimeoutException:
        print(f"{system['name']} -> FAILED: CONNECTION TIMEOUT")

    # except Exception as error:
    #     print(f"{system['name']} -> FAILED: {error}")

    finally:
        if connection:
            connection.disconnect()


def main():
    system = get_device("FONI-Router-01")

    if system is None:
        print("FONI-Router-01 was not found in inventory.py.")
        return

    run_cisco_lifecycle(system)


if __name__ == "__main__":
    main()
