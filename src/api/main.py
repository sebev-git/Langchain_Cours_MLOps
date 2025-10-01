from fastapi import FastAPI, HTTPException, UploadFile, File, Response, Cookie
from pydantic import BaseModel

from langchain_core.documents import Document
from langchain_core.runnables.history import RunnableWithMessageHistory

from src.documents import tools
from src.core.chains import summary_chain, classification_chain, translation_chain, chat_chain
from src.core.parsers import summary_parser, classification_parser, translation_parser
from src.core.llm import llm
from src.memory.session import SessionManager
from src.agents.doc_agent import agent

from typing import List, Dict, Optional
import os, json, uuid

app = FastAPI(title="LangChain Project API", version="3.1.0")
session_manager = SessionManager(memory_type="file", token_limit=500)

# === USERS (stockage JSON) ===
USERS_FILE = "users.json"
if not os.path.exists(USERS_FILE):
    with open(USERS_FILE, "w") as f:
        json.dump({}, f)

def load_users() -> Dict[str, Dict[str, str]]:
    if not os.path.exists(USERS_FILE):
        return {}
    try:
        with open(USERS_FILE, "r") as f:
            content = f.read().strip()
            if not content:  
                return {}
            return json.loads(content)
    except json.JSONDecodeError:
        return {}

def save_users(users: Dict[str, Dict[str, str]]) -> None:
    with open(USERS_FILE, "w") as f:
        json.dump(users, f)

# === SESSIONS with cookies ===
SESSIONS: Dict[str, str] = {}  

def get_user_from_cookie(session_id: Optional[str]) -> str:
    if not session_id or session_id not in SESSIONS:
        raise HTTPException(status_code=401, detail="User not connected")
    return SESSIONS[session_id]

# === MODELS ===
class User(BaseModel):
    username: str
    password: str

# === AUTH ROUTES ===
@app.post("/register")
def register(user: User):
    users = load_users()
    if user.username in users:
        raise HTTPException(status_code=400, detail="User already exists.")
    users[user.username] = {"password": user.password}
    save_users(users)
    session_manager.create_session(user.username)
    return {"message": f"User {user.username} created successfully."}

@app.post("/login")
def login(user: User, response: Response):
    users = load_users()
    if user.username not in users or users[user.username]["password"] != user.password:
        raise HTTPException(status_code=401, detail="Nom d'utilisateur ou mot de passe incorrect.")
    session_manager.create_session(user.username)
    session_id = str(uuid.uuid4())
    SESSIONS[session_id] = user.username
    response.set_cookie(key="session_id", value=session_id, httponly=True)
    return {"message": "Connexion réussie", "user_id": user.username}

@app.post("/upload_file")
async def upload_file(file: UploadFile = File(...), session_id: Optional[str] = Cookie(None)):
    user_id = get_user_from_cookie(session_id)
    filename = file.filename.lower()

    if filename.endswith(".pdf"):
        folder, loader = "data/pdf", tools.load_pdf_tool
        payload = {"path": None}
    elif filename.endswith(".txt"):
        folder, loader = "data/txt", tools.load_txt_tool
        payload = {"path": None}
    elif filename.endswith(".md") or filename.endswith(".markdown"):
        folder, loader = "data/md", tools.load_markdown_tool
        payload = {"path": None}
    else:
        raise HTTPException(status_code=400, detail="Unsupported format. Only PDF, TXT, and Markdown are accepted.")

    os.makedirs(folder, exist_ok=True)
    file_path = os.path.join(folder, filename)
    content = await file.read()
    with open(file_path, "wb") as f:
        f.write(content)

    try:
        payload["path"] = file_path
        docs: List[Document] = loader.invoke(payload)
        cleaned_docs = [
            Document(
                page_content=tools.clean_text_tool.invoke({"text": doc.page_content}),
                metadata=doc.metadata,
            )
            for doc in docs
        ]
        tools.DOC_STORE = cleaned_docs

        return {"message": f"Fichier {filename} chargé et nettoyé", "pages": len(docs), "path": file_path}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur upload: {e}")

@app.post("/doc_summary")
def doc_summary(session_id: Optional[str] = Cookie(None)):
    user_id = get_user_from_cookie(session_id)
    memory = session_manager.create_session(user_id)
    text = " ".join(doc.page_content for doc in tools.DOC_STORE)

    try:
        result = summary_chain.invoke({
            "input": text,
            "format_instructions": summary_parser.get_format_instructions()
            })

        memory.add_ai_message(f"Global Summary : {result.summary}")
        return {"summary": result.summary}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Summary error: {e}")

@app.post("/doc_classify")
def doc_classify(session_id: Optional[str] = Cookie(None)):
    user_id = get_user_from_cookie(session_id)
    memory = session_manager.create_session(user_id)
    summary_res = doc_summary(session_id)
    text_to_classify = summary_res["summary"]

    try:
        result = classification_chain.invoke({
            "input": text_to_classify,
            "format_instructions": classification_parser.get_format_instructions()
            })

        memory.add_ai_message(f"Classification : {result.category}")
        return {"category": result.category, "confidence": result.confidence}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Classification error: {e}")

@app.post("/doc_translate")
def doc_translate(session_id: Optional[str] = Cookie(None)):
    user_id = get_user_from_cookie(session_id)
    memory = session_manager.create_session(user_id)
    text_to_translate = doc_summary(session_id)["summary"]

    try:
        result = translation_chain.invoke({
            "input": text_to_translate,
            "format_instructions": translation_parser.get_format_instructions()
        })

        memory.add_ai_message(f"Translation : {result.translated_text}")
        return {"translated": result.translated_text}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Translation error: {e}")

class AgentInput(BaseModel):
    query: str

@app.post("/agent")
def run_agent(input: AgentInput, session_id: Optional[str] = Cookie(None)):
    user_id = get_user_from_cookie(session_id)
    memory = session_manager.create_session(user_id)

    try:
        # Step 1: The agent searches using the tools
        raw_results = "\n\n".join(doc.page_content for doc in tools.DOC_STORE)

        # Step 2: LLM outputs directly without tools
        response_text = llm.invoke(
            f"Here are the extracts found in the document for '{input.query}':\n{raw_results}\n"
            "Write a clear and concise response for the user."
        )

        memory.add_user_message(input.query)
        memory.add_ai_message(str(response_text))

        return {
            "response": response_text.content,
            "context": raw_results
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Agent error: {e}")

@app.get("/history")
def get_history(session_id: Optional[str] = Cookie(None)):
    user_id = get_user_from_cookie(session_id)
    try:
        messages = session_manager.read_session(user_id) or []
        return {"user_id": user_id, "messages": messages}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"History reading error: {e}")

@app.post("/chat")
def chat(input: AgentInput, session_id: Optional[str] = Cookie(None)):
    
    user_id = get_user_from_cookie(session_id)
    conversation = RunnableWithMessageHistory(
        chat_chain,
        lambda user_id:session_manager.create_session(user_id),  
        input_messages_key="input",
        history_messages_key="history",
    )
    try:
        result = conversation.invoke(
            {"input": input.query},
            config={"configurable": {"session_id": user_id}}  
        )
        return {"response": result.content}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Chat error: {e}")