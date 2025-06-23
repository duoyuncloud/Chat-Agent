# chat-agent

A full-stack project with a FastAPI backend and a React/Streamlit frontend for model conversion and chat.

---

## 项目简介
chat-agent 是一个包含 FastAPI 后端和 React/Streamlit 前端的全栈项目，支持模型转换和聊天功能。

---

## Backend 启动方法 (How to run backend)

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
```

访问 http://localhost:8000/docs 查看 API 文档。

---

## Frontend 启动方法 (How to run frontend)

```bash
cd frontend
npm install
npm start
```

默认访问 http://localhost:3000

---

## 目录结构 (Project Structure)

- backend/  —— FastAPI 后端
- frontend/ —— React/Streamlit 前端 