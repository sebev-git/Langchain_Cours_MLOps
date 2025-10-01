from fastapi import FastAPI, HTTPException, UploadFile, File, Response, Cookie
from pydantic import BaseModel
from typing import List, Dict, Optional
import os, json, uuid
from langchain_core.documents import Document
from langchain_core.runnables.history import RunnableWithMessageHistory
from dotenv import load_dotenv

load_dotenv()


# === CHAÎNES / AGENT / OUTILS ===
from src.documents import tools
from src.core.chains import summary_chain, classification_chain, translation_chain, chat_chain
from src.core.parsers import summary_parser, classification_parser, translation_parser
from src.core.llm import llm
from src.memory.session import SessionManager
from src.agents.doc_agent import agent

# === CONFIG ===
app = FastAPI(title="LangChain Project API", version="1.0.0")
session_manager = SessionManager(memory_type="file", token_limit=1000)

# === USERS (stockage JSON simple) ===
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

# === SESSIONS (multi-utilisateurs via cookies) ===
SESSIONS: Dict[str, str] = {}  # session_id -> username

def get_user_from_cookie(session_id: Optional[str]) -> str:
    if not session_id or session_id not in SESSIONS:
        raise HTTPException(status_code=401, detail="Utilisateur non connecté")
    return SESSIONS[session_id]

# === MODELS ===
class User(BaseModel):
    username: str
    password: str

class AgentInput(BaseModel):
    query: str

# === AUTH ROUTES ===
@app.post("/register")
def register(user: User):
    users = load_users()
    if user.username in users:
        raise HTTPException(status_code=400, detail="Utilisateur déjà existant.")
    users[user.username] = {"password": user.password}
    save_users(users)
    session_manager.create_session(user.username)
    return {"message": f"Utilisateur {user.username} créé avec succès."}

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

# === PIPELINE ===

# 1) Upload + Nettoyage
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
        raise HTTPException(status_code=400, detail="Format non supporté. Seuls PDF, TXT et Markdown sont acceptés.")

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

        memory = session_manager.create_session(user_id)
        memory.add_ai_message(f"Fichier {filename} chargé et nettoyé ({len(docs)} pages).")

        return {"message": f"Fichier {filename} chargé et nettoyé", "pages": len(docs), "path": file_path}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur upload: {e}")

# 2) Résumé
@app.post("/doc_summary")
def doc_summary(session_id: Optional[str] = Cookie(None)):
    user_id = get_user_from_cookie(session_id)
    if not tools.DOC_STORE:
        raise HTTPException(status_code=400, detail="Aucun document chargé")
    fmt = summary_parser.get_format_instructions()
    text = " ".join(doc.page_content for doc in tools.DOC_STORE)
    try:
        result = summary_chain.invoke({"texte": text, "format_instructions": fmt})
        memory = session_manager.create_session(user_id)
        memory.add_ai_message(f"Résumé global : {result.summary}")
        return {"summary": result.summary}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur résumé: {e}")

# 3) Classification
@app.post("/doc_classify")  
def doc_classify(session_id: Optional[str] = Cookie(None)):
    user_id = get_user_from_cookie(session_id)
    if not tools.DOC_STORE:
        raise HTTPException(status_code=400, detail="Aucun document chargé")
    fmt = classification_parser.get_format_instructions()
    try:
        summary_res = doc_summary(session_id)
        text_to_classify = summary_res["summary"]
        res = classification_chain.invoke({"texte": text_to_classify, "format_instructions": fmt})
        memory = session_manager.create_session(user_id)
        memory.add_ai_message(f"Classification : {res.category}")
        return {"category": res.category, "confidence": res.confidence}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur classification: {e}")

# 4) Traduction
@app.post("/doc_translate")
def doc_translate(mode: str = "summary", session_id: Optional[str] = Cookie(None)):
    user_id = get_user_from_cookie(session_id)
    if not tools.DOC_STORE:
        raise HTTPException(status_code=400, detail="Aucun document chargé")
    fmt = translation_parser.get_format_instructions()
    try:
        if mode == "summary":
            text_to_translate = doc_summary(session_id)["summary"]
        else:
            text_to_translate = " ".join(doc.page_content for doc in tools.DOC_STORE)
        res = translation_chain.invoke({"texte": text_to_translate, "format_instructions": fmt})
        memory = session_manager.create_session(user_id)
        memory.add_ai_message(f"Traduction : {res.translated_text}")
        return {"translated": res.translated_text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur traduction: {e}")

# 5) Agent
@app.post("/agent")
def run_agent(input: AgentInput, session_id: Optional[str] = Cookie(None)):
    user_id = get_user_from_cookie(session_id)
    if not tools.DOC_STORE:
        raise HTTPException(status_code=400, detail="Aucun document chargé")

    try:
        # Étape 1 : l'agent cherche avec les tools
        raw_results = agent.invoke({"input": input.query})

        # Étape 2 : LLM restitue directement sans tool
        response_text = llm.invoke(
            f"Voici les extraits trouvés dans le document pour '{input.query}':\n{raw_results}\n"
            "Rédige une réponse claire et synthétique pour l’utilisateur."
        )

        # Sauvegarde mémoire
        memory = session_manager.create_session(user_id)
        memory.add_user_message(input.query)
        memory.add_ai_message(str(response_text))

        return {
            "response": response_text.content,
            "context": raw_results
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur agent: {e}")


# 6) Historique
@app.get("/history")
def get_history(session_id: Optional[str] = Cookie(None)):
    user_id = get_user_from_cookie(session_id)
    try:
        messages = session_manager.read_session(user_id) or []
        return {"user_id": user_id, "messages": messages}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"History reading error: {e}")

# 7) Chat Libre
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
        raise HTTPException(status_code=500, detail=f"Chat Error: {e}")