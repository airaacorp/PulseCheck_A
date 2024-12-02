import os
import subprocess
from datetime import date
from itertools import count
from select import error
from getpass import getpass
from time import sleep

from click import command
from cloudinit.config.cc_snap import run_commands

class NVMePerformaceCheck:
    def __init__(self, device, sudo_password):
        self.device = device
        self.sudo_password = sudo_password
        self.fio_results = {}
        self.DD_results = {}
        self.ioping_results = {}

    '''
    This is Common Function which can run all commands by using subprocess if there is any Errors in command
    it will return to user and it stores in LOG's'''

    def run_command(self, command):
        try:
            full_command = f"echo {self.sudo_password} | sudo -S {command}"
            result = subprocess.check_output(full_command, stderr=subprocess.STDOUT, shell=True,
                                             universal_newlines=True)
            return result
        except subprocess.CalledProcessError as e:
            return f"Error executing command: {e.output}"

    # ---Fio Commands ---

    #Fio performance test with specified parameters.
    def fio_performance_test(self, name, ioengine, rw, bs, size, numjobs, runtime, iodepth=1):
        command = (
            f"fio --name={name} "
            f"--ioengine={ioengine} "
            f"--rw={rw} "
            f"--bs={bs} "
            f"--size={size} "
            f"--numjobs={numjobs} "
            f"--runtime={runtime} "
            f"--iodepth={iodepth} "
            f"--group_reporting"
        )
        return self.run_command(command)

    #A Sequential Read Test measures how efficiently the storage device reads data in a continuous manner.
    # This test simulates workloads like streaming large files, sequential database access, or backups.

    def sequential_read_test(self):
        return self.fio_performance_test("seq_read", "libaio", "read", "128k", "131072", 1, 60)

    #This test is designed to stress the device's ability to handle concurrent I/O operations by using a high I/O depth.
    # It simulates workloads where multiple read and write requests are queued simultaneously,
    # such as in high-performance databases or heavily loaded systems.

    def high_iodepth_test(self):
        return self.fio_performance_test("high_iodepth", "libaio", "randrw", "4k", "131072", 4, 60, iodepth=32)

    #This  evaluates the performance of a device when writing data to random locations,
    #simulating workloads like database transactions, logging systems, and virtual machines

    def random_write_test(self):
        return self.fio_performance_test("rand_write", "libaio", "randwrite", "4k", "131072", 4, 60)

    #This will test sequential write performance,
    #which is commonly seen in tasks like writing large files in a continuous manner
    def sequential_write_test(self):
        return self.fio_performance_test("seq_write", "libaio", "write", "128k", "131072", 1, 60)

    #This test will evaluate random read performance,
    #which is useful for testing database-like workloads that frequently access random data

    def random_read_test(self):
        return self.fio_performance_test("rand_read", "libaio", "randread", "4k", "131072", 4, 60)

    #This test mixes both read and write operations.
    #It’s essential for workloads like file system performance and database operations where both read and write actions occur concurrently.

    def mixed_read_write_test(self):
        return self.fio_performance_test("rand_read_write", "libaio", "randwrite", "4k", "131072", 4, 60, iodepth=8)

    #This test is designed to assess the performance of large sequential reads,
    #which could be used for tasks like reading large video or database files.
    def large_block_sequential_read_test(self):
        return self.fio_performance_test("large_seq_read", "libaio", "read", "1M", "131072", 1, 60)

    #This test evaluates the performance of large block random writes.
    #These kinds of tests are important for large file systems or applications that perform large writes at random locations
    def large_block_random_write_test(self):
        return self.fio_performance_test("large_rand_write", "libaio", "randwrite", "128k", "131072", 8, 60, iodepth=16)

    #This test evaluates the maximum throughput of the device by using a high number of jobs and large block sizes
    def throughput_test(self):
        return self.fio_performance_test("throughput", "libaio", "write", "128k", "131072", 1, 60, iodepth=32)

    # DD Commands

    #Sequential write test using dd command
    def dd_sequential_write_test(self, block_size, count):
        command = f"dd if=/dev/zero of={self.device} bs={block_size} count={count} oflag=direct status=progress"
        return self.run_command(command)

    #Sequential read test using dd command
    def dd_sequential_read_test(self, block_size, count):
        command = f"dd if={self.device} of=/dev/null bs={block_size} count={count} iflag=direct status=progress"
        return self.run_command(command)

    #Random write test using dd command
    def dd_random_write_test(self, block_size, count):
        command = f"dd if=/dev/urandom of={self.device} bs={block_size} count={count} oflag=direct status=progress"
        return self.run_command(command)

    #Random read test using dd command
    def dd_random_read_test(self, block_size, count):
        command = f"dd if={self.device} of=/dev/null bs={block_size} count={count} iflag=direct status=progress"
        return self.run_command(command)

    #Throughput using dd with large block size
    def dd_throughput_test(self, block_size, count):
        command = f"dd if=/dev/zero of={self.device} bs={block_size} count={count} oflag=direct status=progress"
        return self.run_command(command)

    #Write Speed with Different Block Sizes using DD
    def dd_write_speed_with_different_block(self,block_size,count):
        command = f"dd if=/dev/zero of={self.device} bs={block_size} count={count} oflag=direct status=progress"
        return self.run_command(command)

    #Read Speed with Different Block Sizes using DD
    def dd_read_speed_with_different_block(self,block_size,count):
        command = f"dd if={self.device} of=/dev/null bs={block_size} count={count} iflag=direct status=progress"
        return self.run_command(command)

    #Test Write Latency using DD
    def dd_test_write_latency(self,block_size,count):
        command = f"dd if=/dev/zero of={self.device} bs={block_size} count={count} oflag=direct status=progress"
        return self.run_command(command)

    #Test Read Latency using DD
    def dd_test_read_latency(self,block_size,count):
        command = f"dd if={self.device} of=/dev/null bs={block_size} count={count} iflag=direct status=progress"
        return self.run_command(command)

    #Io_Ping Commands

    #Sequential I/O Latency Test using ioping
    def ioping_sequential_test(self,count,block_size):
        command = f"ioping -c {count} -s {block_size} -D {self.device}"
        return self.run_command(command)

    #Random I/O Latency Test using ioping
    # def ioping_random_test(self, count, block_size):
    #     command = f"ioping -c {count} -s {block_size} -i 1 {self.device}"
    #     return self.run_command(command)

    #Continuous I/O Latency Test (stressing the device continuously)
    def ioping_continuous_test(self,IoTests,count):
        command = f"ioping -c {IoTests} -s {count} {self.device}"
        return self.run_command(command)

    # Maximum I/O Latency Test (measuring latency with high number of IO requests)
    def ioping_max_latency_test(self,count,block_size,interval):
        command = f"ioping -c {count} -s {block_size} -i {interval} {self.device}"
        return self.run_command(command)

    # Test Write Latency with ioping
    def ioping_write_latency_test(self,count):
        command = f"ioping -c {count} -W {self.device}"
        return self.run_command(command)

    # Test Read Latency with ioping
    def ioping_read_latency_test(self,count):
        command = f"ioping -c {count} -R {self.device}"
        return self.run_command(command)

    # Test Block Read and Write Latency using ioping
    def ioping_block_read_write_latency_test(self,count,block_size):
        command = f"ioping -c {count} -s {block_size} -W {self.device}"
        return self.run_command(command)


    # TestS_Runner

    def run_all_fio_tests(self):
        self.fio_results['Sequential_Read_Info'] = self.sequential_read_test()
        self.fio_results['Random_Write_Info'] = self.random_write_test()
        self.fio_results['IO_depth_Info'] = self.high_iodepth_test()
        self.fio_results['Sequential_Write_Info'] = self.sequential_write_test()
        self.fio_results['Random_Read_Test'] = self.random_read_test()
        self.fio_results['Mixed_Read_Write_Test'] = self.mixed_read_write_test()
        self.fio_results['Large_Block_Sequential_Read_Test'] = self.large_block_sequential_read_test()
        self.fio_results['Large_Block_Random_Write_Test'] = self.large_block_random_write_test()
        self.fio_results['Throughput_Test'] = self.throughput_test()

    def run_all_dd_tests(self):
        self.DD_results['Sequential_Write_Test'] = self.dd_sequential_write_test("128k", 1024)
        self.DD_results['Sequential_Read_Test'] = self.dd_sequential_read_test("128k", 1024)
        self.DD_results['Random_Write_Test'] = self.dd_random_write_test("4k", 1024)
        self.DD_results['Random_Read_Test'] = self.dd_random_read_test("4k", 1024)
        self.DD_results['Throughput_Test'] = self.dd_throughput_test("128k", 1024)
        self.DD_results['write_speed_different_block'] = self.dd_write_speed_with_different_block("124",1024)
        self.DD_results['read_speed_different_block'] = self.dd_read_speed_with_different_block("128k",1024)
        self.DD_results['write_latency_test'] = self.dd_test_write_latency("4k",1024)
        self.DD_results['read_latency_test'] = self.dd_test_read_latency("4K",1024)

    def run_all_ioPing_tests(self):
        self.ioping_results['Sequential_IO_Latency'] = self.ioping_sequential_test("4k",10)
        #self.ioping_results['Random_IO_Latency'] = self.ioping_random_test("4k",10)
        self.ioping_results['Continuous_IO_Latency'] = self.ioping_continuous_test(10,"4k")
        self.ioping_results['Max_IO_Latency'] = self.ioping_max_latency_test(10,"1M",0.5)
        self.ioping_results['Write_Latency_Test'] = self.ioping_write_latency_test(count=10)
        self.ioping_results['Read _Latency_Test'] = self.ioping_read_latency_test(count=10)
        self.ioping_results['Block_Read_Write_Latency'] = self.ioping_block_read_write_latency_test(10,"1M")


    #Save The Results In Directory
    def save_results(self, base_dir):
        # Create folders for FIO and DD and IoPing results
        Fio_Dir = os.path.join(base_dir, "Fio_Results")
        DD_Dir = os.path.join(base_dir, "DD_Results")
        IoPing_Dir = os.path.join(base_dir, "IO_Ping_Results")
        os.makedirs(Fio_Dir, exist_ok=True)
        os.makedirs(DD_Dir, exist_ok=True)
        os.makedirs(IoPing_Dir, exist_ok=True)

        # Save Fio results
        for test_name, output in self.fio_results.items():
            file_name = f"{test_name.replace(' ', '_').lower()}.txt"
            file_path = os.path.join(Fio_Dir, file_name)
            with open(file_path, "w") as file:
                file.write(f"{test_name}\n{'=' * 40}\n{output}")
            print(f"Saved {test_name} results to {file_path}")

        # Save DD results
        for test_name, output in self.DD_results.items():
            file_name = f"{test_name.replace(' ', '_').lower()}.txt"
            file_path = os.path.join(DD_Dir, file_name)
            with open(file_path, "w") as file:
                file.write(f"{test_name}\n{'=' * 40}\n{output}")
            print(f"Saved {test_name} results to {file_path}")

        #Save IO_Ping Results
        for test_name, output in self.ioping_results.items():
            file_name = f"{test_name.replace(' ', '_').lower()}.txt"
            file_path = os.path.join(IoPing_Dir, file_name)
            with open(file_path, "w") as file:
                file.write(f"{test_name}\n{'=' * 40}\n{output}")
            print(f"Saved {test_name} results to {file_path}")

        print("Results saved successfully in", base_dir)