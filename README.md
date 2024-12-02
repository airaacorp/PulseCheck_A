# SSD_VALIDATION
**SSD_VALIDATION** 

This script automates the process of validating NVMe SSDs by running a series of tests designed to check the drive's performance, reliability, and functionality. Each test is generated and executed dynamically based on the parameters provided, ensuring comprehensive coverage for a wide range of NVMe SSD models.

---

## Table of Contents
1. [Overview](#overview)
2. [Features](#features)
3. [Repository](#repository)
4. [Validation](#validation)
    - [Endurance](#endurance)
    - [File_System_integrity](#file_system_integrity)
    - [Health_Monitoring](#health_monitoring)
    - [Performance_Benchmarking](#performance_benchmarking)
    - [Power_Monitoring](#power_monitoring)
    - [Security](#security)
5. [Results_and_Outputs](#results_and_Outputs)
    - [SSD_Test_Results](#SSD_Test_Results)
6. [License](#License)

---

## Overview

The **SSD_VALIDATION** script is designed to automate the validation of NVMe SSDs across different test cases, ensuring that each drive meets industry standards for performance and reliability. The script supports a variety of test cases including endurance testing, performance benchmarking, health monitoring, and more. By providing an easy-to-use command-line interface, it can be executed dynamically to validate multiple SSDs with a wide range of parameters.

---

## Features

- **Endurance Testing**: Simulates prolonged workloads to evaluate SSD longevity and durability.
- **File System Integrity**: Verifies data consistency and resilience under various conditions.
- **Health Monitoring**: Tracks critical SSD health metrics like temperature and bad sectors.
- **Performance Benchmarking**: Measures read/write speed, latency, and IOPS.
- **Power Monitoring**: Evaluates energy efficiency and detects abnormal power usage.
- **Security**: Tests encryption, secure erasure, and tamper resistance.

---

## Repository
 You can find repositary here :
```
git clone https://github.com/airaacorp/PulseCheck_A
```
---

## Validation
The Validation process is designed to thoroughly test various aspects of the NVMe SSD to ensure its performance, durability, and reliability under real-world conditions. Each of the following tests provides critical insights into the SSD’s overall functionality, helping users confirm the SSD’s readiness for extended use. The validation tests are executed using industry-standard tools, and their results are saved for analysis.

### **Endurance**
This test simulates continuous read and write operations to assess the SSD’s durability and endurance under extended workloads. It measures critical metrics such as Total Bytes Written (TBW) and tracks wear leveling to ensure that the SSD does not wear out prematurely.It also provides metrics such as:
    - **Total Bytes Written (TBW)**: The total amount of data written to the SSD over time.
    - **Wear Leveling**: Tracks how evenly data is written across the SSD to prevent excessive wear on specific cells.
    - **Data Retention**: Ensures that the drive maintains data integrity even after extended use.
    - **Read/Write Performance**: Measures the SSD’s ability to handle both read and write operations under load, ensuring that performance does not degrade over time.

- **Tools**: `fio`, `stress-ng`
- **Basic Command**:
    ```bash
    fio --name=write-test --ioengine=sync --rw=write --bs=4k --numjobs=4 --size=1M --runtime=60 --time_based
    ```

---

### **File_System_integrity**
Validates that the SSD reliably handles file system operations without errors. This includes checking for file system consistency, error detection, and ensuring that the SSD does not corrupt data.Key aspects include:
    - **File System Consistency**: Ensures that files are stored and retrieved correctly without corruption, even after unexpected shutdowns or power losses.
    - **Data Integrity**: Verifies that data written to the SSD is preserved accurately, preventing silent data corruption that might go unnoticed in normal usage.
    - **Error Detection**: Detects file system errors that might arise from underlying hardware issues, ensuring that the SSD performs reliably in a production environment.

- **Tools**: `fsck`, `badblocks`
- **Basic Commands**:
    ```bash
    fsck -f /dev/nvme0n1p1
    badblocks -w -v /dev/nvme0n1p1
    ```

---

### **Health_Monitoring**
Tracks the health of the SSD using S.M.A.R.T. data, including temperature, bad sectors, and the remaining life expectancy of the drive. This helps detect potential failures before they happen.Key metrics include:
    - **Temperature**: Monitors the operating temperature of the SSD to prevent overheating.
    - **Bad Sectors**: Detects the presence of defective areas on the drive that could affect performance.
    - **Remaining Life Expectancy**: Estimates how much longer the SSD will function optimally based on wear and usage patterns.

- **Tools**: `smartctl`, `nvme-cli`
- **Basic Commands**:
    ```bash
    smartctl -a /dev/nvme0n1
    nvme smart-log /dev/nvme0n1
    ```

---

### **Performance_Benchmarking**
Measures the SSD’s performance through various read/write tests, providing metrics like throughput, latency, and IOPS to assess its speed and efficiency.his test provides detailed metrics like:
    - **Throughput (MB/s)**: Measures the rate at which data can be read or written to the drive.
    - **Latency**: Tracks the delay in accessing data on the SSD, which impacts overall performance.
    - **IOPS (Input/Output Operations Per Second)**: Measures how many read/write operations the SSD can handle per second, which is crucial for high-performance applications.

- **Tools**: `fio`, `dd`, `ioping`
- **Basic Commands**:
    ```bash
    fio --name=seq-write --ioengine=sync --rw=write --bs=1M --numjobs=1 --size=1M
    dd if=/dev/zero of=/dev/nvme0n1 bs=1M count=1024
    ioping -c 10 /dev/nvme0n1
    ```

---

### **Power_Monitoring**
Monitors power consumption during SSD testing to ensure the drive operates efficiently. Detects abnormal power usage or spikes that could indicate hardware problems. Key aspects include:
    - **Power Consumption**: Measures the energy usage of the SSD during different workloads, ensuring that it operates within expected power ranges.
    - **Power Spikes**: Detects sudden increases in power usage that might indicate issues like overheating or malfunctioning components.
    - **Power Efficiency**: Assesses how efficiently the SSD consumes power during various operations, helping ensure that the drive is energy-efficient and suitable for environments where power consumption is a concern.

- **Tools**: `lm-sensors`, `nvme-cli`
- **Basic Command**:
    ```bash
    nvme smart-log /dev/nvme0n1
    ```

---

### **Security**
Validates the SSD’s security features, including encryption, secure erasure, and tamper protection. Ensures that the SSD can protect sensitive data through built-in security features. This includes:
    - **Encryption**: Verifies whether the SSD supports hardware-based encryption (e.g., AES 256-bit) to protect stored data.
    - **Secure Erase**: Tests the SSD’s ability to securely delete data, ensuring that deleted data cannot be recovered.
    - **Password Protection**: Assesses whether the SSD supports password-based protection, preventing unauthorized access to the drive.
    - **Data Sanitization**: Ensures that all data on the SSD can be securely wiped following industry standards, such as the DoD 5220.22-M method.
    - **Tamper Protection**: Tests the ability of the SSD to resist physical tampering and ensure the security of data even if the drive is physically altered or removed.

- **Tools**: `nvme-cli`, `hdparm`, `shred`
- **Basic Commands**:
    ```bash
    nvme format /dev/nvme0n1 --ses=1
    hdparm --user-master u --security-erase "password" /dev/nvme0n1
    shred -v -n 5 /dev/nvme0n1
    ```

---


