import os
import subprocess

class SecurityValidation:
    def __init__(self, device, sudo_password):
        # Initialize the class with device name and sudo password
        self.device = device
        self.sudo_password = sudo_password
        self.security_results = {}  # To store results of security tests

    def run_command(self, command):
        """
        Executes a shell command with sudo privileges.
        Redirects errors to /dev/null to suppress unwanted outputs.
        """
        try:
            # Build the full command string to include the sudo password
            full_command = f"echo {self.sudo_password} | sudo -S {command} 2>/dev/null"
            # Execute the command and capture the output
            result = subprocess.check_output(
                full_command, stderr=subprocess.STDOUT, shell=True, universal_newlines=True
            )
            return result.strip()  # Return the output, stripped of extra spaces
        except subprocess.CalledProcessError as e:
            # Handle errors and return the error message
            return f"Error executing command: {e.output.strip()}"

    def check_sanitize_capabilities(self):
        """
        Checks if the NVMe device supports sanitize operations.
        Command:
        nvme id-ctrl {device} | grep -i 'sanicap'
        - `nvme id-ctrl`: Fetches controller information of the NVMe device.
        - `grep -i 'sanicap'`: Filters the output to check for "sanicap" field, case-insensitive.
        """
        command = f"nvme id-ctrl {self.device} | grep -i 'sanicap'"
        return self.run_command(command)

    def sanitize_device(self):
        """
        Initiates a sanitize operation on the NVMe device.
        Command:
        nvme sanitize {device} --sanitize=1
        - `--sanitize=1`: Specifies block erase sanitize type.
        """
        command = f"nvme sanitize {self.device} --sanitize=1"
        return self.run_command(command)

    def verify_sanitize_progress(self):
        """
        Checks the progress of an ongoing sanitize operation.
        Command:
        nvme sanitize-log {device}
        - Fetches sanitize operation progress from the NVMe device's sanitize log.
        """
        command = f"nvme sanitize-log {self.device}"
        return self.run_command(command)

    def check_encryption_capabilities(self):
        """
        Checks if the NVMe device supports encryption features.
        Command:
        nvme id-ctrl {device} | grep -i 'oacs'
        - `oacs`: Optional Admin Command Support, indicates encryption capabilities.
        """
        command = f"nvme id-ctrl {self.device} | grep -i 'oacs'"
        return self.run_command(command)

    def enable_password_protection(self, password):
        """
        Enables password protection on the NVMe device.
        Command:
        nvme format {device} --ses=1 --key={password}
        - `--ses=1`: Specifies user data encryption during format.
        - `--key={password}`: Specifies the password for protection.
        """
        command = f"nvme format {self.device} --ses=1 --key={password}"
        return self.run_command(command)

    def verify_password_protection(self):
        """
        Verifies if password protection is enabled on the NVMe device.
        Command:
        nvme id-ctrl {device} | grep -i 'security'
        - Checks the security field in the controller information.
        """
        command = f"nvme id-ctrl {self.device} | grep -i 'security'"
        return self.run_command(command)

    def check_firmware_security(self):
        """
        Reads the NVMe device firmware log for security details.
        Command:
        nvme fw-log {device}
        - Retrieves firmware log entries for the device.
        """
        command = f"nvme fw-log {self.device}"
        return self.run_command(command)

    def read_smart_log(self):
        """
        Reads the SMART log for the NVMe device.
        Command:
        nvme smart-log {device}
        - Provides health status and other diagnostic information of the device.
        """
        command = f"nvme smart-log {self.device}"
        return self.run_command(command)

    def secure_erase(self):
        """
        Performs a secure erase on the NVMe device.
        Command:
        nvme format {device} --ses=1
        - Securely erases the data using encryption session (SES) 1.
        """
        command = f"nvme format {self.device} --ses=1"
        return self.run_command(command)

    def verify_data_after_erase(self):
        """
        Verifies if the data is erased by reading a portion of the device.
        Command:
        dd if={device} of=/dev/null bs=1M count=10
        - `if={device}`: Input file (device).
        - `of=/dev/null`: Discards the output.
        - `bs=1M`: Reads data in blocks of 1MB.
        - `count=10`: Reads the first 10 blocks.
        """
        command = f"dd if={self.device} of=/dev/null bs=1M count=10"
        return self.run_command(command)

    def run_all_security_tests(self, password):
        """
        Runs all the security tests and stores the results.
        """
        self.security_results['check_sanitize_capabilities'] = self.check_sanitize_capabilities()
        self.security_results['sanitize_device'] = self.sanitize_device()
        self.security_results['verify_sanitize_progress'] = self.verify_sanitize_progress()
        self.security_results['check_encryption_capabilities'] = self.check_encryption_capabilities()
        self.security_results['enable_password_protection'] = self.enable_password_protection(password)
        self.security_results['verify_password_protection'] = self.verify_password_protection()
        self.security_results['check_firmware_security'] = self.check_firmware_security()
        self.security_results['read_smart_log'] = self.read_smart_log()
        self.security_results['secure_erase'] = self.secure_erase()
        self.security_results['verify_data_after_erase'] = self.verify_data_after_erase()

    def save_results(self, base_dir):
        """
        Saves the results of the security tests to a directory.
        - Creates a folder named `Hdparm_Results` in the given `base_dir`.
        - Writes each test's result into a separate `.txt` file.
        """
        security_dir = os.path.join(base_dir, "Security_Results")
        os.makedirs(security_dir, exist_ok=True)  # Create directory if it doesn't exist
        for test_name, output in self.security_results.items():
            file_name = f"{test_name.replace(' ', '_').lower()}.txt"
            file_path = os.path.join(security_dir, file_name)
            with open(file_path, "w") as file:
                # Write test results with a header and divider line
                file.write(f"{test_name}\n{'=' * 40}\n{output}\n")
                print(f"Saved {test_name} results to {file_path}")