import os
import subprocess
from getpass import getpass
from Validation_Scritps.Health_Monitoring import SSDValidation
from Validation_Scritps.Performance_Benchmarking import NVMePerformaceCheck
from Validation_Scritps.File_System_integrity import FileSystemIntegrityMonitoring
from Validation_Scritps.Power_Monitoring import NVMePowerMonitoring
from Validation_Scritps.Endurance_script import EnduranceValidation
from Validation_Scritps.Security_script import SecurityValidation

def get_ssd_devices():
    """
    Fetch and return a list of SSD devices (NVMe or SATA) connected to the system.
    """
    # Using lsblk we are listing block devices and filter by type SSD or NVMe
    try:
        result = subprocess.run(['lsblk', '-d', '-o', 'NAME,MODEL,TYPE', '-p'], stdout=subprocess.PIPE, text=True)
        devices = result.stdout.splitlines()

        ssd_devices = []
        for device in devices:
            if 'disk' in device:
                # Check for SSD devices (both SATA and NVMe)
                if 'NVMe' in device or 'SSD' in device:
                    device_info = device.split()
                    device_path = device_info[0]
                    device_name = device_info[1]
                    ssd_devices.append(f"{device_name} ({device_path})")

        return ssd_devices
    except Exception as e:
        print(f"Error fetching SSD devices: {e}")
        return []

def main():
    print("Starting Comprehensive SSD Validation")

    # Fetch the available SSD devices
    ssd_devices = get_ssd_devices()

    # If no SSD devices found, print a message and exit
    if not ssd_devices:
        print("No SSD devices found on the system.")
        return

    # List available devices for the user to choose from
    print("Available SSD devices:")
    for index, device in enumerate(ssd_devices, start=1):
        print(f"{index}. {device}")

    # Prompt the user to select a device
    while True:
        try:
            device_index = int(input("Select the SSD device to validate (enter number): ")) - 1
            if 0 <= device_index < len(ssd_devices):
                device = ssd_devices[device_index].split('(')[-1].strip(')')
                break
            else:
                print("Invalid selection, please choose a valid device number.")
        except ValueError:
            print("Invalid input, please enter a number.")

    # Prompt for sudo password
    sudo_password = getpass("Enter your sudo password: ")

    # Initialize the SSDValidation instance
    validator = SSDValidation(device, sudo_password)

    performance_validator = NVMePerformaceCheck(device, sudo_password)

    nvme_monitor = NVMePowerMonitoring(device, sudo_password)

    fs_monitor = FileSystemIntegrityMonitoring(sudo_password)

    endurance_validator = EnduranceValidation(device, sudo_password)

    security_validator = SecurityValidation(device, sudo_password)


    # Run all tests for SSD_Validation HealthMonitoring
    print("\nRunning HealthMonitoring Tests With smartctl...")
    validator.run_all_smartctl_tests()

    print("\nRunning HealthMonitoring Tests With nvme-cli...")
    validator.run_all_nvmecli_tests()

    # Run all tests for SSD_Validation PerformaceBenchmarking
    print("\nRunning PerformaceBenchmarking Tests With Fio...")
    performance_validator.run_all_fio_tests()

    print("\nRunning PerformanceBenchmarking Tests With DD....")
    performance_validator.run_all_dd_tests()

    print("\nRunning PerformanceBenchmarking Tests With IoPing....")
    performance_validator.run_all_ioPing_tests()

    print("\nRunning NVMe Power and Thermal Monitoring Tests...")
    nvme_monitor.run_all_power_thermal_tests()

    print("\nRunning File System Integrity Monitoring Tests...")
    fs_monitor.run_all_fs_integrity_tests()

    print("\nRunning Endurance Monitoring Tests...")
    endurance_validator.run_all_fio_tests()

    print("\nRunning Security Monitoring Tests....")
    security_validator.run_all_security_tests(password="secure_password")



    # Define the directory where results will be saved
    results_dir = "/home/vamsimikkili/Downloads/SSD_Validation_Automation_Python-master/SSD_Test_Results"
    os.makedirs(results_dir, exist_ok=True)

    # Save results
    validator.save_results(results_dir)
    performance_validator.save_results(results_dir)
    nvme_monitor.save_results(results_dir)
    fs_monitor.save_results(results_dir)
    endurance_validator.save_results(results_dir)
    security_validator.save_results(results_dir)

    print("\nSSD validation completed successfully!")

if __name__ == '__main__':
    main()
