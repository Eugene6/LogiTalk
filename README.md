# 💬 LogiTalk Messenger

**LogiTalk** is a lightweight, real-time desktop chat application built with Python. It provides a simple server-client setup allowing multiple users to connect, customize their profiles, and talk to each other.

---

## 🚀 Key Features

* **Multi-User Chat Room** - Instantly broadcasts text messages to all connected users.
* **Nickname Customization** - Ability to easily choose and change your unique username.
* **Image Sharing** - Support for sending and viewing photos inside the chat.
* **Multi-threaded Server** - Handles multiple socket connections smoothly using Python's `threading`.

---

## 🛠️ Tech Stack

* **Language:** Python 
* **Core Libraries:** `socket` & `threading` (TCP/IP socket connection for real-time data sync)
* **GUI Framework:** Built-in Python Tkinter graphics

---

## 💻 How to Run Locally

Follow these quick steps in your terminal to host the server and launch chat windows:

1. **Start the Server:**
   Open `server.py` and run it:
   ```bash
   python server.py
   ```
   *Note: The server runs on `HOST = '0.0.0.0'` and `PORT = 8080` by default.*

2. **Launch the Clients:**
   Run `LogiTalk1.py` (you can run this script multiple times to open different users):
   ```bash
   python LogiTalk1.py
   ```

3. **Connect to the Chat:**
   * **Username:** Enter any nickname.
   * **Host:** `127.0.0.1` (or `localhost`).
   * **Port:** `8080`.
   * Click **Connect**.
