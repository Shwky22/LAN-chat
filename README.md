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