from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import SystemMessage, BaseMessage
from src.core.llm import llm
from src.utils.token import count_tokens

def summarize_messages(messages):
    """Build a long summary (~1000 tokens) of the full history."""
    content = "\n".join([f"{msg.type.upper()}: {msg.content}" for msg in messages])

    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful assistant."),
        ("system", "Summarize the following conversation into about 1000 tokens. "
                   "Keep important details like user identity, preferences, goals, "
                   "facts, and key points mentioned."),
        ("human", content)
    ])

    chain = prompt | llm
    return chain.invoke({"input": content}).content

class SummarizedHistoryWrapper:
    """Wrapper that chooses between raw history and a summary."""

    def __init__(self, history, token_limit: int = 500):
        self.history = history
        self.token_limit = token_limit
        self._summary = None

    @property
    def messages(self):
        """Return either the raw messages or an injected summary."""
        tokens = count_tokens(self.history.messages)
        if tokens > self.token_limit:
            self._summary = summarize_messages(self.history.messages)
            return [SystemMessage(content=f"Summary of conversation : {self._summary}")]
        else:
            return self.history.messages

    def add_user_message(self, message: str):
        return self.history.add_user_message(message)

    def add_ai_message(self, message: str):
        return self.history.add_ai_message(message)

    def add_messages(self, messages: list[BaseMessage]):
        """Add a list of messages (required by RunnableWithMessageHistory)."""
        return self.history.add_messages(messages)

    def clear(self):
        return self.history.clear()