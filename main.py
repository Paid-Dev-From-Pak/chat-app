from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from datetime import datetime, timezone, timedelta
from typing import Dict
import json
import os
import shutil
import uuid

from firebase_config import db, auth_client

app = FastAPI(title="Chat App API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

PKT = timezone(timedelta(hours=5))

def now_pkt():
    return datetime.now(PKT).isoformat()

# ============ MODELS ============
class UserRegister(BaseModel):
    email: str
    password: str
    username: str
    phone: str

class UserLogin(BaseModel):
    email: str
    password: str

class MessageSend(BaseModel):
    sender_id: str
    receiver_id: str
    text: str = ""
    temp_id: str = None
    file_url: str = None
    file_type: str = None
    file_name: str = None

class MarkRead(BaseModel):
    reader_id: str
    sender_id: str

class DeleteAccount(BaseModel):
    user_id: str

class UpdateUsername(BaseModel):
    user_id: str
    new_username: str

class UpdateDP(BaseModel):
    user_id: str
    dp_url: str

class SaveContact(BaseModel):
    owner_id: str
    contact_id: str
    saved_name: str

# ============ CONNECTION MANAGER ============
class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}

    async def connect(self, user_id: str, websocket: WebSocket):
        await websocket.accept()
        self.active_connections[user_id] = websocket
        print(f"User connected: {user_id}")
        await self.broadcast({"type": "user_online", "user_id": user_id})

    def disconnect(self, user_id: str):
        if user_id in self.active_connections:
            del self.active_connections[user_id]
            print(f"User disconnected: {user_id}")

    async def send_to_user(self, user_id: str, message: dict):
        if user_id in self.active_connections:
            try:
                await self.active_connections[user_id].send_text(json.dumps(message))
                return True
            except Exception as e:
                print(f"Send error: {e}")
                self.disconnect(user_id)
                return False
        return False

    def is_online(self, user_id: str):
        return user_id in self.active_connections

    def get_online_users(self):
        return list(self.active_connections.keys())

    async def close_user(self, user_id: str):
        if user_id in self.active_connections:
            ws = self.active_connections[user_id]
            try:
                await ws.close(code=1008, reason="User deleted")
            except:
                pass
            del self.active_connections[user_id]

    async def broadcast(self, message: dict):
        for uid in list(self.active_connections.keys()):
            await self.send_to_user(uid, message)

manager = ConnectionManager()

# ============ UPLOAD FOLDER ============
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_DIR = os.path.join(BASE_DIR, "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)

# ============ ROUTES ============

@app.get("/")
def root():
    return FileResponse(os.path.join(BASE_DIR, "frontend", "index.html"))

@app.post("/register")
def register(user: UserRegister):
    try:
        phone_clean = user.phone.replace(" ", "").replace("-", "").strip()
        existing = db.collection("users").where("phone", "==", phone_clean).stream()
        for e in existing:
            raise HTTPException(status_code=400, detail="Yeh phone number pehle se register hai")

        firebase_user = auth_client.create_user(
            email=user.email,
            password=user.password,
            display_name=user.username
        )
        db.collection("users").document(firebase_user.uid).set({
            "uid": firebase_user.uid,
            "email": user.email,
            "username": user.username,
            "phone": phone_clean,
            "dp_url": "",
            "created_at": now_pkt()
        })
        return {"success": True, "uid": firebase_user.uid, "username": user.username, "phone": phone_clean}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/login")
def login(user: UserLogin):
    users = db.collection("users").where("email", "==", user.email).stream()
    user_data = None
    for u in users:
        user_data = u.to_dict()
        break
    if not user_data:
        raise HTTPException(status_code=404, detail="User nahi mila")
    return {
        "success": True,
        "uid": user_data["uid"],
        "username": user_data["username"],
        "phone": user_data.get("phone", ""),
        "dp_url": user_data.get("dp_url", "")
    }

@app.get("/find-user/{email}")
def find_user(email: str):
    users = db.collection("users").where("email", "==", email).stream()
    for u in users:
        data = u.to_dict()
        return {"success": True, "user": data}
    raise HTTPException(status_code=404, detail="User nahi mila")

@app.get("/find-phone/{phone}")
def find_phone(phone: str):
    phone_clean = phone.replace(" ", "").replace("-", "").strip()
    users = db.collection("users").where("phone", "==", phone_clean).stream()
    for u in users:
        data = u.to_dict()
        return {"success": True, "user": data}
    raise HTTPException(status_code=404, detail="User nahi mila")

@app.post("/update-username")
async def update_username(data: UpdateUsername):
    user_doc = db.collection("users").document(data.user_id).get()
    if not user_doc.exists:
        raise HTTPException(status_code=404, detail="User nahi mila")
    db.collection("users").document(data.user_id).update({"username": data.new_username})
    try:
        auth_client.update_user(data.user_id, display_name=data.new_username)
    except Exception as e:
        print(f"Auth update error: {e}")
    await manager.broadcast({
        "type": "username_updated",
        "user_id": data.user_id,
        "new_username": data.new_username
    })
    return {"success": True, "new_username": data.new_username}

@app.post("/update-dp")
async def update_dp(data: UpdateDP):
    user_doc = db.collection("users").document(data.user_id).get()
    if not user_doc.exists:
        raise HTTPException(status_code=404, detail="User nahi mila")
    db.collection("users").document(data.user_id).update({"dp_url": data.dp_url})
    await manager.broadcast({
        "type": "dp_updated",
        "user_id": data.user_id,
        "dp_url": data.dp_url
    })
    return {"success": True, "dp_url": data.dp_url}

@app.post("/save-contact")
def save_contact(data: SaveContact):
    owner_doc = db.collection("users").document(data.owner_id).get()
    contact_doc = db.collection("users").document(data.contact_id).get()
    if not owner_doc.exists or not contact_doc.exists:
        raise HTTPException(status_code=404, detail="User nahi mila")
    db.collection("contacts").document(data.owner_id).collection("saved").document(data.contact_id).set({
        "contact_id": data.contact_id,
        "saved_name": data.saved_name,
        "saved_at": now_pkt()
    })
    return {"success": True, "saved_name": data.saved_name}

@app.get("/contacts/{owner_id}")
def get_contacts(owner_id: str):
    contacts = db.collection("contacts").document(owner_id).collection("saved").stream()
    result = {}
    for c in contacts:
        data = c.to_dict()
        result[data["contact_id"]] = data["saved_name"]
    return {"contacts": result}

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    try:
        ext = os.path.splitext(file.filename)[1]
        unique_name = f"{uuid.uuid4().hex}{ext}"
        file_path = os.path.join(UPLOAD_DIR, unique_name)

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        content_type = file.content_type or ""
        if content_type.startswith("image"):
            file_type = "image"
        elif content_type.startswith("video"):
            file_type = "video"
        elif content_type.startswith("audio"):
            file_type = "audio"
        else:
            file_type = "file"

        return {
            "success": True,
            "file_url": f"/uploads/{unique_name}",
            "file_name": file.filename,
            "file_type": file_type
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/download/{filename}")
def download_file(filename: str):
    file_path = os.path.join(UPLOAD_DIR, filename)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File nahi mili")
    return FileResponse(file_path, filename=filename, media_type="application/octet-stream")

@app.post("/send-message")
async def send_message(msg: MessageSend):
    sender_doc = db.collection("users").document(msg.sender_id).get()
    if not sender_doc.exists:
        await manager.close_user(msg.sender_id)
        raise HTTPException(status_code=401, detail="User deleted")

    chat_id = "_".join(sorted([msg.sender_id, msg.receiver_id]))
    chat_ref = db.collection("chats").document(chat_id)
    chat_doc = chat_ref.get()
    if not chat_doc.exists:
        chat_ref.set({
            "chat_id": chat_id,
            "participants": [msg.sender_id, msg.receiver_id],
            "created_at": now_pkt(),
            "last_message": msg.text or "[attachment]",
            "last_timestamp": now_pkt()
        })
    else:
        chat_ref.update({
            "last_message": msg.text or "[attachment]",
            "last_timestamp": now_pkt()
        })

    message_data = {
        "sender_id": msg.sender_id,
        "receiver_id": msg.receiver_id,
        "text": msg.text or "",
        "timestamp": now_pkt(),
        "delivered": False,
        "read": False,
        "file_url": msg.file_url,
        "file_type": msg.file_type,
        "file_name": msg.file_name
    }

    doc_ref = chat_ref.collection("messages").add(message_data)
    full_message = message_data | {"id": doc_ref[1].id}

    await manager.send_to_user(msg.sender_id, {
        "type": "message_sent",
        "chat_id": chat_id,
        "message": full_message,
        "temp_id": msg.temp_id
    })

    receiver_online = manager.is_online(msg.receiver_id)

    if receiver_online:
        doc_ref[1].update({"delivered": True})
        full_message["delivered"] = True
        await manager.send_to_user(msg.receiver_id, {
            "type": "new_message",
            "chat_id": chat_id,
            "message": full_message
        })
        await manager.send_to_user(msg.sender_id, {
            "type": "message_delivered",
            "chat_id": chat_id,
            "message_id": doc_ref[1].id
        })

    return {"success": True, "message_id": doc_ref[1].id}

@app.get("/messages/{user1}/{user2}")
def get_messages(user1: str, user2: str, limit: int = 50):
    chat_id = "_".join(sorted([user1, user2]))
    messages = db.collection("chats").document(chat_id).collection("messages")\
        .order_by("timestamp", direction="DESCENDING").limit(limit).stream()
    result = [m.to_dict() | {"id": m.id} for m in messages]
    return {"chat_id": chat_id, "messages": list(reversed(result))}

@app.post("/mark-read")
async def mark_read(data: MarkRead):
    chat_id = "_".join(sorted([data.reader_id, data.sender_id]))
    messages = db.collection("chats").document(chat_id).collection("messages")\
        .where("receiver_id", "==", data.reader_id)\
        .where("sender_id", "==", data.sender_id)\
        .where("read", "==", False).stream()

    message_ids = []
    for m in messages:
        m.reference.update({"read": True, "delivered": True})
        message_ids.append(m.id)

    if message_ids:
        await manager.send_to_user(data.sender_id, {
            "type": "messages_read",
            "chat_id": chat_id,
            "reader_id": data.reader_id,
            "message_ids": message_ids
        })
    return {"success": True, "count": len(message_ids)}

@app.get("/chat-list/{user_id}")
def get_chat_list(user_id: str):
    chats = db.collection("chats").stream()
    result = []
    for chat in chats:
        chat_id = chat.id
        if user_id not in chat_id.split("_"):
            continue
        parts = chat_id.split("_")
        other_uid = parts[0] if parts[1] == user_id else parts[1]
        other_doc = db.collection("users").document(other_uid).get()
        if not other_doc.exists:
            continue
        other_user = other_doc.to_dict()

        latest = db.collection("chats").document(chat_id).collection("messages")\
            .order_by("timestamp", direction="DESCENDING").limit(1).stream()
        latest_msg = None
        for m in latest:
            latest_msg = m.to_dict() | {"id": m.id}
            break

        unread = db.collection("chats").document(chat_id).collection("messages")\
            .where("receiver_id", "==", user_id)\
            .where("read", "==", False).stream()
        unread_count = sum(1 for _ in unread)

        if latest_msg:
            result.append({
                "user": other_user,
                "latest_message": latest_msg,
                "unread_count": unread_count,
                "is_online": manager.is_online(other_uid)
            })

    result.sort(key=lambda x: x["latest_message"]["timestamp"], reverse=True)
    return {"chats": result}

@app.get("/online-users")
def get_online():
    return {"online": manager.get_online_users()}

@app.post("/delete-account")
async def delete_account(data: DeleteAccount):
    user_id = data.user_id
    user_doc = db.collection("users").document(user_id).get()
    if not user_doc.exists:
        raise HTTPException(status_code=404, detail="User nahi mila")

    chats = db.collection("chats").stream()
    for chat in chats:
        chat_id = chat.id
        if user_id in chat_id.split("_"):
            messages = db.collection("chats").document(chat_id).collection("messages").stream()
            for m in messages:
                m.reference.delete()
            db.collection("chats").document(chat_id).delete()

    contacts = db.collection("contacts").document(user_id).collection("saved").stream()
    for c in contacts:
        c.reference.delete()

    db.collection("users").document(user_id).delete()
    try:
        auth_client.delete_user(user_id)
    except Exception as e:
        print(f"Auth delete error: {e}")

    await manager.close_user(user_id)
    return {"success": True, "message": "Account delete ho gaya"}

# ============ WEBSOCKET ============
@app.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: str):
    user_doc = db.collection("users").document(user_id).get()
    if not user_doc.exists:
        await websocket.close(code=1008, reason="User not found")
        return

    await manager.connect(user_id, websocket)
    try:
        while True:
            data = await websocket.receive_text()
            user_doc = db.collection("users").document(user_id).get()
            if not user_doc.exists:
                await websocket.close(code=1008, reason="User deleted")
                manager.disconnect(user_id)
                return
            payload = json.loads(data)

            if payload.get("type") == "send_message":
                msg = MessageSend(**payload["data"])
                await send_message(msg)
            elif payload.get("type") == "typing":
                await manager.send_to_user(payload["receiver_id"], {"type": "typing", "sender_id": user_id})
            elif payload.get("type") == "stop_typing":
                await manager.send_to_user(payload["receiver_id"], {"type": "stop_typing", "sender_id": user_id})
            elif payload.get("type") == "mark_read":
                await mark_read(MarkRead(reader_id=payload.get("reader_id"), sender_id=payload.get("sender_id")))
    except WebSocketDisconnect:
        manager.disconnect(user_id)
        await manager.broadcast({"type": "user_offline", "user_id": user_id})
    except Exception as e:
        print(f"Error: {e}")
        manager.disconnect(user_id)

# ============ FRONTEND ============
frontend_path = os.path.join(BASE_DIR, "frontend")
if os.path.exists(frontend_path):
    app.mount("/static", StaticFiles(directory=frontend_path), name="static")

app.mount("/uploads", StaticFiles(directory=UPLOAD_DIR), name="uploads")

@app.get("/chat")
def chat_page():
    return FileResponse(os.path.join(frontend_path, "chat.html"))