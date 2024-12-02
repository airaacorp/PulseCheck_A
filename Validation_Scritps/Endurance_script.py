import os
import subprocess
from datetime import datetime

class EnduranceValidation:
    def __init__(self, device, sudo_password):
        """
        Initializes the class with the device and sudo password.
        Args:
            device (str): Path to the device (e.g., /dev/nvme0n1).
            sudo_password (str): Sudo password for executing privileged commands.
        """
        self.device = device
        self.sudo_password = sudo_password
        self.fio_results = {}  # Stores results of FIO tests and other checks.

    def run_command(self, command):
        """
        Runs a command using subprocess with sudo privileges.
        Args:
            command (str): Command to be executed.
        Returns:
            str: Command output or error message if the command fails.
        """
        try:
            full_command = f"echo {self.sudo_password} | sudo -S {command}"
            result = subprocess.check_output(
                full_command, stderr=subprocess.STDOUT, shell=True, universal_newlines=True
            )
            return result
        except subprocess.CalledProcessError as e:
            return f"Error executing command: {e.output}"

    def run_seq_write(self):
        """
        Runs sequential write test using FIO.
        Command:
            fio --name=seq_write --filename={device} --rw=write --bs=1M --size=10G
                --numjobs=1 --time_based --runtime=10 --group_reporting
        - `--rw=write`: Sequential write operation.
        - `--bs=1M`: Block size of 1MB.
        - `--size=10G`: Total size of data to write.
        - `--time_based --runtime=10`: Runs the test for 10 seconds.
        """
        command = (
            f"fio --name=seq_write --filename={self.device} --rw=write --bs=1M --size=1024 --numjobs=1 --time_based --runtime=10 --group_reporting"
        )
        return self.run_command(command)

    def run_rand_write(self):
        """
        Runs random write test using FIO.
        Command:
            fio --name=rand_write --filename={device} --rw=randwrite --bs=4k --size=10G
                --numjobs=4 --time_based --runtime=10 --group_reporting
        - `--rw=randwrite`: Random write operation.
        - `--bs=4k`: Block size of 4KB.
        - `--numjobs=4`: Number of parallel jobs.
        """
        command = (
            f"fio --name=rand_write --filename={self.device} --rw=randwrite --bs=4k --size=4096 --numjobs=4 --time_based --runtime=10 --group_reporting"
        )
        return self.run_command(command)

    def run_mixed_rw(self):
        """
        Runs mixed read/write test using FIO.
        Command:
            fio --name=mixed_rw --filename={device} --rw=randrw --rwmixread=70 --bs=4k
                --size=10G --numjobs=4 --time_based --runtime=10 --group_reporting
        - `--rw=randrw`: Random read/write mix.
        - `--rwmixread=70`: 70% read and 30% write operations.
        """
        command = (
            f"fio --name=mixed_rw --filename={self.device} --rw=randrw --rwmixread=70 --bs=4k --size=4096 --numjobs=4 --time_based --runtime=10 --group_reporting"
        )
        return self.run_command(command)

    def run_seq_read(self):
        """
        Runs sequential read test using FIO.
        Command:
            fio --name=seq_read --filename={device} --rw=read --bs=1M --size=10G
                --numjobs=1 --time_based --runtime=10 --group_reporting
        - `--rw=read`: Sequential read operation.
        """
        command = (
            f"fio --name=seq_read --filename={self.device} --rw=read --bs=1M --size=1M --numjobs=1 --time_based --runtime=10 --group_reporting"
        )
        return self.run_command(command)

    def run_rand_read(self):
        """
        Runs random read test using FIO.
        Command:
            fio --name=rand_read --filename={device} --rw=randread --bs=4k --size=10G
                --numjobs=4 --time_based --runtime=10 --group_reporting
        """
        command = (
            f"fio --name=rand_read --filename={self.device} --rw=randread --bs=4k --size=4096 --numjobs=4 --time_based --runtime=10 --group_reporting"
        )
        return self.run_command(command)

    def run_write_integrity(self):
        """
        Tests data integrity during random write using CRC32 verification.
        Command:
            fio --name=write_integrity --filename={device} --rw=randwrite --bs=4k
                --verify=crc32 --size=10G --numjobs=4 --group_reporting
        - `--verify=crc32`: Verifies data integrity using CRC32 checksum.
        """
        command = (
            f"fio --name=write_integrity --filename={self.device} --rw=randwrite --bs=4k --verify=crc32 --size=4096 --numjobs=4 --group_reporting"
        )
        return self.run_command(command)

    def run_temperature_monitoring(self):
        """
        Monitors the device temperature using SMART logs.
        Command:
            nvme smart-log {device} | grep -i 'temperature'
        """
        command = f"nvme smart-log {self.device} | grep -i 'temperature'"
        return self.run_command(command)

    def run_smart_attributes(self):
        """
        Fetches SMART attributes for the device.
        Command:
            smartctl -a {device}
        """
        command = f"smartctl -a {self.device}"
        return self.run_command(command)

    def run_disk_health(self):
        """
        Checks the health status of the disk using SMART tools.
        Command:
            smartctl -a {device}
        """
        command = f"smartctl -a {self.device}"
        return self.run_command(command)

    def run_nvme_smart_log(self):
        """
        Retrieves the NVMe SMART log.
        Command:
            nvme smart-log {device}
        """
        command = f"nvme smart-log {self.device}"
        return self.run_command(command)

    def run_error_log(self):
        """
        Reads the error log of the NVMe device.
        Command:
            nvme error-log {device}
        """
        command = f"nvme error-log {self.device}"
        return self.run_command(command)

    def run_power_state(self):
        """
        Checks the power state of the NVMe device.
        Command:
            nvme power-state {device}
        """
        command = f"nvme power-state {self.device}"
        return self.run_command(command)

    def run_all_fio_tests(self):
        """
        Runs all the FIO and monitoring tests and saves the results.
        """
        self.fio_results['run_seq_write'] = self.run_seq_write()
        self.fio_results['run_rand_write'] = self.run_rand_write()
        self.fio_results['run_mixed_rw'] = self.run_mixed_rw()
        self.fio_results['run_seq_read'] = self.run_seq_read()
        self.fio_results['run_rand_read'] = self.run_rand_read()
        self.fio_results['run_write_integrity'] = self.run_write_integrity()
        self.fio_results['run_temperature_monitoring'] = self.run_temperature_monitoring()
        self.fio_results['run_smart_attributes'] = self.run_smart_attributes()
        self.fio_results['run_disk_health'] = self.run_disk_health()
        self.fio_results['run_nvme_smart_log'] = self.run_nvme_smart_log()
        self.fio_results['run_error_log'] = self.run_error_log()
        self.fio_results['run_power_state'] = self.run_power_state()

    def save_results(self, base_dir):
        """
        Saves all the test results into a directory.
        Args:
            base_dir (str): Base directory where results are saved.
        """
        Fio_Dir_E = os.path.join(base_dir, "Endurance_Results")
        os.makedirs(Fio_Dir_E, exist_ok=True)  # Create results directory if it doesn't exist
        for test_name, output in self.fio_results.items():
            file_name = f"{test_name.replace(' ', '_').lower()}.txt"
            file_path = os.path.join(Fio_Dir_E, file_name)
            with open(file_path, "w") as file:
                # Write the test name, separator, and output to a file
                file.write(f"{test_name}\n{'=' * 40}\n{output}")
                print(f"Saved {test_name} results to {file_path}")