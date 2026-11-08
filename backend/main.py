from fastapi import FastAPI, Depends, HTTPException
from fastapi import UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr, Field
from pathlib import Path
from dotenv import load_dotenv
import os

from backend.database import get_connection, init_db
from backend.security import (
    hash_password,
    verify_password,
    create_access_token,
    get_current_user
)
from backend.agent import get_health_agent_reply

load_dotenv()

app = FastAPI(
    title="Aarogya AI Backend",
    description="AI Powered Health Monitoring System",
    version="1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8501"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

UPLOAD_DIR = Path("backend/uploads")
UPLOAD_DIR.mkdir(exist_ok=True)


@app.on_event("startup")
def startup():
    init_db()


class RegisterInput(BaseModel):
    name: str = Field(min_length=2, max_length=80)
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)


class LoginInput(BaseModel):
    email: EmailStr
    password: str


class ChatInput(BaseModel):
    message: str = Field(min_length=1, max_length=3000)


class FeedbackInput(BaseModel):
    rating: int = Field(ge=1, le=5)
    comment: str = Field(default="", max_length=1000)


# Home API
@app.get("/")
def home():
    return {
        "message": "Welcome to Aarogya AI Backend!"
    }


# Health Check
@app.get("/health")
def health_check():
    return {"status": "ok"}


# User Registration
@app.post("/api/auth/register")
def register(data: RegisterInput):

    with get_connection() as conn:

        try:
            cursor = conn.execute(
                """
                INSERT INTO users(name, email, password_hash)
                VALUES (?, ?, ?)
                """,
                (
                    data.name.strip(),
                    data.email.lower(),
                    hash_password(data.password)
                )
            )

        except Exception as e:
            if "UNIQUE" in str(e).upper():
                raise HTTPException(
                    status_code=409,
                    detail="Email already registered"
                )
            raise HTTPException(
                status_code=500,
                detail="Registration failed"
            )

    return {
        "message": "Registration successful",
        "user_id": cursor.lastrowid
    }


# User Login
@app.post("/api/auth/login")
def login(data: LoginInput):

    with get_connection() as conn:

        user = conn.execute(
            "SELECT * FROM users WHERE email = ?",
            (data.email.lower(),)
        ).fetchone()

    if not user or not verify_password(
        data.password,
        user["password_hash"]
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    token = create_access_token(user["id"])

    return {
        "access_token": token,
        "token_type": "bearer"
    }


# User Profile
@app.get("/api/auth/me")
def profile(user=Depends(get_current_user)):
    return user


# AI Chat API
@app.post("/api/chat")
def chat(
    data: ChatInput,
    user=Depends(get_current_user)
):

    answer = get_health_agent_reply(data.message)

    with get_connection() as conn:

        cursor = conn.execute(
            """
            INSERT INTO chats(user_id, message, response)
            VALUES (?, ?, ?)
            """,
            (user["id"], data.message, answer)
        )

    return {
        "chat_id": cursor.lastrowid,
        "message": data.message,
        "response": answer
    }


# Chat History
@app.get("/api/chat/history")
def chat_history(user=Depends(get_current_user)):

    with get_connection() as conn:

        rows = conn.execute(
            """
            SELECT id, message, response, created_at
            FROM chats
            WHERE user_id = ?
            ORDER BY id DESC
            LIMIT 50
            """,
            (user["id"],)
        ).fetchall()

    return {
        "history": [dict(row) for row in rows]
    }


# File Upload
@app.post("/api/files/upload")
async def upload_file(
    file: UploadFile = File(...),
    user=Depends(get_current_user)
):

    allowed = {".csv", ".json", ".txt"}
    extension = Path(file.filename or "").suffix.lower()

    if extension not in allowed:
        raise HTTPException(
            status_code=400,
            detail="Only CSV, JSON and TXT files allowed"
        )

    content = await file.read(5 * 1024 * 1024 + 1)

    if len(content) > 5 * 1024 * 1024:
        raise HTTPException(
            status_code=413,
            detail="File exceeds 5 MB limit"
        )

    filename = f"user_{user['id']}_{os.urandom(8).hex()}{extension}"
    saved_path = UPLOAD_DIR / filename
    saved_path.write_bytes(content)

    with get_connection() as conn:

        conn.execute(
            """
            INSERT INTO uploads(user_id, filename, saved_path)
            VALUES (?, ?, ?)
            """,
            (
                user["id"],
                Path(file.filename or "upload").name,
                str(saved_path)
            )
        )

    return {
        "message": "File uploaded successfully"
    }


# Feedback API
@app.post("/api/feedback")
def feedback(
    data: FeedbackInput,
    user=Depends(get_current_user)
):

    with get_connection() as conn:

        cursor = conn.execute(
            """
            INSERT INTO feedback(user_id, rating, comment)
            VALUES (?, ?, ?)
            """,
            (user["id"], data.rating, data.comment)
        )

    return {
        "message": "Feedback submitted successfully",
        "feedback_id": cursor.lastrowid
    }


# Analytics API
@app.get("/api/analytics")
def analytics(user=Depends(get_current_user)):

    with get_connection() as conn:

        chats = conn.execute(
            "SELECT COUNT(*) FROM chats WHERE user_id = ?",
            (user["id"],)
        ).fetchone()[0]

        uploads = conn.execute(
            "SELECT COUNT(*) FROM uploads WHERE user_id = ?",
            (user["id"],)
        ).fetchone()[0]

        feedbacks = conn.execute(
            "SELECT COUNT(*) FROM feedback WHERE user_id = ?",
            (user["id"],)
        ).fetchone()[0]

    return {
        "total_chats": chats,
        "total_uploads": uploads,
        "total_feedback": feedbacks
    }