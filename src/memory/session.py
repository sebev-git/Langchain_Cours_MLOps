import os
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_community.chat_message_histories import FileChatMessageHistory, SQLChatMessageHistory
from src.memory.memory import SummarizedHistoryWrapper  

class SessionManager:
    def __init__(self, memory_type="inmemory", storage_path="sessions.db", token_limit=500):
        self.memory_type = memory_type
        self.storage_path = storage_path
        self.token_limit = token_limit
        os.makedirs("session_history", exist_ok=True)

    def create_session(self, user_id: str):
        """Return the history corresponding to the user, wrapped with the summarized wrapper"""
        if self.memory_type == "inmemory":
            base_history = InMemoryChatMessageHistory()
        elif self.memory_type == "file":
            base_history = FileChatMessageHistory(f"session_history/{user_id}.json")
        elif self.memory_type == "sql":
            base_history = SQLChatMessageHistory(
                session_id=user_id,
                connection_string=f"sqlite:///{self.storage_path}"
            )
        else:
            raise ValueError("Unknown memory type")

        return SummarizedHistoryWrapper(base_history, token_limit=self.token_limit)

    def reset_session(self, user_id: str):
        """Reset the session by clearing the history"""
        if self.memory_type == "inmemory":
            base_history = InMemoryChatMessageHistory()
        elif self.memory_type == "file":
            filepath = f"session_history/{user_id}.json"
            if os.path.exists(filepath):
                os.remove(filepath)
            base_history = FileChatMessageHistory(filepath)
        elif self.memory_type == "sql":
            base_history = SQLChatMessageHistory(
                session_id=user_id,
                connection_string=f"sqlite:///{self.storage_path}"
            )
        else:
            raise ValueError("Unknown memory type")

        return SummarizedHistoryWrapper(base_history, token_limit=self.token_limit)

    def delete_session(self, user_id: str):
        """Completely delete the session"""
        if self.memory_type == "inmemory":
            return None
        elif self.memory_type == "file":
            filepath = f"session_history/{user_id}.json"
            if os.path.exists(filepath):
                os.remove(filepath)
            return f"Session {user_id} deleted (file removed)"
        elif self.memory_type == "sql":
            return f"Manual deletion required for {user_id} in database {self.storage_path}"
        else:
            raise ValueError("Unknown memory type")

    def read_session(self, user_id: str):
        """Retourne l’historique (brut ou résumé) pour un utilisateur"""
        memory = self.create_session(user_id)
        return [{"type": msg.type, "content": msg.content} for msg in memory.messages]