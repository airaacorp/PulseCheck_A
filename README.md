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
This test simulates continuous read and write operations to assess the SSD’s durability and endurance under extended workloads. It measures critical metrics such as Total Bytes Written (TBW) and tracks wear leveling to ensure that the SSD does not wear out prematurely.

- **Tools**: `fio`, `stress-ng`
- **Basic Command**:
    ```bash
    fio --name=write-test --ioengine=sync --rw=write --bs=4k --numjobs=4 --size=1M --runtime=60 --time_based
    ```

---

### **File_System_integrity**
Validates that the SSD reliably handles file system operations without errors. This includes checking for file system consistency, error detection, and ensuring that the SSD does not corrupt data.

- **Tools**: `fsck`, `badblocks`
- **Basic Commands**:
    ```bash
    fsck -f /dev/nvme0n1p1
    badblocks -w -v /dev/nvme0n1p1
    ```

---

### **Health_Monitoring**
Tracks the health of the SSD using S.M.A.R.T. data, including temperature, bad sectors, and the remaining life expectancy of the drive. This helps detect potential failures before they happen.

- **Tools**: `smartctl`, `nvme-cli`
- **Basic Commands**:
    ```bash
    smartctl -a /dev/nvme0n1
    nvme smart-log /dev/nvme0n1
    ```

---

### **Performance_Benchmarking**
Measures the SSD’s performance through various read/write tests, providing metrics like throughput, latency, and IOPS to assess its speed and efficiency.

- **Tools**: `fio`, `dd`, `ioping`
- **Basic Commands**:
    ```bash
    fio --name=seq-write --ioengine=sync --rw=write --bs=1M --numjobs=1 --size=1M
    dd if=/dev/zero of=/dev/nvme0n1 bs=1M count=1024
    ioping -c 10 /dev/nvme0n1
    ```

---

### **Power_Monitoring**
Monitors power consumption during SSD testing to ensure the drive operates efficiently. Detects abnormal power usage or spikes that could indicate hardware problems.

- **Tools**: `lm-sensors`, `nvme-cli`
- **Basic Command**:
    ```bash
    nvme smart-log /dev/nvme0n1
    ```

---

### **Security**
Validates the SSD’s security features, including encryption, secure erasure, and tamper protection. Ensures that the SSD can protect sensitive data through built-in security features.

- **Tools**: `nvme-cli`, `hdparm`, `shred`
- **Basic Commands**:
    ```bash
    nvme format /dev/nvme0n1 --ses=1
    hdparm --user-master u --security-erase "password" /dev/nvme0n1
    shred -v -n 5 /dev/nvme0n1
    ```

---


