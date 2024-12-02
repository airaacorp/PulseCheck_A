import os
import subprocess
from getpass import getpass

class FileSystemIntegrityMonitoring:
    def __init__(self, sudo_password):
        self.sudo_password = sudo_password
        self.fs_integrity_results = {}

    '''This is a common function that runs all commands using subprocess.
    If there are any errors in the command, it will return to the user and store it in logs.'''

    def run_command(self, command):
        try:
            full_command = f"echo {self.sudo_password} | sudo -S {command}"
            result = subprocess.check_output(full_command, stderr=subprocess.STDOUT, shell=True,
        universal_newlines=True)
            return result
        except subprocess.CalledProcessError as e:
            return f"Error executing command: {e.output}"

    # --- File System Integrity Commands ---

    def check_filesystem_status(self):
        '''Check the file system status using fsck (file system consistency check)'''
        command = "sudo fsck -Af -M"
        return self.run_command(command)

    def check_disk_usage(self):
        '''Check the disk usage (percent space used on file system)'''
        command = "df -h"
        return self.run_command(command)

    def check_inodes_usage(self):
        '''Check the inode usage (useful to check if the file system is running out of inodes)'''
        command = "df -i"
        return self.run_command(command)

    def check_for_orphaned_inodes(self):
        '''Find orphaned inodes using debugfs (on ext filesystems)'''
        command = "sudo debugfs -R 'stats' /dev/nvme0n1"
        return self.run_command(command)

    def check_mount_status(self):
        '''Check the mount status of file systems'''
        command = "mount -v"
        return self.run_command(command)

    def check_disk_smart_status(self):
        '''Check the SMART status of the disks (for hardware integrity)'''
        command = "sudo smartctl -a /dev/nvme0n1"
        return self.run_command(command)

    def check_filesystem_type(self):
        '''Check the file system type of the mounted disks'''
        command = "lsblk -f"
        return self.run_command(command)

    def check_filesystem_health(self):
        '''Check the health of the file system (using smartctl or fsck if needed)'''
        command = "sudo smartctl -H /dev/nvme0n1"
        return self.run_command(command)

    def check_log_for_errors(self):
        '''Check system logs for file system related errors'''
        command = "journalctl -xe | grep -i 'filesystem'"
        return self.run_command(command)

    def check_filesystem_resizing(self):
        '''Check if filesystem resizing has completed successfully'''
        command = "sudo resize2fs -P /dev/nvme0n1"
        return self.run_command(command)

    # def check_for_bad_blocks(self):
    #     '''Check for bad blocks on the disk (using badblocks)'''
    #     command = "sudo badblocks -v /dev/nvme0n1"
    #     return self.run_command(command)

    def check_filesystem_detailed_status(self):
        '''Check the detailed status of ext4 file systems (using tune2fs)'''
        command = "sudo tune2fs -l /dev/nvme0n1"
        return self.run_command(command)

    def check_filesystem_safety(self):
        '''Check the safety of the filesystem by verifying mounts and attributes'''
        command = "sudo mount -o check /dev/nvme0n1"
        return self.run_command(command)

    # def check_for_journal_errors(self):
    #     '''Check for any errors in the file system journal'''
    #     command = "sudo journalctl -f | grep -i 'ext4'"
    #     return self.run_command(command)

    # --- Test Runner ---
    def run_all_fs_integrity_tests(self):
        '''Run all the file system integrity tests and store results'''
        # File System Specific Tests
        self.fs_integrity_results['FileSystem_Status'] = self.check_filesystem_status()
        self.fs_integrity_results['Disk_Usage'] = self.check_disk_usage()
        self.fs_integrity_results['Inode_Usage'] = self.check_inodes_usage()
        self.fs_integrity_results['Orphaned_Inodes'] = self.check_for_orphaned_inodes()
        self.fs_integrity_results['Mount_Status'] = self.check_mount_status()
        self.fs_integrity_results['Disk_SMART_Status'] = self.check_disk_smart_status()
        self.fs_integrity_results['FileSystem_Type'] = self.check_filesystem_type()
        self.fs_integrity_results['FileSystem_Health'] = self.check_filesystem_health()
        self.fs_integrity_results['System_Logs_Errors'] = self.check_log_for_errors()
        self.fs_integrity_results['FileSystem_Resizing'] = self.check_filesystem_resizing()
        #self.fs_integrity_results['Bad_Blocks'] = self.check_for_bad_blocks()
        self.fs_integrity_results['FileSystem_Detailed_Status'] = self.check_filesystem_detailed_status()
        self.fs_integrity_results['FileSystem_Safety'] = self.check_filesystem_safety()
        #self.fs_integrity_results['Journal_Errors'] = self.check_for_journal_errors()

    # --- Save Results Function ---
    def save_results(self, base_dir):
        '''Save all results into txt files'''
        # Create directory for file system integrity results
        fs_integrity_dir = os.path.join(base_dir, "File_System_Integrity_Results")
        os.makedirs(fs_integrity_dir, exist_ok=True)

        # Save each test result in separate files
        for test_name, output in self.fs_integrity_results.items():
            file_name = f"{test_name.replace(' ', '_').lower()}.txt"
            file_path = os.path.join(fs_integrity_dir, file_name)
            with open(file_path, "w") as file:
                file.write(f"{test_name}\n{'=' * 40}\n{output}")
            print(f"Saved {test_name} results to {file_path}")