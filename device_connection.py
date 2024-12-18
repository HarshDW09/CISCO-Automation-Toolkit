import netmiko
from typing import Dict

def connect_to_device(device_params: Dict):
    try:
        connection = netmiko.ConnectHandler(**device_params)
        connection.enable()
        return connection
    except Exception as e:
        print(f"Connection failed: {e}")
        return None
