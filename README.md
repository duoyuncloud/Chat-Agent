# chat-agent

<<<<<<< HEAD
A full-stack project with a FastAPI backend and a Streamlit frontend for chat.
=======
A full-stack project with a FastAPI backend and a Streamlit frontend for model conversion and chat.
>>>>>>> 80eb6f8 (refactor: clean up frontend, improve Streamlit UI, update docs)

---

## 项目简介
<<<<<<< HEAD
chat-agent 是一个包含 FastAPI 后端和 Streamlit 前端的全栈项目，支持聊天功能。
=======
chat-agent 是一个包含 FastAPI 后端和 Streamlit 前端的全栈项目，支持模型转换和多模型聊天功能。
>>>>>>> 80eb6f8 (refactor: clean up frontend, improve Streamlit UI, update docs)

---

## Backend 启动方法 (How to run backend)

### Ollama 版本
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
```

### Claude4 版本
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main_claude:app --reload
```

访问 http://localhost:8000/docs 查看 API 文档。

---

## Frontend 启动方法 (How to run frontend)

```bash
cd frontend
pip install -r ../backend/requirements.txt  # 确保依赖齐全
streamlit run chat_streamlit.py
```

默认访问 http://localhost:8501

---

## LLM 选择与 API Key
- 前端支持 LLM 选择（Ollama/Claude4）。
- 选择 Claude4 时，需在前端输入 Claude API Key（sk-ant-...）。
- Ollama 版本无需 API Key。
- 每个模型下方有简要介绍，帮助用户理解各自特点和适用场景。

---

## 多轮对话与美化 UI
- 支持多轮对话，历史消息自动保留在页面。
- 聊天气泡样式美观，区分用户与机器人。
- Claude API Key 格式自动校验，错误友好提示。
- 支持一键清空对话。
- UI 交互体验优化，按钮、输入框、分割线等更友好。

---

## 目录结构 (Project Structure)

<<<<<<< HEAD
- backend/  —— FastAPI 后端
- frontend/ —— React/Streamlit 前端 
=======
- backend/main.py —— Ollama 后端
- backend/main_claude.py —— Claude4 后端
- frontend/chat_streamlit.py —— Streamlit 前端
- requirements.txt —— 后端与前端依赖

---

## 依赖安装 (Dependencies)

```bash
pip install -r backend/requirements.txt
```

---

## 其他说明
- CORS 设置为全开放，生产环境建议限制来源。
- 如需支持更多 LLM，只需在前端 LLM_OPTIONS 中扩展，并在后端增加新接口。
- Claude4 实际为 Claude 3 Opus 占位，后续可直接升级。 
>>>>>>> 80eb6f8 (refactor: clean up frontend, improve Streamlit UI, update docs)
