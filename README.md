# 💬 Real-Time LAN Multi-User Chat Application

A robust, multi-threaded console-based chat application built using Python sockets. This application enables real-time, bi-directional text communication between multiple clients connected over a Local Area Network (LAN) using a Client-Server architecture.

---

## 📑 Table of Contents
* [Features](#-features)
* [Architecture Overview](#-architecture-overview)
* [Requirements](#-requirements)
* [Project Structure](#-project-structure)
* [LAN Network Setup Guide](#-lan-network-setup-guide)
* [How to Run](#-how-to-run)
* [Under the Hood: Technical Explanation](#-under-the-hood-technical-explanation)
  * [Socket Programming & TCP Protocol](#1-socket-programming--tcp-protocol)
  * [Multi-Threading & Concurrency](#2-multi-threading--concurrency)
  * [Message Routing & Broadcasting](#3-message-routing--broadcasting)
  * [Error Handling & Connection Lifecycle](#4-error-handling--connection-lifecycle)

---

## ✨ Features
* **Multi-User Support:** Allows multiple users to join the chatroom concurrently.
* **LAN Compatibility:** Operates seamlessly across different machines on the same local network.
* **Real-Time Broadcasting:** Instantly routes messages sent by any user to all other connected peers.
* **Non-Blocking I/O:** Utilizes multi-threading to handle sending and receiving messages simultaneously.
* **Graceful Disconnection:** Handles client disconnections without crashing the server or disturbing other users.

---

## 🏗️ Architecture Overview

The system follows a classic **Centralized Client-Server Model**:


```
[ Client 1 ] <--->

[ Client 2 ] <------> [ Central Server ] (Port 5000)
/
[ Client 3 ] <--->
```

1. **Server:** Listens for incoming socket connections, registers client nicknames, and broadcasts incoming payloads.
2. **Client:** Establishes a TCP connection with the server IP, listens for incoming chat streams, and sends user input.

---

## 📦 Requirements

* **Operating System:** Windows, macOS, or Linux.
* **Language Environment:** Python 3.7 or higher.
* **External Dependencies:** **None** (Built entirely using Python standard libraries: `socket`, `threading`, and `sys`).

---

## 📁 Project Structure

```text
.
├── server.py       # Central server script handling routing and connections
├── client.py       # Client-side interface for joining the chatroom
└── README.md       # Comprehensive documentation

```
## 🌐 LAN Network Setup Guide
To establish a multi-device connection over LAN, you must identify the **IP Address** of the host machine running server.py.
### Step 1: Find the Server's Local IP Address
 * **Windows:**
   1. Open Command Prompt (cmd).
   2. Run: ipconfig
   3. Locate **IPv4 Address** under your active network adapter (e.g., 192.168.1.15).
 * **Linux / macOS:**
   1. Open Terminal.
   2. Run: ifconfig or ip a
   3. Locate the IP address associated with your Wi-Fi (wlan0) or Ethernet (eth0/en0).
### Step 2: Configure Firewall Settings (If Applicable)
Ensure port **5000** allows inbound TCP traffic on the server machine:
 * **Windows Firewall:** Add an inbound rule allowing TCP traffic on port 5000.
 * **Linux (ufw):** Run sudo ufw allow 5000/tcp.
## 🚀 How to Run
### 1. Launch the Server
Run the server script on the main host computer:
```bash
python server.py

```
> The server will start listening on 0.0.0.0:5000 for local incoming connections.
> 
### 2. Launch Client(s)
Run the client script on any computer (or separate terminal windows on the same machine):
```bash
python client.py

```
### 3. Connection Steps:
 1. When prompted, enter the **Server's IP Address** (Use 127.0.0.1 if testing locally on the same computer, or the IPv4 address found earlier for LAN testing).
 2. Enter your desired **Nickname**.
 3. Start typing messages! Type /exit to safely leave the chatroom.
## 🧠 Under the Hood: Technical Explanation
### 1. Socket Programming & TCP Protocol
 * **Protocol Choice:** The application utilizes **TCP (Transmission Control Protocol)** via Python's socket.AF_INET (IPv4) and socket.SOCK_STREAM (TCP) flags. TCP was selected over UDP because text messaging requires reliable, in-order, and lossless data delivery.
 * **Server Binding:** The server binds to 0.0.0.0, an all-zero IP address that instructs the server to listen to connection requests on **all available network interfaces** (Ethernet, Wi-Fi, Localhost).
### 2. Multi-Threading & Concurrency
Standard network code operates synchronously (blocking I/O). To prevent user input execution from blocking message reception, **Multi-threading** (threading module) is used:
 * **Server Concurrency:** The server runs a primary loop executing server.accept(). For every accepted connection, it spawns a dedicated worker thread running handle_client(client_socket). This allows the server to manage N clients simultaneously without blocking.
 * **Client Concurrency:** The client initiates two concurrent threads:
   1. **Receive Thread:** Continuously listens for incoming data stream (client_socket.recv()) and outputs it to the console.
   2. **Send Loop (Main Thread):** Captures console input (input()) and pushes byte streams to the socket.
### 3. Message Routing & Broadcasting
Message distribution operates on a **Pub-Sub style broadcast routine**:
 1. When a client sends a text message, it is serialized into UTF-8 bytes and sent across the socket buffer.
 2. The server receives the byte array in its handle_client execution thread.
 3. The server calls broadcast(message), iterating through the global clients list and calling .send() to relay the message to every connected client socket.
### 4. Error Handling & Connection Lifecycle
 * **Socket Reuse:** The server executes server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) to allow immediate port rebinding upon server restarts.
 * **Disconnect Detection:** When a client closes their application or experiences network failure, recv() returns an empty string or throws an exception. The server gracefully catches this exception, removes the socket object from the active clients list, closes the socket safely, and notifies remaining participants.
```

```