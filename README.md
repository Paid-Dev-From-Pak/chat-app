<div align="center">

# 💬 Chat App

### Real-time messaging, reimagined.

A modern chat application built with **FastAPI**, **Firebase**, and **WebSocket**.

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
## 👨‍💻 Developer

<div align="center">

  

<a href="https://www.instagram.com/byteforge_technologies_/"
   target="_blank"
   style="display: inline-flex; align-items: center; text-decoration: none;">
  <img src="https://img.icons8.com/fluency/48/instagram-new.png"
       width="28"
       style="margin-right: 8px;"
       alt="Instagram" />
  <span>@byteforge_technologies_</span>
</a>



---

### ⭐ If you like this project, please give it a star!

**Made with ❤️ by ByteForge Technologies**

</div>
