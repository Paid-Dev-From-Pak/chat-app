<div align="center">

# 💬 Chat App

### Real-time messaging, reimagined.

A modern chat application built with **FastAPI**, **Firebase**, and **WebSocket**.

[![Visit Now](https://img.shields.io/badge/🚀_Visit_Now-success?style=for-the-badge)](https://chat-app-awa9.onrender.com)

<img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/python/python-original.svg" width="40" />
<img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/fastapi/fastapi-original.svg" width="40" />
<img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/firebase/firebase-plain.svg" width="40" />
<img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/html5/html5-original.svg" width="40" />
<img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/css3/css3-original.svg" width="40" />
<img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/javascript/javascript-original.svg" width="40" />

---

</div>

## ✨ Features

<div align="center">

<table>
<tr>
<td width="50%" valign="top">

### 💬 Messaging
- ⚡ Real-time delivery
- ✅ Read receipts
- ⌨️ Typing indicators
- ↩️ Forward messages

</td>
<td width="50%" valign="top">

### 👤 User Experience
- 🟢 Online/offline status
- 📎 File sharing
- 👤 Profile pictures
- ✏️ Username change

</td>
</tr>
<tr>
<td width="50%" valign="top">

### 🔍 Discovery
- 📧 Search by email
- 📱 Search by phone
- 📇 Save contacts
- 🌍 Multi-country support

</td>
<td width="50%" valign="top">

### 📱 Design
- 📱 Fully responsive
- 🎨 Clean interface
- ⚡ Fast & smooth
- 🌙 Mobile-first

</td>
</tr>
</table>

</div>

---

## 🛠️ Tech Stack

<div align="center">

| **Backend** | **Frontend** | **Database** | **Real-time** | **Hosting** |
|:---:|:---:|:---:|:---:|:---:|
| 🐍 Python | 🌐 HTML/CSS/JS | 🔥 Firebase | ⚡ WebSocket | 🚀 Render |
| FastAPI | Vanilla JS | Firestore | Async | Cloud |

</div>

---

## 🚀 Live Demo

<div align="center">

### 👉 [**chat-app-awa9.onrender.com**](https://chat-app-awa9.onrender.com) 👈

</div>

---

## 📁 Project Structure

```
chat-app/
├── 📂 frontend/
│   ├── 📄 index.html      # Login / Register
│   ├── 📄 chat.html       # Main chat interface
│   └── 🎨 style.css       # Styling
├── 📂 uploads/            # Uploaded files
├── 🐍 main.py             # FastAPI backend
├── 🔥 firebase_config.py  # Firebase setup
├── 📋 requirements.txt    # Dependencies
└── 📖 README.md
```


---

## 🎯 API Endpoints

<details>
<summary><b>Click to expand</b></summary>

| Method | Endpoint | Description |
|:---:|:---|:---|
| `POST` | `/register` | Register new user |
| `POST` | `/login` | Login user |
| `GET` | `/find-user/{email}` | Find by email |
| `GET` | `/find-phone/{phone}` | Find by phone |
| `POST` | `/send-message` | Send message |
| `GET` | `/messages/{u1}/{u2}` | Get chat history |
| `POST` | `/mark-read` | Mark as read |
| `GET` | `/chat-list/{id}` | Get chat list |
| `POST` | `/upload` | Upload file |
| `WS` | `/ws/{user_id}` | WebSocket |

</details>

---

<div align="center">

## 👨‍💻 Developer

**ByteForge Technologies**

<a href="https://www.instagram.com/byteforge_technologies_/" target="_blank">
  <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="#E4405F" style="vertical-align: middle; margin-right: 8px;">
    <path d="M12 2.163c3.204 0 3.584.012 4.85.07 3.252.148 4.771 1.691 4.919 4.919.058 1.265.069 1.645.069 4.849 0 3.205-.012 3.584-.069 4.849-.149 3.225-1.664 4.771-4.919 4.919-1.266.058-1.644.07-4.85.07-3.204 0-3.584-.012-4.849-.07-3.26-.149-4.771-1.699-4.919-4.92-.058-1.265-.07-1.644-.07-4.849 0-3.204.013-3.583.07-4.849.149-3.227 1.664-4.771 4.919-4.919 1.266-.057 1.645-.069 4.849-.069zm0-2.163c-3.259 0-3.667.014-4.947.072-4.358.2-6.78 2.618-6.98 6.98-.059 1.281-.073 1.689-.073 4.948 0 3.259.014 3.668.072 4.948.2 4.358 2.618 6.78 6.98 6.98 1.281.058 1.689.072 4.948.072 3.259 0 3.668-.014 4.948-.072 4.354-.2 6.782-2.618 6.979-6.98.059-1.28.073-1.689.073-4.948 0-3.259-.014-3.667-.072-4.947-.196-4.354-2.617-6.78-6.979-6.98-1.281-.059-1.69-.073-4.949-.073zm0 5.838c-3.403 0-6.162 2.759-6.162 6.162s2.759 6.163 6.162 6.163 6.162-2.759 6.162-6.163c0-3.403-2.759-6.162-6.162-6.162zm0 10.162c-2.209 0-4-1.79-4-4 0-2.209 1.791-4 4-4s4 1.791 4 4c0 2.21-1.791 4-4 4zm6.406-11.845c-.796 0-1.441.645-1.441 1.44s.645 1.44 1.441 1.44c.795 0 1.439-.645 1.439-1.44s-.644-1.44-1.439-1.44z"/>
  </svg>
  <span style="vertical-align: middle;">@byteforge_technologies_</span>
</a>

---

### ⭐ If you like this project, please give it a star!

**Made with ❤️ by ByteForge Technologies**

</div>
