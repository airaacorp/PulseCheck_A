import os
import subprocess
from getpass import getpass
from click import command

class NVMePowerMonitoring:
    def __init__(self, device, sudo_password):
        self.device = device
        self.sudo_password = sudo_password
        self.power_thermal_results = {}

    '''This is a common function which can run all commands using subprocess.
    If there are any errors in the command, it will return to the user and store it in logs.'''

    def run_command(self, command):
        try:
            full_command = f"echo {self.sudo_password} | sudo -S {command}"
            result = subprocess.check_output(full_command, stderr=subprocess.STDOUT, shell=True,
                                             universal_newlines=True)
            return result
        except subprocess.CalledProcessError as e:
            return f"Error executing command: {e.output}"

    # --- NVMe Power & Thermal Monitoring Commands ---
    def get_nvme_temperature(self):
        command = f"nvme smart-log {self.device} | grep temperature"
        return self.run_command(command)

    def get_nvme_power(self):
        command = f"nvme smart-log {self.device} | grep 'Power' "
        return self.run_command(command)

    def get_power_on_hours(self):
        command = f"nvme smart-log {self.device} | grep 'Power_On_Hours'"
        return self.run_command(command)

    def get_power_cycles(self):
        command = f"nvme smart-log {self.device} | grep 'Power_Cycles'"
        return self.run_command(command)

    def get_smartctl_temperature(self):
        command = f"smartctl -a {self.device} | grep Temperature_Celsius"
        return self.run_command(command)

    def get_smartctl_power_on(self):
        command = f"smartctl -a {self.device} | grep Power_On_Hours"
        return self.run_command(command)

    def get_thermal_throttling(self):
        command = f"nvme smart-log {self.device} | grep 'Thermal Throttling'"
        return self.run_command(command)

    def get_device_health(self):
        command = f"nvme smart-log {self.device} | grep 'health'"
        return self.run_command(command)

    def get_nvme_firmware_version(self):
        command = f"nvme id-ctrl {self.device} | grep 'frimware_version'"
        return self.run_command(command)

    def get_operating_status(self):
        command = f"nvme smart-log {self.device} | grep 'Operating Status'"
        return self.run_command(command)

    def get_nvme_power_state(self):
        command = f"nvme id-ctrl {self.device} | grep 'Power State'"
        return self.run_command(command)

    # --- lm-sensors Monitoring Commands (System-wide) ---
    def get_system_temperature(self):
        # Use lm-sensors to get system-wide temperature information
        command = "sensors"
        return self.run_command(command)

    def get_system_fan_speed(self):
        # Get fan speed information (useful for thermal performance)
        command = "sensors | grep 'fan'"
        return self.run_command(command)

    # --- Power & Thermal Test Runners ---
    def run_all_power_thermal_tests(self):
        '''Run all the power and thermal tests and store results'''
        # NVMe Specific Tests
        self.power_thermal_results['NVMe_Temperature'] = self.get_nvme_temperature()
        self.power_thermal_results['NVMe_Power_Consumption'] = self.get_nvme_power()
        self.power_thermal_results['Power_On_Hours'] = self.get_power_on_hours()
        self.power_thermal_results['Power_Cycles'] = self.get_power_cycles()
        self.power_thermal_results['SMARTCTL_Temperature'] = self.get_smartctl_temperature()
        self.power_thermal_results['SMARTCTL_Power_On_Hours'] = self.get_smartctl_power_on()
        self.power_thermal_results['Thermal_Throttling'] = self.get_thermal_throttling()
        self.power_thermal_results['Device_Health'] = self.get_device_health()
        self.power_thermal_results['NVMe_Firmware_Version'] = self.get_nvme_firmware_version()
        self.power_thermal_results['Operating_Status'] = self.get_operating_status()
        self.power_thermal_results['NVMe_Power_State'] = self.get_nvme_power_state()

        # System-wide (lm-sensors) Tests
        self.power_thermal_results['System_Temperature'] = self.get_system_temperature()
        self.power_thermal_results['System_Fan_Speed'] = self.get_system_fan_speed()

    # --- Save Results Function ---
    def save_results(self, base_dir):
        '''Save all results into txt files'''
        # Create directory for power and thermal results
        power_thermal_dir = os.path.join(base_dir, "Power_Thermal_Results")
        os.makedirs(power_thermal_dir, exist_ok=True)

        # Save each test result in separate files
        for test_name, output in self.power_thermal_results.items():
            file_name = f"{test_name.replace(' ', '_').lower()}.txt"
            file_path = os.path.join(power_thermal_dir, file_name)
            with open(file_path, "w") as file:
                file.write(f"{test_name}\n{'=' * 40}\n{output}")
            print(f"Saved {test_name} results to {file_path}")
