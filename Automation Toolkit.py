import netmiko
import logging
import csv
from typing import Dict, List, Any

#TO-DO :  Try this with other CISCO routers too. Need to take advise for further functionality.
class NetworkAutomationToolkit:
    def __init__(self, devices: List[Dict]):
        """
        Initialize network automation toolkit
        
        :param devices: List of device connection parameters
        """
        # Configure logging
        logging.basicConfig(
            level=logging.INFO, 
            format='%(asctime)s - %(levelname)s: %(message)s',
            filename='network_automation.log'
        )
        self.logger = logging.getLogger(__name__)
        self.devices = devices
    
    def backup_configurations(self, backup_dir='config_backups'):
        """
        Backup configurations for multiple devices
        
        :param backup_dir: Directory to store configuration backups
        """
        import os
        os.makedirs(backup_dir, exist_ok=True)
        
        for device in self.devices:
            try:
                connection = netmiko.ConnectHandler(**device)
                connection.enable()
                
                # Backup running configuration
                config = connection.send_command("show running-config")
                
                # Generate backup filename
                backup_file = os.path.join(
                    backup_dir, 
                    f"{device['ip']}_backup.txt"
                )
                
                with open(backup_file, 'w') as f:
                    f.write(config)
                
                self.logger.info(f"Backed up {device['ip']} configuration")
                connection.disconnect()
            
            except Exception as e:
                self.logger.error(f"Backup failed for {device['ip']}: {e}")
    
    def collect_network_inventory(self, output_file='network_inventory.csv'):
        """
        Collect inventory information from network devices
        
        :param output_file: CSV file to store inventory data
        """
        inventory_data = []
        
        for device in self.devices:
            try:
                connection = netmiko.ConnectHandler(**device)
                connection.enable()
                
                # Collect inventory information
                inventory = connection.send_command("show inventory")
                interfaces = connection.send_command("show interfaces status")
                
                device_info = {
                    'ip': device['ip'],
                    'inventory': inventory,
                    'interfaces': interfaces
                }
                
                inventory_data.append(device_info)
                connection.disconnect()
            
            except Exception as e:
                self.logger.error(f"Inventory collection failed for {device['ip']}: {e}")
        
        # Write inventory to CSV
        self._write_inventory_to_csv(inventory_data, output_file)
    
    def _write_inventory_to_csv(self, data: List[Dict], filename: str):
        """
        Write inventory data to CSV
        
        :param data: List of inventory dictionaries
        :param filename: Output CSV filename
        """
        try:
            with open(filename, 'w', newline='') as csvfile:
                fieldnames = ['IP', 'Inventory', 'Interfaces']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                
                writer.writeheader()
                for item in data:
                    writer.writerow({
                        'IP': item['ip'],
                        'Inventory': item['inventory'],
                        'Interfaces': item['interfaces']
                    })
            
            self.logger.info(f"Inventory saved to {filename}")
        
        except Exception as e:
            self.logger.error(f"CSV writing error: {e}")
    
    def configure_vlans(self, vlan_config: List[Dict]):
        """
        Configure VLANs across multiple devices
        
        :param vlan_config: List of VLAN configurations
        """
        for device in self.devices:
            try:
                connection = netmiko.ConnectHandler(**device)
                connection.enable()
                
                for vlan in vlan_config:
                    config_commands = [
                        f"vlan {vlan['id']}",
                        f"name {vlan['name']}"
                    ]
                    connection.send_config_set(config_commands)
                
                self.logger.info(f"VLANs configured on {device['ip']}")
                connection.disconnect()
            
            except Exception as e:
                self.logger.error(f"VLAN configuration failed for {device['ip']}: {e}")

def main():
       # Delete User name and password
       # I have now put Dummy Password and ID . For actual contact IT.
    devices = [
        {
            'device_type': 'cisco_ios',
            'ip': '192.168.1.1',
            'username': 'admin',
            'password': 'password',
            'secret': 'enable_password'
        },
        # Add more devices as needed
    ]
    
    # VLAN Configuration Example
    # Delete User name and password
    vlan_configs = [
        {"id": 10, "name": "Management"},
        {"id": 20, "name": "Staff"},
        {"id": 30, "name": "Guest"}
    ]
    
 
    network_tool = NetworkAutomationToolkit(devices)
    
    
    network_tool.backup_configurations()
    network_tool.collect_network_inventory()
    network_tool.configure_vlans(vlan_configs)

if __name__ == "__main__":
    main()

