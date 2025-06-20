# SmartEdge Setup Program

This is a setup program for the **SmartEdge networking system**. It automates the installation of all dependencies and environment setup needed to run the SmartEdge artifacts on a freshly formatted **x64 Ubuntu machine**.

## 📦 Purpose

The setup program:
- Installs all required packages, tools, and libraries.
- Configures network interfaces based on the selected artifact.
- Sets up a Python virtual environment.
- Prepares the system to run SmartEdge seamlessly.

---

## 🚀 Usage Instructions

### 🔧 Prerequisites

Before using this program, ensure:

- You have at least **10 GB of free disk space**.
- The machine is connected to the **Internet**.
- The machine runs **Ubuntu 22.04 or 24.04 LTS**.
- You have a **Docker Hub account** (optional but recommended).

### 📁 Getting Started

1. Download the setup program as a **ZIP file**.
2. Extract the ZIP content into a **USB stick**.
3. Insert the USB into the installation machine.
4. Open a terminal and navigate to the extracted folder:


## 🧠 Program Behavior

The program starts by updating the system and installing general dependencies.
It prompts you to select which SmartEdge artifact to install:
 co → Coordinator
 ap → Access Point
 sn → Smart Node

Based on your choice, it will ask you to select:
 A wireless interface (for hotspot or connection)
 An Ethernet interface (for backend communication)

After installation, the setup program asks:
 👉 Do you want to start the artifact now?
   If you answer yes, it opens a new shell and activates the virtual environment :
 👉 To start the artifact, type: source run.sh [co|ap|sn] 10

## 🐳 Docker Images Note

If you face issues when downloading Docker images like bmv2 or cassandra, make sure you are logged into your Docker account using:
 docker login
Then, restart the setup process.

